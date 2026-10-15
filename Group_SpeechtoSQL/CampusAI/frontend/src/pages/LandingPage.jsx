import { useNavigate } from 'react-router-dom';
import {
  Brain, GraduationCap, Users, Mic, BarChart3,
  FileSearch, ChevronRight, Shield, Zap, Globe,
  BookOpen, Award, ArrowRight,
} from 'lucide-react';

const features = [
  { icon: Mic,       title: 'Voice-Powered Queries', desc: 'Ask questions naturally using your voice — our AI understands and responds instantly.' },
  { icon: BarChart3, title: 'Real-Time Analytics',   desc: 'Get live insights on attendance, CGPA, fees, and department statistics at a glance.' },
  { icon: FileSearch,title: 'Smart Document Search', desc: 'Find relevant policies, syllabus, and guidelines using AI-powered semantic search.' },
  { icon: Award,     title: 'Scholarship Tracker',   desc: 'Discover and track scholarship opportunities based on student eligibility automatically.' },
  { icon: Shield,    title: 'Role-Based Access',      desc: 'Separate, secure dashboards for admin/faculty and students with appropriate data views.' },
  { icon: Zap,       title: 'Instant SQL Generation', desc: 'Natural language is converted into precise SQL queries in milliseconds by the AI engine.' },
];

const stats = [
  { value: '5000+', label: 'Students Managed' },
  { value: '12',    label: 'Departments' },
  { value: '98%',   label: 'Query Accuracy' },
  { value: '< 1s',  label: 'Response Time' },
];

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div style={{ fontFamily: 'var(--font-sans)', background: 'white', overflowX: 'hidden' }}>
      {/* ── HEADER ── */}
      <header style={{
        position: 'sticky', top: 0, zIndex: 50,
        background: 'rgba(255,255,255,0.92)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid var(--border)',
        padding: '0 40px',
      }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', display: 'flex', alignItems: 'center', height: 64 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{
              width: 36, height: 36,
              background: 'linear-gradient(135deg, var(--primary), var(--teal))',
              borderRadius: 10,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <Brain size={20} color="white" />
            </div>
            <span style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 20, color: 'var(--primary-dark)' }}>CampusAI</span>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: 12, alignItems: 'center' }}>
            <button
              id="header-admin-login-btn"
              onClick={() => navigate('/login?role=admin')}
              className="btn btn-outline btn-sm"
            >
              Admin / Faculty
            </button>
            <button
              id="header-student-login-btn"
              onClick={() => navigate('/login?role=student')}
              className="btn btn-primary btn-sm"
            >
              Student Login
            </button>
          </div>
        </div>
      </header>

      {/* ── HERO ── */}
      <section style={{
        minHeight: '92vh',
        display: 'flex', alignItems: 'center',
        background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 30%, #f0fdf4 60%, #eff6ff 100%)',
        padding: '60px 40px',
        position: 'relative',
        overflow: 'hidden',
      }}>
        {/* Decorative blobs */}
        <div style={{
          position: 'absolute', width: 600, height: 600,
          background: 'radial-gradient(circle, rgba(30,64,175,0.08) 0%, transparent 70%)',
          top: -200, left: -200, borderRadius: '50%',
        }} />
        <div style={{
          position: 'absolute', width: 500, height: 500,
          background: 'radial-gradient(circle, rgba(13,148,136,0.08) 0%, transparent 70%)',
          bottom: -150, right: -100, borderRadius: '50%',
        }} />

        <div style={{ maxWidth: 1200, margin: '0 auto', width: '100%', display: 'flex', gap: 60, alignItems: 'center', position: 'relative', zIndex: 1 }}>
          {/* Left: Text */}
          <div style={{ flex: 1 }} className="animate-fade-in">
            {/* Badge */}
            <div style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              padding: '6px 16px',
              background: 'linear-gradient(135deg, #dbeafe, #ccfbf1)',
              borderRadius: 99,
              marginBottom: 24,
              border: '1px solid #bfdbfe',
            }}>
              <Globe size={14} color="var(--primary)" />
              <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--primary)' }}>AI-Powered College ERP</span>
            </div>

            <h1 style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(38px, 5vw, 64px)',
              fontWeight: 800,
              lineHeight: 1.1,
              letterSpacing: '-1.5px',
              marginBottom: 24,
              color: 'var(--text-primary)',
            }}>
              Manage Campus with<br />
              <span style={{
                background: 'linear-gradient(135deg, var(--primary), var(--teal))',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}>
                Intelligent AI
              </span>
            </h1>

            <p style={{
              fontSize: 18, color: 'var(--text-secondary)',
              lineHeight: 1.7, marginBottom: 40,
              maxWidth: 520,
            }}>
              CampusAI transforms how colleges manage academic data. Ask questions in plain language, get instant answers, and discover insights — all with your voice.
            </p>

            {/* CTA Buttons */}
            <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
              <button
                id="hero-admin-btn"
                onClick={() => navigate('/login?role=admin')}
                className="btn btn-primary btn-lg"
                style={{ gap: 10 }}
              >
                <Shield size={18} />
                Admin / Faculty Login
                <ArrowRight size={16} />
              </button>
              <button
                id="hero-student-btn"
                onClick={() => navigate('/login?role=student')}
                className="btn btn-teal btn-lg"
                style={{ gap: 10 }}
              >
                <GraduationCap size={18} />
                Student Login
                <ArrowRight size={16} />
              </button>
            </div>

            {/* Micro stat pills */}
            <div style={{ display: 'flex', gap: 20, marginTop: 40, flexWrap: 'wrap' }}>
              {[
                { val: '5k+', lab: 'Students' },
                { val: '12', lab: 'Departments' },
                { val: '< 1s', lab: 'AI Response' },
              ].map(({ val, lab }) => (
                <div key={lab} style={{ textAlign: 'center' }}>
                  <p style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 22, color: 'var(--primary)' }}>{val}</p>
                  <p style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 500 }}>{lab}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right: Visual card */}
          <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }} className="animate-float">
            <div style={{
              width: '100%', maxWidth: 420,
              background: 'white',
              borderRadius: 24,
              padding: 32,
              boxShadow: '0 30px 60px rgba(30,64,175,0.15), 0 10px 20px rgba(13,148,136,0.1)',
              border: '1px solid rgba(30,64,175,0.1)',
            }}>
              {/* Mock query interface */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 24 }}>
                <div style={{
                  width: 44, height: 44,
                  background: 'linear-gradient(135deg, var(--primary), var(--teal))',
                  borderRadius: 12,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>
                  <Brain size={24} color="white" />
                </div>
                <div>
                  <p style={{ fontWeight: 700, color: 'var(--text-primary)' }}>AI Query Assistant</p>
                  <p style={{ fontSize: 12, color: 'var(--success)' }}>● Active</p>
                </div>
              </div>

              {/* Mock voice query */}
              <div style={{ padding: '14px 16px', background: '#f0f9ff', borderRadius: 12, marginBottom: 12, border: '1px solid #bfdbfe' }}>
                <p style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 4 }}>🎤 Voice Query</p>
                <p style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: 15 }}>"Show students with attendance below 75%"</p>
              </div>

              {/* Mock SQL output */}
              <div style={{ padding: '12px 14px', background: '#0f172a', borderRadius: 10, marginBottom: 12 }}>
                <p style={{ fontSize: 11, color: '#64748b', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Generated SQL</p>
                <code style={{ color: '#7dd3fc', fontSize: 12, fontFamily: 'monospace' }}>
                  SELECT * FROM students<br/>
                  WHERE attendance &lt; 75
                </code>
              </div>

              {/* Mock result */}
              <div style={{ padding: '12px 16px', background: '#f0fdf4', borderRadius: 10, border: '1px solid #bbf7d0' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--success)' }} />
                  <p style={{ fontSize: 12, fontWeight: 600, color: '#15803d' }}>AI Insight</p>
                </div>
                <p style={{ fontSize: 13, color: '#166534' }}>18 students have attendance below 75%. CSE dept has the highest count (6 students).</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section style={{
        background: 'linear-gradient(135deg, var(--primary-dark), var(--primary), var(--teal-dark))',
        padding: '48px 40px',
      }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 32 }}>
          {stats.map(({ value, label }) => (
            <div key={label} style={{ textAlign: 'center' }}>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: 40, fontWeight: 800, color: 'white', lineHeight: 1 }}>{value}</p>
              <p style={{ color: 'rgba(255,255,255,0.7)', marginTop: 6, fontWeight: 500 }}>{label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── FEATURES ── */}
      <section style={{ padding: '80px 40px', background: 'white' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 56 }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '6px 16px', background: '#eff6ff', borderRadius: 99, marginBottom: 16, border: '1px solid #bfdbfe' }}>
              <Zap size={14} color="var(--primary)" />
              <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--primary)' }}>Core Features</span>
            </div>
            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 40, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 16 }}>
              Everything your campus needs
            </h2>
            <p style={{ fontSize: 17, color: 'var(--text-secondary)', maxWidth: 520, margin: '0 auto' }}>
              From voice queries to AI-powered analytics, CampusAI has all the tools to make campus management effortless.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24 }}>
            {features.map(({ icon: Icon, title, desc }) => (
              <div
                key={title}
                className="card"
                style={{ padding: 28, cursor: 'default' }}
              >
                <div style={{
                  width: 52, height: 52, borderRadius: 14,
                  background: 'linear-gradient(135deg, #eff6ff, #f0fdf4)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  marginBottom: 16,
                  border: '1px solid var(--border)',
                }}>
                  <Icon size={24} color="var(--primary)" />
                </div>
                <h3 style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 8, fontSize: 17 }}>{title}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: 14, lineHeight: 1.6 }}>{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section style={{ padding: '80px 40px', background: 'linear-gradient(135deg, #f8fafc, #f0f9ff)' }}>
        <div style={{ maxWidth: 900, margin: '0 auto', textAlign: 'center' }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 36, fontWeight: 800, marginBottom: 48, color: 'var(--text-primary)' }}>
            How CampusAI Works
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 32 }}>
            {[
              { step: '01', title: 'Speak or Type', desc: 'Ask your question using voice or text in plain English or regional language.' },
              { step: '02', title: 'AI Processes',   desc: 'Our NLP engine understands intent and generates an optimized SQL query instantly.' },
              { step: '03', title: 'Get Insights',   desc: 'View results in a structured table with an AI-generated insight summary.' },
            ].map(({ step, title, desc }) => (
              <div key={step} style={{ textAlign: 'center', padding: 24 }}>
                <div style={{
                  width: 56, height: 56, borderRadius: '50%', margin: '0 auto 16px',
                  background: 'linear-gradient(135deg, var(--primary), var(--teal))',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  color: 'white', fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 18,
                }}>
                  {step}
                </div>
                <h3 style={{ fontWeight: 700, marginBottom: 8, color: 'var(--text-primary)' }}>{title}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: 14, lineHeight: 1.6 }}>{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section style={{
        padding: '80px 40px',
        background: 'linear-gradient(135deg, var(--primary-dark), var(--primary), var(--teal-dark))',
        textAlign: 'center',
      }}>
        <div style={{ maxWidth: 700, margin: '0 auto' }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 40, fontWeight: 800, color: 'white', marginBottom: 16 }}>
            Ready to transform your campus?
          </h2>
          <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: 17, marginBottom: 40 }}>
            Choose your role and get started with CampusAI today.
          </p>
          <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              id="cta-admin-btn"
              onClick={() => navigate('/login?role=admin')}
              style={{
                padding: '14px 32px', borderRadius: 'var(--radius-lg)',
                background: 'white', color: 'var(--primary-dark)',
                fontWeight: 700, fontSize: 16, border: 'none', cursor: 'pointer',
                display: 'flex', alignItems: 'center', gap: 10,
                boxShadow: '0 4px 20px rgba(0,0,0,0.2)',
                transition: 'transform 0.2s',
              }}
              onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-2px)'}
              onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
            >
              <Shield size={18} /> Admin / Faculty Login
            </button>
            <button
              id="cta-student-btn"
              onClick={() => navigate('/login?role=student')}
              style={{
                padding: '14px 32px', borderRadius: 'var(--radius-lg)',
                background: 'rgba(255,255,255,0.15)',
                color: 'white',
                fontWeight: 700, fontSize: 16,
                border: '2px solid rgba(255,255,255,0.4)',
                cursor: 'pointer',
                display: 'flex', alignItems: 'center', gap: 10,
                backdropFilter: 'blur(8px)',
                transition: 'all 0.2s',
              }}
              onMouseEnter={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.25)'; e.currentTarget.style.transform = 'translateY(-2px)'; }}
              onMouseLeave={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.15)'; e.currentTarget.style.transform = 'translateY(0)'; }}
            >
              <GraduationCap size={18} /> Student Login
            </button>
          </div>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer style={{ padding: '32px 40px', background: 'var(--text-primary)', color: 'rgba(255,255,255,0.5)', textAlign: 'center', fontSize: 14 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center', marginBottom: 8 }}>
          <Brain size={16} color="var(--teal-light)" />
          <span style={{ color: 'white', fontWeight: 700 }}>CampusAI</span>
          <span>— Intelligent Voice-Based College ERP Assistant</span>
        </div>
        <p>© {new Date().getFullYear()} CampusAI. All rights reserved.</p>
      </footer>
    </div>
  );
}
