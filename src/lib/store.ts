import { useSyncExternalStore } from "react"
import { BYID, DEFIS, ITEMS, MAIN, PROFIL_IDS, STEPS, VIS, applyProfil, validDrill, type Item, type Step } from "./content"

/* Clé d'origine conservée : les progressions déjà enregistrées restent lisibles. */
export const KEY = "parcours-ia-juriste-v2"
export const RANKS: [number, string][] = [
  [0, "Débutant"],
  [150, "Utilisateur régulier"],
  [400, "Utilisateur confirmé"],
  [700, "Référent prompts"],
  [1000, "Architecte d'agents"],
  [1300, "Expert IA de l'équipe"],
]
export const INTERVALS = [1, 2, 4, 8, 16]
export const GOALS = [10, 20, 30, 50]
export const XP = { lesson: 10, review: 5, ex: 20, exam: 50, perfect: 20, step: 30, notions: 5, defi: 15 }
export const HEARTS = 5

export type StepState = {
  ex: Record<string, boolean>
  best: number
  passed: boolean
  date: string
  lessons: number
  xpEx: Record<string, boolean>
  perfect: boolean
  val: boolean
  notions: boolean
}
export type Srs = { box: number; due: string; seen: number; ok: number; ko: number }
/** cadre : 1 navigateur, 2 connecteurs et applications, 3 API, code et agents. profil : métier choisi à l'ouverture (vide tant qu'il n'est pas choisi). */
export type Settings = { sound: boolean; haptics: boolean; cadre: number; outil: string; profil: string }
export type State = {
  updatedAt: number
  xp: number
  streak: { count: number; lastDay: string }
  daily: { day: string; xp: number; goal: number }
  steps: Record<string, StepState>
  srs: Record<string, Srs>
  free: boolean
  settings: Settings
  defis: Record<string, string>
}
export type Answer = { t: number; step: string; item: string; kind: string; ok: boolean }
export type Plan = { week?: string; message?: string; focus?: string[]; drills?: unknown[] }
export type Root = { state: State; notes: Record<string, string | number>; answers: Record<string, { items: Answer[] }>; plan: Plan | null; journal: unknown; tutor: unknown }

/* ---------- Dates ---------- */
const pad = (n: number) => (n < 10 ? "0" : "") + n
export const dayStr = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
export const today = () => dayStr(new Date())
export function addDays(day: string, n: number) {
  const p = day.split("-")
  return dayStr(new Date(+p[0], +p[1] - 1, +p[2] + n))
}
const isObj = (o: unknown): o is Record<string, any> => !!o && typeof o === "object" && !Array.isArray(o)

/* ---------- Normalisation (compatible avec la V2 publiée sur claude.ai) ---------- */
function blankState(): State {
  return {
    updatedAt: 0,
    xp: 0,
    streak: { count: 0, lastDay: "" },
    daily: { day: today(), xp: 0, goal: 20 },
    steps: {},
    srs: {},
    free: false,
    settings: { sound: true, haptics: true, cadre: 1, outil: "", profil: "" },
    defis: {},
  }
}
export function normState(o: unknown): State {
  const b = blankState()
  if (!isObj(o)) return b
  b.updatedAt = +o.updatedAt || 0
  b.xp = Math.max(0, +o.xp || 0)
  if (isObj(o.streak)) b.streak = { count: +o.streak.count || 0, lastDay: String(o.streak.lastDay || "") }
  if (isObj(o.daily))
    b.daily = {
      day: String(o.daily.day || today()),
      xp: +o.daily.xp || 0,
      goal: GOALS.includes(+o.daily.goal) ? +o.daily.goal : 20,
    }
  if (isObj(o.steps))
    for (const k of Object.keys(o.steps)) {
      const x = o.steps[k]
      if (!isObj(x)) continue
      b.steps[k] = {
        ex: isObj(x.ex) ? x.ex : {},
        best: +x.best || 0,
        passed: !!x.passed,
        date: x.date || "",
        lessons: +x.lessons || 0,
        xpEx: isObj(x.xpEx) ? x.xpEx : {},
        perfect: !!x.perfect,
        val: !!x.val,
        notions: !!x.notions,
      }
    }
  if (isObj(o.srs))
    for (const k of Object.keys(o.srs)) {
      const e = o.srs[k]
      if (!isObj(e)) continue
      b.srs[k] = { box: Math.min(5, Math.max(1, +e.box || 1)), due: String(e.due || today()), seen: +e.seen || 0, ok: +e.ok || 0, ko: +e.ko || 0 }
    }
  b.free = !!o.free
  if (isObj(o.settings))
    b.settings = {
      sound: o.settings.sound !== false,
      haptics: o.settings.haptics !== false,
      cadre: [1, 2, 3].includes(+o.settings.cadre) ? +o.settings.cadre : 1,
      outil: typeof o.settings.outil === "string" ? o.settings.outil.slice(0, 40) : "",
      profil: PROFIL_IDS.includes(o.settings.profil) ? o.settings.profil : "",
    }
  if (isObj(o.defis)) for (const k of Object.keys(o.defis)) b.defis[k] = String(o.defis[k])
  return b
}

/* ---------- Magasin ---------- */
let R: Root = { state: blankState(), notes: {}, answers: {}, plan: null, journal: null, tutor: null }
let version = 0
const listeners = new Set<() => void>()

function load() {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return
    const o = JSON.parse(raw)
    R = {
      state: normState(o.state),
      notes: isObj(o.notes) ? o.notes : {},
      answers: isObj(o.answers) ? o.answers : {},
      plan: isObj(o.plan) ? o.plan : null,
      journal: o.journal ?? null,
      tutor: o.tutor ?? null,
    }
  } catch {
    /* stockage indisponible : la séance fonctionne sans mémoire */
  }
}
load()
applyProfil(R.state.settings.profil)
registerCoach()

function save() {
  R.state.updatedAt = Date.now()
  try {
    localStorage.setItem(KEY, JSON.stringify(R))
  } catch {
    /* navigation privée ou quota plein */
  }
}
function emit() {
  version++
  listeners.forEach((l) => l())
}
const commitHooks = new Set<() => void>()
/** Appelé après chaque enregistrement local (synchronisation par compte). */
export const onCommit = (f: () => void) => (commitHooks.add(f), () => commitHooks.delete(f))
export function commit() {
  save()
  emit()
  commitHooks.forEach((f) => f())
}
/** Remplace toute la sauvegarde (après fusion avec le serveur), sans relancer la synchronisation. */
export function replaceRoot(o: any) {
  R = {
    state: normState(o?.state),
    notes: isObj(o?.notes) ? o.notes : {},
    answers: isObj(o?.answers) ? o.answers : {},
    plan: isObj(o?.plan) ? o.plan : null,
    journal: o?.journal ?? null,
    tutor: o?.tutor ?? null,
  }
  applyProfil(R.state.settings.profil)
  registerCoach()
  try {
    localStorage.setItem(KEY, JSON.stringify(R))
  } catch {
    /* stockage indisponible */
  }
  emit()
}
export function useStore() {
  useSyncExternalStore(
    (l) => {
      listeners.add(l)
      return () => listeners.delete(l)
    },
    () => version,
  )
  return R
}
export const getRoot = () => R

/* ---------- Lecture ---------- */
const S = () => R.state
export function st(id: string): StepState {
  return (S().steps[id] ||= { ex: {}, best: 0, passed: false, date: "", lessons: 0, xpEx: {}, perfect: false, val: false, notions: false })
}
export const peek = (id: string): StepState =>
  S().steps[id] || { ex: {}, best: 0, passed: false, date: "", lessons: 0, xpEx: {}, perfect: false, val: false, notions: false }
export const exDone = (s: Step) => s.ex.every((e, i) => e.opt || peek(s.id).ex[i])
export const validated = (s: Step) => !!peek(s.id).passed && exDone(s)
/* Seuils d'ouverture des voies. L'ancienne étape 05 validée ouvre aussi la voie Expert : les acquis de la V2 restent. */
const GATE: Record<string, () => boolean> = {
  socle: () => true,
  metier: () => !!BYID.so4 && validated(BYID.so4),
  expert: () => (!!BYID.so6 && validated(BYID.so6)) || !!S().steps.s5?.passed,
  bonus: () => true,
}
export const voieOpen = (v: string) => S().free || (GATE[v] ?? GATE.socle)()
export function unlocked(s: Step) {
  if (S().free || s.voie === "bonus") return true
  const same = MAIN.filter((x) => x.voie === s.voie)
  const i = same.indexOf(s)
  return i <= 0 ? voieOpen(s.voie) : validated(same[i - 1])
}
export function currentStep() {
  return MAIN.find((s) => unlocked(s) && !validated(s)) || null
}
/** Au-delà de la pratique autorisée au poste, selon le cadre réglé dans le profil. */
export const beyondCadre = (s: { cadre?: number }) => (s.cadre || 1) > S().settings.cadre

/* ---------- Compétences ---------- */
/**
 * Niveau 0 à 4 : 1 étape commencée ; 2 une étape validée ; 3 toutes les étapes Socle et Métier
 * de la compétence validées ; 4 en plus, une étape Expert validée ou trois défis faits.
 */
export function compLevel(id: string) {
  const steps = VIS.filter((s) => s.comp?.includes(id))
  const base = steps.filter((s) => s.voie === "socle" || s.voie === "metier")
  const val = steps.filter(validated)
  const started = steps.some((s) => peek(s.id).notions || peek(s.id).lessons > 0)
  const defis = DEFIS.filter((d) => d.comp === id && S().defis[d.id]).length
  if (!started && !val.length && !defis) return 0
  if (!val.length) return 1
  if (!base.every(validated)) return 2
  return val.some((s) => s.voie === "expert") || defis >= 3 ? 4 : 3
}

/* ---------- Défis ---------- */
/** Défi du jour : rotation quotidienne parmi les défis du cadre réglé, en commençant par ceux non faits. */
export function defiDuJour() {
  const pool = DEFIS.filter((d) => d.cadre <= S().settings.cadre)
  const todo = pool.filter((d) => !S().defis[d.id])
  const list = todo.length ? todo : pool
  const n = Math.floor(new Date(today()).getTime() / 864e5)
  return list[n % list.length]
}
export function doneDefi(id: string) {
  if (S().defis[id]) return false
  S().defis[id] = today()
  commit()
  award(XP.defi)
  return true
}
export function rankIndex(xp = S().xp) {
  let r = 0
  RANKS.forEach((k, i) => {
    if (xp >= k[0]) r = i
  })
  return r
}
export function streakNow() {
  const t = today()
  return S().streak.lastDay === t || S().streak.lastDay === addDays(t, -1) ? S().streak.count : 0
}
export function dailyXp() {
  return S().daily.day === today() ? S().daily.xp : 0
}

/* Nœuds du chemin : chaque étape se parcourt en quatre stations. */
export type NodeKind = "notions" | "lecon" | "ex" | "exam"
export const NODE_KINDS: NodeKind[] = ["notions", "lecon", "ex", "exam"]
/* Libellé long de chaque nœud du chemin (tiroir, colonne de droite). */
export const NAME_NODE: Record<NodeKind, string> = { notions: "Notions", lecon: "Leçon", ex: "Exercices pratiques", exam: "Examen de validation" }
export function nodeDone(s: Step, k: NodeKind) {
  const x = peek(s.id)
  if (k === "notions") return x.notions || x.lessons > 0 || x.passed
  if (k === "lecon") return x.lessons > 0 || x.passed
  if (k === "ex") return exDone(s)
  return x.passed
}
export function currentNode(): { step: Step; kind: NodeKind } | null {
  const s = currentStep()
  if (!s) return null
  return { step: s, kind: NODE_KINDS.find((k) => !nodeDone(s, k)) || "exam" }
}

/* ---------- Écriture ---------- */
function rollDay() {
  const t = today()
  if (S().daily.day !== t) S().daily = { day: t, xp: 0, goal: S().daily.goal }
}
/** Ajoute de l'XP. Renvoie true si la série vient de progresser aujourd'hui. */
export function award(n: number): boolean {
  if (!n) return false
  rollDay()
  const t = today()
  const s = S()
  s.xp += n
  s.daily.xp += n
  let bumped = false
  if (s.streak.lastDay !== t) {
    s.streak.count = s.streak.lastDay === addDays(t, -1) ? s.streak.count + 1 : 1
    s.streak.lastDay = t
    bumped = true
  }
  commit()
  return bumped
}
export function record(it: Item, ok: boolean, mode: string) {
  const t = today()
  const e = (S().srs[it.id] ||= { box: 0, due: t, seen: 0, ok: 0, ko: 0 })
  e.seen++
  if (ok) {
    e.ok++
    e.box = Math.min(5, e.box + 1)
  } else {
    e.ko++
    e.box = 1
  }
  e.due = addDays(t, INTERVALS[e.box - 1])
  const d = (R.answers[t] ||= { items: [] })
  if (d.items.length < 400) d.items.push({ t: Date.now(), step: it.step || "", item: it.id, kind: mode, ok })
  const keys = Object.keys(R.answers).sort()
  while (keys.length > 60) delete R.answers[keys.shift()!]
  commit()
}
/** Valide l'étape si les conditions sont réunies. Renvoie true au moment de la validation. */
export function checkValidation(s: Step) {
  const x = st(s.id)
  if (validated(s) && !x.val) {
    x.val = true
    award(XP.step)
    return true
  }
  return false
}
export function toggleEx(s: Step, i: number) {
  const x = st(s.id)
  x.ex[i] = !x.ex[i]
  let gained = 0
  if (x.ex[i] && !x.xpEx[i]) {
    x.xpEx[i] = true
    gained = XP.ex
  }
  commit()
  if (gained) award(gained)
  return { gained, validatedNow: checkValidation(s) }
}
export function markNotions(s: Step) {
  const x = st(s.id)
  if (x.notions) return false
  x.notions = true
  commit()
  award(XP.notions)
  return true
}
export function setNote(id: string, text: string) {
  R.notes[id] = text
  R.notes.updatedAt = Date.now()
  save()
}
export function setGoal(g: number) {
  rollDay()
  S().daily.goal = g
  commit()
}
export function setSetting<K extends keyof Settings>(k: K, v: Settings[K]) {
  S().settings[k] = v
  commit()
}
/** Change le profil métier : les étapes Métier et les exemples suivent ; les acquis restent enregistrés. */
export function setProfil(p: string) {
  S().settings.profil = p
  applyProfil(p)
  registerCoach()
  commit()
}
/** Profil métier déjà suggéré par les acquis : une progression sur la voie Métier d'origine indique un juriste. */
export const profilSuggere = () => (Object.keys(S().steps).some((k) => /^me\d$/.test(k)) ? "juriste" : "")
export function setFree(v: boolean) {
  S().free = v
  commit()
}

/* ---------- Questions et révision ---------- */
function registerCoach() {
  for (const k of Object.keys(ITEMS)) if (k.startsWith("c:")) delete ITEMS[k]
  const p = R.plan
  if (!p || !Array.isArray(p.drills)) return
  p.drills.forEach((d, i) => {
    if (!validDrill(d)) return
    const id = `c:${String(p.week || "s")}:${i}`
    ITEMS[id] = { ...(d as object), id, kind: "coach", step: typeof (d as any).step === "string" ? (d as any).step : "" } as Item
  })
}
export function shuffle<T>(a: T[]) {
  a = a.slice()
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}
export function dueIds() {
  const t = today()
  /* Questions du coach et de l'actualité : dues dès leur arrivée. */
  const fresh = (id: string) => id.startsWith("c:") || id.startsWith("n:")
  const out = Object.keys(ITEMS).filter((id) => fresh(id) && (!S().srs[id] || S().srs[id].due <= t))
  const rest = Object.keys(S().srs)
    .filter((id) => ITEMS[id] && !fresh(id) && S().srs[id].due <= t)
    .sort((a, b) => (S().srs[a].due < S().srs[b].due ? -1 : S().srs[a].due > S().srs[b].due ? 1 : S().srs[a].box - S().srs[b].box))
  return out.concat(rest)
}
export function lessonIds(s: Step) {
  const d = shuffle(s.drills.map((_, i) => `d:${s.id}:${i}`))
  const q = shuffle(s.quiz.map((_, i) => `q:${s.id}:${i}`))
  return shuffle(d.concat(q).slice(0, 10))
}
export const examIds = (s: Step) => shuffle(s.quiz.map((_, i) => `q:${s.id}:${i}`))
/**
 * Entraînement du jour. Sans question due, on reprend les plus fragiles ;
 * sans aucun historique, on part des exercices courts de l'étape en cours
 * (la V2 renvoyait alors un simple message, ce qui bloquait un débutant).
 */
export function dailyIds(): { ids: string[]; label: string } {
  const due = dueIds().slice(0, 10)
  if (due.length) return { ids: due, label: "Entraînement du jour" }
  const seen = Object.keys(S().srs)
    .filter((k) => ITEMS[k])
    .sort((a, b) => S().srs[a].box - S().srs[b].box || (S().srs[a].due < S().srs[b].due ? -1 : 1))
    .slice(0, 10)
  if (seen.length) return { ids: seen, label: "Entraînement libre" }
  const s = currentStep() || MAIN[0]
  return { ids: shuffle(s.drills.map((_, i) => `d:${s.id}:${i}`)), label: "Premier entraînement" }
}

/* ---------- Séance terminée ---------- */
export function finishLesson(s: Step) {
  st(s.id).lessons++
  commit()
}
export function finishExam(s: Step, score: number) {
  const x = st(s.id)
  let passedNow = false
  if (score > x.best) x.best = score
  commit()
  if (score >= 0.8 && !x.passed) {
    x.passed = true
    x.date = today()
    commit()
    award(XP.exam)
    passedNow = true
  }
  if (score === 1 && !x.perfect) {
    x.perfect = true
    commit()
    award(XP.perfect)
  }
  return { passedNow, validatedNow: checkValidation(s) }
}

/* ---------- Sauvegarde ---------- */
export function exportJson() {
  return JSON.stringify(R)
}
export function importJson(text: string): string | null {
  let o: any
  try {
    o = JSON.parse(text)
  } catch {
    return "Fichier illisible : ce n'est pas un JSON valide. Rien n'a été modifié."
  }
  if (!isObj(o) || !isObj(o.state) || !isObj(o.state.steps)) return "Ce fichier ne contient pas de sauvegarde du parcours. Rien n'a été modifié."
  R.state = normState(o.state)
  applyProfil(R.state.settings.profil)
  if (isObj(o.notes)) R.notes = o.notes
  if (isObj(o.answers)) R.answers = o.answers
  if (isObj(o.plan)) R.plan = o.plan
  if (o.journal) R.journal = o.journal
  if (o.tutor) R.tutor = o.tutor
  registerCoach()
  commit()
  return null
}
export function resetAll() {
  R = { state: blankState(), notes: {}, answers: {}, plan: null, journal: null, tutor: null }
  applyProfil("")
  registerCoach()
  commit()
}

export { BYID, STEPS }
