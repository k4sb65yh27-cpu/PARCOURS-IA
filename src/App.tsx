import { useEffect, useState } from "react"
import { AnimatePresence, motion } from "motion/react"
import { BookA, Dumbbell, Flame, Map as MapIcon, Star, UserRound } from "lucide-react"
import { Toaster } from "@/components/ui/sonner"
import { toast } from "sonner"
import { PathView, type Go } from "@/components/PathView"
import { Session, type Mode } from "@/components/Session"
import { NotionsReader, StepGuide } from "@/components/StepGuide"
import { GlossView, ProfileView, ReviewView } from "@/components/Views"
import { type Step } from "@/lib/content"
import { dailyXp, dueIds, examIds, lessonIds, streakNow, today, useStore } from "@/lib/store"

type Tab = "path" | "review" | "gloss" | "profile"
type Overlay =
  | { t: "session"; mode: Mode; stepId?: string; ids: string[]; label: string; key: number }
  | { t: "guide"; step: Step; tab?: string }
  | { t: "notions"; step: Step }
  | null

const TABS: { id: Tab; label: string; Icon: typeof MapIcon }[] = [
  { id: "path", label: "Parcours", Icon: MapIcon },
  { id: "review", label: "Réviser", Icon: Dumbbell },
  { id: "gloss", label: "Glossaire", Icon: BookA },
  { id: "profile", label: "Profil", Icon: UserRound },
]

function useTheme() {
  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)")
    const apply = () => {
      document.documentElement.classList.toggle("dark", mq.matches)
      document.querySelector('meta[name="theme-color"]')?.setAttribute("content", mq.matches ? "#141a1f" : "#ffffff")
    }
    apply()
    mq.addEventListener("change", apply)
    return () => mq.removeEventListener("change", apply)
  }, [])
}

export default function App() {
  useTheme()
  const [tab, setTab] = useState<Tab>("path")
  const [ov, setOv] = useState<Overlay>(null)

  /* Le bouton retour d'Android ferme l'écran ouvert au lieu de quitter l'application. */
  useEffect(() => {
    if (!ov) return
    history.pushState({ ov: true }, "")
    const on = () => setOv(null)
    window.addEventListener("popstate", on)
    return () => window.removeEventListener("popstate", on)
  }, [ov?.t])
  const close = () => {
    if (history.state?.ov) history.back()
    else setOv(null)
  }

  const start = (mode: Mode, ids: string[], label: string, stepId?: string) => {
    if (!ids.length) return
    toast.dismiss() // un toast restant masquerait la correction en bas d'écran
    setOv({ t: "session", mode, ids, label, stepId, key: Date.now() })
  }

  const go: Go = ({ kind, step, tab: t }) => {
    if (kind === "guide") return setOv({ t: "guide", step, tab: t })
    if (kind === "notions") return setOv({ t: "notions", step })
    if (kind === "lecon") return start("lesson", lessonIds(step), "Leçon", step.id)
    if (kind === "exam") return start("exam", examIds(step), "Examen", step.id)
    if (kind === "ex") return setOv({ t: "guide", step, tab: "exercices" })
  }

  return (
    <div className="flex min-h-dvh flex-col">
      <TopBar onTab={setTab} />
      <main id="main" className="flex-1 pb-24">
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={tab}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.18 }}
          >
            {tab === "path" && <PathView onGo={go} />}
            {tab === "review" && <ReviewView onStart={(ids, label) => start("review", ids, label)} />}
            {tab === "gloss" && <GlossView />}
            {tab === "profile" && <ProfileView />}
          </motion.div>
        </AnimatePresence>
      </main>
      <BottomNav tab={tab} setTab={(t) => { setTab(t); window.scrollTo(0, 0) }} />

      {ov?.t === "guide" && <StepGuide key={ov.step.id} step={ov.step} tab={ov.tab} onBack={close} />}
      {ov?.t === "notions" && <NotionsReader step={ov.step} onClose={close} />}
      {ov?.t === "session" && <Session key={ov.key} mode={ov.mode} stepId={ov.stepId} ids={ov.ids} label={ov.label} onClose={close} />}
      <Toaster position="bottom-center" offset={96} mobileOffset={{ bottom: 96 }} duration={2200} toastOptions={{ className: "!rounded-2xl !border-2 !font-extrabold" }} />
    </div>
  )
}

function TopBar({ onTab }: { onTab: (t: Tab) => void }) {
  const root = useStore()
  const s = root.state
  const streak = streakNow()
  const activeToday = s.streak.lastDay === today()
  const dx = dailyXp()
  const goal = s.daily.goal
  const due = dueIds().length
  const r = 15
  const c = 2 * Math.PI * r
  const frac = Math.min(1, dx / goal)
  return (
    <header className="sticky top-0 z-20 border-b-2 border-line bg-background/95 backdrop-blur-sm safe-t">
      <div className="mx-auto flex h-[58px] w-full max-w-xl items-center justify-between px-4">
        <button
          type="button"
          onClick={() => onTab("profile")}
          className="flex min-h-11 items-center gap-1.5 text-lg font-black"
          aria-label={`Série : ${streak} jour${streak > 1 ? "s" : ""}${activeToday ? ", prolongée aujourd'hui" : ""}`}
          style={{ color: activeToday ? "var(--sun)" : "var(--muted-foreground)" }}
        >
          <Flame className="size-6" fill={activeToday ? "currentColor" : "none"} strokeWidth={2.2} />
          {streak}
        </button>
        <button type="button" onClick={() => onTab("profile")} className="flex min-h-11 items-center gap-1.5 text-lg font-black text-teal" aria-label={`${s.xp} XP au total`}>
          <Star className="size-6" fill="currentColor" strokeWidth={0} />
          {s.xp}
        </button>
        <button type="button" onClick={() => onTab("review")} className="relative flex min-h-11 items-center gap-1.5 text-lg font-black" aria-label={`Objectif du jour : ${dx} sur ${goal} XP${due ? `, ${due} questions à revoir` : ""}`}>
          <svg width="36" height="36" viewBox="0 0 36 36" aria-hidden="true">
            <circle cx="18" cy="18" r={r} fill="none" stroke="var(--line)" strokeWidth="5" />
            <motion.circle
              cx="18"
              cy="18"
              r={r}
              fill="none"
              stroke={frac >= 1 ? "var(--sun)" : "var(--teal)"}
              strokeWidth="5"
              strokeLinecap="round"
              strokeDasharray={c}
              initial={false}
              animate={{ strokeDashoffset: c * (1 - frac) }}
              transition={{ type: "spring", bounce: 0, duration: 0.8 }}
              transform="rotate(-90 18 18)"
            />
          </svg>
          <span className="text-sm tabular-nums">
            {dx}/{goal}
          </span>
        </button>
      </div>
    </header>
  )
}

function BottomNav({ tab, setTab }: { tab: Tab; setTab: (t: Tab) => void }) {
  useStore()
  const due = dueIds().length
  return (
    <nav aria-label="Navigation principale" className="fixed inset-x-0 bottom-0 z-20 border-t-2 border-line bg-background safe-b">
      <ul className="mx-auto grid max-w-xl grid-cols-4">
        {TABS.map(({ id, label, Icon }) => {
          const on = tab === id
          return (
            <li key={id}>
              <button
                type="button"
                onClick={() => setTab(id)}
                aria-current={on ? "page" : undefined}
                className="flex min-h-16 w-full flex-col items-center justify-center gap-0.5 text-xs font-extrabold"
                style={{ color: on ? "var(--teal)" : "var(--muted-foreground)" }}
              >
                <span
                  className="relative grid h-8 w-12 place-items-center rounded-xl border-2 transition-colors"
                  style={{ borderColor: on ? "var(--teal)" : "transparent", background: on ? "var(--teal-soft)" : "transparent" }}
                >
                  <Icon className="size-5" strokeWidth={on ? 2.6 : 2.2} />
                  {id === "review" && due > 0 && (
                    <span className="absolute -top-1.5 -right-1.5 grid min-w-5 place-items-center rounded-full bg-ko px-1 text-[0.65rem] font-black text-white" aria-label={`${due} à revoir`}>
                      {due > 9 ? "9+" : due}
                    </span>
                  )}
                </span>
                {label}
              </button>
            </li>
          )
        })}
      </ul>
    </nav>
  )
}
