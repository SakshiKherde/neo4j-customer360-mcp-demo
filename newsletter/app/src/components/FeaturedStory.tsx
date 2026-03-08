import { useState } from 'react'
import { motion } from 'framer-motion'
import { Bookmark, BookmarkCheck, ArrowUpRight, Zap } from 'lucide-react'
import type { Story } from '../data/mockData'
import SectionLabel from './SectionLabel'

const sectionAccent: Record<string, string> = {
  Tech:     '#2D6FA8',
  Fashion:  '#A0405E',
  Wellness: '#2A7A5A',
}

interface Props { story: Story }

export default function FeaturedStory({ story }: Props) {
  const [saved, setSaved]           = useState(false)
  const [whyOpen, setWhyOpen]       = useState(false)
  const accent = sectionAccent[story.section] ?? '#B8906A'

  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className="rounded-3xl overflow-hidden"
      style={{
        background: '#FFFFFF',
        border: '1px solid rgba(0,0,0,0.07)',
        boxShadow: '0 4px 24px rgba(0,0,0,0.07)',
      }}
    >
      {/* Color band */}
      <div className="h-2" style={{ background: accent }} />

      <div className="p-6 md:p-8">
        {/* Meta */}
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2">
            <SectionLabel section={story.section} size="sm" />
            <span className="font-mono text-[10px] text-ink-muted">{story.source} · {story.readTime}</span>
          </div>
          <button
            onClick={() => setSaved(!saved)}
            style={{ color: saved ? accent : '#C0BEB8' }}
          >
            {saved ? <BookmarkCheck size={17} /> : <Bookmark size={17} />}
          </button>
        </div>

        {/* Headline */}
        <a href={story.url} target="_blank" rel="noopener noreferrer">
          <h2
            className="font-serif font-bold leading-tight text-ink-primary mb-4 hover:underline cursor-pointer"
            style={{ fontSize: 'clamp(1.35rem, 3vw, 1.85rem)' }}
          >
            {story.headline}
          </h2>
        </a>

        <p className="font-sans text-sm leading-relaxed text-ink-secondary mb-5">
          {story.summary}
        </p>

        {/* Why it matters toggle */}
        <button
          onClick={() => setWhyOpen(!whyOpen)}
          className="flex items-center gap-2 font-mono text-[10px] font-semibold tracking-widest uppercase px-4 py-2 rounded-full mb-4 transition-all"
          style={{
            color: accent,
            background: whyOpen ? `${accent}15` : `${accent}09`,
            border: `1px solid ${accent}25`,
          }}
        >
          <Zap size={11} />
          {whyOpen ? 'Hide' : 'Why it matters'}
        </button>

        {whyOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.22 }}
            className="rounded-2xl p-4 mb-5 overflow-hidden"
            style={{ background: `${accent}0D`, borderLeft: `3px solid ${accent}` }}
          >
            <p className="font-serif text-sm leading-relaxed text-ink-secondary">
              {story.whyItMatters}
            </p>
            {story.personalAngle && (
              <p className="font-sans text-xs italic mt-2" style={{ color: '#B8906A' }}>
                ◆ {story.personalAngle}
              </p>
            )}
          </motion.div>
        )}

        {/* Tags + CTA */}
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="flex flex-wrap gap-1.5">
            {story.tags.map((tag) => (
              <span
                key={tag}
                className="font-mono text-[9px] px-2.5 py-1 rounded-full text-ink-muted"
                style={{ background: 'rgba(0,0,0,0.04)' }}
              >
                {tag}
              </span>
            ))}
          </div>
          <a
            href={story.url}
            className="flex items-center gap-1 font-sans text-xs font-semibold px-4 py-2 rounded-full transition-all"
            style={{ color: accent, background: `${accent}12` }}
          >
            Read story <ArrowUpRight size={13} />
          </a>
        </div>
      </div>
    </motion.article>
  )
}
