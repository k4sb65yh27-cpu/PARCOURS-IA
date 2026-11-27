import { Fragment, useEffect, useRef, useState } from "react"
import { Check, Copy, Download, Dumbbell, ExternalLink, Flame, Newspaper, RotateCcw, Upload } from "lucide-react"
import { toast } from "sonner"
import { Switch } from "@/components/ui/switch"
import { BYID, CADRES, COMPS, DEFIS, GLOSS, GLOSS_THEMES, ITEMS, LEVELS, NEWS, PROFIL, PROFILS, STEPS, VIS, profilOf, type Step } from "@/lib/content"
import { OUTILS, ProfilPicker } from "@/components/Onboarding"
import { copyText } from "@/lib/tutor"
import { fetchBoard, login, logout, setOptin, syncNow, useSync, type Board } from "@/lib/sync"
import { CadreNote } from "@/components/CadreNote"
import {
  GOALS,
  INTERVALS,
  RANKS,
  XP,
  addDays,
  compLevel,
  dailyIds,
  defiDuJour,
  doneDefi,
  dailyXp,
  dueIds,
  exportJson,
  importJson,
  rankIndex,
  resetAll,
  setFree,
  setGoal,
  setProfil,
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

      <DefiPanel />
      <NewsPanel onStart={onStart} />

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


function DefiCard({ id }: { id: string }) {
  const root = useStore()
  const df = DEFIS.find((x) => x.id === id)!
  const done = root.state.defis[id]
  const comp = COMPS.find((c) => c.id === df.comp)?.nom
  return (
    <div>
      <p className="flex flex-wrap items-center gap-2 text-xs font-black tracking-widest text-muted-foreground uppercase">
        {comp} <CadreNote cadre={df.cadre} compact />
      </p>
      <h3 className="mt-0.5 text-lg font-black">{df.titre}</h3>
      <p className="mt-2 rounded-xl bg-secondary p-3 font-serif text-[0.95rem] leading-relaxed">{df.consigne}</p>
      <p className="mt-2 text-sm"><span className="font-extrabold">Réussi si :</span> {df.critere}</p>
      <div className="mt-3 grid grid-cols-2 gap-2">
        <button type="button" className="tile justify-center" onClick={() => { sfx.tap(); copyText(df.consigne, "Consigne copiée : collez-la dans votre assistant.") }}>
          <Copy className="size-5" /> Copier
        </button>
        <button
          type="button"
          className="tile justify-center"
          data-state={done ? "good" : undefined}
          disabled={!!done}
          onClick={() => {
            if (doneDefi(id)) {
              sfx.ok()
              toast(`+${XP.defi} XP · défi relevé`)
            }
          }}
        >
          <Check className="size-5" /> {done ? "Relevé" : "Fait"}
        </button>
      </div>
    </div>
  )
}

function DefiPanel() {
  const root = useStore()
  const today_ = defiDuJour()
  const n = Object.keys(root.state.defis).length
  return (
    <Panel className="mt-4">
      <div className="mb-3 flex items-baseline justify-between gap-3">
        <h2 className="font-black">Défi du jour</h2>
        <span className="text-sm font-bold text-muted-foreground">{n} / {DEFIS.length} relevés</span>
      </div>
      {today_ && <DefiCard id={today_.id} />}
      <details className="mt-4 group">
        <summary className="flex min-h-11 cursor-pointer items-center font-extrabold text-teal">Tous les défis, par compétence</summary>
        <div className="mt-2 grid gap-5">
          {COMPS.map((c) => {
            const list = DEFIS.filter((x) => x.comp === c.id)
            if (!list.length) return null
            return (
              <div key={c.id}>
                <h3 className="mb-2 text-sm font-black tracking-widest text-muted-foreground uppercase">{c.nom}</h3>
                <div className="grid gap-4">
                  {list.map((x) => (
                    <div key={x.id} className="rounded-2xl border-2 border-line p-3">
                      <DefiCard id={x.id} />
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      </details>
    </Panel>
  )
}

function NewsPanel({ onStart }: { onStart: (ids: string[], label: string) => void }) {
  const [w, ...older] = NEWS
  if (!w) return null
  const ids = (x: typeof w) => x.drills.map((_, i) => `n:${x.week}:${i}`)
  const date = (x: typeof w) => `${x.date.slice(8)}/${x.date.slice(5, 7)}/${x.date.slice(0, 4)}`
  return (
    <Panel className="mt-4">
      <p className="flex items-center gap-2 text-xs font-black tracking-widest text-muted-foreground uppercase">
        <Newspaper className="size-4" aria-hidden="true" /> Cette semaine · {date(w)}
      </p>
      <h2 className="mt-1 text-lg font-black">{w.titre}</h2>
      <ul className="mt-3 grid gap-3">
        {w.items.map((it) => (
          <li key={it.titre}>
            <p className="font-extrabold">{it.titre}</p>
            <p className="mt-0.5 text-[0.95rem]">{it.texte}</p>
            <p className="mt-1 flex flex-wrap items-center gap-2 text-xs font-bold text-muted-foreground">
              <span className="rounded-md bg-secondary px-1.5 py-0.5">{it.statut}</span>
              {it.u && (
                <a href={it.u} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-teal underline-offset-4 hover:underline">
                  Source <ExternalLink className="size-3.5" aria-hidden="true" />
                </a>
              )}
            </p>
          </li>
        ))}
      </ul>
      {w.drills.length > 0 && (
        <button type="button" className="btn3d mt-4 w-full" onClick={() => onStart(ids(w), "Actualité de la semaine")}>
          {w.drills.length} questions sur l'actualité
        </button>
      )}
      {older.length > 0 && (
        <details className="mt-3">
          <summary className="flex min-h-11 cursor-pointer items-center font-extrabold text-teal">Semaines précédentes ({older.length})</summary>
          <ul className="grid gap-2">
            {older.map((x) => (
              <li key={x.week}>
                <button type="button" className="tile" onClick={() => onStart(ids(x), x.titre)}>
                  <span className="text-sm font-black text-muted-foreground">{date(x)}</span> {x.titre}
                </button>
              </li>
            ))}
          </ul>
        </details>
      )}
    </Panel>
  )
}

/* ---------- Glossaire ---------- */
/** Étape à ouvrir depuis le glossaire : celle du profil si l'étape citée appartient à une autre voie Métier. */
function glossStep(id: string): Step | undefined {
  if (!id) return undefined
  return VIS.find((s) => s.id === id) || VIS.find((s) => s.cote === BYID[id]?.cote)
}
export function GlossView({ onOpen }: { onOpen?: (s: Step) => void }) {
  const [q, setQ] = useState("")
  const [th, setTh] = useState("")
  const [open, setOpen] = useState<Record<string, boolean>>({})
  const norm = (x: string) => x.toLowerCase().normalize("NFD").replace(/\p{M}/gu, "")
  const nq = norm(q.trim())
  const list = GLOSS.filter((g) => (!th || g.th === th) && (!nq || norm(`${g.t} ${g.d}`).includes(nq)))
  return (
    <div className="mx-auto w-full max-w-xl px-4 pt-5 pb-10">
      <H1 sub={`${GLOSS.length} termes. Touchez un terme pour lire sa définition et un exemple.`}>Glossaire</H1>
      <label className="grid gap-1 text-sm font-extrabold">
        Rechercher
        <input
          type="search"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="token, projet, skill…"
          className="min-h-12 rounded-xl border-2 border-line bg-card px-3 text-base font-semibold"
        />
      </label>
      <div className="-mx-4 mt-3 overflow-x-auto px-4 pb-1" role="group" aria-label="Filtrer par thème">
        <div className="flex w-max gap-2">
          {["", ...GLOSS_THEMES].map((x) => (
            <button
              key={x || "tous"}
              type="button"
              aria-pressed={th === x}
              onClick={() => {
                sfx.tap()
                setTh(x)
              }}
              className={`min-h-11 rounded-xl border-2 border-b-4 px-3 text-sm font-extrabold whitespace-nowrap ${th === x ? "border-teal bg-teal text-white" : "border-line bg-card"}`}
            >
              {x || "Tous"}
            </button>
          ))}
        </div>
      </div>
      <p className="mt-3 text-sm text-muted-foreground" aria-live="polite">
        {list.length === GLOSS.length ? "" : `${list.length} terme${list.length > 1 ? "s" : ""}`}
      </p>
      <ul className="mt-1 grid gap-2">
        {list.map((g) => {
          const o = !!open[g.t]
          const st = glossStep(g.step)
          return (
            <li key={g.t} className="rounded-2xl border-2 border-b-[5px] border-line bg-card">
              <button
                type="button"
                aria-expanded={o}
                onClick={() => {
                  sfx.tap()
                  setOpen((f) => ({ ...f, [g.t]: !f[g.t] }))
                }}
                className="flex min-h-14 w-full items-center justify-between gap-3 px-4 py-3 text-left"
              >
                <span>
                  <span className="block font-black">{g.t}</span>
                  <span className="block text-xs font-bold text-muted-foreground">{g.th}</span>
                </span>
                <span aria-hidden className={`text-xl font-black text-muted-foreground transition-transform ${o ? "rotate-45" : ""}`}>+</span>
              </button>
              {o && (
                <div className="border-t-2 border-line px-4 pt-3 pb-4">
                  <p className="leading-relaxed">{g.d}</p>
                  <p className="mt-2 text-sm leading-relaxed">
                    <span className="font-extrabold">Exemple : </span>
                    {g.ex}
                  </p>
                  {st && onOpen && (
                    <button type="button" className="mt-3 min-h-11 text-sm font-extrabold text-teal" onClick={() => onOpen(st)}>
                      Voir l'étape {st.cote} : {st.titre}
                    </button>
                  )}
                </div>
              )}
            </li>
          )
        })}
      </ul>
      {!list.length && <p className="mt-4 text-muted-foreground">Aucun terme ne correspond. Essayez un autre mot ou le filtre « Tous ».</p>}
    </div>
  )
}

/* ---------- Classement (version serveur, si le RSI l'a activé) ---------- */
const PERIODS: { id: Board["period"]; label: string }[] = [
  { id: "week", label: "Semaine" },
  { id: "month", label: "Mois" },
  { id: "all", label: "Depuis le début" },
]
export function BoardView() {
  const sy = useSync()
  const [p, setP] = useState<Board["period"]>("week")
  const [data, setData] = useState<{ board: Board | null; stale: boolean } | null>(null)
  const [name, setName] = useState(sy.display)
  const [err, setErr] = useState("")
  const [busy, setBusy] = useState(false)
  useEffect(() => {
    let live = true
    fetchBoard(p).then((r) => live && setData(r))
    return () => {
      live = false
    }
  }, [p, sy.optin])
  useEffect(() => setName(sy.display), [sy.display])
  const b = data?.board
  const nom = (id: string) => PROFILS.find((x) => x.id === id)?.court || id
  const save = async (optin: boolean) => {
    setErr("")
    setBusy(true)
    try {
      await setOptin(optin, name)
      toast.success(optin ? "Participation enregistrée." : "Vous ne participez plus au classement. Vos données de classement sont effacées.")
    } catch (x: any) {
      setErr(x.message || "Enregistrement impossible.")
    } finally {
      setBusy(false)
    }
  }
  return (
    <div className="mx-auto w-full max-w-xl px-4 pt-5 pb-10">
      <H1 sub="Les points d'XP des salariés qui ont choisi d'y figurer.">Classement</H1>
      <Panel className="mb-4">
        <h2 className="font-black">Ma participation</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Participation volontaire, sous le nom de votre choix. Vous pouvez vous retirer à tout moment : vos données de classement sont alors effacées.
        </p>
        <label className="mt-3 grid gap-1 text-sm font-extrabold">
          Nom affiché (prénom ou pseudonyme)
          <input
            value={name}
            maxLength={24}
            onChange={(e) => setName(e.target.value)}
            className="min-h-12 rounded-xl border-2 border-line bg-card px-3 text-base font-semibold"
          />
        </label>
        {err && <p className="mt-2 text-sm font-bold text-ko" role="alert">{err}</p>}
        <div className="mt-3 grid grid-cols-2 gap-2">
          <button type="button" className="btn3d w-full" disabled={busy || name.trim().length < 2} onClick={() => save(true)}>
            {sy.optin ? "Renommer" : "Participer"}
          </button>
          {sy.optin && (
            <button type="button" className="tile justify-center" disabled={busy} onClick={() => save(false)}>
              Me retirer
            </button>
          )}
        </div>
      </Panel>
      <div className="mb-4 grid grid-cols-3 gap-2" role="group" aria-label="Période">
        {PERIODS.map((x) => (
          <button
            key={x.id}
            type="button"
            aria-pressed={p === x.id}
            onClick={() => {
              sfx.tap()
              setP(x.id)
            }}
            className={`min-h-11 rounded-xl border-2 border-b-4 px-2 text-sm font-extrabold ${p === x.id ? "border-teal bg-teal text-white" : "border-line bg-card"}`}
          >
            {x.label}
          </button>
        ))}
      </div>
      {!data && <p className="text-muted-foreground">Chargement…</p>}
      {data && !b && <p className="text-muted-foreground">Classement indisponible hors connexion.</p>}
      {b && (
        <>
          {data?.stale && (
            <p className="mb-3 text-sm font-bold text-muted-foreground">
              Hors connexion : classement du {new Date(b.at * 1000).toLocaleString("fr-FR", { dateStyle: "short", timeStyle: "short" })}.
            </p>
          )}
          <Panel className="mb-4">
            <h2 className="font-black">Ensemble des participants</h2>
            <dl className="mt-2 grid grid-cols-[1fr_auto] gap-x-3 gap-y-1">
              <dt>XP gagnés</dt>
              <dd className="text-right font-black tabular-nums">{b.collectif.xp}</dd>
              <dt>Participants</dt>
              <dd className="text-right font-black tabular-nums">{b.participants}</dd>
              {b.collectif.objectif !== null && (
                <>
                  <dt>Objectif de la semaine</dt>
                  <dd className="text-right font-black tabular-nums">{b.collectif.objectif}</dd>
                </>
              )}
            </dl>
            {b.collectif.objectif !== null && (
              <div className="mt-3 h-3 overflow-hidden rounded-full bg-secondary" role="progressbar" aria-label="Objectif collectif" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.min(100, pct(b.collectif.xp, b.collectif.objectif))}>
                <div className="h-full rounded-full bg-sun" style={{ width: `${Math.min(100, pct(b.collectif.xp, b.collectif.objectif))}%` }} />
              </div>
            )}
          </Panel>
          {b.profils.length > 0 && (
            <Panel className="mb-4">
              <h2 className="font-black">Par métier</h2>
              <dl className="mt-2 grid grid-cols-[1fr_auto] gap-x-3 gap-y-1">
                {b.profils.map((x) => (
                  <Fragment key={x.profil}>
                    <dt>
                      {nom(x.profil)} <span className="text-sm text-muted-foreground">({x.n})</span>
                    </dt>
                    <dd className="text-right font-black tabular-nums">{x.xp} XP</dd>
                  </Fragment>
                ))}
              </dl>
            </Panel>
          )}
          <Panel className="mb-4">
            <h2 className="font-black">Les dix premiers</h2>
            {b.top.length ? (
              <ol className="mt-2 grid gap-1">
                {b.top.map((x) => (
                  <li key={x.display} className={`grid min-h-11 grid-cols-[2.5rem_1fr_auto] items-center gap-2 rounded-xl px-2 ${x.display === sy.display ? "bg-secondary font-extrabold" : ""}`}>
                    <span className="font-black tabular-nums text-muted-foreground">{x.rang}</span>
                    <span className="truncate">{x.display}</span>
                    <span className="font-black tabular-nums">{x.xp} XP</span>
                  </li>
                ))}
              </ol>
            ) : (
              <p className="mt-1 text-sm text-muted-foreground">Aucun participant pour l'instant.</p>
            )}
            {b.moi && !b.top.some((x) => x.display === sy.display) && (
              <p className="mt-3 border-t-2 border-line pt-3 text-sm">
                Votre position : <span className="font-black">{b.moi.rang}</span>, avec {b.moi.xp} XP.
              </p>
            )}
          </Panel>
        </>
      )}
      <p className="text-sm text-muted-foreground">Ce classement sert l'émulation. Il n'est utilisé pour aucune évaluation.</p>
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
  const validatedN = VIS.filter(validated).length

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

      <AccountPanel />

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
              {validatedN} / {VIS.length}
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
        <h2 className="font-black">Compétences</h2>
        <p className="text-sm text-muted-foreground">Niveaux : {LEVELS.slice(1).join(", ")}.</p>
        <ul className="mt-3 grid gap-3">
          {COMPS.filter((c) => compLevel(c.id) > 0).map((c) => {
            const lv = compLevel(c.id)
            return (
              <li key={c.id}>
                <div className="flex items-baseline justify-between gap-3">
                  <span className="font-extrabold">{c.nom}</span>
                  <span className={`text-sm font-black ${lv ? "" : "text-muted-foreground"}`}>{LEVELS[lv]}</span>
                </div>
                <div className="mt-1 grid grid-cols-4 gap-1" role="img" aria-label={`${c.nom} : niveau ${lv} sur 4`}>
                  {[1, 2, 3, 4].map((k) => (
                    <span key={k} className="h-2.5 rounded-full" style={{ background: k <= lv ? (lv === 4 ? "var(--sun)" : "var(--teal)") : "var(--line-deep)" }} />
                  ))}
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{c.desc}</p>
              </li>
            )
          })}
        </ul>
        {COMPS.some((c) => !compLevel(c.id)) && (
          <p className="mt-3 text-sm text-muted-foreground">
            Pas encore abordées : {COMPS.filter((c) => !compLevel(c.id)).map((c) => c.nom).join(", ")}.
          </p>
        )}
      </Panel>

      <Panel className="mt-4">
        <h2 className="font-black">Réponses par jour</h2>
        <p className="text-sm text-muted-foreground">14 derniers jours</p>
        {days.filter((x) => x.n).length < 3 ? (
          <p className="mt-3 rounded-xl bg-secondary p-3 text-sm">
            Le graphique apparaît après trois jours de pratique. {days.filter((x) => x.n).length ? "Bon début : revenez demain." : "Commencez par une leçon de l'étape S1."}
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
          {STEPS.filter((st) => per[st.id]).length === 0 && <li className="text-sm text-muted-foreground">Apparaît après vos premières réponses.</li>}
          {STEPS.filter((st) => per[st.id]).map((st) => {
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
        <h2 className="mb-1 font-black">Votre métier</h2>
        <p className="mb-3 text-sm text-muted-foreground">Il choisit la voie Métier et les exemples des exercices. Les étapes déjà validées restent acquises.</p>
        <ProfilPicker
          value={PROFIL}
          onPick={(id) => {
            if (id === PROFIL) return
            setProfil(id)
            toast(`Voie Métier : ${profilOf(id)?.court}.`)
          }}
        />
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
        <p className="mt-5 mb-1 text-sm font-extrabold">Pratique autorisée au poste</p>
        <p className="mb-2 text-sm text-muted-foreground">Selon la règle de votre entreprise. Au-delà, les étapes et défis sont signalés « projet perso ».</p>
        <div className="grid gap-2" role="radiogroup" aria-label="Pratique autorisée au poste">
          {[1, 2, 3].map((k) => (
            <button
              key={k}
              type="button"
              role="radio"
              aria-checked={s.settings.cadre === k}
              onClick={() => {
                sfx.tap()
                setSetting("cadre", k)
              }}
              className="tile items-start"
              data-state={s.settings.cadre === k ? "sel" : undefined}
            >
              <span>
                <span className="block">Jusqu'au cadre {k} · {CADRES[k].nom}</span>
                <span className="mt-0.5 block text-sm font-semibold opacity-75">{CADRES[k].desc}</span>
              </span>
            </button>
          ))}
        </div>
        <label htmlFor="outil" className="mt-5 mb-2 block text-sm font-extrabold">Assistant utilisé au quotidien</label>
        <select
          id="outil"
          value={s.settings.outil}
          onChange={(e) => setSetting("outil", e.target.value)}
          className="min-h-12 w-full rounded-xl border-2 border-line bg-card px-3 font-extrabold"
        >
          <option value="">Non précisé</option>
          {OUTILS.map((o) => (
            <option key={o}>{o}</option>
          ))}
        </select>
      </Panel>

      <Panel className="mt-4">
        <h2 className="font-black">Sauvegarde</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Sans compte, la progression reste dans ce navigateur. Exportez-la pour changer d'appareil ; le fichier de la version claude.ai est accepté.
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
        Exercices sur documents fictifs ou publics uniquement. Contenu mis à jour chaque semaine ; vos acquis sont conservés.
      </p>
    </div>
  )
}

function AccountPanel() {
  const sy = useSync()
  const [email, setEmail] = useState("")
  const [pw, setPw] = useState("")
  const [create, setCreate] = useState(false)
  const [err, setErr] = useState("")
  if (!sy.enabled) return null
  const time = sy.last ? new Date(sy.last).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" }) : ""
  return (
    <Panel className="mb-4">
      <h2 className="font-black">Compte</h2>
      {sy.email ? (
        <>
          <p className="mt-1 text-sm">
            Connecté : <span className="font-extrabold">{sy.email}</span>. La progression suit le compte sur le PC et le téléphone.
          </p>
          <p className="mt-1 text-sm text-muted-foreground" aria-live="polite">
            {sy.busy ? "Synchronisation…" : sy.error || (time ? `Synchronisé à ${time}.` : "")}
          </p>
          <div className="mt-3 grid grid-cols-2 gap-2">
            <button type="button" className="tile justify-center" disabled={sy.busy} onClick={() => syncNow()}>
              Synchroniser
            </button>
            {sy.mode === "local" && (
              <button type="button" className="tile justify-center" onClick={() => logout()}>
                Se déconnecter
              </button>
            )}
          </div>
        </>
      ) : (
        <form
          className="mt-2 grid gap-2"
          onSubmit={async (e) => {
            e.preventDefault()
            setErr("")
            try {
              await login(email, pw, create)
              setPw("")
              toast.success("Connecté. Progression synchronisée.")
            } catch (x: any) {
              setErr(x.message || "Connexion impossible.")
            }
          }}
        >
          <p className="text-sm text-muted-foreground">Connectez-vous pour retrouver votre progression sur tous vos appareils.</p>
          <label className="grid gap-1 text-sm font-extrabold">
            Courriel professionnel
            <input type="email" required autoComplete="username" value={email} onChange={(e) => setEmail(e.target.value)} className="min-h-12 rounded-xl border-2 border-line bg-card px-3 text-base font-semibold" />
          </label>
          <label className="grid gap-1 text-sm font-extrabold">
            Mot de passe{create ? " (10 caractères minimum)" : ""}
            <input type="password" required minLength={create ? 10 : 1} autoComplete={create ? "new-password" : "current-password"} value={pw} onChange={(e) => setPw(e.target.value)} className="min-h-12 rounded-xl border-2 border-line bg-card px-3 text-base font-semibold" />
          </label>
          {(err || sy.error) && <p className="text-sm font-bold text-ko" role="alert">{err || sy.error}</p>}
          <button type="submit" className="btn3d mt-1 w-full" disabled={sy.busy}>
            {create ? "Créer mon compte" : "Se connecter"}
          </button>
          <button type="button" className="min-h-11 text-sm font-extrabold text-teal" onClick={() => setCreate(!create)}>
            {create ? "J'ai déjà un compte" : "Première fois : créer un compte"}
          </button>
        </form>
      )}
    </Panel>
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
