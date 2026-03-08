import { motion } from 'framer-motion'
import type { NewsletterData } from '../data/mockData'
import TopicBubbles from './TopicBubbles'

interface Props { data: NewsletterData }

export default function Hero({ data }: Props) {
  return (
    <section className="pt-16 pb-10 relative">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
      >
        {/* Eyebrow */}
        <div className="flex items-center gap-2 mb-6">
          <span className="w-1.5 h-1.5 rounded-full bg-gold animate-pulse-gold" />
          <span className="font-mono text-[10px] tracking-widest text-ink-muted uppercase">
            {data.date}
          </span>
        </div>

        {/* Masthead */}
        <h1
          className="font-serif font-bold leading-[1.05] mb-4"
          style={{ fontSize: 'clamp(2.6rem, 7vw, 5rem)', letterSpacing: '-0.025em' }}
        >
          <span className="text-gradient-gold">The Daily</span>
          <br />
          <span className="text-ink-primary">Brief.</span>
        </h1>

        <p className="font-serif text-base italic text-ink-secondary mb-8">{data.greeting}</p>

        {/* Topic bubbles */}
        <TopicBubbles />

        {/* Opening note */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="mt-8 rounded-3xl p-6 border"
          style={{
            background: 'linear-gradient(135deg, rgba(184,144,106,0.06), rgba(184,144,106,0.02))',
            borderColor: 'rgba(184,144,106,0.18)',
          }}
        >
          <div className="flex items-center gap-2 mb-3">
            <span
              className="font-mono text-[9px] font-bold tracking-widest px-3 py-1 rounded-full uppercase"
              style={{ color: '#B8906A', background: 'rgba(184,144,106,0.12)' }}
            >
              ✦ What matters today
            </span>
          </div>
          <p className="font-serif text-[15px] leading-relaxed text-ink-secondary">
            {data.openingNote}
          </p>
        </motion.div>
      </motion.div>
    </section>
  )
}
