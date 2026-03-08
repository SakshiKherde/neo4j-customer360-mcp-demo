import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bookmark, BookmarkCheck, ExternalLink } from 'lucide-react'
import type { Story } from '../data/mockData'
import SectionLabel from './SectionLabel'

const sectionAccent: Record<string, string> = {
  Tech:     '#2D6FA8',
  Fashion:  '#A0405E',
  Wellness: '#2A7A5A',
}

const sectionGradient: Record<string, string> = {
  Tech:     'linear-gradient(135deg, rgba(107,159,212,0.08), rgba(107,159,212,0.02))',
  Fashion:  'linear-gradient(135deg, rgba(201,122,150,0.08), rgba(201,122,150,0.02))',
  Wellness: 'linear-gradient(135deg, rgba(107,175,148,0.08), rgba(107,175,148,0.02))',
}

interface Props {
  story: Story
  width?: number
}

export default function CarouselStoryCard({ story, width = 300 }: Props) {
  const [saved, setSaved]       = useState(false)
  const [open, setOpen]         = useState(false)
  const accent = sectionAccent[story.section] ?? '#B8906A'

  return (
    <motion.article
      whileHover={{ y: -3, boxShadow: '0 12px 40px rgba(0,0,0,0.10)' }}
      whileTap={{ scale: 0.98 }}
      className="rounded-3xl overflow-hidden cursor-pointer flex-shrink-0"
      style={{
        width,
        background: '#FFFFFF',
        border: '1px solid rgba(0,0,0,0.07)',
        boxShadow: '0 2px 12px rgba(0,0,0,0.06)',
        transition: 'box-shadow 0.2s ease',
      }}
      onClick={() => setOpen(!open)}
    >
      {/* Color header strip */}
      <div
        className="h-1.5"
        style={{ background: accent }}
      />

      {/* Gradient bg area */}
      <div
        className="px-5 pt-4 pb-1"
        style={{ background: sectionGradient[story.section] }}
      >
        <div className="flex items-center justify-between mb-3">
          <SectionLabel section={story.section} />
          <button
            onClick={(e) => { e.stopPropagation(); setSaved(!saved) }}
            style={{ color: saved ? accent : '#C0BEB8' }}
          >
            {saved ? <BookmarkCheck size={15} /> : <Bookmark size={15} />}
          </button>
        </div>
      </div>

      <div className="px-5 pt-3 pb-5">
        {/* Headline */}
        <a href={story.url} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}>
          <h3
            className="font-serif font-bold leading-snug text-ink-primary mb-2 hover:underline"
            style={{ fontSize: 15 }}
          >
            {story.headline}
          </h3>
        </a>

        {/* Summary */}
        <p className="font-sans text-xs leading-relaxed text-ink-muted mb-3 line-clamp-3">
          {story.summary}
        </p>

        {/* Expandable why */}
        <AnimatePresence>
          {open && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.22 }}
              className="overflow-hidden"
            >
              <div
                className="rounded-xl p-3 mb-3"
                style={{ background: `${accent}12`, borderLeft: `2px solid ${accent}` }}
              >
                <p className="font-mono text-[9px] tracking-widest uppercase mb-1" style={{ color: accent }}>
                  Why it matters
                </p>
                <p className="font-serif text-xs leading-relaxed text-ink-secondary">
                  {story.whyItMatters}
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        <div className="flex items-center justify-between">
          <span className="font-mono text-[9px] text-ink-muted">{story.source} · {story.readTime}</span>
          <a
            href={story.url}
            onClick={(e) => e.stopPropagation()}
            className="p-1 rounded-full"
            style={{ color: accent }}
          >
            <ExternalLink size={12} />
          </a>
        </div>
      </div>
    </motion.article>
  )
}
