import { useState, useEffect } from 'react';
import { FileSearch, Search, BookOpen, FileText, BookMarked, Briefcase, ExternalLink, TrendingUp, AlertCircle } from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import { searchDocuments, listDocuments } from '../../services/api';

const docCategories = [
  { key: '',            label: 'All',               icon: FileSearch },
  { key: 'Syllabus',    label: 'Syllabus',           icon: BookOpen },
  { key: 'ExamRules',   label: 'Exam Rules',         icon: FileText },
  { key: 'Scholarship', label: 'Scholarship',        icon: BookMarked },
  { key: 'Placement',   label: 'Placement Policies', icon: Briefcase },
];

function ScoreBar({ score }) {
  const pct = Math.min(100, Math.round((score || 0) * 100));
  const color = pct >= 70 ? '#10b981' : pct >= 40 ? '#f59e0b' : '#64748b';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <div style={{ flex: 1, height: 6, background: '#f1f5f9', borderRadius: 3, maxWidth: 80 }}>
        <div style={{ height: '100%', width: `${pct}%`, background: color, borderRadius: 3, transition: 'width 0.5s ease' }} />
      </div>
      <span style={{ fontSize: 12, fontWeight: 600, color }}>{pct}%</span>
    </div>
  );
}

export default function DocumentSearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [docLoading, setDocLoading] = useState(true);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    listDocuments()
      .then(d => setDocs(Array.isArray(d) ? d : (d.data || [])))
      .catch(() => {})
      .finally(() => setDocLoading(false));
  }, []);

  const handleSearch = async (q) => {
    const searchQ = q || query;
    if (!searchQ.trim()) return;
    setLoading(true); setError(''); setResults([]); setSearched(true);
    try {
      const data = await searchDocuments(searchQ.trim(), 8);
      setResults(data.results || []);
      if (!data.results?.length) {
        setError('No documents matched your query. Try different keywords.');
      }
    } catch {
      setError('Document search failed. The search engine may not be initialized.');
    } finally {
      setLoading(false);
    }
  };

  const suggestions = [
    'Exam attendance requirements', 'Scholarship eligibility criteria',
    'Syllabus for Computer Science', 'Placement policy', 'Fee payment rules',
  ];

  return (
    <DashboardLayout role="admin">
      <div style={{ padding: '28px 32px' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 24 }}>
          <div style={{ width: 46, height: 46, borderRadius: 14, background: 'linear-gradient(135deg, #7c3aed, #4f46e5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <FileSearch size={24} color="white" />
          </div>
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)' }}>Document Search</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Search exam rules, syllabus, scholarship guidelines, and placement policies</p>
          </div>
        </div>

        {/* Search box */}
        <div className="card" style={{ padding: 24, marginBottom: 24 }}>
          <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
            <div style={{ flex: 1, position: 'relative' }}>
              <Search size={18} color="var(--text-muted)" style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)' }} />
              <input
                id="doc-search-input"
                className="input"
                style={{ paddingLeft: 44 }}
                placeholder="Search documents, policies, guidelines…"
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <button
              id="doc-search-btn"
              className="btn btn-primary"
              onClick={() => handleSearch()}
              disabled={loading || !query.trim()}
            >
              {loading ? <span className="spinner" style={{ width: 16, height: 16 }} /> : <Search size={16} />}
              Search
            </button>
          </div>

          {/* Suggestion pills */}
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <span style={{ fontSize: 12, color: 'var(--text-muted)', alignSelf: 'center', fontWeight: 500 }}>Try:</span>
            {suggestions.map(s => (
              <button
                key={s}
                onClick={() => { setQuery(s); handleSearch(s); }}
                style={{
                  padding: '4px 12px', borderRadius: 99, border: '1px solid var(--border)',
                  background: 'white', cursor: 'pointer', fontSize: 12, color: 'var(--text-secondary)',
                  transition: 'all 0.15s',
                }}
                onMouseEnter={e => { e.target.style.background = '#eff6ff'; e.target.style.color = 'var(--primary)'; e.target.style.borderColor = '#bfdbfe'; }}
                onMouseLeave={e => { e.target.style.background = 'white'; e.target.style.color = 'var(--text-secondary)'; e.target.style.borderColor = 'var(--border)'; }}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        {/* Results or document list */}
        {error && <Alert type={results.length ? 'info' : 'warning'} message={error} style={{ marginBottom: 20 }} />}

        {loading && <LoadingSpinner message="Searching documents…" />}

        {!loading && searched && results.length > 0 && (
          <div>
            <p style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 16 }}>{results.length} results for "<strong>{query}</strong>"</p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              {results.map((r, i) => (
                <div key={i} className="card animate-fade-in" style={{ padding: 22 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
                    <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                      <div style={{ width: 36, height: 36, borderRadius: 10, background: '#ede9fe', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, marginTop: 2 }}>
                        <FileText size={18} color="#7c3aed" />
                      </div>
                      <div>
                        <p style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 2 }}>{r.document_title || r.title || 'Document'}</p>
                        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                          {r.category && <span className="badge badge-purple">{r.category}</span>}
                          {r.chunk_index !== undefined && <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>Section {r.chunk_index + 1}</span>}
                        </div>
                      </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
                      <div>
                        <p style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 3, textAlign: 'right' }}>Relevance</p>
                        <ScoreBar score={r.score} />
                      </div>
                    </div>
                  </div>
                  <div style={{ padding: '12px 16px', background: '#f8fafc', borderRadius: 'var(--radius)', borderLeft: '3px solid #7c3aed', fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.7 }}>
                    {r.text || r.content || r.paragraph || 'No excerpt available.'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Document list */}
        {!searched && (
          <div className="card" style={{ padding: 24 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 20 }}>
              <TrendingUp size={18} color="var(--primary)" />
              <p style={{ fontWeight: 700, color: 'var(--text-primary)' }}>Available Documents</p>
            </div>
            {docLoading ? <LoadingSpinner message="Loading documents…" /> : docs.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-muted)' }}>
                <AlertCircle size={40} color="#cbd5e1" style={{ marginBottom: 12 }} />
                <p style={{ fontWeight: 500 }}>No documents found</p>
                <p style={{ fontSize: 13, marginTop: 4 }}>Upload documents through the backend admin panel.</p>
              </div>
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Document Title</th>
                      <th>Category</th>
                      <th>Uploaded</th>
                    </tr>
                  </thead>
                  <tbody>
                    {docs.map((d, i) => (
                      <tr key={i}>
                        <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{d.title}</td>
                        <td><span className="badge badge-purple">{d.category}</span></td>
                        <td style={{ fontSize: 13, color: 'var(--text-muted)' }}>{d.uploaded_date ? new Date(d.uploaded_date).toLocaleDateString('en-IN') : '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
