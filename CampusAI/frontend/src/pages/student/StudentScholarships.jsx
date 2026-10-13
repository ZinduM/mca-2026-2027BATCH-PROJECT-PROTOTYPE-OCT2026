import { useState, useEffect } from 'react';
import { Award, Briefcase, ExternalLink, DollarSign, Calendar, MapPin, Tag, Search, AlertCircle, Star } from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import { useAuth } from '../../hooks/useAuth';
import { getStudentScholarships, getExternalInternships } from '../../services/api';

export default function StudentScholarships() {
  const { user } = useAuth();
  const studentId = user?.student_id || user?.user_id;

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
          getStudentScholarships(studentId),
          getExternalInternships(),
        ]);
        if (sc.status === 'fulfilled') setScholarships(sc.value.data || sc.value || []);
        if (it.status === 'fulfilled') setInternships(it.value.results || it.value.data || []);
      } catch {
        setError('Failed to load opportunities.');
      } finally {
        setLoading(false);
      }
    };
    if (studentId) load();
  }, [studentId]);

  return (
    <DashboardLayout role="student">
      <div style={{ padding: '28px 32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 24 }}>
          <div style={{ width: 46, height: 46, borderRadius: 14, background: 'linear-gradient(135deg, #d97706, #f59e0b)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Award size={24} color="white" />
          </div>
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)' }}>Scholarships & Internships</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Your scholarships and internship opportunities</p>
          </div>
        </div>

        {/* Tabs + Search */}
        <div style={{ display: 'flex', gap: 16, marginBottom: 24, alignItems: 'center', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', background: 'white', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: 4, gap: 4 }}>
            {[{ key: 'scholarships', label: 'My Scholarships', icon: Award }, { key: 'internships', label: 'Internships', icon: Briefcase }].map(({ key, label, icon: Icon }) => (
              <button key={key} onClick={() => setTab(key)} style={{
                display: 'flex', alignItems: 'center', gap: 6,
                padding: '8px 18px', borderRadius: 8, border: 'none', cursor: 'pointer',
                fontSize: 13, fontWeight: 600,
                background: tab === key ? 'linear-gradient(135deg, var(--primary), var(--teal))' : 'transparent',
                color: tab === key ? 'white' : 'var(--text-secondary)',
                transition: 'all 0.2s',
              }}>
                <Icon size={15} /> {label}
              </button>
            ))}
          </div>

          <div style={{ flex: 1, position: 'relative', maxWidth: 350 }}>
            <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)' }} />
            <input className="input" style={{ paddingLeft: 38, height: 40 }} placeholder={`Search ${tab}…`}
              value={search} onChange={e => setSearch(e.target.value)} />
          </div>
        </div>

        {error && <Alert type="warning" message={error} style={{ marginBottom: 16 }} />}

        {loading ? <LoadingSpinner message={`Loading ${tab}…`} /> : tab === 'scholarships' ? (
          scholarships.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12 }} />
              <p style={{ fontWeight: 600 }}>No scholarships found</p>
              <p style={{ fontSize: 14, marginTop: 4 }}>You may not have any scholarship applications yet.</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 20 }}>
              {scholarships.filter(s => !search || (s.scholarship_name || '').toLowerCase().includes(search.toLowerCase())).map((s, i) => (
                <div key={i} className="card animate-fade-in" style={{ padding: 22 }}>
                  <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', marginBottom: 14 }}>
                    <div style={{ width: 44, height: 44, borderRadius: 12, background: '#fef3c7', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                      <Award size={22} color="#d97706" />
                    </div>
                    <div style={{ flex: 1 }}>
                      <p style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 4 }}>{s.scholarship_name || 'Scholarship'}</p>
                      <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>{s.provider || '—'}</p>
                    </div>
                    <span style={{
                      padding: '4px 10px', borderRadius: 99, fontSize: 12, fontWeight: 700,
                      background: s.application_status === 'Approved' ? '#d1fae5' : s.application_status === 'Rejected' ? '#fee2e2' : '#fef3c7',
                      color: s.application_status === 'Approved' ? '#065f46' : s.application_status === 'Rejected' ? '#991b1b' : '#92400e',
                    }}>
                      {s.application_status || 'Pending'}
                    </span>
                  </div>
                  <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                    {s.amount && <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 13, color: 'var(--text-secondary)' }}><DollarSign size={13} /> ₹{Number(s.amount).toLocaleString('en-IN')}</span>}
                    {s.eligibility_status && <span className="badge badge-blue">{s.eligibility_status}</span>}
                  </div>
                </div>
              ))}
            </div>
          )
        ) : (
          internships.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12 }} />
              <p style={{ fontWeight: 600 }}>No internships available</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 20 }}>
              {internships.filter(i => !search || (i.title || i.company || '').toLowerCase().includes(search.toLowerCase())).map((it, i) => (
                <div key={i} className="card animate-fade-in" style={{ padding: 22 }}>
                  <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
                    <div style={{ width: 44, height: 44, borderRadius: 12, background: '#e0f2fe', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                      <Briefcase size={22} color="var(--primary)" />
                    </div>
                    <div style={{ flex: 1 }}>
                      <p style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 2 }}>{it.title || it.internship_title || 'Internship'}</p>
                      <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>{it.company || it.organization || '—'}</p>
                    </div>
                    {it.stipend && <p style={{ fontSize: 14, fontWeight: 700, color: 'var(--teal-dark)', flexShrink: 0 }}>₹{Number(it.stipend).toLocaleString('en-IN')}/mo</p>}
                  </div>
                  <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 14 }}>
                    {it.location && <span style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', gap: 3, alignItems: 'center' }}><MapPin size={12} />{it.location}</span>}
                    {it.duration && <span style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', gap: 3, alignItems: 'center' }}><Calendar size={12} />{it.duration}</span>}
                  </div>
                  <button className="btn btn-primary btn-sm" style={{ gap: 6 }}>
                    <ExternalLink size={13} /> Apply Now
                  </button>
                </div>
              ))}
            </div>
          )
        )}
      </div>
    </DashboardLayout>
  );
}
