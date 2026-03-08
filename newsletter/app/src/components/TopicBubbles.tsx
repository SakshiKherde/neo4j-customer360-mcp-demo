import { motion } from 'framer-motion'

const topics = [
  { label: 'Tech',     emoji: '⚡', color: '#2D6FA8', bg: 'rgba(45,111,168,0.10)'  },
  { label: 'Fashion',  emoji: '✦',  color: '#A0405E', bg: 'rgba(160,64,94,0.10)'   },
  { label: 'Wellness', emoji: '◎',  color: '#2A7A5A', bg: 'rgba(42,122,90,0.10)'   },
  { label: 'Finance',  emoji: '◈',  color: '#5C5EA8', bg: 'rgba(92,94,168,0.10)'   },
  { label: 'Watching', emoji: '↗',  color: '#B8906A', bg: 'rgba(184,144,106,0.10)' },
  { label: 'Content',  emoji: '✎',  color: '#9B8ED4', bg: 'rgba(155,142,212,0.10)' },
]

export default function TopicBubbles() {
  const scrollTo = (id: string) =>
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })

  return (
    <div className="flex gap-3 overflow-x-auto pb-1" style={{ scrollbarWidth: 'none' }}>
      {topics.map((t, i) => (
        <motion.button
          key={t.label}
          initial={{ opacity: 0, scale: 0.85 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: i * 0.07, duration: 0.3 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => scrollTo(t.label.toLowerCase())}
          className="flex flex-col items-center gap-1.5 flex-shrink-0"
        >
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center text-xl font-medium"
            style={{ background: t.bg, border: `1.5px solid ${t.color}30` }}
          >
            {t.emoji}
          </div>
          <span
            className="font-sans text-[10px] font-semibold tracking-wide"
            style={{ color: t.color }}
          >
            {t.label}
          </span>
        </motion.button>
      ))}
    </div>
  )
}
