import raw from "@/data/content.json"

export type Quiz = { q: string; o: string[]; a: number; e?: string }
export type Drill =
  | { type: "tf"; q: string; a: boolean; e?: string; step?: string }
  | { type: "cloze" | "mcq"; q: string; o: string[]; a: number; e?: string; step?: string }
  | { type: "order"; q: string; items: string[]; e?: string; step?: string }
  | { type: "match"; q: string; pairs: [string, string][]; e?: string; step?: string }
export type Exercise = { t: string; c: string; opt?: boolean }
/** Variantes par profil : chemin (« quiz.2 », « notions.3 », « ex.0 », « obj.1 », « titre ») vers la valeur du profil. */
export type Variants = Record<string, Record<string, unknown>>
export type Step = {
  id: string
  cote: string
  titre: string
  bloc: string
  voie: "socle" | "metier" | "expert" | "bonus"
  cadre: number
  comp: string[]
  duree: string
  obj: string[]
  notions: [string, string][]
  res: [string, string][]
  ex: Exercise[]
  quiz: Quiz[]
  drills: Drill[]
  /** Voie Métier : profil auquel l'étape appartient. */
  profil?: string
  pv?: Variants
}
export type Profil = { id: string; nom: string; court: string; desc: string; bloc: string; voie: string }
export type Item = Drill & { id: string; step: string; kind: "quiz" | "drill" | "coach" | "news" }

const data = raw as unknown as {
  SRC: Record<string, { n: string; u: string }>
  STEPS: Step[]
  GLOSS: Gloss[]
  GLOSS_THEMES: string[]
  COMPS: Comp[]
  LEVELS: string[]
  VOIES: { id: string; nom: string; desc: string; open: string }[]
  CADRES: Record<string, { nom: string; desc: string }>
  CADRE_NOTE: string
  DEFIS: Defi[]
  NEWS: News[]
  PROFILS: Profil[]
}
export type Gloss = { t: string; th: string; d: string; ex: string; step: string }
export type Comp = { id: string; nom: string; desc: string }
export type Defi = { id: string; comp: string; cadre: number; titre: string; consigne: string; critere: string; pv?: Record<string, Partial<Defi>> }
export type News = { week: string; date: string; titre: string; items: { titre: string; texte: string; u: string; statut: string }[]; drills: Drill[] }

export const SRC = data.SRC
export const PROFILS = data.PROFILS
export const PROFIL_IDS = PROFILS.map((p) => p.id)
export const STEPS = data.STEPS
export const GLOSS = data.GLOSS
export const GLOSS_THEMES = data.GLOSS_THEMES
export const { COMPS, LEVELS, VOIES, CADRES, CADRE_NOTE, DEFIS } = data
/* Les semaines les plus récentes d'abord ; les anciennes restent jouables. */
export const NEWS = [...data.NEWS].sort((a, b) => (a.week < b.week ? 1 : -1))
export const BYID: Record<string, Step> = Object.fromEntries(STEPS.map((s) => [s.id, s]))

export type Unit = { name: string; steps: Step[]; color: UnitColor }
export type UnitColor = { base: string; deep: string; soft: string }

/* Une couleur par bloc, en rotation. Aucune teinte violette. */
const COLORS: UnitColor[] = [
  { base: "var(--u1)", deep: "var(--u1-d)", soft: "var(--u1-s)" },
  { base: "var(--u2)", deep: "var(--u2-d)", soft: "var(--u2-s)" },
  { base: "var(--u3)", deep: "var(--u3-d)", soft: "var(--u3-s)" },
  { base: "var(--u4)", deep: "var(--u4-d)", soft: "var(--u4-s)" },
]

/* ---------- Profil métier ----------
 * Le contenu commun a une valeur de base ; une étape ou un défi peut porter des variantes par profil (pv).
 * applyProfil réécrit en place les étapes, les défis, les questions et les listes dérivées :
 * les écrans qui lisent ces tableaux au rendu suivent le profil sans autre changement.
 */
const clone = <T,>(o: T): T => JSON.parse(JSON.stringify(o))
const BASE_STEPS = clone(STEPS)
const BASE_DEFIS = clone(DEFIS)
function setPath(o: any, path: string, v: unknown) {
  const ks = path.split(".")
  for (const k of ks.slice(0, -1)) o = o[Array.isArray(o) ? +k : k]
  const last = ks[ks.length - 1]
  o[Array.isArray(o) ? +last : last] = clone(v)
}
/** Étapes du parcours pour le profil courant (hors bonus) : Socle, Métier du profil, Expert. */
export const MAIN: Step[] = []
/** Étapes visibles pour le profil courant, bonus compris. */
export const VIS: Step[] = []
export const UNITS: Unit[] = []
export const ITEMS: Record<string, Item> = {}
export let PROFIL = ""
export const profilOf = (id: string) => PROFILS.find((p) => p.id === id)

export function applyProfil(p: string) {
  PROFIL = PROFIL_IDS.includes(p) ? p : ""
  const key = PROFIL || "support"
  STEPS.forEach((s, i) => {
    const b = BASE_STEPS[i]
    for (const k of ["titre", "obj", "notions", "ex", "quiz", "drills"] as const) (s as any)[k] = clone((b as any)[k])
    for (const [path, v] of Object.entries(b.pv?.[key] || {})) setPath(s, path, v)
  })
  DEFIS.forEach((d, i) => Object.assign(d, clone(BASE_DEFIS[i]), clone(BASE_DEFIS[i].pv?.[key] || {})))
  const vis = STEPS.filter((s) => s.voie !== "metier" || s.profil === key)
  VIS.splice(0, VIS.length, ...vis)
  MAIN.splice(0, MAIN.length, ...vis.filter((s) => s.voie !== "bonus"))
  UNITS.length = 0
  for (const s of vis) {
    const u = UNITS[UNITS.length - 1]
    if (!u || u.name !== s.bloc) UNITS.push({ name: s.bloc, steps: [s], color: COLORS[UNITS.length % COLORS.length] })
    else u.steps.push(s)
  }
  /* Les questions de toutes les étapes restent connues (révision espacée d'un ancien profil). */
  for (const k of Object.keys(ITEMS)) if (k.startsWith("q:") || k.startsWith("d:")) delete ITEMS[k]
  for (const s of STEPS) {
    s.quiz.forEach((q, i) => {
      const id = `q:${s.id}:${i}`
      ITEMS[id] = { id, step: s.id, kind: "quiz", type: "mcq", q: q.q, o: q.o, a: q.a, e: q.e }
    })
    s.drills.forEach((d, i) => {
      const id = `d:${s.id}:${i}`
      ITEMS[id] = { ...d, id, step: s.id, kind: "drill" } as Item
    })
  }
}
applyProfil("")
export const unitOf = (id: string) => UNITS.find((u) => u.steps.some((s) => s.id === id))!

for (const w of NEWS)
  w.drills.forEach((d, i) => {
    const id = `n:${w.week}:${i}`
    ITEMS[id] = { ...d, id, step: "", kind: "news" } as Item
  })

export function validDrill(d: unknown): d is Drill {
  const x = d as Record<string, unknown>
  if (!x || typeof x !== "object" || typeof x.q !== "string") return false
  if (x.type === "tf") return typeof x.a === "boolean"
  if (x.type === "cloze" || x.type === "mcq")
    return Array.isArray(x.o) && x.o.length > 1 && typeof x.a === "number" && x.a >= 0 && x.a < x.o.length
  if (x.type === "order") return Array.isArray(x.items) && x.items.length > 1
  if (x.type === "match")
    return Array.isArray(x.pairs) && x.pairs.length > 1 && x.pairs.every((p) => Array.isArray(p) && p.length === 2)
  return false
}
