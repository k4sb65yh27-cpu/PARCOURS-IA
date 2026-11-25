import { useEffect, useRef, useState } from "react"
import { AnimatePresence, motion, useReducedMotion } from "motion/react"
import { ArrowLeft, Check, ExternalLink, GraduationCap, Target, X } from "lucide-react"
import { toast } from "sonner"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { SRC, type Step } from "@/lib/content"
import { XP, exDone, markNotions, peek, setNote, toggleEx, useStore, validated } from "@/lib/store"
import { sfx } from "@/lib/sound"
import { copyText, tutorPrompt } from "@/lib/tutor"
import { CadreNote } from "@/components/CadreNote"

function Rich({ text }: { text: string }) {
  if (text.startsWith("<pre>"))
    return (
      <pre className="overflow-x-auto rounded-xl bg-secondary p-3 text-sm leading-relaxed whitespace-pre-wrap">
        {text.replace(/^<pre>/, "").replace(/<\/pre>\s*$/, "")}
      </pre>
    )
  /* Les mentions de statut ([Non vérifié], [Inférence]) deviennent des pastilles lisibles. */
  const parts = text.split(/(\[(?:Non vérifié|Inférence|Spéculation)\])/)
  return (
    <p className="leading-relaxed">
      {parts.map((p, i) =>
        /^\[(Non vérifié|Inférence|Spéculation)\]$/.test(p) ? (
          <span key={i} className="mx-0.5 inline-block rounded-md bg-sun-soft px-1.5 align-[1px] text-xs font-extrabold text-sun-deep">
            {p.slice(1, -1)}
          </span>
        ) : (
          p
        ),
      )}
    </p>
  )
}

export function StepGuide({ step, tab = "objectifs", onBack }: { step: Step; tab?: string; onBack: () => void }) {
  const root = useStore()
  const x = peek(step.id)
  const [note, setN] = useState(String(root.notes[step.id] ?? ""))
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined)
  const req = step.ex.filter((e) => !e.opt).length
  const doneReq = step.ex.filter((e, i) => !e.opt && x.ex[i]).length

  return (
    <div className="fixed inset-0 z-30 flex flex-col overflow-y-auto bg-background safe-t">
      <header className="sticky top-0 z-10 border-b-2 border-line bg-background/95 backdrop-blur-sm">
        <div className="mx-auto flex w-full max-w-2xl items-center gap-2 px-2 py-2">
          <button type="button" onClick={onBack} aria-label="Revenir au parcours" className="grid size-11 place-items-center rounded-full hover:bg-secondary">
            <ArrowLeft className="size-6" strokeWidth={2.5} />
          </button>
          <div className="min-w-0">
            <p className="text-xs font-black tracking-widest text-muted-foreground uppercase">
              Étape {step.cote} · {step.bloc} · {step.duree}
            </p>
            <h1 className="truncate text-lg font-black">{step.titre}</h1>
          </div>
          {validated(step) && (
            <span className="ml-auto shrink-0 rounded-full bg-sun-soft px-3 py-1 text-xs font-black text-sun-deep uppercase">Validée</span>
          )}
        </div>
      </header>

      <Tabs defaultValue={tab} className="mx-auto w-full max-w-2xl px-4 pt-4 pb-10">
        <TabsList className="grid h-auto w-full grid-cols-4 rounded-xl bg-secondary p-1">
          {[
            ["objectifs", "Objectifs"],
            ["ressources", "Sources"],
            ["exercices", `Exercices ${doneReq}/${req}`],
            ["carnet", "Carnet"],
          ].map(([v, l]) => (
            <TabsTrigger key={v} value={v} className="min-h-10 rounded-lg px-1 text-[0.8rem] font-extrabold">
              {l}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value="objectifs" className="mt-5">
          {step.cadre > 1 && (
            <div className="mb-4">
              <CadreNote cadre={step.cadre} />
            </div>
          )}
          <ul className="grid gap-3">
            {step.obj.map((o) => (
              <li key={o} className="flex gap-3">
                <Target className="mt-0.5 size-5 shrink-0 text-teal" aria-hidden="true" />
                <span>{o}</span>
              </li>
            ))}
          </ul>
          <h2 className="mt-7 mb-3 text-lg font-black">Notions de l'étape</h2>
          <dl className="grid gap-4">
            {step.notions.map(([t, d]) => (
              <div key={t} className="rounded-2xl border-2 border-line p-4">
                <dt className="mb-1 font-black">{t}</dt>
                <dd className="font-semibold text-foreground/85">
                  <Rich text={d} />
                </dd>
              </div>
            ))}
          </dl>
          <section className="mt-6 rounded-2xl bg-teal-soft/50 p-4">
            <h2 className="flex items-center gap-2 font-black">
              <GraduationCap className="size-5 text-teal" aria-hidden="true" /> Travailler l'étape avec un tuteur
            </h2>
            <p className="mt-1 text-sm">
              Copiez la consigne, collez-la dans votre assistant habituel : il vous interroge question par question jusqu'à ce que vous sachiez faire seul.
            </p>
            <button type="button" className="btn3d mt-3 w-full" onClick={() => { sfx.tap(); copyText(tutorPrompt(step), "Consigne du tuteur copiée.") }}>
              Copier la consigne du tuteur
            </button>
          </section>
        </TabsContent>

        <TabsContent value="ressources" className="mt-5">
          <ul className="grid gap-3">
            {step.res.map(([k, d]) => {
              const s = SRC[k]
              return (
                <li key={k} className="rounded-2xl border-2 border-line p-4">
                  {s ? (
                    <a href={s.u} target="_blank" rel="noopener noreferrer" className="inline-flex items-start gap-1.5 font-black text-u2 underline-offset-4 hover:underline" style={{ color: "var(--u2)" }}>
                      {s.n}
                      <ExternalLink className="mt-1 size-4 shrink-0" aria-hidden="true" />
                    </a>
                  ) : (
                    <span className="font-black">{k}</span>
                  )}
                  <p className="mt-1 text-sm text-muted-foreground">{d}</p>
                </li>
              )
            })}
          </ul>
        </TabsContent>

        <TabsContent value="exercices" className="mt-5">
          <p className="mb-4 text-sm text-muted-foreground">
            À faire hors de l'application, sur des documents fictifs ou publics. Cochez quand le critère est rempli : +{XP.ex} XP par exercice.
          </p>
          <ul className="grid gap-3">
            {step.ex.map((e, i) => {
              const on = !!x.ex[i]
              return (
                <li key={i}>
                  <button
                    type="button"
                    role="checkbox"
                    aria-checked={on}
                    onClick={() => {
                      const r = toggleEx(step, i)
                      if (r.validatedNow) {
                        sfx.unlock()
                        toast.success(`Étape ${step.cote} validée. +${XP.step} XP`)
                      } else if (r.gained) {
                        sfx.ok()
                        toast(`+${r.gained} XP`)
                      } else sfx.tap()
                    }}
                    className="tile items-start"
                    data-state={on ? "good" : undefined}
                  >
                    <span
                      className="mt-0.5 grid size-7 shrink-0 place-items-center rounded-lg border-2"
                      style={{ background: on ? "var(--teal)" : "transparent", borderColor: on ? "var(--teal)" : "var(--line-deep)" }}
                    >
                      {on && <Check className="size-4 text-white" strokeWidth={4} />}
                    </span>
                    <span>
                      <span className="block">
                        {e.t}
                        {e.opt && <span className="ml-2 rounded-md bg-secondary px-1.5 py-0.5 text-xs font-extrabold text-muted-foreground">facultatif</span>}
                      </span>
                      <span className="mt-1 block text-sm font-semibold opacity-75">Critère de réussite : {e.c}</span>
                    </span>
                  </button>
                </li>
              )
            })}
          </ul>
          {exDone(step) && !x.passed && <p className="mt-4 text-sm font-bold text-teal">Exercices faits. Il reste l'examen pour valider l'étape.</p>}
        </TabsContent>

        <TabsContent value="carnet" className="mt-5">
          <label htmlFor="note" className="mb-2 block font-black">
            Carnet de l'étape
          </label>
          <Textarea
            id="note"
            rows={10}
            value={note}
            onChange={(e) => {
              setN(e.target.value)
              clearTimeout(timer.current)
              const v = e.target.value
              timer.current = setTimeout(() => setNote(step.id, v), 400)
            }}
            onBlur={() => setNote(step.id, note)}
            placeholder="Ce que vous retenez, ce qui reste flou, les consignes à réutiliser."
            className="min-h-48 rounded-2xl border-2 text-base font-semibold"
          />
          <p className="mt-2 text-sm text-muted-foreground">Enregistré sur cet appareil pendant la saisie. Pas de données de dossier.</p>
        </TabsContent>
      </Tabs>
    </div>
  )
}

/** Lecture des notions en fiches, une par écran, avant la première leçon. */
export function NotionsReader({ step, onClose }: { step: Step; onClose: () => void }) {
  const reduce = useReducedMotion()
  const [i, setI] = useState(0)
  const [dir, setDir] = useState(1)
  const n = step.notions.length
  const last = i === n - 1
  const go = (d: number) => {
    sfx.tap()
    setDir(d)
    setI((v) => Math.min(n - 1, Math.max(0, v + d)))
  }
  const finish = () => {
    const first = markNotions(step)
    sfx.done()
    if (first) toast(`+${XP.notions} XP · notions lues`)
    onClose()
  }
  useEffect(() => {
    const on = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight") last ? finish() : go(1)
      if (e.key === "ArrowLeft") go(-1)
      if (e.key === "Escape") onClose()
    }
    window.addEventListener("keydown", on)
    return () => window.removeEventListener("keydown", on)
  })
  const [t, d] = step.notions[i]
  return (
    <div className="fixed inset-0 z-40 flex flex-col bg-background safe-t">
      <header className="mx-auto flex w-full max-w-2xl items-center gap-3 px-4 pt-4 pb-2">
        <button type="button" onClick={onClose} aria-label="Fermer" className="grid size-11 place-items-center rounded-full text-muted-foreground hover:bg-secondary">
          <X className="size-6" strokeWidth={3} />
        </button>
        <div className="flex flex-1 gap-1.5" aria-label={`Fiche ${i + 1} sur ${n}`}>
          {step.notions.map((_, k) => (
            <span key={k} className="h-2.5 flex-1 rounded-full" style={{ background: k <= i ? "var(--teal)" : "var(--line)" }} />
          ))}
        </div>
      </header>
      <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col overflow-y-auto px-4 pt-6">
        <p className="text-sm font-extrabold tracking-wide text-muted-foreground uppercase">
          Étape {step.cote} · notion {i + 1} sur {n}
        </p>
        <AnimatePresence mode="wait" initial={false} custom={dir}>
          <motion.article
            key={i}
            initial={reduce ? { opacity: 0 } : { opacity: 0, x: 40 * dir }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, x: -40 * dir }}
            transition={{ type: "spring", bounce: 0, duration: 0.3 }}
            className="mt-3 rounded-3xl border-2 border-b-[5px] border-line p-5"
          >
            <h2 className="text-2xl font-black">{t}</h2>
            <div className="mt-3 text-[1.05rem] font-semibold">
              <Rich text={d} />
            </div>
          </motion.article>
        </AnimatePresence>
      </main>
      <footer className="safe-b border-t-2 border-line">
        <div className="mx-auto grid w-full max-w-2xl grid-cols-[auto_1fr] gap-3 px-4 pt-4 pb-5">
          <button type="button" onClick={() => go(-1)} disabled={i === 0} className="btn3d px-4" style={{ "--c": "var(--card)", "--cd": "var(--line)", "--fg": "var(--foreground)", border: "2px solid var(--line)", borderBottomWidth: 4 } as React.CSSProperties} aria-label="Fiche précédente">
            <ArrowLeft className="size-5" strokeWidth={3} />
          </button>
          <button type="button" onClick={() => (last ? finish() : go(1))} className="btn3d">
            {last ? "J'ai compris" : "Suivante"}
          </button>
        </div>
      </footer>
    </div>
  )
}
