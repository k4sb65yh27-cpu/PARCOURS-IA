import { motion, useReducedMotion, type TargetAndTransition, type Transition } from "motion/react"

/**
 * Mascotte : l'anneau du logo SATT Sud-Est, avec un visage, des yeux et des lunettes.
 * idle : respire et cligne ; happy : saute ; sad : penche et baisse les yeux ; cheer : saut et tour de l'anneau ;
 * worried : dernière vie, yeux ronds et léger tremblement.
 */
export type Mood = "idle" | "happy" | "sad" | "cheer" | "worried"

const INK = "#1d2327"
const ring = `${import.meta.env.BASE_URL}mascot-ring.png`

export function Mascot({ mood = "idle", size = 96, className = "" }: { mood?: Mood; size?: number; className?: string }) {
  const reduce = useReducedMotion()
  const body: Record<Mood, TargetAndTransition> = {
    idle: { y: [0, -3, 0], rotate: 0, scaleY: 1 },
    happy: { y: [0, -16, 0, -6, 0], scaleY: [1, 1.06, 0.94, 1.02, 1], rotate: 0 },
    sad: { y: 4, rotate: -7, scaleY: 0.97 },
    cheer: { y: [0, -24, 0, -10, 0], scaleY: [1, 1.08, 0.92, 1.03, 1], rotate: 0 },
    worried: { x: [0, -2, 2, -1, 0], y: 0, rotate: 0, scaleY: 1 },
  }
  const bodyT: Record<Mood, Transition> = {
    idle: { duration: 2.6, repeat: Infinity, ease: "easeInOut" },
    happy: { duration: 0.7, ease: "easeOut" },
    sad: { type: "spring", bounce: 0.3, duration: 0.6 },
    cheer: { duration: 0.9, ease: "easeOut", repeat: 1, repeatDelay: 0.6 },
    worried: { duration: 0.5, repeat: Infinity, repeatDelay: 2.2 },
  }
  const joyful = mood === "happy" || mood === "cheer"
  return (
    <motion.div
      aria-hidden="true"
      className={`relative shrink-0 ${className}`}
      style={{ width: size, height: size * (255 / 236), originY: 1 }}
      animate={reduce ? undefined : body[mood]}
      transition={reduce ? undefined : bodyT[mood]}
    >
      <motion.img
        src={ring}
        alt=""
        draggable={false}
        className="absolute inset-0 size-full select-none"
        animate={reduce ? undefined : { rotate: mood === "cheer" ? 360 : 0 }}
        transition={mood === "cheer" ? { duration: 1.1, ease: [0.3, 0, 0.2, 1], delay: 0.15 } : { duration: 0.3 }}
      />
      <svg viewBox="0 0 236 255" className="absolute inset-0 size-full overflow-visible">
        <circle cx="118" cy="132" r="64" fill="#fff" />
        <motion.g
          animate={reduce || joyful ? undefined : { scaleY: [1, 1, 0.1, 1, 1] }}
          transition={{ duration: 4, times: [0, 0.9, 0.93, 0.96, 1], repeat: Infinity }}
          style={{ originY: "126px", originX: "118px" }}
        >
          {joyful ? (
            <>
              <path d="M84 132 q11 -14 22 0" fill="none" stroke={INK} strokeWidth="6" strokeLinecap="round" />
              <path d="M130 132 q11 -14 22 0" fill="none" stroke={INK} strokeWidth="6" strokeLinecap="round" />
            </>
          ) : (
            <>
              <circle cx="95" cy={mood === "sad" ? 132 : 126} r={mood === "worried" ? 10.5 : 8.5} fill={INK} />
              <circle cx="141" cy={mood === "sad" ? 132 : 126} r={mood === "worried" ? 10.5 : 8.5} fill={INK} />
              <circle cx="98" cy={mood === "sad" ? 129 : 123} r="2.6" fill="#fff" />
              <circle cx="144" cy={mood === "sad" ? 129 : 123} r="2.6" fill="#fff" />
            </>
          )}
        </motion.g>
        {/* Lunettes */}
        <g fill="none" stroke={INK} strokeWidth="5">
          <circle cx="95" cy="127" r="20" />
          <circle cx="141" cy="127" r="20" />
          <path d="M115 124 q3 -5 6 0" strokeLinecap="round" />
          <path d="M75 122 l-11 -4 M161 122 l11 -4" strokeLinecap="round" />
        </g>
        {mood === "worried" ? (
          <ellipse cx="118" cy="166" rx="7" ry="8" fill={INK} />
        ) : mood === "sad" ? (
          <path d="M106 170 q12 -8 24 0" fill="none" stroke={INK} strokeWidth="5" strokeLinecap="round" />
        ) : joyful ? (
          <path d="M101 160 q17 20 34 0 z" fill={INK} stroke={INK} strokeWidth="3" strokeLinejoin="round" />
        ) : (
          <path d="M106 163 q12 9 24 0" fill="none" stroke={INK} strokeWidth="5" strokeLinecap="round" />
        )}
      </svg>
    </motion.div>
  )
}
