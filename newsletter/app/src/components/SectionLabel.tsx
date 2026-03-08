import clsx from 'clsx'

const config = {
  Tech:     { color: '#2D6FA8', bg: 'rgba(45,111,168,0.10)'  },
  Fashion:  { color: '#A0405E', bg: 'rgba(160,64,94,0.10)'   },
  Wellness: { color: '#2A7A5A', bg: 'rgba(42,122,90,0.10)'   },
} as const

type SectionName = keyof typeof config

interface Props {
  section: SectionName | string
  size?: 'sm' | 'xs'
}

export default function SectionLabel({ section, size = 'xs' }: Props) {
  const c = config[section as SectionName] ?? { color: '#B8906A', bg: 'rgba(184,144,106,0.10)' }
  return (
    <span
      className={clsx(
        'inline-flex items-center font-mono font-semibold tracking-widest uppercase rounded-full',
        size === 'xs' ? 'text-[9px] px-2.5 py-1' : 'text-[10px] px-3 py-1.5'
      )}
      style={{ color: c.color, background: c.bg }}
    >
      {section}
    </span>
  )
}
