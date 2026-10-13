import { useState, useEffect } from 'react';
import { Bot, Lightbulb, Tag } from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import VoiceInput from '../../components/VoiceInput';
import QueryResult from '../../components/QueryResult';
import Alert from '../../components/Alert';
import { processQuery, getSampleQueries } from '../../services/api';

const categoryColors = {
  Academic:    { bg: '#dbeafe', text: '#1e40af' },
  Attendance:  { bg: '#ccfbf1', text: '#0f766e' },
  Department:  { bg: '#ede9fe', text: '#7c3aed' },
  Scholarship: { bg: '#fef3c7', text: '#92400e' },
  Finance:     { bg: '#fee2e2', text: '#991b1b' },
  Comparison:  { bg: '#e0f2fe', text: '#0369a1' },
  Count:       { bg: '#fce7f3', text: '#9d174d' },
  Internship:  { bg: '#d1fae5', text: '#065f46' },
  Demographics:{ bg: '#fdf4ff', text: '#6d28d9' },
};

export default function AdminQueryPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [sampleQueries, setSampleQueries] = useState([]);

  useEffect(() => {
    getSampleQueries()
      .then(d => setSampleQueries(d.queries || []))
      .catch(() => {});
  }, []);

  const handleQuery = async (query) => {
    setLoading(true); setError(''); setResult(null);
    try {
      const data = await processQuery(query);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Query failed. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout role="admin">
      <div style={{ padding: '28px 32px', maxWidth: 960, margin: '0 auto', width: '100%' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 8 }}>
          <div style={{ width: 46, height: 46, borderRadius: 14, background: 'linear-gradient(135deg, var(--primary), var(--teal))', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Bot size={24} color="white" />
          </div>
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)' }}>AI Query Assistant</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Ask anything about your campus data using voice or text</p>
          </div>
        </div>

        <div style={{ height: 1, background: 'var(--border)', margin: '20px 0 28px' }} />

        {/* Voice Input Card */}
        <div className="card" style={{ padding: 28, marginBottom: 24 }}>
          <VoiceInput
            onSubmit={handleQuery}
            isLoading={loading}
            placeholder="e.g. Show top 10 students based on CGPA…"
          />
        </div>

        {/* Error */}
        {error && <Alert type="error" message={error} style={{ marginBottom: 20 }} />}

        {/* Query Result */}
        {(result || loading) && (
          <div style={{ marginBottom: 24 }}>
            {loading ? (
              <div className="card" style={{ padding: 40, textAlign: 'center' }}>
                <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 16 }}>
                  {[0,1,2].map(i => (
                    <div key={i} style={{
                      width: 10, height: 10, borderRadius: '50%', background: 'var(--primary)',
                      margin: '0 4px',
                      animation: `bounce-dots 0.8s ease ${i * 0.15}s infinite`,
                    }} />
                  ))}
                </div>
                <p style={{ color: 'var(--text-muted)', fontWeight: 500 }}>Processing your query…</p>
                <p style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 4 }}>AI is analyzing and generating SQL</p>
              </div>
            ) : (
              <QueryResult result={result} onRecommendedQuery={handleQuery} />
            )}
          </div>
        )}

        {/* Sample Queries */}
        {!result && !loading && sampleQueries.length > 0 && (
          <div className="card" style={{ padding: 24 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
              <Lightbulb size={18} color="var(--primary)" />
              <p style={{ fontWeight: 700, color: 'var(--text-primary)' }}>Example Queries</p>
              <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>— Click to try</span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>
              {sampleQueries.map(({ text, category }) => {
                const c = categoryColors[category] || { bg: '#f1f5f9', text: '#475569' };
                return (
                  <button
                    key={text}
                    onClick={() => handleQuery(text)}
                    style={{
                      display: 'flex', alignItems: 'center', gap: 8,
                      padding: '8px 14px',
                      background: 'white',
                      border: '1.5px solid var(--border)',
                      borderRadius: 99,
                      cursor: 'pointer',
                      fontSize: 13, fontWeight: 500,
                      color: 'var(--text-secondary)',
                      transition: 'all 0.2s',
                    }}
                    onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--primary)'; e.currentTarget.style.color = 'var(--primary)'; }}
                    onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-secondary)'; }}
                  >
                    <span style={{ padding: '2px 8px', borderRadius: 99, fontSize: 11, fontWeight: 700, background: c.bg, color: c.text }}>
                      {category}
                    </span>
                    {text}
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
