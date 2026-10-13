import { useEffect, useState } from 'react';
import {
  Users, Building2, BarChart3, GraduationCap,
  Award, CreditCard, TrendingUp, UserCheck,
  RefreshCw,
} from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import Alert from '../../components/Alert';
import { getDashboardStats, getDepartmentStats } from '../../services/api';
import { formatNumber, formatPercent, formatCurrency } from '../../utils/format';

function StatCard({ icon: Icon, label, value, sub, color, bg }) {
  return (
    <div className="card" style={{ padding: 24, display: 'flex', alignItems: 'flex-start', gap: 16, transition: 'transform 0.2s' }}
      onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-2px)'}
      onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
    >
      <div style={{ width: 52, height: 52, borderRadius: 14, background: bg, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Icon size={24} color={color} />
      </div>
      <div>
        <p style={{ fontSize: 13, color: 'var(--text-muted)', fontWeight: 500, marginBottom: 4 }}>{label}</p>
        <p style={{ fontSize: 28, fontFamily: 'var(--font-display)', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1 }}>{value}</p>
        {sub && <p style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>{sub}</p>}
      </div>
    </div>
  );
}

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [deptStats, setDeptStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true); setError('');
    try {
      const [s, d] = await Promise.all([getDashboardStats(), getDepartmentStats()]);
      setStats(s);
      setDeptStats(Array.isArray(d) ? d : (d.data || []));
    } catch {
      setError('Failed to load dashboard data. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const cards = stats ? [
    { icon: Users,       label: 'Total Students',      value: formatNumber(stats.total_students),     sub: 'Enrolled this year',            color: '#1e40af', bg: '#dbeafe' },
    { icon: Building2,   label: 'Departments',          value: formatNumber(stats.total_departments),  sub: `${formatNumber(stats.total_faculty)} faculty members`, color: '#0f766e', bg: '#ccfbf1' },
    { icon: BarChart3,   label: 'Avg Attendance',       value: formatPercent(stats.avg_attendance),   sub: 'Across all subjects',           color: '#7c3aed', bg: '#ede9fe' },
    { icon: GraduationCap,label:'Average CGPA',         value: stats.avg_cgpa?.toFixed(2) || '—',     sub: 'Academic performance',          color: '#0369a1', bg: '#e0f2fe' },
    { icon: Award,       label: 'Scholarships',         value: formatNumber(stats.scholarship_count), sub: 'Approved scholarships',         color: '#d97706', bg: '#fef3c7' },
    { icon: CreditCard,  label: 'Pending Fees',         value: formatNumber(stats.pending_fees),       sub: 'Students with due payments',    color: '#dc2626', bg: '#fee2e2' },
  ] : [];

  return (
    <DashboardLayout role="admin">
      <div style={{ padding: '28px 32px' }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 28 }}>
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 4 }}>
              Admin Dashboard
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Live overview of campus academic data</p>
          </div>
          <button onClick={load} className="btn btn-outline btn-sm" style={{ gap: 6 }}>
            <RefreshCw size={14} style={loading ? { animation: 'spin 1s linear infinite' } : {}} />
            Refresh
          </button>
        </div>

        {error && <Alert type="error" message={error} style={{ marginBottom: 24 }} />}

        {/* Stat Cards */}
        {loading ? (
          <LoadingSpinner message="Fetching dashboard statistics…" />
        ) : (
          <>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20, marginBottom: 32 }}>
              {cards.map((c) => <StatCard key={c.label} {...c} />)}
            </div>

            {/* Department Stats Table */}
            {deptStats.length > 0 && (
              <div className="card" style={{ padding: 24 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 20 }}>
                  <div style={{ width: 36, height: 36, borderRadius: 10, background: '#eff6ff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <TrendingUp size={18} color="var(--primary)" />
                  </div>
                  <div>
                    <p style={{ fontWeight: 700, color: 'var(--text-primary)' }}>Department-wise Statistics</p>
                    <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>Students, CGPA, and Attendance per department</p>
                  </div>
                </div>
                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>Department</th>
                        <th>Students</th>
                        <th>Avg CGPA</th>
                        <th>Avg Attendance</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {deptStats.map((d, i) => {
                        const att = parseFloat(d.avg_attendance) || 0;
                        const statusColor = att >= 80 ? '#10b981' : att >= 70 ? '#f59e0b' : '#ef4444';
                        const statusLabel = att >= 80 ? 'Good' : att >= 70 ? 'Average' : 'Low';
                        return (
                          <tr key={i}>
                            <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{d.department_name}</td>
                            <td><span className="badge badge-blue">{formatNumber(d.student_count)}</span></td>
                            <td style={{ fontWeight: 600 }}>{d.avg_cgpa || '—'}</td>
                            <td>
                              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <div style={{ flex: 1, height: 6, background: '#f1f5f9', borderRadius: 3, maxWidth: 80 }}>
                                  <div style={{ height: '100%', width: `${att}%`, background: statusColor, borderRadius: 3, transition: 'width 0.6s ease' }} />
                                </div>
                                <span style={{ fontSize: 13 }}>{formatPercent(att)}</span>
                              </div>
                            </td>
                            <td>
                              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4, padding: '3px 10px', borderRadius: 99, fontSize: 12, fontWeight: 600, background: `${statusColor}18`, color: statusColor }}>
                                <UserCheck size={12} /> {statusLabel}
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
