import { useSyncExternalStore } from "react"
import { getRoot, onCommit, replaceRoot, type Root } from "./store"

/**
 * Synchronisation par compte, active seulement si le serveur publie config.json avec { "syncUrl": "..." }.
 * Sans ce fichier (GitHub Pages), l'application reste locale.
 */
const KEY = "parcours-ia-sync"
type Sess = { token?: string; email?: string; last?: number }
type Status = { enabled: boolean; mode: "local" | "remote_user"; email: string; last: number; busy: boolean; error: string }

let url = ""
let sess: Sess = {}
let status: Status = { enabled: false, mode: "local", email: "", last: 0, busy: false, error: "" }
const subs = new Set<() => void>()
const set = (p: Partial<Status>) => {
  status = { ...status, ...p }
  subs.forEach((f) => f())
}
export const useSync = () =>
  useSyncExternalStore(
    (f) => (subs.add(f), () => subs.delete(f)),
    () => status,
  )

function saveSess() {
  try {
    localStorage.setItem(KEY, JSON.stringify(sess))
  } catch {
    /* stockage indisponible */
  }
}

async function api(a: string, method = "GET", body?: unknown) {
  const r = await fetch(`${url}?a=${a}`, {
    method,
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", ...(sess.token ? { Authorization: `Bearer ${sess.token}` } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  const j = await r.json().catch(() => ({}))
  if (!r.ok) throw Object.assign(new Error(j.error || `Erreur ${r.status}`), { status: r.status })
  return j
}

/* ---------- Fusion : rien d'acquis ne se perd, d'un appareil à l'autre ---------- */
const obj = (o: any) => (o && typeof o === "object" && !Array.isArray(o) ? o : {})
export function merge(a: Root, b: Root): Root {
  const A = a.state, B = b.state
  const newer = A.updatedAt >= B.updatedAt ? a : b
  const steps: Record<string, any> = {}
  for (const k of new Set([...Object.keys(A.steps), ...Object.keys(B.steps)])) {
    const x: any = A.steps[k], y: any = B.steps[k]
    if (!x || !y) { steps[k] = x || y; continue }
    const or = (p: any, q: any) => { const o: any = { ...p }; for (const i in q) o[i] = o[i] || q[i]; return o }
    steps[k] = {
      ex: or(x.ex, y.ex), xpEx: or(x.xpEx, y.xpEx), best: Math.max(x.best, y.best), passed: x.passed || y.passed,
      date: [x.date, y.date].filter(Boolean).sort()[0] || "", lessons: Math.max(x.lessons, y.lessons),
      perfect: x.perfect || y.perfect, val: x.val || y.val, notions: x.notions || y.notions,
    }
  }
  const srs: Record<string, any> = { ...A.srs }
  for (const k in B.srs) if (!srs[k] || B.srs[k].seen > srs[k].seen || (B.srs[k].seen === srs[k].seen && B.srs[k].due > srs[k].due)) srs[k] = B.srs[k]
  const defis: Record<string, string> = { ...B.defis }
  for (const k in A.defis) defis[k] = !defis[k] || A.defis[k] < defis[k] ? A.defis[k] : defis[k]
  const day = A.daily.day === B.daily.day ? { ...newer.state.daily, xp: Math.max(A.daily.xp, B.daily.xp) } : A.daily.day > B.daily.day ? A.daily : B.daily
  const streak = A.streak.lastDay === B.streak.lastDay ? (A.streak.count >= B.streak.count ? A.streak : B.streak) : A.streak.lastDay > B.streak.lastDay ? A.streak : B.streak
  const answers: Record<string, any> = { ...obj(b.answers) }
  for (const d in obj(a.answers)) {
    const seen = new Set((answers[d]?.items || []).map((i: any) => `${i.t}|${i.item}`))
    answers[d] = { items: [...(answers[d]?.items || []), ...(a.answers[d]?.items || []).filter((i: any) => !seen.has(`${i.t}|${i.item}`))] }
  }
  const notes: Record<string, any> = { ...obj(newer === a ? b.notes : a.notes), ...obj(newer.notes) }
  return {
    ...newer,
    notes,
    answers,
    state: { ...newer.state, settings: { ...newer.state.settings, profil: newer.state.settings.profil || (newer === a ? B : A).settings.profil }, xp: Math.max(A.xp, B.xp), streak, daily: day, steps, srs, defis, updatedAt: Math.max(A.updatedAt, B.updatedAt) },
  }
}

/* ---------- Cycle : récupérer, fusionner, renvoyer ---------- */
let timer: ReturnType<typeof setTimeout> | undefined
let running: Promise<void> | null = null
export function syncNow(): Promise<void> {
  if (!status.enabled || (!sess.token && status.mode === "local")) return Promise.resolve()
  if (running) return running
  set({ busy: true })
  running = (async () => {
    try {
      const remote = await api("pull")
      const local = getRoot()
      const merged = remote.data?.state ? merge(local, remote.data as Root) : local
      if (merged !== local) replaceRoot(merged)
      await api("push", "PUT", { data: merged, updatedAt: merged.state.updatedAt })
      sess.last = Date.now()
      saveSess()
      set({ last: sess.last, error: "" })
    } catch (e: any) {
      if (e.status === 401 && status.mode === "local") {
        sess = {}
        saveSess()
        set({ email: "" })
      }
      set({ error: navigator.onLine ? e.message : "Hors connexion : la synchronisation reprendra au retour du réseau." })
    } finally {
      running = null
      set({ busy: false })
    }
  })()
  return running
}
const later = () => {
  clearTimeout(timer)
  timer = setTimeout(syncNow, 2500)
}

export async function login(email: string, password: string, create: boolean) {
  const r = await api(create ? "register" : "login", "POST", { email, password })
  sess = { token: r.token, email: r.email }
  saveSess()
  set({ email: r.email, error: "" })
  await syncNow()
}
export async function logout() {
  await api("logout", "POST").catch(() => {})
  sess = {}
  saveSess()
  set({ email: "", last: 0 })
}

export async function initSync() {
  try {
    const c = await fetch("config.json", { cache: "no-store" }).then((r) => (r.ok ? r.json() : null))
    if (!c?.syncUrl) return
    url = c.syncUrl
  } catch {
    return
  }
  try {
    sess = JSON.parse(localStorage.getItem(KEY) || "{}")
  } catch {
    sess = {}
  }
  set({ enabled: true, email: sess.email || "", last: sess.last || 0 })
  /* Mode SSO : l'identité vient du serveur, pas de mot de passe dans l'application. */
  try {
    const me = await api("me")
    if (me.mode === "remote_user") set({ mode: "remote_user", email: me.email })
  } catch {
    /* pas connecté en mode local : normal */
  }
  onCommit(later)
  addEventListener("online", () => syncNow())
  document.addEventListener("visibilitychange", () => document.visibilityState === "visible" && syncNow())
  syncNow()
}
