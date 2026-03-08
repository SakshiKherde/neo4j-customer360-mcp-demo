import { motion } from 'framer-motion'
import ReadingProgress from './components/ReadingProgress'
import TopicsNav from './components/TopicsNav'
import Hero from './components/Hero'
import FeaturedStory from './components/FeaturedStory'
import CarouselStoryCard from './components/CarouselStoryCard'
import Carousel from './components/Carousel'
import SectionRail from './components/SectionRail'
import WorthWatching from './components/WorthWatching'
import ForContent from './components/ForContent'
import ConversationStarter from './components/ConversationStarter'
import { mockData } from './data/mockData'

export default function App() {
  return (
    <div className="min-h-screen bg-white text-ink-primary">
      <ReadingProgress />
      <TopicsNav />

      <main className="max-w-3xl mx-auto px-5 md:px-8">
        {/* Hero */}
        <Hero data={mockData} />

        {/* ── Top Stories ── */}
        <section id="top-stories" className="mt-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
            className="flex items-center gap-3 mb-5"
          >
            <span className="text-2xl w-10 h-10 rounded-2xl flex items-center justify-center"
                  style={{ background: 'rgba(184,144,106,0.08)' }}>★</span>
            <div>
              <p className="font-mono text-[9px] tracking-widest text-ink-muted uppercase mb-0.5">01</p>
              <h2 className="font-serif font-bold text-2xl text-ink-primary leading-none">Top Stories</h2>
            </div>
          </motion.div>

          {/* Featured */}
          <FeaturedStory story={mockData.topStories[0]} />

          {/* Rest as horizontal carousel */}
          <div className="mt-4">
            <Carousel>
              {mockData.topStories.slice(1).map((story, i) => (
                <CarouselStoryCard key={i} story={story} index={i + 2} width={290} />
              ))}
            </Carousel>
          </div>
        </section>

        {/* ── Section rails ── */}
        {mockData.sections.map((section, i) => (
          <SectionRail
            key={section.name}
            section={section}
            number={String(i + 2).padStart(2, '0')}
          />
        ))}

        {/* ── Worth Watching ── */}
        <WorthWatching items={mockData.worthWatching} />

        {/* ── For Content ── */}
        <ForContent items={mockData.forContent} />

        {/* ── Conversation Starter ── */}
        <ConversationStarter data={mockData.conversationStarter} />

        {/* Footer */}
        <footer className="mt-16 pb-12 pt-8 border-t" style={{ borderColor: 'rgba(0,0,0,0.07)' }}>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-serif font-semibold text-sm text-gold mb-0.5">The Daily Brief</p>
              <p className="font-mono text-[10px] text-ink-muted">{mockData.date}</p>
            </div>
            <div className="flex gap-1.5">
              {['⚡ Tech', '✦ Fashion', '◎ Wellness', '◈ Finance'].map((s) => (
                <span key={s} className="font-mono text-[9px] px-2.5 py-1 rounded-full text-ink-muted"
                      style={{ background: 'rgba(0,0,0,0.04)' }}>{s}</span>
              ))}
            </div>
          </div>
        </footer>
      </main>
    </div>
  )
}
