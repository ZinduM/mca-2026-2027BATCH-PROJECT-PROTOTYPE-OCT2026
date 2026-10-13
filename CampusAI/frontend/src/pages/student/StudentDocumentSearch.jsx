import { useState, useEffect } from 'react';
import { FileSearch, Search, AlertCircle } from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import { searchDocuments } from '../../services/api';

function ScoreBar({ score }) {
  const pct = Math.min(100, Math.round((score || 0) * 100));
  const color = pct >= 70 ? '#10b981' : pct >= 40 ? '#f59e0b' : '#64748b';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <div style={{ flex: 1, height: 6, background: '#f1f5f9', borderRadius: 3, maxWidth: 80 }}>
        <div style={{ height: '100%', width: `${pct}%`, background: color, borderRadius: 3 }} />
      </div>
      <span style={{ fontSize: 12, fontWeight: 600, color }}>{pct}%</span>
    </div>
  );
}

export default function StudentDocumentSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);

  const handleSearch = async (q) => {
    const sq = q || query;
    if (!sq.trim()) return;
    setLoading(true); setError(''); setResults([]); setSearched(true);
    try {
      const data = await searchDocuments(sq.trim(), 8);
      setResults(data.results || []);
      if (!data.results?.length) setError('No results found. Try different keywords.');
    } catch {
      setError('Document search is not available right now.');
    } finally {
      setLoading(false);
    }
  };

  const suggestions = ['Exam rules', 'Scholarship criteria', 'Attendance policy', 'Placement guidelines'];

  return (
    <DashboardLayout role="student">
      <div style={{ padding: '28px 32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 24 }}>
          <div style={{ width: 46, height: 46, borderRadius: 14, background: 'linear-gradient(135deg, #7c3aed, #4f46e5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <FileSearch size={24} color="white" />
          </div>
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)' }}>Document Search</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Search campus documents, policies, and guidelines</p>
          </div>
        </div>

        <div className="card" style={{ padding: 24, marginBottom: 24 }}>
          <div style={{ display: 'flex', gap: 12, marginBottom: 14 }}>
            <div style={{ flex: 1, position: 'relative' }}>
              <Search size={17} color="var(--text-muted)" style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)' }} />
              <input
                id="student-doc-search"
                className="input"
                style={{ paddingLeft: 44 }}
                placeholder="Search exam rules, syllabus, guidelines…"
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <button className="btn btn-primary" onClick={() => handleSearch()} disabled={loading || !query.trim()}>
              {loading ? <span className="spinner" style={{ width: 16, height: 16 }} /> : <Search size={16} />} Search
            </button>
          </div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <span style={{ fontSize: 12, color: 'var(--text-muted)', alignSelf: 'center' }}>Try:</span>
            {suggestions.map(s => (
              <button key={s} onClick={() => { setQuery(s); handleSearch(s); }}
                style={{ padding: '4px 12px', borderRadius: 99, border: '1px solid var(--border)', background: 'white', cursor: 'pointer', fontSize: 12, color: 'var(--text-secondary)', transition: 'all 0.15s' }}
                onMouseEnter={e => { e.target.style.background = '#eff6ff'; e.target.style.color = 'var(--primary)'; }}
                onMouseLeave={e => { e.target.style.background = 'white'; e.target.style.color = 'var(--text-secondary)'; }}
              >{s}</button>
            ))}
          </div>
        </div>

        {error && <Alert type="warning" message={error} style={{ marginBottom: 20 }} />}
        {loading && <LoadingSpinner message="Searching…" />}

        {!loading && results.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {results.map((r, i) => (
              <div key={i} className="card animate-fade-in" style={{ padding: 20 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
                  <div>
                    <p style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 4 }}>{r.document_title || r.title || 'Document'}</p>
                    {r.category && <span className="badge badge-purple">{r.category}</span>}
                  </div>
                  <div>
                    <p style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>Relevance</p>
                    <ScoreBar score={r.score} />
                  </div>
                </div>
                <div style={{ padding: '10px 14px', background: '#f8fafc', borderRadius: 'var(--radius)', borderLeft: '3px solid #7c3aed', fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.65 }}>
                  {r.text || r.content || r.paragraph || 'No excerpt available.'}
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && !searched && (
          <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>
            <FileSearch size={56} color="#cbd5e1" style={{ marginBottom: 16 }} />
            <p style={{ fontWeight: 600, fontSize: 16 }}>Search campus documents</p>
            <p style={{ fontSize: 14, marginTop: 6, maxWidth: 400, margin: '8px auto 0' }}>Use the search bar above to find exam rules, syllabus, scholarship guidelines, and placement policies.</p>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
