import { useState } from "react"
import { AnimatePresence, motion, useReducedMotion } from "motion/react"
import { BriefcaseBusiness, Building2, FileSearch, Handshake, Scale } from "lucide-react"
import { Mascot } from "@/components/Mascot"
import { PROFILS } from "@/lib/content"
import { profilSuggere, setProfil, setSetting, useStore } from "@/lib/store"
import { sfx } from "@/lib/sound"

export const OUTILS = ["Claude", "ChatGPT", "Copilot", "Le Chat", "Gemini", "Autre"]

/* Une icône par profil, même famille et même trait (lucide). */
export const PROFIL_ICON: Record<string, typeof Scale> = { juriste: Scale, cdt: Handshake, brevet: FileSearch, support: Building2 }

/** Choix du métier : à l'ouverture et dans le profil. Une tuile par ligne, jamais quatre cartes côte à côte. */
export function ProfilPicker({ value, onPick }: { value: string; onPick: (id: string) => void }) {
  return (
    <div className="grid gap-2.5" role="radiogroup" aria-label="Votre métier">
      {PROFILS.map((p) => {
        const Icon = PROFIL_ICON[p.id] || BriefcaseBusiness
        const on = value === p.id
        return (
          <button
            key={p.id}
            type="button"
            role="radio"
            aria-checked={on}
            data-state={on ? "sel" : undefined}
            onClick={() => {
              sfx.tap()
              onPick(p.id)
            }}
            className="tile items-center py-3"
          >
            <span className="grid size-11 shrink-0 place-items-center rounded-xl border-2 border-current/20" aria-hidden="true">
              <Icon className="size-6" strokeWidth={2.2} />
            </span>
            <span>
              <span className="block text-[1.05rem] font-black">{p.nom}</span>
              <span className="mt-0.5 block text-sm font-semibold opacity-75">{p.desc}</span>
            </span>
          </button>
        )
      })}
    </div>
  )
}

/** Premier lancement (ou progression d'avant les profils) : métier, puis assistant utilisé. */
export function Onboarding() {
  const root = useStore()
  const reduce = useReducedMotion()
  const [page, setPage] = useState(0)
  const [profil, setP] = useState(() => profilSuggere())
  const [outil, setOutil] = useState(root.state.settings.outil)
  const dejaVenu = Object.keys(root.state.steps).length > 0

  const finish = () => {
    sfx.done()
    if (outil !== root.state.settings.outil) setSetting("outil", outil)
    setProfil(profil)
  }
  const bubble =
    page === 0
      ? dejaVenu
        ? "Le parcours s'adapte maintenant à votre métier. Lequel est le vôtre ?"
        : "Bonjour ! Pour adapter les exemples et les exercices, quel est votre métier ?"
      : "Et quel assistant utilisez-vous le plus souvent ?"

  return (
    <div className="fixed inset-0 z-50 flex flex-col overflow-y-auto bg-background safe-t safe-b">
      <div className="mx-auto flex w-full max-w-xl flex-1 flex-col px-4 pt-6 pb-5">
        <p className="text-center text-sm font-extrabold text-muted-foreground">Parcours IA · {page + 1} sur 2</p>
        <div className="mt-5 flex items-end gap-3">
          <Mascot size={76} mood={page === 1 ? "happy" : "idle"} />
          <p className="bubble mb-3 flex-1 text-[1.05rem] font-extrabold leading-snug">{bubble}</p>
        </div>
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={page}
            initial={reduce ? { opacity: 0 } : { opacity: 0, x: 28 }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, x: -28 }}
            transition={{ type: "spring", bounce: 0, duration: 0.3 }}
            className="mt-6 flex-1"
          >
            {page === 0 ? (
              <>
                <ProfilPicker value={profil} onPick={setP} />
                <p className="mt-4 text-sm font-semibold text-muted-foreground">
                  Le socle est commun à tous. Le métier change la voie Métier et les exemples ; il se modifie à tout moment dans le profil.
                </p>
              </>
            ) : (
              <div className="grid grid-cols-2 gap-2.5" role="radiogroup" aria-label="Assistant utilisé">
                {OUTILS.map((o) => (
                  <button
                    key={o}
                    type="button"
                    role="radio"
                    aria-checked={outil === o}
                    data-state={outil === o ? "sel" : undefined}
                    onClick={() => {
                      sfx.tap()
                      setOutil(o)
                    }}
                    className="tile justify-center text-[1.05rem]"
                  >
                    {o}
                  </button>
                ))}
              </div>
            )}
          </motion.div>
        </AnimatePresence>
        <div className="mt-6 grid gap-2">
          {page === 0 ? (
            <button type="button" className="btn3d w-full" disabled={!profil} onClick={() => setPage(1)}>
              Continuer
            </button>
          ) : (
            <>
              <button type="button" className="btn3d w-full" onClick={finish}>
                {dejaVenu ? "Reprendre le parcours" : "Commencer"}
              </button>
              <button type="button" onClick={() => setPage(0)} className="min-h-11 text-sm font-extrabold text-muted-foreground hover:text-foreground">
                Revenir au choix du métier
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
