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
    sub = "La leçon n'est pas comptée. Les XP gagnés restent acquis."
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
          initial={reduce ? false : { scale: 0.4, rotate: -12, opacity: 0 }}
          animate={{ scale: 1, rotate: 0, opacity: 1 }}
          transition={{ type: "spring", bounce: 0.45, duration: 0.7 }}
        >
          <Medal tone={tone} validated={!!sm.validated} />
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
            <span className="text-teal">{sm.mode === "exam" ? pct(sm.good, sm.total) : precision} %</span>
          </Row>
          <Row label="Temps">
            <span className="text-teal tabular-nums">
              {Math.floor(sec / 60)} min {String(sec % 60).padStart(2, "0")} s
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

function Medal({ tone, validated }: { tone: "sun" | "ko"; validated: boolean }) {
  const c = tone === "ko" ? ["var(--ko)", "var(--ko-soft)", "var(--ko-deep)"] : ["var(--sun)", "var(--sun-soft)", "var(--sun-deep)"]
  return (
    <svg width="132" height="132" viewBox="0 0 132 132" aria-hidden="true">
      {validated && (
        <>
          <path d="M44 92 30 128l18-8 10 14 8-36z" fill="var(--teal)" />
          <path d="M88 92l14 36-18-8-10 14-8-36z" fill="var(--teal-deep)" />
        </>
      )}
      <circle cx="66" cy="62" r="56" fill={c[0]} />
      <circle cx="66" cy="62" r="56" fill="none" stroke={c[2]} strokeWidth="5" strokeDasharray="0 0" opacity=".35" />
      <circle cx="66" cy="62" r="41" fill={c[1]} />
      {tone === "ko" ? (
        <path d="M51 47l30 30M81 47 51 77" stroke={c[2]} strokeWidth="9" strokeLinecap="round" />
      ) : (
        <path d="M66 33l8.6 17.6 19.4 2.8-14 13.6 3.3 19.3L66 77.2l-17.3 9.1 3.3-19.3-14-13.6 19.4-2.8z" fill={c[2]} />
      )}
    </svg>
  )
}
