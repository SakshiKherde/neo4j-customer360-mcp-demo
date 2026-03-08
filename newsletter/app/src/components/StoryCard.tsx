import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bookmark, BookmarkCheck, ChevronDown, ExternalLink, Zap } from 'lucide-react'
import type { Story } from '../data/mockData'
import SectionLabel from './SectionLabel'

const sectionAccent: Record<string, string> = {
  Tech:     '#2D6FA8',
  Fashion:  '#A0405E',
  Wellness: '#2A7A5A',
}

interface Props {
  story: Story
  index?: number
}

export default function StoryCard({ story, index }: Props) {
  const [saved,    setSaved]    = useState(false)
  const [expanded, setExpanded] = useState(false)
  const accent = sectionAccent[story.section] ?? '#B8906A'

  return (
    <motion.article
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.4, delay: index ? (index % 4) * 0.07 : 0 }}
      whileHover={{ y: -2, boxShadow: '0 8px 32px rgba(0,0,0,0.08)' }}
      className="relative rounded-xl overflow-hidden cursor-pointer"
      style={{
        background: '#FFFFFF',
        border: '1px solid rgba(0,0,0,0.07)',
        boxShadow: '0 1px 4px rgba(0,0,0,0.05)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
      }}
      onClick={() => setExpanded(!expanded)}
    >
      {/* Left accent bar */}
      <div
        className="absolute left-0 top-0 bottom-0 w-[2px]"
        style={{ background: `linear-gradient(to bottom, ${accent}, ${accent}40)` }}
      />

      <div className="p-5 pl-6">
        {/* Meta */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-2 flex-wrap">
            {index !== undefined && (
              <span className="font-mono text-[11px] font-bold text-ink-muted/60">
                {String(index).padStart(2, '0')}
              </span>
            )}
            <SectionLabel section={story.section} />
            <span className="font-mono text-[10px] text-ink-muted">{story.source}</span>
          </div>
          <div className="flex items-center gap-1.5 flex-shrink-0">
            <span className="font-mono text-[10px] text-ink-muted">{story.readTime}</span>
            <button
              onClick={(e) => { e.stopPropagation(); setSaved(!saved) }}
              className="p-1 rounded transition-colors"
              style={{ color: saved ? accent : '#C0BEB8' }}
            >
              {saved ? <BookmarkCheck size={14} /> : <Bookmark size={14} />}
            </button>
          </div>
        </div>

        {/* Headline */}
        <h3 className="font-serif font-semibold text-base leading-snug text-ink-primary mb-2">
          {story.headline}
        </h3>

        {/* Summary */}
        <p className="font-sans text-sm leading-relaxed text-ink-muted line-clamp-2 mb-3">
          {story.summary}
        </p>

        {/* Expandable: Why it matters */}
        <AnimatePresence>
          {expanded && (
            <motion.div
              key="why"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.25 }}
              className="overflow-hidden"
            >
              <div
                className="rounded-lg p-3.5 mb-3"
                style={{
                  background: `${accent}0D`,
                  borderLeft: `2px solid ${accent}`,
                }}
              >
                <p
                  className="font-mono text-[9px] tracking-widest uppercase mb-1.5"
                  style={{ color: accent }}
                >
                  Why it matters
                </p>
                <p className="font-serif text-sm leading-relaxed text-ink-secondary">
                  {story.whyItMatters}
                </p>
                {story.personalAngle && (
                  <p
                    className="font-sans text-xs italic mt-2 flex items-start gap-1.5"
                    style={{ color: '#B8906A' }}
                  >
                    <Zap size={10} className="mt-0.5 flex-shrink-0" />
                    {story.personalAngle}
                  </p>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        <div className="flex items-center justify-between">
          <div className="flex flex-wrap gap-1.5">
            {story.tags.slice(0, 2).map((tag) => (
              <span
                key={tag}
                className="font-mono text-[9px] px-2 py-0.5 rounded-full text-ink-muted"
                style={{ background: 'rgba(0,0,0,0.04)' }}
              >
                {tag}
              </span>
            ))}
          </div>
          <div className="flex items-center gap-2">
            <a
              href={story.url}
              onClick={(e) => e.stopPropagation()}
              className="p-1 rounded transition-colors text-ink-muted/50 hover:text-ink-muted"
            >
              <ExternalLink size={13} />
            </a>
            <motion.span
              animate={{ rotate: expanded ? 180 : 0 }}
              className="text-ink-muted/50"
            >
              <ChevronDown size={14} />
            </motion.span>
          </div>
        </div>
      </div>
    </motion.article>
  )
}
