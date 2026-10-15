import { useState, useEffect, useCallback } from 'react';
import {
  GraduationCap,
  Briefcase,
  Search,
  ExternalLink,
  Award,
  MapPin,
  Calendar,
  DollarSign,
  Tag,
  Star,
  AlertCircle,
  Filter,
  Sparkles,
  Layers,
  Cpu,
  RefreshCw,
  Clock
} from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import {
  searchScholarshipsAdmin,
  searchInternshipsAdmin,
  listScholarships,
  listInternships
} from '../../services/api';

function MatchBadge({ score, percent }) {
  const p = percent || (typeof score === 'string' ? parseInt(score) : 80);
  let bg = '#dcfce7';
  let color = '#15803d';
  let border = '#bbf7d0';

  if (p < 70) {
    bg = '#fef3c7';
    color = '#92400e';
    border = '#fde68a';
  } else if (p < 85) {
    bg = '#e0f2fe';
    color = '#0369a1';
    border = '#bae6fd';
  }

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 4,
        padding: '3px 9px',
        borderRadius: 99,
        fontSize: 12,
        fontWeight: 700,
        background: bg,
        color: color,
        border: `1px solid ${border}`,
      }}
    >
      <Sparkles size={12} />
      {p}% Match
    </span>
  );
}

function ScholarshipCard({ item, rank }) {
  return (
    <div className="card animate-fade-in" style={{ padding: 22, position: 'relative', overflow: 'hidden', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        {/* Top Bar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 12 }}>
          <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', flex: 1 }}>
            <div style={{
              width: 44,
              height: 44,
              borderRadius: 12,
              background: 'linear-gradient(135deg, #fef3c7, #fde68a)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
              boxShadow: '0 2px 8px rgba(217, 119, 6, 0.15)'
            }}>
              <Award size={22} color="#d97706" />
            </div>
            <div>
              <h3 style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: 16, margin: 0, lineHeight: 1.35 }}>
                {item.scholarship_name || item.name || 'Scholarship'}
              </h3>
              <p style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 3 }}>
                Provider: <strong style={{ color: 'var(--text-secondary)' }}>{item.provider || 'State Government / AICTE'}</strong>
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
            {rank <= 5 && (
              <span style={{
                display: 'inline-flex', alignItems: 'center', gap: 3,
                padding: '2px 8px', borderRadius: 99, fontSize: 11, fontWeight: 700,
                background: rank === 1 ? '#fef3c7' : rank === 2 ? '#f1f5f9' : '#fff7ed',
                color: rank === 1 ? '#d97706' : rank === 2 ? '#475569' : '#c2410c',
                border: '1px solid rgba(0,0,0,0.06)'
              }}>
                <Star size={11} fill="currentColor" /> #{rank}
              </span>
            )}
            {item.relevance_score && (
              <MatchBadge score={item.relevance_score} percent={item.relevance_percent} />
            )}
          </div>
        </div>

        {/* Amount & Status Metadata */}
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', alignItems: 'center', marginBottom: 12 }}>
          {item.amount && (
            <div style={{
              display: 'flex', alignItems: 'center', gap: 4, fontSize: 14, fontWeight: 800,
              color: 'var(--teal-dark)', background: '#f0fdf4', padding: '3px 10px', borderRadius: 6, border: '1px solid #bbf7d0'
            }}>
              <DollarSign size={14} />
              ₹{Number(item.amount).toLocaleString('en-IN')}
            </div>
          )}

          {item.course && (
            <span style={{ fontSize: 11, fontWeight: 600, background: '#f1f5f9', color: '#475569', padding: '3px 8px', borderRadius: 4 }}>
              Target: {item.course}
            </span>
          )}

          {item.min_cgpa > 0 && (
            <span style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 3 }}>
              <GraduationCap size={13} /> Min CGPA: <strong>{item.min_cgpa}</strong>
            </span>
          )}

          <span style={{
            padding: '3px 8px', borderRadius: 6, fontSize: 11, fontWeight: 700,
            background: item.eligibility_status === 'Eligible' ? '#e0f2fe' : '#fef3c7',
            color: item.eligibility_status === 'Eligible' ? '#0369a1' : '#92400e'
          }}>
            {item.eligibility_status || 'Eligible'}
          </span>
        </div>

        {/* Excerpt / Criteria */}
        {(item.snippet || item.description || item.eligibility_criteria) && (
          <p style={{
            fontSize: 13,
            color: 'var(--text-secondary)',
            lineHeight: 1.55,
            marginBottom: 12,
            background: '#f8fafc',
            padding: '10px 12px',
            borderRadius: 8
          }}>
            {item.snippet || item.description || item.eligibility_criteria}
          </p>
        )}

        {/* Matched Terms */}
        {item.matched_terms && item.matched_terms.length > 0 && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap', marginBottom: 12 }}>
            <span style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 700 }}>MATCHED:</span>
            {item.matched_terms.map((t, idx) => (
              <span key={idx} style={{ fontSize: 11, background: '#fef3c7', color: '#92400e', padding: '1px 7px', borderRadius: 4, fontWeight: 600 }}>
                {t}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Footer Info */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: 10, borderTop: '1px solid var(--border)', fontSize: 12, color: 'var(--text-muted)' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <Clock size={13} /> Deadline: {item.deadline || '2026-11-30'}
        </span>
        <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>
          {item.student_name ? `Assigned: ${item.student_name}` : 'Open Catalog'}
        </span>
      </div>
    </div>
  );
}

function InternshipCard({ item, rank }) {
  return (
    <div className="card animate-fade-in" style={{ padding: 22, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        {/* Top Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 12 }}>
          <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', flex: 1 }}>
            <div style={{
              width: 44,
              height: 44,
              borderRadius: 12,
              background: 'linear-gradient(135deg, #e0f2fe, #bfdbfe)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0
            }}>
              <Briefcase size={22} color="var(--primary)" />
            </div>
            <div>
              <h3 style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: 16, margin: 0 }}>
                {item.role || item.title || 'Internship'}
              </h3>
              <p style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 3 }}>
                Company: <strong style={{ color: 'var(--text-secondary)' }}>{item.company_name || item.company}</strong> • Domain: <span style={{ color: 'var(--primary)' }}>{item.domain}</span>
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
            {item.stipend && (
              <div style={{ textAlign: 'right' }}>
                <p style={{ fontSize: 14, fontWeight: 800, color: 'var(--teal-dark)', margin: 0 }}>
                  ₹{Number(item.stipend).toLocaleString('en-IN')}/mo
                </p>
              </div>
            )}
            {item.relevance_score && (
              <MatchBadge score={item.relevance_score} percent={item.relevance_percent} />
            )}
          </div>
        </div>

        {/* Location & Duration */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, marginBottom: 12, alignItems: 'center' }}>
          {item.location && (
            <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, color: 'var(--text-muted)' }}>
              <MapPin size={13} /> {item.location}
            </span>
          )}
          {item.duration && (
            <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, color: 'var(--text-muted)' }}>
              <Calendar size={13} /> {item.duration}
            </span>
          )}
        </div>

        {/* Skills Required */}
        {item.skills_required && (
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 5 }}>
              Required Technical Skills:
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
              {item.skills_required.split(',').map((skill, i) => (
                <span key={i} style={{ fontSize: 11, background: '#f1f5f9', color: '#0369a1', padding: '2px 8px', borderRadius: 4, fontWeight: 600 }}>
                  {skill.trim()}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Description Snippet */}
        {(item.snippet || item.description) && (
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.55, marginBottom: 12, background: '#f8fafc', padding: '10px 12px', borderRadius: 8 }}>
            {item.snippet || item.description}
          </p>
        )}

        {item.eligibility && (
          <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 10, display: 'flex', gap: 4 }}>
            <Tag size={13} style={{ flexShrink: 0, marginTop: 2 }} />
            <span>Eligibility: {item.eligibility}</span>
          </div>
        )}
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: 10, borderTop: '1px solid var(--border)', fontSize: 12, color: 'var(--text-muted)' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <Clock size={13} /> Deadline: {item.deadline || '2026-12-31'}
        </span>
        <span style={{ fontWeight: 600, color: 'var(--teal-dark)' }}>Verified Opportunity</span>
      </div>
    </div>
  );
}

export default function ScholarshipsPage() {
  const [tab, setTab] = useState('scholarships');
  const [scholarships, setScholarships] = useState([]);
  const [internships, setInternships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [irInfo, setIrInfo] = useState(null);

  const fetchOpportunities = useCallback(async (queryStr = '') => {
    setLoading(true);
    setError('');
    try {
      if (tab === 'scholarships') {
        const data = await searchScholarshipsAdmin(queryStr, null, 40);
        setScholarships(data.results || []);
        setIrInfo(data.ir_metadata || null);
      } else {
        const data = await searchInternshipsAdmin(queryStr, null, 40);
        setInternships(data.results || []);
        setIrInfo(data.ir_metadata || null);
      }
    } catch (err) {
      console.error(err);
      setError('Search failed. Ensure backend server is running.');
    } finally {
      setLoading(false);
    }
  }, [tab]);

  useEffect(() => {
    fetchOpportunities(search);
  }, [fetchOpportunities]);

  const handleSearchSubmit = (e) => {
    if (e) e.preventDefault();
    fetchOpportunities(search);
  };

  const handleQuickFilter = (term) => {
    setSearch(term);
    fetchOpportunities(term);
  };

  return (
    <DashboardLayout role="admin">
      <div style={{ padding: '28px 32px', maxWidth: 1280, margin: '0 auto' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20, flexWrap: 'wrap', gap: 14 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{
              width: 48,
              height: 48,
              borderRadius: 14,
              background: 'linear-gradient(135deg, #d97706, #f59e0b)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 12px rgba(217, 119, 6, 0.25)'
            }}>
              <Award size={26} color="white" />
            </div>
            <div>
              <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)', margin: 0 }}>
                Scholarships & Internships Administration
              </h1>
              <p style={{ color: 'var(--text-muted)', fontSize: 14, marginTop: 4 }}>
                Search and manage institutional and national scholarship and internship opportunities.
              </p>
            </div>
          </div>
        </div>

        {/* Tabs and Search Controls */}
        <div style={{ display: 'flex', gap: 16, marginBottom: 18, alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap' }}>
          {/* Tab Selector */}
          <div style={{ display: 'flex', background: '#f1f5f9', borderRadius: 'var(--radius)', padding: 4, gap: 4 }}>
            {[
              { key: 'scholarships', label: 'Scholarships Directory', icon: Award },
              { key: 'internships', label: 'Internships Directory', icon: Briefcase }
            ].map(({ key, label, icon: Icon }) => (
              <button
                key={key}
                onClick={() => {
                  setTab(key);
                  setSearch('');
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '9px 18px',
                  borderRadius: 8,
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: 13,
                  fontWeight: 600,
                  background: tab === key ? 'linear-gradient(135deg, var(--primary), var(--teal))' : 'transparent',
                  color: tab === key ? 'white' : 'var(--text-secondary)',
                  boxShadow: tab === key ? '0 2px 6px rgba(0,0,0,0.1)' : 'none',
                  transition: 'all 0.2s',
                }}
              >
                <Icon size={16} /> {label}
              </button>
            ))}
          </div>

          {/* Search Input */}
          <form onSubmit={handleSearchSubmit} style={{ flex: 1, display: 'flex', gap: 8, maxWidth: 460 }}>
            <div style={{ flex: 1, position: 'relative' }}>
              <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)' }} />
              <input
                id="sch-search-input"
                className="input"
                style={{ paddingLeft: 38, height: 42, fontSize: 13 }}
                placeholder={
                  tab === 'scholarships'
                    ? 'Search all scholarships, AICTE, MahaDBT, above 50000...'
                    : 'Search internships, Python, AI/ML, Cloud, stipend...'
                }
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <button type="submit" className="btn btn-primary btn-sm" style={{ height: 42, padding: '0 18px' }}>
              Search
            </button>
          </form>
        </div>

        {/* Quick Filter Pills */}
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center', marginBottom: 24 }}>
          <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
            <Filter size={13} /> Quick Filters:
          </span>
          {tab === 'scholarships' ? (
            [
              { label: 'All', query: '' },
              { label: 'AICTE', query: 'AICTE' },
              { label: 'Maharashtra / MahaDBT', query: 'Maharashtra' },
              { label: 'MCA Scholarships', query: 'MCA' },
              { label: 'Above ₹50,000', query: 'above 50000' },
              { label: 'Technical Grants', query: 'technical education' }
            ].map((f, i) => (
              <button
                key={i}
                type="button"
                onClick={() => handleQuickFilter(f.query)}
                style={{
                  padding: '5px 12px',
                  borderRadius: 99,
                  fontSize: 12,
                  fontWeight: 600,
                  background: search.toLowerCase() === f.query.toLowerCase() ? 'var(--primary)' : 'white',
                  color: search.toLowerCase() === f.query.toLowerCase() ? 'white' : 'var(--text-secondary)',
                  border: '1px solid var(--border)',
                  cursor: 'pointer',
                  transition: 'all 0.15s'
                }}
              >
                {f.label}
              </button>
            ))
          ) : (
            [
              { label: 'All', query: '' },
              { label: 'AI / Machine Learning', query: 'AI ML Python' },
              { label: 'Cloud Computing', query: 'Cloud AWS' },
              { label: 'Full Stack Web', query: 'Web Development React' },
              { label: 'Stipend > ₹30,000', query: 'above 30000' }
            ].map((f, i) => (
              <button
                key={i}
                type="button"
                onClick={() => handleQuickFilter(f.query)}
                style={{
                  padding: '5px 12px',
                  borderRadius: 99,
                  fontSize: 12,
                  fontWeight: 600,
                  background: search.toLowerCase() === f.query.toLowerCase() ? 'var(--primary)' : 'white',
                  color: search.toLowerCase() === f.query.toLowerCase() ? 'white' : 'var(--text-secondary)',
                  border: '1px solid var(--border)',
                  cursor: 'pointer',
                  transition: 'all 0.15s'
                }}
              >
                {f.label}
              </button>
            ))
          )}
        </div>

        {error && <Alert type="warning" message={error} style={{ marginBottom: 20 }} />}

        {/* Content Listing */}
        {loading ? (
          <LoadingSpinner message={`Searching ${tab}...`} />
        ) : tab === 'scholarships' ? (
          scholarships.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12, margin: '0 auto' }} />
              <p style={{ fontWeight: 700, fontSize: 16, color: 'var(--text-primary)' }}>No scholarships found</p>
              <p style={{ fontSize: 14, marginTop: 4 }}>Try clearing the search query or adjusting the amount threshold.</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(430px, 1fr))', gap: 20 }}>
              {scholarships.map((s, idx) => (
                <ScholarshipCard key={s.scholarship_id || idx} item={s} rank={idx + 1} />
              ))}
            </div>
          )
        ) : (
          internships.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12, margin: '0 auto' }} />
              <p style={{ fontWeight: 700, fontSize: 16, color: 'var(--text-primary)' }}>No internships found</p>
              <p style={{ fontSize: 14, marginTop: 4 }}>Try clearing your search query.</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(430px, 1fr))', gap: 20 }}>
              {internships.map((it, idx) => (
                <InternshipCard key={it.internship_id || idx} item={it} rank={idx + 1} />
              ))}
            </div>
          )
        )}
      </div>
    </DashboardLayout>
  );
}
