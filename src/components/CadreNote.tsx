import { Home } from "lucide-react"
import { CADRES, CADRE_NOTE } from "@/lib/content"
import { beyondCadre } from "@/lib/store"

/** Mention discrète pour une étape ou un défi qui dépasse le cadre autorisé au poste. */
export function CadreNote({ cadre, compact = false }: { cadre?: number; compact?: boolean }) {
  if (!beyondCadre({ cadre })) return null
  const c = CADRES[String(cadre)]
  if (compact)
    return (
      <span className="inline-flex items-center gap-1 rounded-md bg-secondary px-1.5 py-0.5 text-xs font-extrabold text-muted-foreground">
        <Home className="size-3.5" aria-hidden="true" /> Projet perso
      </span>
    )
  return (
    <p className="flex gap-2 text-sm text-muted-foreground">
      <Home className="mt-0.5 size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
      <span>
        <span className="font-extrabold text-foreground">Projet perso.</span> Cadre {cadre} : {c?.nom}. {CADRE_NOTE}
      </span>
    </p>
  )
}
