import { motion } from 'framer-motion'
import { TrendingUp, Sparkles, Zap } from 'lucide-react'
import type { WatchItem } from '../data/mockData'

const trendConfig = {
  rising:   { label: 'Rising',   icon: TrendingUp, color: '#6B9FD4', bg: 'rgba(107,159,212,0.10)' },
  emerging: { label: 'Emerging', icon: Sparkles,   color: '#B8906A', bg: 'rgba(184,144,106,0.10)' },
  breaking: { label: 'Breaking', icon: Zap,         color: '#C97A96', bg: 'rgba(201,122,150,0.10)' },
}

interface Props { items: WatchItem[] }

export default function WorthWatching({ items }: Props) {
  return (
    <section id="watching" className="mt-14">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.45 }}
      >
        <div className="flex items-center gap-3 mb-6">
          <span className="text-2xl w-10 h-10 rounded-2xl flex items-center justify-center"
                style={{ background: 'rgba(184,144,106,0.08)' }}>↗</span>
          <div>
            <p className="font-mono text-[9px] tracking-widest text-ink-muted uppercase mb-0.5">05</p>
            <h2 className="font-serif font-bold text-2xl text-ink-primary leading-none">Worth Watching</h2>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {items.map((item, i) => {
            const cfg = trendConfig[item.trend]
            const Icon = cfg.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.35, delay: i * 0.08 }}
                whileHover={{ y: -3, boxShadow: '0 8px 32px rgba(0,0,0,0.08)' }}
                className="rounded-3xl p-5"
                style={{
                  background: '#FFFFFF',
                  border: '1px solid rgba(0,0,0,0.07)',
                  boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
                  transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                }}
              >
                <span
                  className="inline-flex items-center gap-1.5 font-mono text-[9px] font-bold tracking-widest px-2.5 py-1 rounded-full uppercase mb-3"
                  style={{ color: cfg.color, background: cfg.bg }}
                >
                  <Icon size={9} />{cfg.label}
                </span>
                <h3 className="font-serif font-semibold text-sm leading-snug text-ink-primary mb-2">
                  {item.headline}
                </h3>
                <p className="font-sans text-xs leading-relaxed text-ink-muted">{item.insight}</p>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </section>
  )
}
