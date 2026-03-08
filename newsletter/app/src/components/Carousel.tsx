import { useRef } from 'react'
import { motion } from 'framer-motion'
import { ChevronRight } from 'lucide-react'

interface Props {
  children: React.ReactNode[]
  label?: string
}

export default function Carousel({ children, label }: Props) {
  const ref = useRef<HTMLDivElement>(null)

  const scroll = () => {
    ref.current?.scrollBy({ left: 320, behavior: 'smooth' })
  }

  return (
    <div className="relative group">
      {/* Scroll button */}
      <button
        onClick={scroll}
        className="absolute right-0 top-1/2 -translate-y-1/2 z-10 w-8 h-8 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
        style={{ background: '#FFFFFF', boxShadow: '0 4px 16px rgba(0,0,0,0.12)' }}
      >
        <ChevronRight size={16} className="text-ink-secondary" />
      </button>

      {/* Right fade */}
      <div
        className="absolute right-0 top-0 bottom-0 w-16 z-[5] pointer-events-none"
        style={{ background: 'linear-gradient(to left, rgba(255,255,255,0.9), transparent)' }}
      />

      <div
        ref={ref}
        className="flex gap-3 overflow-x-auto pb-2"
        style={{
          scrollSnapType: 'x mandatory',
          WebkitOverflowScrolling: 'touch',
          scrollbarWidth: 'none',
          msOverflowStyle: 'none',
        }}
      >
        <style>{`.carousel-hide::-webkit-scrollbar { display: none; }`}</style>
        {children.map((child, i) => (
          <div key={i} style={{ scrollSnapAlign: 'start', flexShrink: 0 }}>
            {child}
          </div>
        ))}
        {/* Spacer for right fade */}
        <div style={{ flexShrink: 0, width: 32 }} />
      </div>
    </div>
  )
}
