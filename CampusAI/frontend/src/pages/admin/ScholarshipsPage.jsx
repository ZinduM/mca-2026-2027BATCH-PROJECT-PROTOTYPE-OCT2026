import { useState, useEffect } from 'react';
import { GraduationCap, Briefcase, Search, ExternalLink, Award, MapPin, Calendar, DollarSign, Tag, Star, AlertCircle } from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import { getExternalScholarships, getExternalInternships, listInternships, searchExternal } from '../../services/api';

function ScholarshipCard({ item, rank }) {
  return (
    <div className="card animate-fade-in" style={{ padding: 22, position: 'relative', overflow: 'hidden' }}>
      {rank <= 3 && (
        <div style={{ position: 'absolute', top: 16, right: 16 }}>
          <span style={{
            display: 'inline-flex', alignItems: 'center', gap: 4,
            padding: '4px 12px', borderRadius: 99, fontSize: 12, fontWeight: 700,
            background: rank === 1 ? '#fef3c7' : rank === 2 ? '#f3f4f6' : '#fdf2e9',
            color: rank === 1 ? '#d97706' : rank === 2 ? '#6b7280' : '#c05621',
          }}>
            <Star size={12} fill="currentColor" />
            #{rank}
          </span>
        </div>
      )}
      <div style={{ display: 'flex', gap: 14, alignItems: 'flex-start', marginBottom: 12 }}>
        <div style={{ width: 44, height: 44, borderRadius: 12, background: 'linear-gradient(135deg, #fef3c7, #fde68a)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          <Award size={22} color="#d97706" />
        </div>
        <div style={{ flex: 1, marginRight: 60 }}>
          <p style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: 15, marginBottom: 4 }}>
            {item.scholarship_name || item.name || item.title || 'Scholarship'}
          </p>
          <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
            {item.provider || item.source || item.organization || '—'}
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 14 }}>
        {(item.amount || item.stipend) && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: 'var(--text-secondary)' }}>
            <DollarSign size={14} color="var(--teal)" />
            ₹{Number(item.amount || item.stipend).toLocaleString('en-IN')}
          </div>
        )}
        {(item.eligibility_criteria || item.eligibility) && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: 'var(--text-secondary)', gridColumn: 'span 2' }}>
            <Tag size={14} color="var(--primary)" />
            {item.eligibility_criteria || item.eligibility}
          </div>
        )}
      </div>

      {item.application_deadline && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--text-muted)', marginBottom: 14 }}>
          <Calendar size={13} />
          Deadline: {item.application_deadline}
        </div>
      )}

      <div style={{ display: 'flex', gap: 8 }}>
        {(item.url || item.source_url) && (
          <a
            href={item.url || item.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-teal btn-sm"
            style={{ gap: 6, textDecoration: 'none' }}
          >
            <ExternalLink size={14} /> Apply Now
          </a>
        )}
        {!item.url && !item.source_url && (
          <button className="btn btn-outline btn-sm">Apply Now</button>
        )}
      </div>
    </div>
  );
}

function InternshipCard({ item }) {
  return (
    <div className="card animate-fade-in" style={{ padding: 22 }}>
      <div style={{ display: 'flex', gap: 14, alignItems: 'flex-start', marginBottom: 12 }}>
        <div style={{ width: 44, height: 44, borderRadius: 12, background: 'linear-gradient(135deg, #e0f2fe, #bfdbfe)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          <Briefcase size={22} color="var(--primary)" />
        </div>
        <div style={{ flex: 1 }}>
          <p style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: 15, marginBottom: 4 }}>
            {item.title || item.internship_title || item.role || 'Internship'}
          </p>
          <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
            {item.company || item.organization || item.provider || '—'}
          </p>
        </div>
        {item.stipend && (
          <div style={{ textAlign: 'right', flexShrink: 0 }}>
            <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--teal-dark)' }}>₹{Number(item.stipend).toLocaleString('en-IN')}</p>
            <p style={{ fontSize: 11, color: 'var(--text-muted)' }}>per month</p>
          </div>
        )}
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 14 }}>
        {item.location && (
          <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, color: 'var(--text-muted)' }}>
            <MapPin size={13} />{item.location}
          </span>
        )}
        {item.duration && (
          <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, color: 'var(--text-muted)' }}>
            <Calendar size={13} />{item.duration}
          </span>
        )}
        {item.skills_required && (
          <span className="badge badge-blue">{item.skills_required}</span>
        )}
      </div>

      {item.description && (
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: 14 }}>
          {item.description}
        </p>
      )}

      <a
        href={item.url || item.application_link || '#'}
        target="_blank"
        rel="noopener noreferrer"
        className="btn btn-primary btn-sm"
        style={{ gap: 6, textDecoration: 'none' }}
      >
        <ExternalLink size={14} /> Apply Now
      </a>
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

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const [sc, it] = await Promise.allSettled([
          getExternalScholarships(),
          listInternships(),
        ]);
        if (sc.status === 'fulfilled') setScholarships(sc.value.results || sc.value.data || []);
        if (it.status === 'fulfilled') setInternships(it.value.data || it.value || []);
      } catch {
        setError('Could not load data. The web crawler may not be initialized.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const handleSearch = async () => {
    if (!search.trim()) return;
    setLoading(true);
    try {
      const data = await searchExternal(search, tab === 'scholarships' ? 'scholarship' : 'internship');
      if (tab === 'scholarships') setScholarships(data.results || []);
      else setInternships(data.results || []);
    } catch {
      setError('Search failed.');
    } finally {
      setLoading(false);
    }
  };

  const filteredSc = scholarships.filter(s =>
    !search || (s.scholarship_name || s.name || s.title || '').toLowerCase().includes(search.toLowerCase())
  );
  const filteredIt = internships.filter(i =>
    !search || (i.title || i.internship_title || i.company || '').toLowerCase().includes(search.toLowerCase())
  );

  return (
    <DashboardLayout role="admin">
      <div style={{ padding: '28px 32px' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 24 }}>
          <div style={{ width: 46, height: 46, borderRadius: 14, background: 'linear-gradient(135deg, #d97706, #f59e0b)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Award size={24} color="white" />
          </div>
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)' }}>Scholarships & Internships</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Discover opportunities for students</p>
          </div>
        </div>

        {/* Tabs + Search */}
        <div style={{ display: 'flex', gap: 16, marginBottom: 24, alignItems: 'center', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', background: 'white', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: 4, gap: 4 }}>
            {[
              { key: 'scholarships', label: 'Scholarships', icon: Award },
              { key: 'internships',  label: 'Internships',  icon: Briefcase },
            ].map(({ key, label, icon: Icon }) => (
              <button
                key={key}
                onClick={() => setTab(key)}
                style={{
                  display: 'flex', alignItems: 'center', gap: 6,
                  padding: '8px 18px', borderRadius: 8, border: 'none', cursor: 'pointer',
                  fontSize: 13, fontWeight: 600,
                  background: tab === key ? 'linear-gradient(135deg, var(--primary), var(--teal))' : 'transparent',
                  color: tab === key ? 'white' : 'var(--text-secondary)',
                  transition: 'all 0.2s',
                }}
              >
                <Icon size={15} /> {label}
              </button>
            ))}
          </div>

          <div style={{ flex: 1, display: 'flex', gap: 10, maxWidth: 400 }}>
            <div style={{ flex: 1, position: 'relative' }}>
              <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)' }} />
              <input
                id="sch-search-input"
                className="input"
                style={{ paddingLeft: 38, height: 40 }}
                placeholder={`Search ${tab}…`}
                value={search}
                onChange={e => setSearch(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <button onClick={handleSearch} className="btn btn-primary btn-sm" style={{ height: 40 }}>
              <Search size={14} />
            </button>
          </div>
        </div>

        {error && <Alert type="warning" message={error} style={{ marginBottom: 20 }} />}

        {loading ? (
          <LoadingSpinner message={`Loading ${tab}…`} />
        ) : tab === 'scholarships' ? (
          filteredSc.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12 }} />
              <p style={{ fontWeight: 600, fontSize: 16 }}>No scholarships found</p>
              <p style={{ fontSize: 14, marginTop: 4 }}>The web crawler may need to be initialized, or try a different search.</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 20 }}>
              {filteredSc.map((s, i) => <ScholarshipCard key={i} item={s} rank={i + 1} />)}
            </div>
          )
        ) : (
          filteredIt.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12 }} />
              <p style={{ fontWeight: 600, fontSize: 16 }}>No internships found</p>
              <p style={{ fontSize: 14, marginTop: 4 }}>The web crawler may need to be initialized, or try a different search.</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 20 }}>
              {filteredIt.map((it, i) => <InternshipCard key={i} item={it} />)}
            </div>
          )
        )}
      </div>
    </DashboardLayout>
  );
}
