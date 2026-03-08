import { useState } from 'react'
import { motion } from 'framer-motion'
import { Copy, Check } from 'lucide-react'

interface Props { data: { nugget: string; context: string } }

export default function ConversationStarter({ data }: Props) {
  const [copied, setCopied] = useState(false)

  const copy = () => {
    navigator.clipboard.writeText(`"${data.nugget}" — ${data.context}`)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className="mt-14 mb-8"
    >
      <div className="flex items-center gap-3 mb-6">
        <span className="text-2xl w-10 h-10 rounded-2xl flex items-center justify-center"
              style={{ background: 'rgba(184,144,106,0.08)' }}>💬</span>
        <div>
          <p className="font-mono text-[9px] tracking-widest text-ink-muted uppercase mb-0.5">07</p>
          <h2 className="font-serif font-bold text-2xl text-ink-primary leading-none">Drop This Today</h2>
        </div>
      </div>

      <div
        className="rounded-3xl overflow-hidden"
        style={{
          background: 'linear-gradient(135deg, #FDFCFA, #F9F5EE)',
          border: '1px solid rgba(184,144,106,0.2)',
          boxShadow: '0 4px 24px rgba(184,144,106,0.07)',
        }}
      >
        <div className="h-1.5" style={{ background: 'linear-gradient(90deg, #B8906A, #D4B48C)' }} />
        <div className="p-7 md:p-9">
          <div className="flex items-start justify-between gap-4 mb-5">
            <span
              className="font-mono text-[9px] font-bold tracking-widest px-3 py-1.5 rounded-full uppercase"
              style={{ color: '#B8906A', background: 'rgba(184,144,106,0.10)' }}
            >
              Conversation starter
            </span>
            <button
              onClick={copy}
              className="flex items-center gap-1.5 font-sans text-xs px-3 py-1.5 rounded-full border transition-all flex-shrink-0"
              style={{
                color: copied ? '#B8906A' : '#9C9A94',
                borderColor: copied ? 'rgba(184,144,106,0.4)' : 'rgba(0,0,0,0.1)',
                background: copied ? 'rgba(184,144,106,0.06)' : 'transparent',
              }}
            >
              {copied ? <Check size={12} /> : <Copy size={12} />}
              {copied ? 'Copied' : 'Copy'}
            </button>
          </div>

          <blockquote className="mb-5">
            <p
              className="font-serif font-bold leading-snug text-ink-primary"
              style={{ fontSize: 'clamp(1.1rem, 2.5vw, 1.5rem)' }}
            >
              "{data.nugget}"
            </p>
          </blockquote>

          <p
            className="font-sans text-sm text-ink-muted pt-5 border-t"
            style={{ borderColor: 'rgba(184,144,106,0.12)' }}
          >
            {data.context}
          </p>
        </div>
      </div>
    </motion.section>
  )
}
