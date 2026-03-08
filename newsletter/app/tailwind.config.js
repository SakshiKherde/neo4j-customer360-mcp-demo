/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        base:     '#FFFFFF',
        surface:  '#F8F8F8',
        elevated: '#F2F2F2',
        card:     '#FFFFFF',
        gold: {
          DEFAULT: '#B8906A',
          light:   '#D4B48C',
          dim:     'rgba(184,144,106,0.10)',
        },
        tech: {
          DEFAULT: '#6B9FD4',
          dim:     'rgba(107,159,212,0.10)',
          glow:    'rgba(107,159,212,0.16)',
        },
        fashion: {
          DEFAULT: '#C97A96',
          dim:     'rgba(201,122,150,0.10)',
          glow:    'rgba(201,122,150,0.16)',
        },
        wellness: {
          DEFAULT: '#6BAF94',
          dim:     'rgba(107,175,148,0.10)',
          glow:    'rgba(107,175,148,0.16)',
        },
        ink: {
          primary:   '#0F0E0C',
          secondary: '#2E2C28',
          muted:     '#5A5850',
        },
      },
      fontFamily: {
        serif: ['Playfair Display', 'Georgia', 'serif'],
        sans:  ['Inter', 'system-ui', 'sans-serif'],
        mono:  ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'pulse-gold': 'pulseGold 2s ease-in-out infinite',
      },
      keyframes: {
        pulseGold: {
          '0%, 100%': { opacity: '1' },
          '50%':      { opacity: '0.3' },
        },
      },
      boxShadow: {
        'card':      '0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04)',
        'card-hover':'0 4px 12px rgba(0,0,0,0.08), 0 16px 40px rgba(0,0,0,0.06)',
        'featured':  '0 2px 8px rgba(0,0,0,0.06), 0 20px 60px rgba(0,0,0,0.08)',
      },
    },
  },
  plugins: [],
}
