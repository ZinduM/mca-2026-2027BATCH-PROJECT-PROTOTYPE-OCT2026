import { Link } from 'react-router-dom';
import { Brain, Home, ArrowLeft } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #f0f9ff, #e0f2fe, #f0fdf4)',
      padding: 40,
      textAlign: 'center',
    }}>
      <div style={{ width: 72, height: 72, borderRadius: '50%', background: 'linear-gradient(135deg, var(--primary), var(--teal))', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 24, animation: 'float 3s ease-in-out infinite' }}>
        <Brain size={36} color="white" />
      </div>
      <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 80, fontWeight: 800, background: 'linear-gradient(135deg, var(--primary), var(--teal))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', lineHeight: 1, marginBottom: 8 }}>404</h1>
      <h2 style={{ fontWeight: 700, fontSize: 24, color: 'var(--text-primary)', marginBottom: 12 }}>Page Not Found</h2>
      <p style={{ color: 'var(--text-secondary)', fontSize: 16, marginBottom: 32, maxWidth: 400 }}>The page you're looking for doesn't exist or has been moved.</p>
      <div style={{ display: 'flex', gap: 12 }}>
        <Link to="/" className="btn btn-primary" style={{ gap: 8, textDecoration: 'none' }}>
          <Home size={16} /> Back to Home
        </Link>
        <button onClick={() => window.history.back()} className="btn btn-outline" style={{ gap: 8 }}>
          <ArrowLeft size={16} /> Go Back
        </button>
      </div>
    </div>
  );
}
