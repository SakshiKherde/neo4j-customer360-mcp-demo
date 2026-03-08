import { useState } from 'react'
import { motion } from 'framer-motion'
import { Copy, Check } from 'lucide-react'
import type { ContentIdea } from '../data/mockData'
import Carousel from './Carousel'

const platformConfig = {
  LinkedIn:  { color: '#5A8FC9', bg: 'rgba(90,143,201,0.08)',  bar: '#5A8FC9', emoji: '💼' },
  Instagram: { color: '#C9728A', bg: 'rgba(201,114,138,0.08)', bar: '#C9728A', emoji: '✦'  },
  Substack:  { color: '#C98F5A', bg: 'rgba(201,143,90,0.08)',  bar: '#C98F5A', emoji: '✎'  },
}

function ContentCard({ idea }: { idea: ContentIdea }) {
  const [copied, setCopied] = useState(false)
  const cfg = platformConfig[idea.platform]

  const copyIdea = () => {
    navigator.clipboard.writeText(`${idea.title}\n\n${idea.angle}`)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <motion.div
      whileHover={{ y: -3, boxShadow: '0 10px 36px rgba(0,0,0,0.09)' }}
      whileTap={{ scale: 0.98 }}
      className="rounded-3xl overflow-hidden flex-shrink-0"
      style={{
        width: 280,
        background: '#FFFFFF',
        border: '1px solid rgba(0,0,0,0.07)',
        boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
      }}
    >
      <div className="h-1.5" style={{ background: cfg.bar }} />
      <div className="p-5">
        <div className="flex items-center justify-between mb-4">
          <span
            className="font-mono text-[9px] font-bold tracking-widest px-3 py-1.5 rounded-full uppercase"
            style={{ color: cfg.color, background: cfg.bg }}
          >
            {cfg.emoji} {idea.platform}
          </span>
          <button
            onClick={copyIdea}
            className="p-1.5 rounded-full transition-all"
            style={{ color: copied ? cfg.color : '#C0BEB8', background: copied ? cfg.bg : 'transparent' }}
          >
            {copied ? <Check size={13} /> : <Copy size={13} />}
          </button>
        </div>
        <h3 className="font-serif font-bold text-[15px] leading-snug text-ink-primary mb-2">
          {idea.title}
        </h3>
        <p className="font-sans text-xs leading-relaxed text-ink-muted">{idea.angle}</p>
      </div>
    </motion.div>
  )
}

interface Props { items: ContentIdea[] }

export default function ForContent({ items }: Props) {
  return (
    <section id="content" className="mt-14">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.45 }}
      >
        <div className="flex items-center gap-3 mb-6">
          <span className="text-2xl w-10 h-10 rounded-2xl flex items-center justify-center"
                style={{ background: 'rgba(155,142,212,0.08)' }}>✎</span>
          <div>
            <p className="font-mono text-[9px] tracking-widest text-ink-muted uppercase mb-0.5">06</p>
            <h2 className="font-serif font-bold text-2xl text-ink-primary leading-none">For Content</h2>
          </div>
        </div>

        <Carousel>
          {items.map((idea, i) => (
            <ContentCard key={i} idea={idea} />
          ))}
        </Carousel>
      </motion.div>
    </section>
  )
}
