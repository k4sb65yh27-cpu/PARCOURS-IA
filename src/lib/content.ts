import raw from "@/data/content.json"

export type Quiz = { q: string; o: string[]; a: number; e?: string }
export type Drill =
  | { type: "tf"; q: string; a: boolean; e?: string; step?: string }
  | { type: "cloze" | "mcq"; q: string; o: string[]; a: number; e?: string; step?: string }
  | { type: "order"; q: string; items: string[]; e?: string; step?: string }
  | { type: "match"; q: string; pairs: [string, string][]; e?: string; step?: string }
export type Exercise = { t: string; c: string; opt?: boolean }
export type Step = {
  id: string
  cote: string
  titre: string
  bloc: string
  duree: string
  obj: string[]
  notions: [string, string][]
  res: [string, string][]
  ex: Exercise[]
  quiz: Quiz[]
  drills: Drill[]
}
export type Item = Drill & { id: string; step: string; kind: "quiz" | "drill" | "coach" }

const data = raw as unknown as {
  SRC: Record<string, { n: string; u: string }>
  STEPS: Step[]
  GLOSS: [string, string][]
}

export const SRC = data.SRC
export const STEPS = data.STEPS
export const GLOSS = data.GLOSS
export const MAIN = STEPS.filter((s) => s.id !== "bonus")
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

export const UNITS: Unit[] = []
for (const s of STEPS) {
  const u = UNITS[UNITS.length - 1]
  if (!u || u.name !== s.bloc) UNITS.push({ name: s.bloc, steps: [s], color: COLORS[UNITS.length % COLORS.length] })
  else u.steps.push(s)
}
export const unitOf = (id: string) => UNITS.find((u) => u.steps.some((s) => s.id === id))!

export const ITEMS: Record<string, Item> = {}
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
