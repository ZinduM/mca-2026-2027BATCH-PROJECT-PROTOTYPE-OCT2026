import { useState } from 'react';
import { Bot, Lightbulb } from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import VoiceInput from '../../components/VoiceInput';
import QueryResult from '../../components/QueryResult';
import Alert from '../../components/Alert';
import { useAuth } from '../../hooks/useAuth';
import { processQuery } from '../../services/api';

const studentSampleQueries = [
  { text: 'Show my attendance', icon: '📊' },
  { text: 'Show my semester results', icon: '📚' },
  { text: 'Show my pending fees', icon: '💰' },
  { text: 'Show my scholarship status', icon: '🏆' },
  { text: 'What is my CGPA?', icon: '🎓' },
  { text: 'Which subjects have low attendance?', icon: '⚠️' },
];

export default function StudentQueryPage() {
  const { user } = useAuth();
  const studentId = user?.student_id || user?.user_id;

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleQuery = async (query) => {
    setLoading(true); setError(''); setResult(null);
    try {
      const data = await processQuery(query, studentId);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Query failed. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout role="student">
      <div style={{ padding: '28px 32px', maxWidth: 900, margin: '0 auto', width: '100%' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 8 }}>
          <div style={{ width: 46, height: 46, borderRadius: 14, background: 'linear-gradient(135deg, var(--teal-dark), var(--teal-light))', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Bot size={24} color="white" />
          </div>
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)' }}>AI Query Assistant</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Ask about your academics, attendance, fees, or scholarships</p>
          </div>
        </div>

        <div style={{ height: 1, background: 'var(--border)', margin: '20px 0 28px' }} />

        {/* Info notice */}
        <div style={{
          padding: '12px 18px', marginBottom: 20,
          background: '#f0fdf4', borderRadius: 'var(--radius)', border: '1px solid #bbf7d0',
          display: 'flex', gap: 10, alignItems: 'center', fontSize: 13, color: '#15803d',
        }}>
          <Lightbulb size={16} />
          <span>Your queries are automatically scoped to your student ID — you can only see your own data.</span>
        </div>

        {/* Voice Input */}
        <div className="card" style={{ padding: 28, marginBottom: 24 }}>
          <VoiceInput
            onSubmit={handleQuery}
            isLoading={loading}
            placeholder="e.g. Show my attendance this semester…"
          />
        </div>

        {error && <Alert type="error" message={error} style={{ marginBottom: 20 }} />}

        {/* Result */}
        {(result || loading) && (
          <div style={{ marginBottom: 24 }}>
            {loading ? (
              <div className="card" style={{ padding: 40, textAlign: 'center' }}>
                <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 16 }}>
                  {[0,1,2].map(i => (
                    <div key={i} style={{
                      width: 10, height: 10, borderRadius: '50%', background: 'var(--teal)',
                      margin: '0 4px',
                      animation: `bounce-dots 0.8s ease ${i * 0.15}s infinite`,
                    }} />
                  ))}
                </div>
                <p style={{ color: 'var(--text-muted)', fontWeight: 500 }}>Processing your query…</p>
              </div>
            ) : (
              <QueryResult result={result} onRecommendedQuery={handleQuery} />
            )}
          </div>
        )}

        {/* Sample Queries */}
        {!result && !loading && (
          <div className="card" style={{ padding: 24 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
              <Lightbulb size={18} color="var(--teal)" />
              <p style={{ fontWeight: 700, color: 'var(--text-primary)' }}>Try asking…</p>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 10 }}>
              {studentSampleQueries.map(({ text, icon }) => (
                <button
                  key={text}
                  onClick={() => handleQuery(text)}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 10,
                    padding: '12px 16px',
                    background: 'var(--bg)',
                    border: '1.5px solid var(--border)',
                    borderRadius: 'var(--radius)',
                    cursor: 'pointer',
                    fontSize: 13, fontWeight: 500,
                    color: 'var(--text-secondary)',
                    textAlign: 'left',
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--teal)'; e.currentTarget.style.background = '#f0fdfa'; e.currentTarget.style.color = 'var(--teal-dark)'; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.background = 'var(--bg)'; e.currentTarget.style.color = 'var(--text-secondary)'; }}
                >
                  <span style={{ fontSize: 18 }}>{icon}</span>
                  {text}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
