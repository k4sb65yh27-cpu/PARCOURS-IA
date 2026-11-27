import { useEffect, useState } from "react"
import { AnimatePresence, motion } from "motion/react"
import { BookA, Dumbbell, Flame, Map as MapIcon, Medal, Star, UserRound } from "lucide-react"
import { Toaster } from "@/components/ui/sonner"
import { toast } from "sonner"
import { PathView, type Go } from "@/components/PathView"
import { Session, exitGuard, type Mode } from "@/components/Session"
import { Onboarding } from "@/components/Onboarding"
import { NotionsReader, StepGuide } from "@/components/StepGuide"
import { BoardView, GlossView, ProfileView, ReviewView } from "@/components/Views"
import { useSync } from "@/lib/sync"
import { VIS, type Step } from "@/lib/content"
import { NAME_NODE, currentNode, dailyIds, dailyXp, dueIds, examIds, lessonIds, streakNow, today, useStore, validated } from "@/lib/store"

type Tab = "path" | "review" | "gloss" | "board" | "profile"
type Overlay =
  | { t: "session"; mode: Mode; stepId?: string; ids: string[]; label: string; key: number }
  | { t: "guide"; step: Step; tab?: string }
  | { t: "notions"; step: Step }
  | null

const TABS: { id: Tab; label: string; Icon: typeof MapIcon }[] = [
  { id: "path", label: "Parcours", Icon: MapIcon },
  { id: "review", label: "Réviser", Icon: Dumbbell },
  { id: "gloss", label: "Glossaire", Icon: BookA },
  /* Onglet présent seulement si le serveur SATT a activé le classement (config.php). */
  { id: "board", label: "Classement", Icon: Medal },
  { id: "profile", label: "Profil", Icon: UserRound },
]

/* Largeur d'écran suivie en direct (mise en page bureau à partir de 1024 px). */
function useMedia(q: string) {
  const [m, setM] = useState(() => window.matchMedia(q).matches)
  useEffect(() => {
    const mq = window.matchMedia(q)
    const on = () => setM(mq.matches)
    mq.addEventListener("change", on)
    return () => mq.removeEventListener("change", on)
  }, [q])
  return m
}

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
  const root = useStore()
  const desk = useMedia("(min-width: 1024px)")

  /* Le bouton retour d'Android ferme l'écran ouvert au lieu de quitter l'application. */
  useEffect(() => {
    if (!ov) return
    history.pushState({ ov: true }, "")
    const on = () => {
      /* Séance commencée : le retour du téléphone demande confirmation au lieu de fermer. */
      if (exitGuard.ask?.()) {
        history.pushState({ ov: true }, "")
        return
      }
      setOv(null)
    }
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

  const pickTab = (t: Tab) => {
    setTab(t)
    window.scrollTo(0, 0)
  }

  /*
   * Mise en page par largeur (skill interface_web_formation) :
   * moins de 1024 px : barre d'état en haut, onglets en bas, une colonne ;
   * 1024 px et plus : navigation latérale, contenu élargi, plus d'onglets en bas ;
   * 1280 px et plus : colonne d'accompagnement à droite (objectif, étape en cours, progression).
   */
  return (
    <div className="min-h-dvh lg:grid lg:grid-cols-[232px_minmax(0,1fr)] xl:grid-cols-[232px_minmax(0,1fr)_336px]">
      <SideNav tab={tab} setTab={pickTab} />
      <div className="flex min-h-dvh min-w-0 flex-col">
        <TopBar onTab={setTab} />
        <main id="main" className="flex-1 pb-24 lg:pb-12">
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
              {tab === "gloss" && <GlossView onOpen={(step) => setOv({ t: "guide", step })} />}
              {tab === "board" && <BoardView />}
              {tab === "profile" && <ProfileView />}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
      <RightRail
        onGo={go}
        onReview={() => {
          const d = dailyIds()
          start("review", d.ids, d.label)
        }}
        onTab={pickTab}
      />
      <BottomNav tab={tab} setTab={pickTab} />

      {ov?.t === "guide" && <StepGuide key={ov.step.id} step={ov.step} tab={ov.tab} onBack={close} />}
      {ov?.t === "notions" && <NotionsReader step={ov.step} onClose={close} />}
      {ov?.t === "session" && <Session key={ov.key} mode={ov.mode} stepId={ov.stepId} ids={ov.ids} label={ov.label} onClose={close} />}
      {!root.state.settings.profil && <Onboarding />}
      <Toaster position="bottom-center" offset={desk ? 24 : 96} mobileOffset={{ bottom: 96 }} duration={2200} toastOptions={{ className: "!rounded-2xl !border-2 !font-extrabold" }} />
    </div>
  )
}

/* Anneau de l'objectif du jour, commun à la barre d'état et à la colonne de droite. */
function GoalRing({ size = 36, stroke = 5 }: { size?: number; stroke?: number }) {
  const s = useStore().state
  const dx = dailyXp()
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  const frac = Math.min(1, dx / s.daily.goal)
  const h = size / 2
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true" className="shrink-0">
      <circle cx={h} cy={h} r={r} fill="none" stroke="var(--line)" strokeWidth={stroke} />
      <motion.circle
        cx={h}
        cy={h}
        r={r}
        fill="none"
        stroke={frac >= 1 ? "var(--sun)" : "var(--teal)"}
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={c}
        initial={false}
        animate={{ strokeDashoffset: c * (1 - frac) }}
        transition={{ type: "spring", bounce: 0, duration: 0.8 }}
        transform={`rotate(-90 ${h} ${h})`}
      />
    </svg>
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
  return (
    <header className="sticky top-0 z-20 border-b-2 border-line bg-background/95 backdrop-blur-sm safe-t xl:hidden">
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
          <GoalRing />
          <span className="text-sm tabular-nums">
            {dx}/{goal}
          </span>
        </button>
      </div>
    </header>
  )
}

/* Navigation latérale, à partir de 1024 px. Mêmes onglets que la barre du bas, qui disparaît alors. */
function SideNav({ tab, setTab }: { tab: Tab; setTab: (t: Tab) => void }) {
  useStore()
  const sync = useSync()
  const tabs = TABS.filter((x) => x.id !== "board" || sync.board)
  const due = dueIds().length
  return (
    <aside className="sticky top-0 hidden h-dvh flex-col border-r-2 border-line px-3 py-6 lg:flex">
      <p className="flex items-center gap-2.5 px-3 pb-6 text-xl font-black">
        <img src={`${import.meta.env.BASE_URL}mascot-ring.png`} alt="" className="size-9" />
        Parcours IA
      </p>
      <nav aria-label="Navigation principale">
        <ul className="grid gap-1.5">
          {tabs.map(({ id, label, Icon }) => {
            const on = tab === id
            return (
              <li key={id}>
                <button
                  type="button"
                  onClick={() => setTab(id)}
                  aria-current={on ? "page" : undefined}
                  className="flex min-h-12 w-full items-center gap-3 rounded-xl border-2 px-3 text-left font-extrabold transition-colors hover:bg-secondary"
                  style={{ borderColor: on ? "var(--teal)" : "transparent", background: on ? "var(--teal-soft)" : undefined, color: on ? "var(--teal)" : undefined }}
                >
                  <Icon className="size-6 shrink-0" strokeWidth={on ? 2.6 : 2.2} />
                  <span className="flex-1">{label}</span>
                  {id === "review" && due > 0 && (
                    <span className="grid min-w-6 place-items-center rounded-full bg-ko px-1.5 text-xs font-black text-white" aria-label={`${due} à revoir`}>
                      {due > 99 ? "99+" : due}
                    </span>
                  )}
                </button>
              </li>
            )
          })}
        </ul>
      </nav>
    </aside>
  )
}

/* Colonne d'accompagnement, à partir de 1280 px : ce qu'on consulte souvent sans changer d'écran. */
function RightRail({ onGo, onReview, onTab }: { onGo: Go; onReview: () => void; onTab: (t: Tab) => void }) {
  const root = useStore()
  const s = root.state
  const streak = streakNow()
  const dx = dailyXp()
  const due = dueIds().length
  const cur = currentNode()
  const done = VIS.filter(validated).length
  return (
    <aside aria-label="Votre progression" className="sticky top-0 hidden h-dvh flex-col gap-5 overflow-y-auto border-l-2 border-line px-6 py-6 xl:flex">
      <section className="rounded-2xl border-2 border-b-[5px] border-line p-4">
        <h2 className="font-black">Aujourd'hui</h2>
        <div className="mt-3 flex items-center gap-4">
          <GoalRing size={64} stroke={8} />
          <p>
            <span className="block text-2xl font-black tabular-nums">
              {dx} / {s.daily.goal} XP
            </span>
            <span className="text-sm text-muted-foreground">{dx >= s.daily.goal ? "Objectif du jour atteint." : "Objectif du jour"}</span>
          </p>
        </div>
        <button type="button" className="btn3d mt-4 w-full" onClick={onReview}>
          {due ? `Réviser (${due})` : "Entraînement du jour"}
        </button>
      </section>

      {cur && (
        <section className="rounded-2xl border-2 border-b-[5px] border-line p-4">
          <h2 className="font-black">Étape en cours</h2>
          <p className="mt-1 text-sm font-bold text-muted-foreground">Étape {cur.step.cote}</p>
          <p className="font-extrabold">{cur.step.titre}</p>
          <button type="button" className="tile mt-3 justify-center" onClick={() => onGo({ kind: cur.kind, step: cur.step })}>
            {NAME_NODE[cur.kind]}
          </button>
        </section>
      )}

      <section className="rounded-2xl border-2 border-b-[5px] border-line p-4">
        <h2 className="font-black">Progression</h2>
        <dl className="mt-2 grid grid-cols-[1fr_auto] gap-x-3 gap-y-2 text-[0.95rem]">
          <dt className="flex items-center gap-2 font-extrabold">
            <Flame className="size-5 text-sun" fill={s.streak.lastDay === today() ? "currentColor" : "none"} strokeWidth={2} /> Série
          </dt>
          <dd className="text-right font-black tabular-nums">{streak} j</dd>
          <dt className="flex items-center gap-2 font-extrabold">
            <Star className="size-5 text-teal" fill="currentColor" strokeWidth={0} /> XP au total
          </dt>
          <dd className="text-right font-black tabular-nums">{s.xp}</dd>
          <dt className="font-extrabold">Étapes validées</dt>
          <dd className="text-right font-black tabular-nums">
            {done} / {VIS.length}
          </dd>
        </dl>
        <button type="button" className="mt-3 min-h-11 text-sm font-extrabold text-teal" onClick={() => onTab("profile")}>
          Voir le profil complet
        </button>
      </section>
    </aside>
  )
}

function BottomNav({ tab, setTab }: { tab: Tab; setTab: (t: Tab) => void }) {
  useStore()
  const sync = useSync()
  const tabs = TABS.filter((x) => x.id !== "board" || sync.board)
  const due = dueIds().length
  return (
    <nav aria-label="Navigation principale" className="fixed inset-x-0 bottom-0 z-20 border-t-2 border-line bg-background safe-b lg:hidden">
      <ul className={`mx-auto grid max-w-xl ${tabs.length > 4 ? "grid-cols-5" : "grid-cols-4"}`}>
        {tabs.map(({ id, label, Icon }) => {
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
