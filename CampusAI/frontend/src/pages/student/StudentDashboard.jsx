import { useEffect, useState } from 'react';
import { GraduationCap, BarChart3, CreditCard, Award, Bell, RefreshCw, AlertCircle, CheckCircle, Lightbulb, TrendingUp } from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import { useAuth } from '../../hooks/useAuth';
import {
  getStudentAttendance, getStudentFees,
  getStudentScholarships, getStudentSuggestions,
  getStudentAcademics,
} from '../../services/api';
import { formatCurrency, formatPercent, attendanceColor } from '../../utils/format';

function StatCard({ icon: Icon, label, value, sub, color, bg }) {
  return (
    <div className="card" style={{ padding: 22, display: 'flex', alignItems: 'flex-start', gap: 14 }}>
      <div style={{ width: 48, height: 48, borderRadius: 14, background: bg, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Icon size={22} color={color} />
      </div>
      <div>
        <p style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 2 }}>{label}</p>
        <p style={{ fontSize: 24, fontFamily: 'var(--font-display)', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1 }}>{value}</p>
        {sub && <p style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>{sub}</p>}
      </div>
    </div>
  );
}

function SuggestionCard({ suggestion }) {
  const typeConfig = {
    warning:     { bg: '#fef2f2', border: '#fecaca', icon: AlertCircle,   color: '#dc2626' },
    improvement: { bg: '#fffbeb', border: '#fde68a', icon: TrendingUp,    color: '#b45309' },
    finance:     { bg: '#fff7ed', border: '#fed7aa', icon: CreditCard,    color: '#c2410c' },
    opportunity: { bg: '#f0fdf4', border: '#bbf7d0', icon: Award,         color: '#15803d' },
    info:        { bg: '#eff6ff', border: '#bfdbfe', icon: CheckCircle,   color: '#1d4ed8' },
    tip:         { bg: '#fdf4ff', border: '#e9d5ff', icon: Lightbulb,     color: '#7c3aed' },
  };
  const cfg = typeConfig[suggestion.type] || typeConfig.info;
  const Icon = cfg.icon;
  return (
    <div style={{
      padding: '14px 18px',
      borderRadius: 'var(--radius)',
      background: cfg.bg,
      border: `1px solid ${cfg.border}`,
      display: 'flex', gap: 12,
    }}>
      <Icon size={18} color={cfg.color} style={{ flexShrink: 0, marginTop: 2 }} />
      <div>
        <p style={{ fontWeight: 700, color: cfg.color, fontSize: 14, marginBottom: 3 }}>{suggestion.title}</p>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5 }}>{suggestion.message}</p>
      </div>
    </div>
  );
}

export default function StudentDashboard() {
  const { user } = useAuth();
  const studentId = user?.student_id || user?.user_id;

  const [academics, setAcademics] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [fees, setFees] = useState([]);
  const [scholarships, setScholarships] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    if (!studentId) return;
    setLoading(true); setError('');
    try {
      const [ac, att, fe, sc, sg] = await Promise.allSettled([
        getStudentAcademics(studentId),
        getStudentAttendance(studentId),
        getStudentFees(studentId),
        getStudentScholarships(studentId),
        getStudentSuggestions(studentId),
      ]);
      if (ac.status === 'fulfilled') setAcademics(ac.value.data || ac.value || []);
      if (att.status === 'fulfilled') setAttendance(att.value.data || att.value || []);
      if (fe.status === 'fulfilled') setFees(fe.value.data || fe.value || []);
      if (sc.status === 'fulfilled') setScholarships(sc.value.data || sc.value || []);
      if (sg.status === 'fulfilled') setSuggestions(sg.value.suggestions || []);
    } catch {
      setError('Failed to load student data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [studentId]);

  // Compute stats
  const avgCGPA = academics.length
    ? (academics.reduce((s, a) => s + (parseFloat(a.cgpa) || 0), 0) / academics.length).toFixed(2)
    : '—';
  const avgAttendance = attendance.length
    ? attendance.reduce((s, a) => s + (parseFloat(a.attendance_percent) || 0), 0) / attendance.length
    : null;
  const fee = fees[0];
  const scholarship = scholarships.find(s => s.application_status === 'Approved');

  const cards = [
    { icon: GraduationCap, label: 'Current CGPA',    value: avgCGPA, sub: `${academics.length} subjects tracked`, color: '#1e40af', bg: '#dbeafe' },
    { icon: BarChart3,     label: 'Avg Attendance',  value: avgAttendance !== null ? formatPercent(avgAttendance) : '—', sub: avgAttendance < 75 ? '⚠ Below 75%' : 'Above threshold', color: avgAttendance !== null ? attendanceColor(avgAttendance) : '#64748b', bg: '#f1f5f9' },
    { icon: CreditCard,    label: 'Pending Fees',    value: fee ? formatCurrency(fee.pending_amount) : '—', sub: fee?.payment_status || '', color: '#dc2626', bg: '#fee2e2' },
    { icon: Award,         label: 'Scholarship',     value: scholarship ? 'Approved' : (scholarships.length ? 'Pending' : 'None'), sub: scholarship ? scholarship.scholarship_name : 'Check eligibility', color: '#10b981', bg: '#d1fae5' },
  ];

  return (
    <DashboardLayout role="student">
      <div style={{ padding: '28px 32px' }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 28 }}>
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 4 }}>
              Welcome, {user?.name?.split(' ')[0] || 'Student'}! 👋
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Here's a summary of your academic profile</p>
          </div>
          <button onClick={load} className="btn btn-outline btn-sm">
            <RefreshCw size={14} style={loading ? { animation: 'spin 1s linear infinite' } : {}} />
            Refresh
          </button>
        </div>

        {error && <Alert type="error" message={error} style={{ marginBottom: 20 }} />}

        {loading ? <LoadingSpinner message="Loading your academic data…" /> : (
          <>
            {/* Stat Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 28 }}>
              {cards.map(c => <StatCard key={c.label} {...c} />)}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
              {/* AI Suggestions */}
              <div className="card" style={{ padding: 22 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                  <Lightbulb size={18} color="var(--teal)" />
                  <p style={{ fontWeight: 700, color: 'var(--text-primary)' }}>AI Suggestions</p>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {suggestions.length > 0
                    ? suggestions.map((s, i) => <SuggestionCard key={i} suggestion={s} />)
                    : <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>No suggestions at this time.</p>
                  }
                </div>
              </div>

              {/* Attendance summary */}
              <div className="card" style={{ padding: 22 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                  <BarChart3 size={18} color="var(--primary)" />
                  <p style={{ fontWeight: 700, color: 'var(--text-primary)' }}>Subject Attendance</p>
                </div>
                {attendance.length === 0 ? (
                  <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>No attendance records found.</p>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {attendance.slice(0, 6).map((a, i) => {
                      const pct = parseFloat(a.attendance_percent) || 0;
                      const color = attendanceColor(pct);
                      return (
                        <div key={i}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                            <span style={{ fontSize: 13, fontWeight: 500, color: 'var(--text-primary)' }}>{a.subject_name}</span>
                            <span style={{ fontSize: 13, fontWeight: 700, color }}>{formatPercent(pct)}</span>
                          </div>
                          <div style={{ height: 7, background: '#f1f5f9', borderRadius: 4 }}>
                            <div style={{ height: '100%', width: `${Math.min(100, pct)}%`, background: color, borderRadius: 4, transition: 'width 0.6s ease' }} />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
