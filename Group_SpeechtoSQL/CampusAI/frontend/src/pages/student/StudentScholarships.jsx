import { useState, useEffect, useCallback } from 'react';
import {
  Award,
  Briefcase,
  ExternalLink,
  DollarSign,
  Calendar,
  MapPin,
  Tag,
  Search,
  AlertCircle,
  Star,
  CheckCircle2,
  Sparkles,
  Cpu,
  GraduationCap,
  Layers,
  Clock,
  Check
} from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import { useAuth } from '../../hooks/useAuth';
import {
  getRecommendedScholarships,
  getRecommendedInternships,
  getStudentScholarships
} from '../../services/api';

function RelevanceBadge({ score, percent }) {
  const p = percent || (typeof score === 'string' ? parseInt(score) : 75);
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
        gap: 5,
        padding: '4px 10px',
        borderRadius: 99,
        fontSize: 12,
        fontWeight: 700,
        background: bg,
        color: color,
        border: `1px solid ${border}`,
        boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
      }}
    >
      <Sparkles size={13} />
      {p}% Match
    </span>
  );
}

export default function StudentScholarships() {
  const { user } = useAuth();
  const studentId = user?.student_id || user?.user_id;

  const [tab, setTab] = useState('recommended_scholarships');
  const [scholarships, setScholarships] = useState([]);
  const [internships, setInternships] = useState([]);
  const [myApplications, setMyApplications] = useState([]);
  const [irMetadata, setIrMetadata] = useState(null);
  const [studentProfile, setStudentProfile] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [appliedIds, setAppliedIds] = useState(new Set());

  // Load recommendations using IR Engine
  const loadOpportunities = useCallback(async (searchQuery = '') => {
    if (!studentId) return;
    setLoading(true);
    setError('');
    try {
      if (tab === 'recommended_scholarships') {
        const data = await getRecommendedScholarships(studentId, searchQuery, 15);
        setScholarships(data.results || []);
        setIrMetadata(data.ir_metadata || null);
        if (data.student_profile_used) setStudentProfile(data.student_profile_used);
      } else if (tab === 'recommended_internships') {
        const data = await getRecommendedInternships(studentId, searchQuery, 15);
        setInternships(data.results || []);
        setIrMetadata(data.ir_metadata || null);
        if (data.student_profile_used) setStudentProfile(data.student_profile_used);
      } else if (tab === 'my_applications') {
        const data = await getStudentScholarships(studentId);
        setMyApplications(data.data || data || []);
      }
    } catch (err) {
      console.error(err);
      setError('Failed to fetch opportunities from the Information Retrieval engine.');
    } finally {
      setLoading(false);
    }
  }, [studentId, tab]);

  useEffect(() => {
    loadOpportunities(search);
  }, [loadOpportunities]);

  const handleSearchSubmit = (e) => {
    if (e) e.preventDefault();
    loadOpportunities(search);
  };

  const handleApplyClick = (id) => {
    setAppliedIds((prev) => new Set([...prev, id]));
  };

  return (
    <DashboardLayout role="student">
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
                Scholarships & Career Opportunities
              </h1>
              <p style={{ color: 'var(--text-muted)', fontSize: 14, marginTop: 4 }}>
                Find relevant scholarships and internship opportunities based on your profile and interests.
              </p>
            </div>
          </div>

          {/* Student Profile Context Badge */}
          {studentProfile && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              background: '#f8fafc',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius)',
              padding: '8px 14px',
              fontSize: 13
            }}>
              <GraduationCap size={16} color="var(--primary)" />
              <div>
                <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{studentProfile.course || 'MCA'}</span>
                <span style={{ color: 'var(--text-muted)', margin: '0 6px' }}>•</span>
                <span style={{ color: 'var(--text-secondary)' }}>CGPA: <strong>{studentProfile.cgpa || '—'}</strong></span>
                <span style={{ color: 'var(--text-muted)', margin: '0 6px' }}>•</span>
                <span style={{ color: 'var(--teal-dark)', fontWeight: 600 }}>{studentProfile.department || 'Computer Applications'}</span>
              </div>
            </div>
          )}
        </div>

        {/* Tabs and Live IR Search */}
        <div style={{ display: 'flex', gap: 16, marginBottom: 24, alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', background: '#f1f5f9', borderRadius: 'var(--radius)', padding: 4, gap: 4 }}>
            {[
              { key: 'recommended_scholarships', label: 'Scholarship Recommendations', icon: Award },
              { key: 'recommended_internships', label: 'Internship Recommendations', icon: Briefcase },
              { key: 'my_applications', label: 'My Applications', icon: CheckCircle2 }
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

          {tab !== 'my_applications' && (
            <form onSubmit={handleSearchSubmit} style={{ flex: 1, position: 'relative', maxWidth: 420, display: 'flex', gap: 8 }}>
              <div style={{ flex: 1, position: 'relative' }}>
                <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)' }} />
                <input
                  id="student-ir-search"
                  className="input"
                  style={{ paddingLeft: 38, height: 42, fontSize: 13 }}
                  placeholder={
                    tab === 'recommended_scholarships'
                      ? 'Search AICTE, MahaDBT, MCA, merit, above 50000...'
                      : 'Search by role, skills (Python, Cloud, AI), stipend...'
                  }
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
              <button type="submit" className="btn btn-primary btn-sm" style={{ height: 42, padding: '0 16px' }}>
                Search
              </button>
            </form>
          )}
        </div>

        {error && <Alert type="warning" message={error} style={{ marginBottom: 20 }} />}

        {/* Content Render */}
        {loading ? (
          <LoadingSpinner message="Finding relevant opportunities..." />
        ) : tab === 'recommended_scholarships' ? (
          scholarships.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12, margin: '0 auto' }} />
              <p style={{ fontWeight: 700, fontSize: 16, color: 'var(--text-primary)' }}>No matching scholarships found</p>
              <p style={{ fontSize: 14, marginTop: 4 }}>Try broadening your search term or clear the filter.</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(420px, 1fr))', gap: 20 }}>
              {scholarships.map((s, idx) => {
                const isApplied = appliedIds.has(s.scholarship_id);
                return (
                  <div
                    key={s.scholarship_id || idx}
                    className="card animate-fade-in"
                    style={{
                      padding: 22,
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      borderLeft: s.academically_eligible === false ? '4px solid #f87171' : '4px solid var(--teal)',
                      transition: 'transform 0.2s, box-shadow 0.2s'
                    }}
                  >
                    <div>
                      {/* Top Bar: Title & Relevance Badge */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 10 }}>
                        <div style={{ flex: 1 }}>
                          <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: 0, lineHeight: 1.4 }}>
                            {s.scholarship_name}
                          </h3>
                          <p style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 3 }}>
                            Provider: <strong style={{ color: 'var(--text-secondary)' }}>{s.provider || 'AICTE / MahaDBT'}</strong>
                          </p>
                        </div>
                        <RelevanceBadge score={s.relevance_score} percent={s.relevance_percent} />
                      </div>

                      {/* Amount & Status Badges */}
                      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', alignItems: 'center', marginBottom: 12 }}>
                        {s.amount && (
                          <span style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 4,
                            fontSize: 14,
                            fontWeight: 800,
                            color: 'var(--teal-dark)',
                            background: '#f0fdf4',
                            padding: '3px 10px',
                            borderRadius: 6,
                            border: '1px solid #bbf7d0'
                          }}>
                            <DollarSign size={14} />
                            ₹{Number(s.amount).toLocaleString('en-IN')}
                          </span>
                        )}

                        <span style={{
                          padding: '3px 9px',
                          borderRadius: 6,
                          fontSize: 12,
                          fontWeight: 600,
                          background: s.academically_eligible === false ? '#fee2e2' : '#e0f2fe',
                          color: s.academically_eligible === false ? '#991b1b' : '#0369a1',
                        }}>
                          {s.eligibility_status || 'Eligible'}
                        </span>

                        {s.min_cgpa > 0 && (
                          <span style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
                            <GraduationCap size={13} />
                            Min CGPA: <strong>{s.min_cgpa}</strong>
                          </span>
                        )}
                      </div>

                      {/* Course and Department Target */}
                      {(s.course || s.department) && (
                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 12 }}>
                          {s.course && (
                            <span style={{ fontSize: 11, fontWeight: 600, background: '#f1f5f9', color: '#475569', padding: '2px 8px', borderRadius: 4 }}>
                              Course: {s.course}
                            </span>
                          )}
                          {s.department && (
                            <span style={{ fontSize: 11, fontWeight: 600, background: '#ede9fe', color: '#6d28d9', padding: '2px 8px', borderRadius: 4 }}>
                              Dept: {s.department}
                            </span>
                          )}
                        </div>
                      )}

                      {/* Snippet / Meaningful Excerpt */}
                      {s.snippet && (
                        <p style={{
                          fontSize: 13,
                          color: 'var(--text-secondary)',
                          lineHeight: 1.55,
                          marginBottom: 14,
                          background: '#f8fafc',
                          padding: '10px 12px',
                          borderRadius: 8,
                          borderLeft: '3px solid #cbd5e1'
                        }}>
                          "{s.snippet}"
                        </p>
                      )}

                      {/* Matched IR Keywords */}
                      {s.matched_terms && s.matched_terms.length > 0 && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap', marginBottom: 14 }}>
                          <span style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
                            Matched Terms:
                          </span>
                          {s.matched_terms.map((t, i) => (
                            <span key={i} style={{ fontSize: 11, background: '#fef3c7', color: '#92400e', padding: '1px 7px', borderRadius: 4, fontWeight: 600 }}>
                              {t}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Bottom Action Row */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 8, paddingTop: 12, borderTop: '1px solid var(--border)' }}>
                      <span style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
                        <Clock size={13} />
                        Deadline: {s.deadline || '2026-11-30'}
                      </span>

                      <button
                        onClick={() => handleApplyClick(s.scholarship_id)}
                        disabled={isApplied}
                        className={`btn btn-sm ${isApplied ? 'btn-outline' : 'btn-primary'}`}
                        style={{ gap: 6, minWidth: 105 }}
                      >
                        {isApplied ? (
                          <>
                            <Check size={14} color="var(--success)" /> Applied
                          </>
                        ) : (
                          <>
                            <ExternalLink size={13} /> Apply Now
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )
        ) : tab === 'recommended_internships' ? (
          internships.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12, margin: '0 auto' }} />
              <p style={{ fontWeight: 700, fontSize: 16, color: 'var(--text-primary)' }}>No matching internships found</p>
              <p style={{ fontSize: 14, marginTop: 4 }}>Try searching for specific technical skills like Python, Cloud, or ML.</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(420px, 1fr))', gap: 20 }}>
              {internships.map((it, idx) => {
                const isApplied = appliedIds.has(`int_${it.internship_id}`);
                return (
                  <div
                    key={it.internship_id || idx}
                    className="card animate-fade-in"
                    style={{
                      padding: 22,
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      borderLeft: '4px solid var(--primary)'
                    }}
                  >
                    <div>
                      {/* Top Bar: Role & Match Badge */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 8 }}>
                        <div style={{ flex: 1 }}>
                          <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                            {it.role || it.title || 'Software Engineering Intern'}
                          </h3>
                          <p style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 3 }}>
                            Company: <strong style={{ color: 'var(--text-secondary)' }}>{it.company_name || it.company}</strong> • Domain: <span style={{ color: 'var(--primary)' }}>{it.domain}</span>
                          </p>
                        </div>
                        <RelevanceBadge score={it.relevance_score} percent={it.relevance_percent} />
                      </div>

                      {/* Stipend & Location */}
                      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center', marginBottom: 12 }}>
                        {it.stipend && (
                          <span style={{
                            fontSize: 14,
                            fontWeight: 800,
                            color: 'var(--teal-dark)',
                            background: '#f0fdf4',
                            padding: '3px 10px',
                            borderRadius: 6,
                            border: '1px solid #bbf7d0'
                          }}>
                            ₹{Number(it.stipend).toLocaleString('en-IN')}/month
                          </span>
                        )}
                        {it.location && (
                          <span style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
                            <MapPin size={13} /> {it.location}
                          </span>
                        )}
                        {it.duration && (
                          <span style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
                            <Calendar size={13} /> {it.duration}
                          </span>
                        )}
                      </div>

                      {/* Required Skills */}
                      {it.skills_required && (
                        <div style={{ marginBottom: 12 }}>
                          <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 6 }}>
                            Key Technical Skills:
                          </div>
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
                            {it.skills_required.split(',').map((skill, sIdx) => (
                              <span
                                key={sIdx}
                                style={{
                                  fontSize: 11,
                                  background: '#e0f2fe',
                                  color: '#0369a1',
                                  padding: '2px 8px',
                                  borderRadius: 4,
                                  fontWeight: 600
                                }}
                              >
                                {skill.trim()}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Excerpt / Description */}
                      {it.snippet && (
                        <p style={{
                          fontSize: 13,
                          color: 'var(--text-secondary)',
                          lineHeight: 1.55,
                          marginBottom: 14,
                          background: '#f8fafc',
                          padding: '10px 12px',
                          borderRadius: 8
                        }}>
                          {it.snippet}
                        </p>
                      )}

                      {/* Eligibility statement */}
                      {it.eligibility && (
                        <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 12, display: 'flex', gap: 4 }}>
                          <Tag size={13} style={{ flexShrink: 0, marginTop: 2 }} />
                          <span>Eligibility: {it.eligibility}</span>
                        </div>
                      )}
                    </div>

                    {/* Bottom Action Row */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 8, paddingTop: 12, borderTop: '1px solid var(--border)' }}>
                      <span style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
                        <Clock size={13} /> Deadline: {it.deadline || '2026-12-31'}
                      </span>
                      <button
                        onClick={() => handleApplyClick(`int_${it.internship_id}`)}
                        disabled={isApplied}
                        className={`btn btn-sm ${isApplied ? 'btn-outline' : 'btn-primary'}`}
                        style={{ gap: 6, minWidth: 105 }}
                      >
                        {isApplied ? (
                          <>
                            <Check size={14} color="var(--success)" /> Applied
                          </>
                        ) : (
                          <>
                            <ExternalLink size={13} /> Apply Now
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )
        ) : (
          /* Tab 3: My Applications */
          myApplications.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
              <AlertCircle size={48} color="#cbd5e1" style={{ marginBottom: 12, margin: '0 auto' }} />
              <p style={{ fontWeight: 700, fontSize: 16, color: 'var(--text-primary)' }}>No scholarship applications found</p>
              <p style={{ fontSize: 14, marginTop: 4 }}>
                Browse the <strong>Scholarship Recommendations</strong> tab to explore and apply for scholarships.
              </p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: 20 }}>
              {myApplications.map((app, idx) => (
                <div key={idx} className="card animate-fade-in" style={{ padding: 22 }}>
                  <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', marginBottom: 14 }}>
                    <div style={{ width: 44, height: 44, borderRadius: 12, background: '#fef3c7', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                      <Award size={22} color="#d97706" />
                    </div>
                    <div style={{ flex: 1 }}>
                      <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                        {app.scholarship_name || 'Scholarship Application'}
                      </h3>
                      <p style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 2 }}>{app.provider || '—'}</p>
                    </div>
                    <span style={{
                      padding: '4px 10px', borderRadius: 99, fontSize: 12, fontWeight: 700,
                      background: app.application_status === 'Approved' ? '#d1fae5' : app.application_status === 'Rejected' ? '#fee2e2' : '#fef3c7',
                      color: app.application_status === 'Approved' ? '#065f46' : app.application_status === 'Rejected' ? '#991b1b' : '#92400e',
                    }}>
                      {app.application_status || 'Under Review'}
                    </span>
                  </div>

                  <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap', marginBottom: 12 }}>
                    {app.amount && (
                      <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 14, fontWeight: 700, color: 'var(--text-secondary)' }}>
                        <DollarSign size={14} color="var(--teal)" /> ₹{Number(app.amount).toLocaleString('en-IN')}
                      </span>
                    )}
                    {app.eligibility_status && (
                      <span className="badge badge-blue">{app.eligibility_status}</span>
                    )}
                  </div>

                  {app.description && (
                    <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5, background: '#f8fafc', padding: 10, borderRadius: 8 }}>
                      {app.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )
        )}
      </div>
    </DashboardLayout>
  );
}
