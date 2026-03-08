import { motion } from 'framer-motion'
import type { Section } from '../data/mockData'
import CarouselStoryCard from './CarouselStoryCard'
import Carousel from './Carousel'

const sectionConfig = {
  Tech:     { accent: '#2D6FA8', emoji: '⚡', bg: 'rgba(45,111,168,0.07)'  },
  Fashion:  { accent: '#A0405E', emoji: '✦',  bg: 'rgba(160,64,94,0.07)'   },
  Wellness: { accent: '#2A7A5A', emoji: '◎',  bg: 'rgba(42,122,90,0.07)'   },
  Finance:  { accent: '#5C5EA8', emoji: '◈',  bg: 'rgba(92,94,168,0.07)'   },
} as const

interface Props { section: Section; number: string }

export default function SectionRail({ section, number }: Props) {
  const cfg = sectionConfig[section.name]

  return (
    <section id={section.name.toLowerCase()} className="mt-14">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.45 }}
      >
        {/* Section header pill */}
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-3">
            <span
              className="text-2xl w-10 h-10 rounded-2xl flex items-center justify-center"
              style={{ background: cfg.bg }}
            >
              {cfg.emoji}
            </span>
            <div>
              <p className="font-mono text-[9px] tracking-widest text-ink-muted uppercase mb-0.5">
                {number}
              </p>
              <h2
                className="font-serif font-bold text-2xl leading-none"
                style={{ color: cfg.accent }}
              >
                {section.name}
              </h2>
            </div>
          </div>
          <span className="font-sans text-xs text-ink-muted">{section.description}</span>
        </div>

        {/* Horizontal card rail */}
        <Carousel>
          {section.stories.map((story, i) => (
            <CarouselStoryCard key={i} story={{ ...story, section: section.name }} width={300} />
          ))}
        </Carousel>
      </motion.div>
    </section>
  )
}
