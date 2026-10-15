import { useAuth } from '../../hooks/useAuth';
import { getInitials } from '../../utils/format';
import DashboardLayout from '../../layouts/DashboardLayout';
import { User, Mail, Building2, Shield, CalendarDays, BadgeCheck } from 'lucide-react';

export default function AdminProfile() {
  const { user } = useAuth();

  return (
    <DashboardLayout role="admin">
      <div style={{ padding: '28px 32px', maxWidth: 700, margin: '0 auto' }}>
        {/* Header */}
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 24 }}>Profile</h1>

        {/* Profile card */}
        <div className="card" style={{ padding: 0, overflow: 'hidden', marginBottom: 20 }}>
          {/* Banner */}
          <div style={{ height: 100, background: 'linear-gradient(135deg, var(--primary-dark), var(--primary), var(--teal))', position: 'relative' }} />
          {/* Avatar */}
          <div style={{ paddingLeft: 32, paddingRight: 32, paddingBottom: 24, position: 'relative' }}>
            <div style={{
              width: 80, height: 80, borderRadius: '50%', marginTop: -40,
              background: 'linear-gradient(135deg, var(--primary), var(--teal))',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              color: 'white', fontSize: 28, fontWeight: 800,
              border: '4px solid white',
              boxShadow: 'var(--shadow-md)',
              marginBottom: 16,
            }}>
              {getInitials(user?.name || 'A')}
            </div>
            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 22, fontWeight: 800, marginBottom: 4 }}>{user?.name || 'Admin'}</h2>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              <span className="badge badge-blue"><Shield size={12} /> Admin / Faculty</span>
              <span className="badge badge-teal"><BadgeCheck size={12} /> Verified</span>
            </div>
          </div>
        </div>

        {/* Details */}
        <div className="card" style={{ padding: 24 }}>
          <p style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 18, fontSize: 15 }}>Account Information</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {[
              { icon: User,        label: 'Full Name',   value: user?.name || '—' },
              { icon: Mail,        label: 'Email',       value: user?.email || '—' },
              { icon: Building2,   label: 'Department',  value: user?.department || '—' },
              { icon: Shield,      label: 'Role',        value: 'Admin / Faculty' },
            ].map(({ icon: Icon, label, value }) => (
              <div key={label} style={{ display: 'flex', alignItems: 'center', gap: 14, padding: '12px 16px', background: 'var(--bg)', borderRadius: 'var(--radius)', border: '1px solid var(--border)' }}>
                <div style={{ width: 36, height: 36, borderRadius: 10, background: '#eff6ff', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  <Icon size={17} color="var(--primary)" />
                </div>
                <div>
                  <p style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{label}</p>
                  <p style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{value}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
