import { Mascot } from "@/components/Mascot"
import { useEffect, useRef } from "react"
import { motion, useReducedMotion } from "motion/react"
import { Flame } from "lucide-react"
import { Confetti, type ConfettiRef } from "@/components/ui/confetti"
import { NumberTicker } from "@/components/ui/number-ticker"
import { BYID } from "@/lib/content"
import { exDone } from "@/lib/store"
import { sfx } from "@/lib/sound"

export type Summary = {
  mode: "lesson" | "exam" | "review"
  label: string
  stepId?: string
  total: number
  good: number
  ms: number
  xp: number
  out: boolean
  streak: number
  streakBumped: boolean
  score?: number
  passedNow?: boolean
  validated?: boolean
}

const pct = (a: number, b: number) => (b ? Math.round((100 * a) / b) : 0)

export function SessionEnd({ sm, onClose }: { sm: Summary; onClose: () => void }) {
  const reduce = useReducedMotion()
  const conf = useRef<ConfettiRef>(null)
  const step = sm.stepId ? BYID[sm.stepId] : undefined
  const precision = pct(sm.good, sm.total)
  const failedExam = sm.mode === "exam" && (sm.score ?? 0) < 0.8
  const win = !sm.out && !failedExam && precision >= 60
  const sec = Math.round(sm.ms / 1000)

  useEffect(() => {
    if (sm.validated) setTimeout(() => sfx.unlock(), 500)
    else if (sm.streakBumped) setTimeout(() => sfx.streak(), 700)
    if (!win || reduce) return
    const t = setTimeout(() => {
      conf.current?.fire({ particleCount: 90, spread: 75, startVelocity: 38, origin: { y: 0.35 }, colors: ["#0f8f7e", "#f2a516", "#2f6fb0", "#c2612b"], disableForReducedMotion: true })
    }, 250)
    return () => clearTimeout(t)
  }, [win, reduce, sm.validated, sm.streakBumped])

  let title = "Leçon terminée"
  let sub = step ? `Étape ${step.cote} · ${step.titre}` : sm.label
  if (sm.out) {
    title = "Plus de vies"
    sub = "Les XP gagnés restent acquis et les questions ratées reviendront dans l'entraînement du jour. Relisez les notions, puis relancez la leçon."
  } else if (sm.mode === "exam") {
    title = failedExam ? "Examen à repasser" : "Examen réussi"
    sub = failedExam
      ? "Le seuil est de 80 %. Revoyez les notions puis repassez l'examen."
      : sm.validated
        ? "L'étape est validée. La suivante est ouverte."
        : step && !exDone(step)
          ? "Il reste des exercices pratiques à cocher pour valider l'étape."
          : "Le seuil de 80 % est atteint."
  } else if (sm.mode === "review") title = "Entraînement terminé"

  const tone = sm.out || failedExam ? "ko" : "sun"

  return (
    <div className="fixed inset-0 z-40 flex flex-col bg-background safe-t">
      <Confetti ref={conf} manualstart className="pointer-events-none fixed inset-0 z-0 size-full" />
      <main className="relative z-10 mx-auto flex w-full max-w-md flex-1 flex-col items-center overflow-y-auto px-5 pt-12 text-center">
        <motion.div
          initial={reduce ? false : { scale: 0.4, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: "spring", bounce: 0.45, duration: 0.6 }}
        >
          <Mascot size={128} className="mb-4" mood={tone === "ko" ? "sad" : win || sm.validated ? "cheer" : "happy"} />
        </motion.div>
        <motion.h1
          initial={reduce ? false : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15, duration: 0.3 }}
          className={`mt-5 text-3xl font-black ${tone === "ko" ? "text-ko" : "text-sun-deep"}`}
        >
          {sm.validated ? "Étape validée" : title}
        </motion.h1>
        <p className="mt-1.5 text-muted-foreground">{sub}</p>

        <motion.dl
          initial={reduce ? false : { opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.35 }}
          className="mt-7 w-full overflow-hidden rounded-2xl border-2 border-line bg-card text-left"
        >
          <Row label="XP gagnés">
            <span className="text-teal">+</span>
            <NumberTicker value={sm.xp} delay={0.45} className="text-teal tracking-normal dark:text-teal" />
          </Row>
          <Row label={sm.mode === "exam" ? "Score" : "Précision"}>
            <span style={{ color: (sm.mode === "exam" ? pct(sm.good, sm.total) : precision) < 50 ? "var(--ko)" : (sm.mode === "exam" ? pct(sm.good, sm.total) : precision) < 80 ? "var(--sun-deep)" : "var(--teal)" }}>{sm.mode === "exam" ? pct(sm.good, sm.total) : precision} %</span>
          </Row>
          <Row label="Temps">
            <span className="text-teal tabular-nums">
              {sec < 60 ? `${sec} s` : `${Math.floor(sec / 60)} min ${String(sec % 60).padStart(2, "0")} s`}
            </span>
          </Row>
        </motion.dl>

        {sm.streakBumped && sm.streak > 0 && (
          <motion.div
            initial={reduce ? false : { opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, type: "spring", bounce: 0.35, duration: 0.5 }}
            className="mt-4 flex w-full items-center gap-3 rounded-2xl bg-sun-soft p-4 text-left"
          >
            <motion.span
              animate={reduce ? undefined : { rotate: [0, -8, 8, -4, 0], scale: [1, 1.15, 1] }}
              transition={{ delay: 0.9, duration: 0.6 }}
              className="grid size-12 shrink-0 place-items-center rounded-full bg-sun text-white"
            >
              <Flame className="size-7 fill-current" strokeWidth={1.5} />
            </motion.span>
            <span>
              <span className="block text-lg font-black text-sun-deep">
                {sm.streak} jour{sm.streak > 1 ? "s" : ""} de suite
              </span>
              <span className="text-sm text-muted-foreground">Revenez demain pour prolonger la série.</span>
            </span>
          </motion.div>
        )}
      </main>
      <footer className="safe-b relative z-10 mx-auto w-full max-w-md px-5 pt-3 pb-6">
        <button type="button" autoFocus onClick={onClose} className="btn3d w-full">
          Continuer
        </button>
      </footer>
    </div>
  )
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between border-b-2 border-line px-4 py-3 last:border-0">
      <dt className="font-extrabold">{label}</dt>
      <dd className="text-lg font-black">{children}</dd>
    </div>
  )
}
