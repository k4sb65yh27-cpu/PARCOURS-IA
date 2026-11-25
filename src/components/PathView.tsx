import { useEffect, useRef, useState } from "react"
import { motion, useReducedMotion } from "motion/react"
import { BookOpen, Check, ClipboardCheck, Lock, Star, Trophy } from "lucide-react"
import { Drawer, DrawerContent, DrawerDescription, DrawerHeader, DrawerTitle } from "@/components/ui/drawer"
import { UNITS, VOIES, type Step, type Unit } from "@/lib/content"
import { CadreNote } from "@/components/CadreNote"
import { NODE_KINDS, XP, currentNode, nodeDone, peek, unlocked, useStore, validated, voieOpen, type NodeKind } from "@/lib/store"
import { sfx } from "@/lib/sound"

const ICON: Record<NodeKind, typeof Star> = { notions: BookOpen, lecon: Star, ex: ClipboardCheck, exam: Trophy }
const NAME: Record<NodeKind, string> = { notions: "Notions", lecon: "Leçon", ex: "Exercices pratiques", exam: "Examen de validation" }
const SHORT: Record<NodeKind, string> = { notions: "Notions", lecon: "Leçon", ex: "Exercices", exam: "Examen" }
/* Décalage horizontal des nœuds : un serpentin régulier. */
const OFFS = [0, 52, 78, 52, 0, -52, -78, -52]

export type Go = (a: { kind: NodeKind | "guide"; step: Step; tab?: string }) => void

export function PathView({ onGo }: { onGo: Go }) {
  useStore()
  const cur = currentNode()
  const [open, setOpen] = useState<{ step: Step; kind: NodeKind } | null>(null)
  const curRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    curRef.current?.scrollIntoView({ block: "center", behavior: "auto" })
  }, [])

  let n = 0
  return (
    <div className="mx-auto w-full max-w-xl pb-10">
      {UNITS.map((u, ui) => (
        <section key={u.name} aria-label={`Bloc ${u.name}`} className="mb-4">
          {u.steps[0].voie !== UNITS[ui - 1]?.steps[0].voie && <VoieIntro voie={u.steps[0].voie} />}
          <UnitBanner u={u} />
          {u.steps.map((s) => {
            const open_ = unlocked(s)
            return (
              <div key={s.id} className="mt-6 px-4">
                <button
                  type="button"
                  onClick={() => onGo({ kind: "guide", step: s })}
                  className="mx-auto flex w-full max-w-sm items-center gap-3 rounded-xl px-2 py-1.5 text-left hover:bg-secondary"
                >
                  <span className="h-0.5 flex-1 bg-line" />
                  <span className="text-center">
                    <span className="block text-sm font-bold text-muted-foreground">
                      Étape {s.cote}
                      {s.id === "bonus" ? " · facultative" : ""}
                    </span>
                    {s.cadre > 1 && <span className="mt-0.5 block"><CadreNote cadre={s.cadre} compact /></span>}
                    <span className={`block font-extrabold ${open_ ? "" : "text-muted-foreground"}`}>{s.titre}</span>
                  </span>
                  <span className="h-0.5 flex-1 bg-line" />
                </button>
                <div className="relative mt-12 flex flex-col items-center gap-[68px]">
                  {NODE_KINDS.map((k) => {
                    const off = OFFS[n++ % OFFS.length]
                    const isCur = !!cur && cur.step.id === s.id && cur.kind === k
                    return (
                      <PathNode
                        key={k}
                        ref={isCur ? curRef : undefined}
                        u={u}
                        kind={k}
                        off={off}
                        done={nodeDone(s, k)}
                        locked={!open_}
                        current={isCur}
                        big={k === "exam"}
                        onClick={() => {
                          sfx.tap()
                          setOpen({ step: s, kind: k })
                        }}
                      />
                    )
                  })}
                </div>
              </div>
            )
          })}
        </section>
      ))}

      <Drawer open={!!open} onOpenChange={(o) => !o && setOpen(null)}>
        <DrawerContent className="safe-b">
          {open && <NodeSheet step={open.step} kind={open.kind} onGo={(a) => { setOpen(null); onGo(a) }} />}
        </DrawerContent>
      </Drawer>
    </div>
  )
}

function VoieIntro({ voie }: { voie: string }) {
  const v = VOIES.find((x) => x.id === voie)
  if (!v) return null
  const open = voieOpen(voie)
  return (
    <div className="mx-4 mt-8 mb-2 first:mt-4">
      <h2 className="text-2xl font-black">Voie {v.nom}</h2>
      <p className="mt-1 text-[0.95rem] text-muted-foreground">
        {v.desc} {!open && <span className="font-extrabold text-foreground">{v.open}</span>}
      </p>
    </div>
  )
}

function UnitBanner({ u }: { u: Unit }) {
  const total = u.steps.length
  const [voie, title] = u.name.includes(" : ") ? u.name.split(" : ") : ["", u.name]
  const done = u.steps.filter(validated).length
  return (
    <div className="sticky top-[60px] z-10 bg-background/95 px-4 pt-3 pb-1 backdrop-blur-sm">
      <div
        className="flex items-center justify-between gap-3 rounded-2xl px-4 py-3 text-white"
        style={{ background: u.color.base, borderBottom: `4px solid ${u.color.deep}` }}
      >
        <div className="min-w-0">
          <p className="text-xs font-black tracking-widest uppercase opacity-85">
            {voie ? `${voie} · ` : ""}
            {total > 1 ? `Étapes ${u.steps[0].cote} à ${u.steps[total - 1].cote}` : `Étape ${u.steps[0].cote}`}
          </p>
          <h2 className="truncate text-lg font-black first-letter:uppercase">{title}</h2>
        </div>
        <span className="shrink-0 rounded-full bg-black/15 px-2.5 py-1 text-sm font-black tabular-nums" aria-label={`${done} étape${done > 1 ? "s" : ""} validée${done > 1 ? "s" : ""} sur ${total}`}>
          {done}/{total}
        </span>
      </div>
    </div>
  )
}

type NodeProps = {
  u: Unit
  kind: NodeKind
  off: number
  done: boolean
  locked: boolean
  current: boolean
  big: boolean
  onClick: () => void
  ref?: React.Ref<HTMLButtonElement>
}
function PathNode({ u, kind, off, done, locked, current, big, onClick, ref }: NodeProps) {
  const reduce = useReducedMotion()
  const Icon = done ? Check : locked ? Lock : ICON[kind]
  const size = big ? 80 : 70
  const bg = locked ? "var(--line)" : done ? "var(--sun)" : u.color.base
  const deep = locked ? "var(--line-deep)" : done ? "var(--sun-deep)" : u.color.deep
  const label = `${NAME[kind]}${done ? ", terminé" : locked ? ", verrouillé" : current ? ", à faire maintenant" : ""}`
  return (
    <div className="relative" style={{ transform: `translateX(${off}px)` }}>
      {current && (
        <motion.div
          initial={reduce ? false : { y: 6, opacity: 0 }}
          animate={reduce ? { opacity: 1 } : { y: [0, -5, 0], opacity: 1 }}
          transition={reduce ? undefined : { y: { repeat: Infinity, duration: 1.8, ease: "easeInOut" }, opacity: { duration: 0.3 } }}
          className="absolute -top-11 left-1/2 z-10 -translate-x-1/2 rounded-xl border-2 border-line bg-card px-3 py-1.5 text-sm font-black tracking-wider whitespace-nowrap uppercase"
          style={{ color: u.color.base }}
        >
          Commencer
          <span className="absolute -bottom-[7px] left-1/2 size-3 -translate-x-1/2 rotate-45 border-r-2 border-b-2 border-line bg-card" />
        </motion.div>
      )}
      {current && (
        <span
          aria-hidden="true"
          className="absolute -inset-[7px] rounded-full border-[5px]"
          style={{ borderColor: "var(--line)", borderBottomWidth: 8 }}
        />
      )}
      <button
        ref={ref}
        type="button"
        onClick={onClick}
        aria-label={label}
        className="relative grid place-items-center rounded-full text-white transition-[transform,border-bottom-width] duration-75 active:translate-y-[4px] active:[border-bottom-width:2px]"
        style={{
          width: size,
          height: size - 6,
          background: bg,
          borderBottom: `7px solid ${deep}`,
          color: locked ? "var(--muted-foreground)" : "#fff",
        }}
      >
        <Icon className={big ? "size-9" : "size-8"} strokeWidth={done ? 3.5 : 2.5} fill={kind === "lecon" && !done && !locked ? "currentColor" : "none"} />
      </button>
      <span className="absolute top-full left-1/2 mt-1 -translate-x-1/2 text-[13px] font-extrabold whitespace-nowrap text-muted-foreground" aria-hidden="true">
        {SHORT[kind]}
      </span>
    </div>
  )
}

function NodeSheet({ step, kind, onGo }: { step: Step; kind: NodeKind; onGo: Go }) {
  const open = unlocked(step)
  const x = peek(step.id)
  const done = nodeDone(step, kind)
  const nq = Math.min(10, step.quiz.length + step.drills.length)
  const req = step.ex.filter((e) => !e.opt).length
  const desc: Record<NodeKind, string> = {
    notions: `${step.notions.length} fiches à lire, une à la fois. +${XP.notions} XP la première fois.`,
    lecon: `${nq} questions, 5 vies. +${XP.lesson} XP par bonne réponse au premier essai.${x.lessons ? ` Leçons terminées : ${x.lessons}.` : ""}`,
    ex: `${req} exercice${req > 1 ? "s" : ""} obligatoire${req > 1 ? "s" : ""} à faire hors de l'application, puis à cocher. +${XP.ex} XP chacun.`,
    exam: `${step.quiz.length} questions, réussite à 80 %. +${XP.exam} XP, +${XP.perfect} XP sans faute.${x.best ? ` Meilleur score : ${Math.round(x.best * 100)} %.` : ""}`,
  }
  const cta: Record<NodeKind, string> = {
    notions: done ? "Relire" : "Lire les notions",
    lecon: done ? "Refaire une leçon" : "Commencer",
    ex: "Voir les exercices",
    exam: x.passed ? "Repasser l'examen" : "Passer l'examen",
  }
  return (
    <div className="mx-auto w-full max-w-md px-5 pb-6">
      <DrawerHeader className="px-0 text-left">
        <p className="text-xs font-black tracking-widest text-muted-foreground uppercase">
          Étape {step.cote} · {step.titre}
        </p>
        <DrawerTitle className="text-2xl font-black">{NAME[kind]}</DrawerTitle>
        <DrawerDescription className="text-[0.95rem] font-semibold">
          {open ? desc[kind] : locked(step)}
        </DrawerDescription>
      </DrawerHeader>
      {step.cadre > 1 && kind !== "notions" && (
        <div className="mb-4">
          <CadreNote cadre={step.cadre} />
        </div>
      )}
      <div className="grid gap-3">
        <button type="button" disabled={!open} onClick={() => onGo({ kind, step })} className="btn3d w-full">
          {open ? cta[kind] : "Verrouillé"}
        </button>
        <button type="button" onClick={() => onGo({ kind: "guide", step })} className="btn3d w-full" style={{ "--c": "var(--card)", "--cd": "var(--line)", "--fg": "var(--teal)", border: "2px solid var(--line)", borderBottomWidth: 4 } as React.CSSProperties}>
          Guide de l'étape
        </button>
      </div>
    </div>
  )
}

function locked(s: Step) {
  if (!voieOpen(s.voie)) return `${VOIES.find((v) => v.id === s.voie)?.open ?? ""} Le mode libre du profil ouvre tout.`
  return "Validez l'étape précédente de cette voie pour ouvrir celle-ci, ou activez le mode libre dans le profil."
}
