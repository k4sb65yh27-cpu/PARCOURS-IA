import { getRoot } from "./store"

/*
 * Sons synthétisés avec Web Audio : aucun fichier à charger ni à mettre en cache.
 * L'AudioContext naît au premier geste de l'utilisateur (règle d'autoplay des navigateurs).
 */
let ctx: AudioContext | null = null
let master: GainNode | null = null

function ac() {
  if (!getRoot().state.settings.sound) return null
  if (!ctx) {
    try {
      const C = window.AudioContext || (window as any).webkitAudioContext
      ctx = new C()
      master = ctx.createGain()
      master.gain.value = 0.9
      master.connect(ctx.destination)
    } catch {
      return null
    }
  }
  if (ctx.state === "suspended") ctx.resume().catch(() => {})
  return ctx
}

function note(freq: number, at: number, dur: number, type: OscillatorType = "triangle", vol = 0.16, glideTo?: number) {
  const c = ac()
  if (!c || !master) return
  const t0 = c.currentTime + at
  const o = c.createOscillator()
  const g = c.createGain()
  o.type = type
  o.frequency.setValueAtTime(freq, t0)
  if (glideTo) o.frequency.exponentialRampToValueAtTime(glideTo, t0 + dur)
  g.gain.setValueAtTime(0.0001, t0)
  g.gain.linearRampToValueAtTime(vol, t0 + 0.012)
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur)
  o.connect(g)
  g.connect(master)
  o.start(t0)
  o.stop(t0 + dur + 0.03)
}

function buzz(ms: number | number[]) {
  if (!getRoot().state.settings.haptics) return
  try {
    navigator.vibrate?.(ms)
  } catch {
    /* non pris en charge (Safari iOS) */
  }
}

export const sfx = {
  /** Toucher d'une option : clic doux, presque inaudible. */
  tap() {
    note(1250, 0, 0.035, "sine", 0.05)
    buzz(8)
  },
  /** Bonne réponse : deux notes montantes (quinte). */
  ok() {
    note(784, 0, 0.13, "triangle", 0.17)
    note(1175, 0.08, 0.22, "triangle", 0.17)
    buzz(15)
  },
  /** Erreur : note grave courte qui descend, sans agressivité. */
  ko() {
    note(233, 0, 0.16, "square", 0.05, 196)
    note(174, 0.11, 0.24, "square", 0.05, 147)
    buzz([30, 40, 30])
  },
  /** Série de bonnes réponses : petit arpège. */
  combo() {
    ;[880, 1109, 1319].forEach((f, i) => note(f, i * 0.055, 0.12, "triangle", 0.12))
  },
  /** Fin de leçon : accord majeur arpégé puis tenu. */
  done() {
    ;[523, 659, 784, 1047].forEach((f, i) => note(f, i * 0.09, 0.5, "triangle", 0.13))
    note(1568, 0.38, 0.6, "sine", 0.06)
    buzz([20, 60, 20, 60, 40])
  },
  /** Série journalière prolongée. */
  streak() {
    ;[659, 784, 988, 1319].forEach((f, i) => note(f, i * 0.07, 0.3, "sine", 0.12))
  },
  /** Plus de vies. */
  out() {
    ;[392, 330, 262].forEach((f, i) => note(f, i * 0.16, 0.3, "triangle", 0.12))
  },
  /** Déblocage ou validation d'étape. */
  unlock() {
    note(587, 0, 0.12, "triangle", 0.14)
    note(880, 0.1, 0.12, "triangle", 0.14)
    note(1175, 0.2, 0.45, "triangle", 0.14)
    buzz([15, 50, 30])
  },
}
