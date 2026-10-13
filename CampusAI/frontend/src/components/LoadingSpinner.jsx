import { Loader2 } from 'lucide-react';

export default function LoadingSpinner({ message = 'Loading…', fullPage = false }) {
  if (fullPage) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 16,
        background: 'var(--bg)',
      }}>
        <div style={{
          width: 60, height: 60,
          background: 'linear-gradient(135deg, var(--primary), var(--teal))',
          borderRadius: '50%',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <Loader2 size={28} color="white" style={{ animation: 'spin 1s linear infinite' }} />
        </div>
        <p style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>{message}</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '20px 0', justifyContent: 'center' }}>
      <Loader2 size={20} color="var(--primary)" style={{ animation: 'spin 1s linear infinite' }} />
      <span style={{ color: 'var(--text-secondary)', fontSize: 14 }}>{message}</span>
    </div>
  );
}
