import { useEffect, useState } from 'react';
import { User, Mail, Building2, GraduationCap, Hash, BadgeCheck, BarChart3, Award } from 'lucide-react';
import DashboardLayout from '../../layouts/DashboardLayout';
import LoadingSpinner from '../../components/LoadingSpinner';
import { useAuth } from '../../hooks/useAuth';
import { getStudentProfile } from '../../services/api';
import { getInitials, formatPercent } from '../../utils/format';

export default function StudentProfile() {
  const { user } = useAuth();
  const studentId = user?.student_id || user?.user_id;
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!studentId) return;
    getStudentProfile(studentId)
      .then(d => setProfile(d))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [studentId]);

  const student = profile?.student || {};
  const department = profile?.department || {};

  const fields = [
    { icon: User,         label: 'Full Name',   value: student.name   || user?.name },
    { icon: Mail,         label: 'Email',       value: student.email  || user?.email },
    { icon: Building2,    label: 'Department',  value: department.department_name || user?.department },
    { icon: Hash,         label: 'Student ID',  value: `STU-${studentId}` },
    { icon: GraduationCap,label: 'Semester',    value: student.semester ? `Semester ${student.semester}` : '—' },
    { icon: BarChart3,    label: 'Gender',      value: student.gender  || '—' },
  ];

  return (
    <DashboardLayout role="student">
      <div style={{ padding: '28px 32px', maxWidth: 700, margin: '0 auto' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 24 }}>My Profile</h1>

        {loading ? <LoadingSpinner /> : (
          <>
            <div className="card" style={{ padding: 0, overflow: 'hidden', marginBottom: 20 }}>
              <div style={{ height: 100, background: 'linear-gradient(135deg, var(--teal-dark), var(--teal), var(--primary))', position: 'relative' }} />
              <div style={{ paddingLeft: 32, paddingRight: 32, paddingBottom: 24 }}>
                <div style={{
                  width: 80, height: 80, borderRadius: '50%', marginTop: -40,
                  background: 'linear-gradient(135deg, var(--teal), var(--primary))',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  color: 'white', fontSize: 28, fontWeight: 800,
                  border: '4px solid white', boxShadow: 'var(--shadow-md)', marginBottom: 16,
                }}>
                  {getInitials(student.name || user?.name || 'S')}
                </div>
                <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 22, fontWeight: 800, marginBottom: 4 }}>{student.name || user?.name}</h2>
                <div style={{ display: 'flex', gap: 8 }}>
                  <span className="badge badge-teal"><GraduationCap size={12} /> Student</span>
                  <span className="badge badge-blue"><BadgeCheck size={12} /> Verified</span>
                </div>
              </div>
            </div>

            <div className="card" style={{ padding: 24 }}>
              <p style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 18 }}>Account Information</p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                {fields.map(({ icon: Icon, label, value }) => (
                  <div key={label} style={{ display: 'flex', alignItems: 'center', gap: 14, padding: '12px 16px', background: 'var(--bg)', borderRadius: 'var(--radius)', border: '1px solid var(--border)' }}>
                    <div style={{ width: 36, height: 36, borderRadius: 10, background: '#f0fdf4', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                      <Icon size={17} color="var(--teal)" />
                    </div>
                    <div>
                      <p style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{label}</p>
                      <p style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{value || '—'}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
