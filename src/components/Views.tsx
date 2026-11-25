import { useRef, useState } from "react"
import { motion, useReducedMotion } from "motion/react"
import { Download, Dumbbell, Flame, RotateCcw, Upload } from "lucide-react"
import { toast } from "sonner"
import { Switch } from "@/components/ui/switch"
import { BlurFade } from "@/components/ui/blur-fade"
import { GLOSS, ITEMS, STEPS, BYID } from "@/lib/content"
import {
  GOALS,
  INTERVALS,
  RANKS,
  XP,
  addDays,
  dailyIds,
  dailyXp,
  dueIds,
  exportJson,
  importJson,
  rankIndex,
  resetAll,
  setFree,
  setGoal,
  setSetting,
  streakNow,
  today,
  useStore,
  validated,
} from "@/lib/store"
import { sfx } from "@/lib/sound"

const pct = (a: number, b: number) => (b ? Math.round((100 * a) / b) : 0)

function H1({ children, sub }: { children: React.ReactNode; sub?: React.ReactNode }) {
  return (
    <div className="mb-5">
      <h1 className="text-[1.75rem] leading-tight font-black">{children}</h1>
      {sub && <p className="mt-1 text-muted-foreground">{sub}</p>}
    </div>
  )
}
function Panel({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`rounded-2xl border-2 border-line p-4 ${className}`}>{children}</section>
}

/* ---------- Réviser ---------- */
export function ReviewView({ onStart }: { onStart: (ids: string[], label: string) => void }) {
  const root = useStore()
  const due = dueIds()
  const seen = Object.keys(root.state.srs).filter((k) => ITEMS[k])
  const boxes = [0, 0, 0, 0, 0]
  seen.forEach((k) => boxes[root.state.srs[k].box - 1]++)
  const mx = Math.max(1, ...boxes)
  const d = dailyIds()
  return (
    <div className="mx-auto w-full max-w-xl px-4 pt-5 pb-10">
      <H1 sub="Chaque question revient après 1, 2, 4, 8 puis 16 jours. Une erreur la renvoie au début.">Réviser</H1>
      <Panel className="bg-teal-soft/50">
        <div className="flex items-center gap-4">
          <span className="grid size-14 shrink-0 place-items-center rounded-2xl bg-teal text-white" style={{ borderBottom: "4px solid var(--teal-deep)" }}>
            <Dumbbell className="size-7" />
          </span>
          <div>
            <p className="text-xl font-black">{due.length ? `${due.length} question${due.length > 1 ? "s" : ""} à revoir` : "Rien d'échu aujourd'hui"}</p>
            <p className="text-sm text-muted-foreground">{d.label} : {d.ids.length} questions, +{XP.review} XP par bonne réponse.</p>
          </div>
        </div>
        <button type="button" className="btn3d mt-4 w-full" onClick={() => onStart(d.ids, d.label)}>
          {d.label}
        </button>
      </Panel>

      <Panel className="mt-4">
        <h2 className="mb-3 font-black">Boîtes de révision</h2>
        <ul className="grid gap-2.5">
          {boxes.map((n, i) => (
            <li key={i} className="grid grid-cols-[6.5rem_1fr_2rem] items-center gap-3 text-sm">
              <span className="font-extrabold">
                Boîte {i + 1} <span className="font-semibold text-muted-foreground">· {INTERVALS[i]} j</span>
              </span>
              <span className="h-3 overflow-hidden rounded-full bg-line">
                <span className="block h-full rounded-full" style={{ width: `${pct(n, mx)}%`, background: i === 4 ? "var(--sun)" : "var(--teal)" }} />
              </span>
              <span className="text-right font-black tabular-nums">{n}</span>
            </li>
          ))}
        </ul>
        <p className="mt-3 text-sm text-muted-foreground">
          {seen.length} questions vues sur {Object.keys(ITEMS).length}.
        </p>
      </Panel>
    </div>
  )
}

/* ---------- Glossaire ---------- */
export function GlossView() {
  const reduce = useReducedMotion()
  const [flip, setFlip] = useState<Record<number, boolean>>({})
  return (
    <div className="mx-auto w-full max-w-xl px-4 pt-5 pb-10">
      <H1 sub={`${GLOSS.length} cartes. Touchez une carte pour la retourner.`}>Glossaire</H1>
      <div className="grid grid-cols-2 gap-3">
        {GLOSS.map(([t, d], i) => (
          <BlurFade key={t} delay={Math.min(i, 10) * 0.03} inView>
            <button
              type="button"
              aria-pressed={!!flip[i]}
              onClick={() => {
                sfx.tap()
                setFlip((f) => ({ ...f, [i]: !f[i] }))
              }}
              className="relative block h-36 w-full [perspective:800px]"
            >
              <motion.span
                className="absolute inset-0 block [transform-style:preserve-3d]"
                animate={{ rotateY: flip[i] ? 180 : 0 }}
                transition={reduce ? { duration: 0 } : { type: "spring", bounce: 0, duration: 0.45 }}
              >
                <span
                  className="absolute inset-0 flex flex-col items-center justify-center rounded-2xl border-2 border-b-[5px] border-line bg-card p-3 text-center [backface-visibility:hidden]"
                  aria-hidden={!!flip[i]}
                >
                  <span className="text-lg font-black">{t}</span>
                  <span className="mt-1 text-xs font-bold text-muted-foreground">Voir la définition</span>
                </span>
                <span
                  className="absolute inset-0 flex items-center justify-center rounded-2xl p-3 text-center text-sm leading-snug font-bold text-white [backface-visibility:hidden] [transform:rotateY(180deg)]"
                  style={{ background: "var(--u2)", borderBottom: "5px solid var(--u2-d)" }}
                  aria-hidden={!flip[i]}
                >
                  {d}
                </span>
              </motion.span>
            </button>
          </BlurFade>
        ))}
      </div>
    </div>
  )
}

/* ---------- Profil ---------- */
export function ProfileView() {
  const root = useStore()
  const s = root.state
  const r = rankIndex()
  const next = RANKS[r + 1]
  const fileRef = useRef<HTMLInputElement>(null)
  const [confirmReset, setConfirmReset] = useState(false)

  /* Réponses par jour sur 14 jours */
  const t = today()
  const days = Array.from({ length: 14 }, (_, k) => {
    const d = addDays(t, k - 13)
    return { d, n: root.answers[d]?.items.length || 0 }
  })
  const mx = Math.max(5, ...days.map((x) => x.n))
  const per: Record<string, [number, number]> = {}
  for (const k of Object.keys(s.srs)) {
    const it = ITEMS[k]
    if (!it) continue
    const p = (per[it.step] ||= [0, 0])
    p[0] += s.srs[k].ok
    p[1] += s.srs[k].ok + s.srs[k].ko
  }
  const miss = Object.keys(s.srs)
    .filter((k) => ITEMS[k] && s.srs[k].ko > 0)
    .sort((a, b) => s.srs[b].ko - s.srs[a].ko)
    .slice(0, 5)
  const validatedN = STEPS.filter(validated).length

  const download = () => {
    const blob = new Blob([exportJson()], { type: "application/json" })
    const a = document.createElement("a")
    a.href = URL.createObjectURL(blob)
    a.download = `parcours-ia-sauvegarde-${t}.json`
    a.click()
    setTimeout(() => URL.revokeObjectURL(a.href), 2000)
    toast("Sauvegarde téléchargée.")
  }

  return (
    <div className="mx-auto w-full max-w-xl px-4 pt-5 pb-10">
      <H1 sub={next ? `${next[0] - s.xp} XP avant « ${next[1]} »` : "Grade le plus élevé atteint."}>{RANKS[r][1]}</H1>

      <Panel>
        <div className="flex items-center justify-between font-extrabold">
          <span>{s.xp} XP</span>
          <span className="text-muted-foreground">{next ? `${next[0]} XP` : ""}</span>
        </div>
        <div className="mt-2 h-4 overflow-hidden rounded-full bg-line">
          <div className="h-full rounded-full bg-sun" style={{ width: `${next ? pct(s.xp - RANKS[r][0], next[0] - RANKS[r][0]) : 100}%` }} />
        </div>
        <ul className="mt-4 grid gap-2 text-[0.95rem]">
          <li className="flex items-center justify-between">
            <span className="flex items-center gap-2 font-extrabold">
              <Flame className="size-5 text-sun" fill="currentColor" strokeWidth={1.5} /> Série en cours
            </span>
            <span className="font-black">{streakNow()} j</span>
          </li>
          <li className="flex items-center justify-between">
            <span className="font-extrabold">Étapes validées</span>
            <span className="font-black">
              {validatedN} / {STEPS.length}
            </span>
          </li>
          <li className="flex items-center justify-between">
            <span className="font-extrabold">XP aujourd'hui</span>
            <span className="font-black">
              {dailyXp()} / {s.daily.goal}
            </span>
          </li>
        </ul>
      </Panel>

      <Panel className="mt-4">
        <h2 className="font-black">Réponses par jour</h2>
        <p className="text-sm text-muted-foreground">14 derniers jours</p>
        {days.filter((x) => x.n).length < 3 ? (
          <p className="mt-3 rounded-xl bg-secondary p-3 text-sm">
            Le graphique apparaît après trois jours de pratique. {days.filter((x) => x.n).length ? "Bon début : revenez demain." : "Commencez par une leçon de l'étape 00."}
          </p>
        ) : (
        <>
        <div className="mt-3 flex h-28 items-end gap-1.5" role="img" aria-label={`Réponses par jour, maximum ${Math.max(...days.map((x) => x.n))}`}>
          {days.map((x) => (
            <div key={x.d} className="flex h-full flex-1 flex-col justify-end" title={`${x.d.slice(8)}/${x.d.slice(5, 7)} : ${x.n}`}>
              <div className="rounded-t-md" style={{ height: `${x.n ? Math.max(6, pct(x.n, mx)) : 3}%`, background: x.n ? (x.d === t ? "var(--sun)" : "var(--teal)") : "var(--line)" }} />
            </div>
          ))}
        </div>
        <div className="mt-1 flex justify-between text-xs font-bold text-muted-foreground">
          <span>{days[0].d.slice(8)}/{days[0].d.slice(5, 7)}</span>
          <span>aujourd'hui</span>
        </div>
        </>
        )}
      </Panel>

      <Panel className="mt-4">
        <h2 className="mb-3 font-black">Précision par étape</h2>
        <ul className="grid gap-2">
          {STEPS.map((st) => {
            const p = per[st.id]
            const v = p ? pct(p[0], p[1]) : 0
            return (
              <li key={st.id} className="grid grid-cols-[2rem_1fr_3rem] items-center gap-2 text-sm">
                <span className="font-black text-muted-foreground">{st.cote}</span>
                <span className="h-3 overflow-hidden rounded-full bg-line" title={st.titre}>
                  <span className="block h-full rounded-full" style={{ width: `${v}%`, background: v >= 80 ? "var(--teal)" : "var(--sun)" }} />
                </span>
                <span className={`text-right tabular-nums ${p ? "font-black" : "text-xs font-bold text-muted-foreground"}`}>{p ? `${v} %` : "à venir"}</span>
              </li>
            )
          })}
        </ul>
        {miss.length > 0 && (
          <>
            <h3 className="mt-5 mb-2 font-black">Questions les plus ratées</h3>
            <ul className="grid gap-2 text-sm">
              {miss.map((k) => (
                <li key={k} className="flex justify-between gap-3">
                  <span>
                    <span className="font-black text-muted-foreground">{BYID[ITEMS[k].step]?.cote ?? "C"}</span> {ITEMS[k].q}
                  </span>
                  <span className="shrink-0 font-black text-ko">{s.srs[k].ko}×</span>
                </li>
              ))}
            </ul>
          </>
        )}
      </Panel>

      <Panel className="mt-4">
        <h2 className="mb-3 font-black">Réglages</h2>
        <p className="mb-2 text-sm font-extrabold">Objectif quotidien</p>
        <div className="grid grid-cols-4 gap-2" role="radiogroup" aria-label="Objectif quotidien en XP">
          {GOALS.map((g) => (
            <button
              key={g}
              type="button"
              role="radio"
              aria-checked={s.daily.goal === g}
              onClick={() => {
                sfx.tap()
                setGoal(g)
              }}
              className="tile justify-center"
              data-state={s.daily.goal === g ? "sel" : undefined}
            >
              {g} XP
            </button>
          ))}
        </div>
        <div className="mt-4 grid gap-1">
          <Toggle label="Sons" hint="Bonne réponse, erreur, fin de leçon" on={s.settings.sound} set={(v) => setSetting("sound", v)} />
          <Toggle label="Vibrations" hint="Android uniquement" on={s.settings.haptics} set={(v) => setSetting("haptics", v)} />
          <Toggle label="Mode libre" hint="Ouvre toutes les étapes sans validation" on={s.free} set={setFree} />
        </div>
      </Panel>

      <Panel className="mt-4">
        <h2 className="font-black">Sauvegarde</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          La progression reste dans ce navigateur. Exportez-la pour changer d'appareil ; le fichier de la version claude.ai est accepté.
        </p>
        <div className="mt-3 grid grid-cols-2 gap-2">
          <button type="button" onClick={download} className="tile justify-center">
            <Download className="size-5" /> Exporter
          </button>
          <button type="button" onClick={() => fileRef.current?.click()} className="tile justify-center">
            <Upload className="size-5" /> Importer
          </button>
        </div>
        <input
          ref={fileRef}
          type="file"
          accept="application/json,.json,.txt"
          className="hidden"
          onChange={async (e) => {
            const f = e.target.files?.[0]
            if (!f) return
            const err = importJson(await f.text())
            e.target.value = ""
            err ? toast.error(err) : toast.success("Sauvegarde restaurée.")
          }}
        />
        <button
          type="button"
          onClick={() => {
            if (!confirmReset) return setConfirmReset(true)
            resetAll()
            setConfirmReset(false)
            toast("Progression effacée sur cet appareil.")
          }}
          className="mt-3 flex min-h-11 items-center gap-2 text-sm font-extrabold text-ko"
        >
          <RotateCcw className="size-4" /> {confirmReset ? "Toucher de nouveau pour tout effacer" : "Repartir de zéro"}
        </button>
      </Panel>

      <p className="mt-6 text-center text-xs text-muted-foreground">
        Exercices sur documents fictifs ou publics uniquement. Le tuteur IA et le coach hebdomadaire restent dans la version claude.ai.
      </p>
    </div>
  )
}

function Toggle({ label, hint, on, set }: { label: string; hint: string; on: boolean; set: (v: boolean) => void }) {
  const id = `t-${label}`
  return (
    <label htmlFor={id} className="flex min-h-12 items-center justify-between gap-3">
      <span>
        <span className="block font-extrabold">{label}</span>
        <span className="block text-sm text-muted-foreground">{hint}</span>
      </span>
      <Switch id={id} checked={on} onCheckedChange={set} />
    </label>
  )
}
