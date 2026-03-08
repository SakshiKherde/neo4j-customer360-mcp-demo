import { motion } from 'framer-motion'
import type { Section } from '../data/mockData'
import StoryCard from './StoryCard'

const sectionConfig = {
  Tech: {
    accent:  '#6B9FD4',
    dimBg:   'rgba(107,159,212,0.03)',
    border:  'rgba(107,159,212,0.2)',
  },
  Fashion: {
    accent:  '#C97A96',
    dimBg:   'rgba(201,122,150,0.03)',
    border:  'rgba(201,122,150,0.2)',
  },
  Wellness: {
    accent:  '#6BAF94',
    dimBg:   'rgba(107,175,148,0.03)',
    border:  'rgba(107,175,148,0.2)',
  },
} as const

interface Props {
  section: Section
  index: number
}

export default function SectionBlock({ section, index }: Props) {
  const cfg = sectionConfig[section.name]

  return (
    <section id={section.name.toLowerCase()} className="mt-20">
      {/* Section header */}
      <motion.div
        initial={{ opacity: 0, x: -12 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true, margin: '-60px' }}
        transition={{ duration: 0.5 }}
        className="mb-6"
      >
        <div className="flex items-end gap-4 mb-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <span className="font-mono text-[10px] text-ink-muted tracking-widest">
                {String(index + 2).padStart(2, '0')}
              </span>
              <div className="h-px w-6" style={{ background: cfg.accent }} />
            </div>
            <h2
              className="font-serif font-bold leading-none"
              style={{ fontSize: '2rem', color: cfg.accent }}
            >
              {section.name}
            </h2>
            <p className="font-sans text-xs text-ink-muted mt-1 tracking-wide">
              {section.description}
            </p>
          </div>
        </div>

        {/* Color rule */}
        <div
          className="h-px w-full"
          style={{
            background: `linear-gradient(90deg, ${cfg.accent}60, rgba(0,0,0,0.04))`,
          }}
        />
      </motion.div>

      {/* Cards */}
      <div
        className="rounded-2xl p-4"
        style={{ background: cfg.dimBg }}
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {section.stories.map((story, i) => (
            <StoryCard key={i} story={story} />
          ))}
        </div>
      </div>
    </section>
  )
}
