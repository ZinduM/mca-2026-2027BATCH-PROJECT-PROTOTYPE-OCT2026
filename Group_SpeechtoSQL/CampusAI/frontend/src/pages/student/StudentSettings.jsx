import DashboardLayout from '../../layouts/DashboardLayout';
import { Bell, Lock, Palette, Info } from 'lucide-react';

export default function StudentSettings() {
  return (
    <DashboardLayout role="student">
      <div style={{ padding: '28px 32px', maxWidth: 700, margin: '0 auto' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 24 }}>Settings</h1>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {[
            { icon: Bell,    title: 'Notifications', desc: 'Manage alerts for fees, attendance, and exam updates' },
            { icon: Lock,    title: 'Security',       desc: 'Change password and manage account security' },
            { icon: Palette, title: 'Appearance',     desc: 'Light theme active (dark mode coming soon)' },
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card" style={{ padding: '20px 24px', display: 'flex', alignItems: 'center', gap: 16 }}>
              <div style={{ width: 44, height: 44, borderRadius: 12, background: '#f0fdf4', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                <Icon size={20} color="var(--teal)" />
              </div>
              <div style={{ flex: 1 }}>
                <p style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: 2 }}>{title}</p>
                <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>{desc}</p>
              </div>
              <button className="btn btn-outline btn-sm">Configure</button>
            </div>
          ))}

          <div className="card" style={{ padding: '20px 24px', background: '#f0fdf4', borderColor: '#bbf7d0' }}>
            <div style={{ display: 'flex', gap: 14 }}>
              <Info size={20} color="#15803d" style={{ flexShrink: 0, marginTop: 2 }} />
              <div>
                <p style={{ fontWeight: 700, color: '#15803d', marginBottom: 4 }}>CampusAI v1.0.0 — Student Portal</p>
                <p style={{ fontSize: 13, color: '#16a34a' }}>Use the AI Query Assistant to ask questions about your academics anytime.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
