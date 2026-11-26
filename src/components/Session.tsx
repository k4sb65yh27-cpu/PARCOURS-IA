import { Mascot, type Mood } from "@/components/Mascot"
import { Drawer, DrawerContent, DrawerDescription, DrawerTitle } from "@/components/ui/drawer"
import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { AnimatePresence, motion, useAnimationControls, useReducedMotion } from "motion/react"
import { Check, Heart, Volume2, VolumeX, X } from "lucide-react"
import { BYID, ITEMS, type Item } from "@/lib/content"
import {
  HEARTS,
  XP,
  award,
  finishExam,
  finishLesson,
  getRoot,
  record,
  setSetting,
  streakNow,
  shuffle,
  today,
  useStore,
} from "@/lib/store"
import { sfx } from "@/lib/sound"
import { SessionEnd, type Summary } from "./SessionEnd"

export type Mode = "lesson" | "exam" | "review"
type UI =
  | { t: "tf"; sel: boolean | null }
  | { t: "choice"; order: number[]; sel: number | null }
  | { t: "order"; pool: number[]; picked: number[] }
  | { t: "match"; right: number[]; pairs: Record<number, number>; selL: number | null }

const range = (n: number) => Array.from({ length: n }, (_, i) => i)
function prepare(it: Item): UI {
  if (it.type === "mcq" || it.type === "cloze") return { t: "choice", order: shuffle(range(it.o.length)), sel: null }
  if (it.type === "tf") return { t: "tf", sel: null }
  if (it.type === "order") {
    let p = shuffle(range(it.items.length))
    for (let n = 0; n < 8 && p.every((v, i) => v === i); n++) p = shuffle(p)
    return { t: "order", pool: p, picked: [] }
  }
  if (it.type === "match") return { t: "match", right: shuffle(range(it.pairs.length)), pairs: {}, selL: null }
  return { t: "tf", sel: null }
}
function ready(it: Item, u: UI) {
  if (u.t === "order" && it.type === "order") return u.picked.length === it.items.length
  if (u.t === "match" && it.type === "match") return Object.keys(u.pairs).length === it.pairs.length
  if (u.t === "tf" || u.t === "choice") return u.sel !== null
  return false
}
function isCorrect(it: Item, u: UI) {
  if (it.type === "order" && u.t === "order") return u.picked.every((v, i) => it.items[v] === it.items[i])
  if (it.type === "match" && u.t === "match") return it.pairs.every((p, l) => it.pairs[u.pairs[l]][1] === p[1])
  if (it.type === "tf" && u.t === "tf") return u.sel === it.a
  if ((it.type === "mcq" || it.type === "cloze") && u.t === "choice") return u.sel === it.a
  return false
}
function rightText(it: Item) {
  if (it.type === "tf") return it.a ? "Vrai" : "Faux"
  if (it.type === "order") return it.items.join(" → ")
  if (it.type === "match") return it.pairs.map((p) => `${p[0]} : ${p[1]}`).join(" ; ")
  return it.o[it.a]
}
const KIND: Record<Item["type"], string> = {
  tf: "Vrai ou faux ?",
  cloze: "Complétez la phrase",
  mcq: "Choisissez la bonne réponse",
  order: "Remettez dans l'ordre",
  match: "Associez les paires",
}
const PRAISE = ["Bien vu !", "Exact !", "Parfait !", "Très juste !", "C'est ça !"]
const AGAIN = ["On la reverra un peu plus tard.", "Pas grave, elle reviendra.", "Notez la réponse, elle reviendra."]
const LEAVE: Record<Mode, { titre: string; texte: string; rester: string }> = {
  lesson: { titre: "Quitter la leçon ?", texte: "La leçon ne sera pas comptée et reprendra depuis le début. Les XP déjà gagnés restent acquis.", rester: "Continuer la leçon" },
  exam: { titre: "Quitter l'examen ?", texte: "L'examen ne sera pas noté. Vous pourrez le repasser quand vous voulez.", rester: "Continuer l'examen" },
  review: { titre: "Quitter la révision ?", texte: "Les réponses déjà données restent enregistrées ; les autres questions attendront.", rester: "Continuer la révision" },
}

/**
 * Garde de sortie : la séance l'arme dès la première réponse. Le bouton retour du téléphone
 * (géré par App) l'interroge avant de fermer ; elle ouvre alors la confirmation.
 */
export const exitGuard: { ask: null | (() => boolean) } = { ask: null }

export function Session({
  mode,
  stepId,
  ids,
  label,
  onClose,
}: {
  mode: Mode
  stepId?: string
  ids: string[]
  label: string
  onClose: () => void
}) {
  const root = useStore()
  const reduce = useReducedMotion()
  const [queue, setQueue] = useState<string[]>(() => ids.slice(1))
  const [cur, setCur] = useState<Item>(() => ITEMS[ids[0]])
  const [ui, setUi] = useState<UI>(() => prepare(ITEMS[ids[0]]))
  const [checked, setChecked] = useState(false)
  const [ok, setOk] = useState(false)
  const [hearts, setHearts] = useState(HEARTS)
  const [done, setDone] = useState(0)
  const [combo, setCombo] = useState(0)
  const [comboFlash, setComboFlash] = useState<number | null>(null)
  const [summary, setSummary] = useState<Summary | null>(null)
  const [nonce, setNonce] = useState(0)
  const [confirm, setConfirm] = useState(false)
  const confirmRef = useRef(false)
  confirmRef.current = confirm
  const summaryRef = useRef<Summary | null>(null)
  summaryRef.current = summary
  const first = useRef<Record<string, boolean>>({})
  const tries = useRef<Record<string, number>>({})
  const xpGained = useRef(0)
  const lastDay0 = useRef(getRoot().state.streak.lastDay)
  const t0 = useRef(Date.now())
  const shake = useAnimationControls()
  const praise = useMemo(() => PRAISE[Math.floor(Math.random() * PRAISE.length)], [nonce])
  const total = ids.length
  const useHearts = mode === "lesson"
  const step = stepId ? BYID[stepId] : undefined

  const gain = (n: number) => {
    award(n)
    xpGained.current += n
  }

  const end = useCallback(
    (out = false) => {
      const keys = Object.keys(first.current)
      const good = keys.filter((k) => first.current[k]).length
      const sm: Summary = {
        mode,
        label,
        stepId,
        total: keys.length,
        good,
        ms: Date.now() - t0.current,
        xp: xpGained.current,
        out,
        streak: streakNow(),
        streakBumped: false,
      }
      if (!out && step) {
        if (mode === "lesson") finishLesson(step)
        if (mode === "exam") {
          const score = keys.length ? good / keys.length : 0
          const xpBefore = getRoot().state.xp
          const r = finishExam(step, score)
          sm.score = score
          sm.passedNow = r.passedNow
          sm.validated = r.validatedNow
          sm.xp += getRoot().state.xp - xpBefore
        }
      }
      sm.streak = streakNow()
      sm.streakBumped = lastDay0.current !== today() && getRoot().state.streak.lastDay === today()
      setSummary(sm)
    },
    [mode, label, stepId, step],
  )

  const check = useCallback(() => {
    if (checked || !ready(cur, ui)) return
    const good = isCorrect(cur, ui)
    const isFirst = !(cur.id in first.current)
    setChecked(true)
    setOk(good)
    if (isFirst) {
      first.current[cur.id] = good
      record(cur, good, mode)
      if (good && mode === "lesson") gain(XP.lesson)
      if (good && mode === "review") gain(XP.review)
    }
    tries.current[cur.id] = (tries.current[cur.id] || 0) + 1
    if (good) {
      const c = combo + 1
      setCombo(c)
      if (c >= 3 && c % 2 === 1) {
        setComboFlash(c)
        setTimeout(() => sfx.combo(), 160)
      } else setComboFlash(null)
      sfx.ok()
    } else {
      setCombo(0)
      setComboFlash(null)
      sfx.ko()
      if (useHearts) setHearts((h) => h - 1)
      if (!reduce) shake.start({ x: [0, -7, 7, -5, 5, 0], transition: { duration: 0.32 } })
    }
    if (!good && mode !== "exam" && tries.current[cur.id] < 3) setQueue((q) => [...q, cur.id])
    else setDone((d) => d + 1)
  }, [checked, cur, ui, mode, combo, useHearts, reduce, shake])

  const next = useCallback(() => {
    if (useHearts && hearts <= 0) {
      sfx.out()
      end(true)
      return
    }
    if (!queue.length) {
      sfx.done()
      end()
      return
    }
    const [id, ...rest] = queue
    setQueue(rest)
    const it = ITEMS[id]
    setCur(it)
    setUi(prepare(it))
    setChecked(false)
    setOk(false)
    setComboFlash(null)
    setNonce((n) => n + 1)
  }, [queue, hearts, useHearts, end])

  /* Sortie : pas de confirmation tant qu'aucune réponse n'a été donnée ni après la fin. */
  const dirty = () => !summaryRef.current && Object.keys(first.current).length > 0
  const requestClose = useCallback(() => {
    if (dirty()) {
      sfx.tap()
      setConfirm(true)
    } else onClose()
  }, [onClose])
  const leave = () => {
    exitGuard.ask = null
    setConfirm(false)
    onClose()
  }
  useEffect(() => {
    exitGuard.ask = () => {
      if (!dirty()) return false
      setConfirm(true)
      return true
    }
    return () => {
      exitGuard.ask = null
    }
  }, [])

  /* Clavier : 1 à 9 pour choisir, Entrée pour vérifier ou continuer, Échap pour quitter (avec confirmation). */
  useEffect(() => {
    const on = (e: KeyboardEvent) => {
      if (summary || confirmRef.current) return
      if (e.key === "Enter") {
        e.preventDefault()
        checked ? next() : check()
        return
      }
      if (e.key === "Escape") return requestClose()
      const n = parseInt(e.key, 10)
      if (!n || checked) return
      const btn = document.querySelector<HTMLButtonElement>(`[data-key="${n}"]`)
      btn?.click()
    }
    window.addEventListener("keydown", on)
    return () => window.removeEventListener("keydown", on)
  }, [checked, check, next, requestClose, summary])

  if (summary) return <SessionEnd sm={summary} onClose={onClose} />

  const progress = Math.round((100 * done) / total)
  const sound = root.state.settings.sound
  const canCheck = ready(cur, ui)
  const lastLife = useHearts && hearts === 1 && !checked
  const mood: Mood = checked ? (ok ? (combo >= 3 ? "cheer" : "happy") : "sad") : lastLife ? "worried" : "idle"
  const say = checked
    ? ok
      ? combo >= 3
        ? `${combo} de suite, continuez !`
        : praise
      : mode === "exam"
        ? "On passe à la suivante."
        : AGAIN[nonce % AGAIN.length]
    : [mode === "exam" ? "Examen." : "", /[?!.]$/.test(KIND[cur.type]) ? KIND[cur.type] : `${KIND[cur.type]}.`, tries.current[cur.id] ? "Nouvel essai." : "", lastLife ? "Dernière vie : prenez votre temps." : ""]
        .filter(Boolean)
        .join(" ")

  return (
    <div className="fixed inset-0 z-40 flex flex-col bg-background safe-t">
      <header className="mx-auto flex w-full max-w-2xl items-center gap-3 px-4 pt-4 pb-2">
        <button
          type="button"
          onClick={requestClose}
          aria-label="Quitter la séance"
          className="grid size-11 place-items-center rounded-full text-muted-foreground hover:bg-secondary"
        >
          <X className="size-6" strokeWidth={3} />
        </button>
        <div
          className="h-4 flex-1 overflow-hidden rounded-full bg-line"
          role="progressbar"
          aria-label="Avancement de la séance"
          aria-valuemin={0}
          aria-valuemax={total}
          aria-valuenow={done}
        >
          <motion.div
            className="h-full rounded-full bg-teal"
            initial={false}
            animate={{ width: `${Math.max(progress, 3)}%` }}
            transition={{ type: "spring", bounce: 0, duration: 0.45 }}
          >
            <div className="mx-2 mt-1 h-1 rounded-full bg-white/30" />
          </motion.div>
        </div>
        {useHearts ? (
          <motion.span
            key={hearts}
            initial={reduce ? false : { scale: 1.35 }}
            animate={{ scale: 1 }}
            className="flex min-w-11 items-center justify-end gap-1 text-lg font-black text-ko"
            aria-label={`${hearts} vies`}
          >
            <Heart className="size-6 fill-current" strokeWidth={0} />
            {hearts}
          </motion.span>
        ) : (
          <span className="min-w-11 text-right text-sm font-extrabold text-muted-foreground tabular-nums">
            {done}/{total}
          </span>
        )}
        <button
          type="button"
          onClick={() => setSetting("sound", !sound)}
          aria-label={sound ? "Couper les sons" : "Activer les sons"}
          aria-pressed={sound}
          className="grid size-11 place-items-center rounded-full text-muted-foreground hover:bg-secondary"
        >
          {sound ? <Volume2 className="size-5" /> : <VolumeX className="size-5" />}
        </button>
      </header>

      <main className="flex-1 overflow-y-auto">
        {/* La mascotte reste en place d'une question à l'autre et « dit » la consigne. */}
        <div className="mx-auto flex w-full max-w-2xl items-end gap-3 px-4 pt-3">
          <Mascot size={60} mood={mood} />
          <p className="bubble mb-2 flex-1 text-[0.95rem] font-extrabold leading-snug" aria-live="polite">
            {say}
          </p>
        </div>
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={nonce}
            initial={reduce ? { opacity: 0 } : { opacity: 0, x: 36 }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, x: -36 }}
            transition={{ type: "spring", bounce: 0, duration: 0.3 }}
            className="mx-auto w-full max-w-2xl px-4 pt-1 pb-6"
          >
            <Question it={cur} ui={ui} checked={checked} />
            <motion.div animate={shake}>
              <Answers it={cur} ui={ui} setUi={setUi} checked={checked} />
            </motion.div>
          </motion.div>
        </AnimatePresence>
      </main>


      <footer className="relative">
        <AnimatePresence initial={false} mode="popLayout">
          {checked ? (
            <motion.div
              key="fb"
              initial={reduce ? { opacity: 0 } : { y: "100%" }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ type: "spring", bounce: 0, duration: 0.3 }}
              className={`relative safe-b ${ok ? "bg-teal-soft" : "bg-ko-soft"}`}
              role="status"
              aria-live="polite"
            >
              <div className="mx-auto w-full max-w-2xl px-4 pt-4 pb-5">
                <div className={`flex items-center gap-2.5 text-xl font-black ${ok ? "text-teal-deep dark:text-[#8fe0d2]" : "text-ko-deep dark:text-[#f7b5a6]"}`}>
                  <span className={`grid size-8 place-items-center rounded-full text-white ${ok ? "bg-teal" : "bg-ko"}`}>
                    {ok ? <Check className="size-5" strokeWidth={3.5} /> : <X className="size-5" strokeWidth={3.5} />}
                  </span>
                  {ok ? praise : "Pas tout à fait"}
                  {ok && comboFlash && (
                    <motion.span
                      initial={reduce ? false : { scale: 0.6, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ type: "spring", bounce: 0.4, duration: 0.45, delay: 0.1 }}
                      className="ml-auto rounded-full bg-sun px-3 py-1 text-xs font-black tracking-wide text-[#3a2600] uppercase"
                    >
                      {comboFlash} d'affilée
                    </motion.span>
                  )}
                </div>
                <div className={`mt-2 text-[0.95rem] leading-snug ${ok ? "text-teal-deep dark:text-[#bfece4]" : "text-ko-deep dark:text-[#f9c8bd]"}`}>
                  {!ok && (
                    <p className="font-extrabold">
                      Réponse attendue : <span className="font-bold">{rightText(cur)}</span>
                    </p>
                  )}
                  {cur.e && <p className="mt-1 font-semibold">{cur.e}</p>}
                </div>
                <button
                  type="button"
                  autoFocus
                  onClick={next}
                  className="btn3d mt-4 w-full"
                  style={ok ? undefined : ({ "--c": "var(--ko)", "--cd": "var(--ko-deep)" } as React.CSSProperties)}
                >
                  Continuer
                </button>
              </div>
            </motion.div>
          ) : (
            <motion.div key="ck" className="safe-b border-t-2 border-line">
              <div className="mx-auto w-full max-w-2xl px-4 pt-4 pb-5">
                <button type="button" onClick={check} disabled={!canCheck} className="btn3d w-full">
                  Vérifier
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </footer>

      <Drawer open={confirm} onOpenChange={(o) => !o && setConfirm(false)}>
        <DrawerContent className="safe-b">
          <div className="mx-auto w-full max-w-md px-5 pt-2 pb-5 text-center">
            <div className="flex justify-center">
              <Mascot size={72} mood="sad" />
            </div>
            <DrawerTitle className="mt-3 text-xl font-black">{LEAVE[mode].titre}</DrawerTitle>
            <DrawerDescription className="mt-2 text-[0.95rem] font-semibold text-muted-foreground">{LEAVE[mode].texte}</DrawerDescription>
            <button type="button" autoFocus onClick={() => setConfirm(false)} className="btn3d mt-5 w-full">
              {LEAVE[mode].rester}
            </button>
            <button type="button" onClick={leave} className="mt-2 min-h-12 w-full rounded-2xl text-[0.95rem] font-black tracking-wide text-ko uppercase hover:bg-ko-soft">
              Quitter
            </button>
          </div>
        </DrawerContent>
      </Drawer>
    </div>
  )
}

function Question({ it, ui, checked }: { it: Item; ui: UI; checked: boolean }) {
  if (it.type === "cloze" && ui.t === "choice") {
    const parts = it.q.split(/_{2,}/)
    const filled = ui.sel !== null
    return (
      <h2 className="mt-3 font-serif text-[1.4rem] leading-[1.35] font-semibold text-balance">
        {parts[0]}
        <span
          className={`ml-1 inline-block font-sans ${filled ? "" : "min-w-24"} font-black border-b-[3px] px-2 text-center align-baseline ${
            filled ? (checked ? "border-transparent" : "border-u2") : "border-line-deep"
          }`}
          style={{ borderColor: filled && !checked ? "var(--u2)" : undefined, color: filled ? "var(--u2-d)" : undefined }}
        >
          {filled ? it.o[ui.sel!] : " "}
        </span>
        {parts.slice(1).join("___")}
      </h2>
    )
  }
  return <h2 className="mt-3 font-serif text-[1.4rem] leading-[1.35] font-semibold text-balance">{it.q}</h2>
}

function Answers({ it, ui, setUi, checked }: { it: Item; ui: UI; setUi: (u: UI) => void; checked: boolean }) {
  const state = (sel: boolean, right: boolean) => (checked ? (right ? "good" : sel ? "bad" : undefined) : sel ? "sel" : undefined)
  const pick = (u: UI) => {
    sfx.tap()
    setUi(u)
  }

  if (it.type === "tf" && ui.t === "tf")
    return (
      <div className="mt-6 grid grid-cols-2 gap-3" role="group" aria-label="Réponse">
        {[true, false].map((v, k) => (
          <button
            key={String(v)}
            type="button"
            data-key={k + 1}
            disabled={checked}
            aria-pressed={ui.sel === v}
            data-state={state(ui.sel === v, it.a === v)}
            onClick={() => pick({ ...ui, sel: v })}
            className="tile min-h-20 justify-center text-lg"
          >
            {v ? "Vrai" : "Faux"}
          </button>
        ))}
      </div>
    )

  if ((it.type === "mcq" || it.type === "cloze") && ui.t === "choice")
    return (
      <div className={it.type === "cloze" ? "mt-6 flex flex-wrap gap-2.5" : "mt-6 grid gap-3"} role="group" aria-label="Choix">
        {ui.order.map((oi, k) => (
          <button
            key={oi}
            type="button"
            data-key={k + 1}
            disabled={checked}
            aria-pressed={ui.sel === oi}
            data-state={state(ui.sel === oi, it.a === oi)}
            onClick={() => pick({ ...ui, sel: oi })}
            className={it.type === "cloze" ? "tile w-auto" : "tile"}
          >
            {it.type === "mcq" && <span className="kbd">{k + 1}</span>}
            <span>{it.o[oi]}</span>
          </button>
        ))}
      </div>
    )

  if (it.type === "order" && ui.t === "order") {
    const rest = ui.pool.filter((v) => !ui.picked.includes(v))
    return (
      <div className="mt-6">
        <div
          className="grid min-h-32 content-start gap-2.5 rounded-2xl border-2 border-dashed border-line-deep p-2.5"
          aria-label="Votre ordre"
        >
          {!ui.picked.length && <p className="p-2 text-sm text-muted-foreground">Touchez les éléments dans l'ordre.</p>}
          {ui.picked.map((v, k) => (
            <motion.button
              layout
              layoutId={`o${v}`}
              key={v}
              type="button"
              disabled={checked}
              data-state={checked ? (it.items[v] === it.items[k] ? "good" : "bad") : undefined}
              onClick={() => pick({ ...ui, picked: ui.picked.filter((x) => x !== v) })}
              className="tile"
            >
              <span className="kbd">{k + 1}</span>
              <span>{it.items[v]}</span>
            </motion.button>
          ))}
        </div>
        {rest.length > 0 && (
          <div className="mt-4 grid gap-2.5" role="group" aria-label="Éléments à placer">
            {rest.map((v, k) => (
              <motion.button
                layout
                layoutId={`o${v}`}
                key={v}
                type="button"
                data-key={k + 1}
                onClick={() => pick({ ...ui, picked: [...ui.picked, v] })}
                className="tile"
              >
                {it.items[v]}
              </motion.button>
            ))}
          </div>
        )}
      </div>
    )
  }

  if (it.type === "match" && ui.t === "match") {
    const inv: Record<number, number> = {}
    for (const l of Object.keys(ui.pairs)) inv[ui.pairs[+l]] = +l
    const clickL = (l: number) => {
      if (ui.pairs[l] !== undefined) {
        const p = { ...ui.pairs }
        delete p[l]
        return pick({ ...ui, pairs: p, selL: l })
      }
      pick({ ...ui, selL: l })
    }
    const clickR = (r: number) => {
      if (ui.selL === null) {
        if (inv[r] !== undefined) {
          const p = { ...ui.pairs }
          delete p[inv[r]]
          pick({ ...ui, pairs: p })
        }
        return
      }
      const p = { ...ui.pairs }
      if (inv[r] !== undefined) delete p[inv[r]]
      p[ui.selL] = r
      const free = it.pairs.map((_, i) => i).find((i) => p[i] === undefined && i !== ui.selL)
      pick({ ...ui, pairs: p, selL: free === undefined ? null : free })
    }
    return (
      <div className="mt-6">
        <p className="mb-3 text-sm text-muted-foreground">Touchez un élément à gauche, puis sa correspondance à droite.</p>
        <div className="grid grid-cols-2 gap-2.5">
          {it.pairs.map((_, row) => {
            const l = row
            const r = ui.right[row]
            const lp = ui.pairs[l] !== undefined
            const rp = inv[r] !== undefined
            const lgood = checked && lp && it.pairs[ui.pairs[l]][1] === it.pairs[l][1]
            const rgood = checked && rp && it.pairs[inv[r]][1] === it.pairs[r][1]
            return [
              <button
                key={`l${l}`}
                type="button"
                disabled={checked}
                aria-pressed={ui.selL === l}
                data-state={checked ? (lgood ? "good" : "bad") : ui.selL === l || lp ? "sel" : undefined}
                onClick={() => clickL(l)}
                className="tile text-[0.92rem]"
                style={!checked && lp && ui.selL !== l ? { opacity: 0.75 } : undefined}
              >
                {lp && <span className="kbd">{l + 1}</span>}
                <span>{it.pairs[l][0]}</span>
              </button>,
              <button
                key={`r${r}`}
                type="button"
                disabled={checked}
                data-state={checked ? (rgood ? "good" : "bad") : rp ? "sel" : undefined}
                onClick={() => clickR(r)}
                className="tile text-[0.92rem] font-semibold"
                style={!checked && rp ? { opacity: 0.75 } : undefined}
              >
                {rp && <span className="kbd">{inv[r] + 1}</span>}
                <span>{it.pairs[r][1]}</span>
              </button>,
            ]
          })}
        </div>
      </div>
    )
  }
  return null
}
