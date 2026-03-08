import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import clsx from 'clsx'

const sections = [
  { id: 'top-stories', label: 'Top Stories' },
  { id: 'tech',        label: 'Tech',        color: '#6B9FD4' },
  { id: 'fashion',     label: 'Fashion',     color: '#C97A96' },
  { id: 'wellness',    label: 'Wellness',    color: '#6BAF94' },
  { id: 'watching',    label: 'Watching' },
  { id: 'content',     label: 'For Content' },
]

export default function TopicsNav() {
  const [active, setActive] = useState('top-stories')
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const onScroll = () => {
      setVisible(window.scrollY > 320)
      for (const sec of [...sections].reverse()) {
        const el = document.getElementById(sec.id)
        if (el && window.scrollY >= el.offsetTop - 120) {
          setActive(sec.id)
          break
        }
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const scrollTo = (id: string) =>
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })

  return (
    <motion.nav
      initial={{ y: -48, opacity: 0 }}
      animate={{ y: visible ? 0 : -48, opacity: visible ? 1 : 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="fixed top-[2px] left-0 right-0 z-40 flex justify-center"
    >
      <div
        className="flex items-center gap-1 px-4 py-2 mt-2 rounded-full border"
        style={{
          background: 'rgba(250,249,245,0.92)',
          backdropFilter: 'blur(20px)',
          borderColor: 'rgba(0,0,0,0.08)',
          boxShadow: '0 4px 24px rgba(0,0,0,0.06)',
        }}
      >
        {sections.map((sec) => (
          <button
            key={sec.id}
            onClick={() => scrollTo(sec.id)}
            className={clsx(
              'relative px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200',
              active === sec.id ? 'text-ink-primary' : 'text-ink-muted hover:text-ink-secondary'
            )}
            style={{ color: active === sec.id && sec.color ? sec.color : undefined }}
          >
            {active === sec.id && (
              <motion.span
                layoutId="nav-pill"
                className="absolute inset-0 rounded-full"
                style={{ background: 'rgba(0,0,0,0.05)' }}
                transition={{ type: 'spring', stiffness: 400, damping: 35 }}
              />
            )}
            <span className="relative">{sec.label}</span>
          </button>
        ))}
      </div>
    </motion.nav>
  )
}
