import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Bot, FileSearch, GraduationCap,
  User, Settings, LogOut, Brain, ChevronRight,
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { getInitials } from '../utils/format';

const adminNav = [
  { to: '/admin/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/admin/query',     icon: Bot,             label: 'AI Query Assistant' },
  { to: '/admin/documents', icon: FileSearch,       label: 'Document Search' },
  { to: '/admin/scholarships', icon: GraduationCap, label: 'Scholarships & Internships' },
  { to: '/admin/profile',   icon: User,            label: 'Profile' },
  { to: '/admin/settings',  icon: Settings,        label: 'Settings' },
];

const studentNav = [
  { to: '/student/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/student/query',     icon: Bot,             label: 'AI Query Assistant' },
  { to: '/student/documents', icon: FileSearch,       label: 'Document Search' },
  { to: '/student/scholarships', icon: GraduationCap, label: 'Scholarships & Internships' },
  { to: '/student/profile',   icon: User,            label: 'Profile' },
  { to: '/student/settings',  icon: Settings,        label: 'Settings' },
];

function SidebarNav({ items }) {
  return (
    <nav style={{ padding: '8px 12px', flex: 1 }}>
      {items.map(({ to, icon: Icon, label }) => (
        <NavLink
          key={to}
          to={to}
          style={({ isActive }) => ({
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            padding: '10px 14px',
            borderRadius: 'var(--radius)',
            marginBottom: 4,
            textDecoration: 'none',
            fontSize: 14,
            fontWeight: isActive ? 600 : 500,
            color: isActive ? 'var(--primary)' : 'var(--text-secondary)',
            background: isActive ? 'linear-gradient(135deg, #eff6ff, #f0fdff)' : 'transparent',
            borderLeft: isActive ? '3px solid var(--primary)' : '3px solid transparent',
            transition: 'all 0.2s',
          })}
        >
          {({ isActive }) => (
            <>
              <Icon size={18} color={isActive ? 'var(--primary)' : 'var(--text-muted)'} />
              <span style={{ flex: 1 }}>{label}</span>
              {isActive && <ChevronRight size={14} color="var(--primary)" />}
            </>
          )}
        </NavLink>
      ))}
    </nav>
  );
}

export default function DashboardLayout({ children, role = 'admin' }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const navItems = role === 'admin' ? adminNav : studentNav;

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg)' }}>
      {/* Sidebar */}
      <aside style={{
        width: 260,
        minHeight: '100vh',
        background: 'white',
        borderRight: '1px solid var(--border)',
        display: 'flex',
        flexDirection: 'column',
        position: 'fixed',
        top: 0, left: 0,
        zIndex: 100,
        boxShadow: '2px 0 8px rgba(0,0,0,0.04)',
      }}>
        {/* Logo */}
        <div style={{
          padding: '20px 24px',
          borderBottom: '1px solid var(--border)',
          background: 'linear-gradient(135deg, var(--primary-dark), var(--primary))',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{
              width: 38, height: 38,
              background: 'rgba(255,255,255,0.2)',
              borderRadius: 'var(--radius)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              backdropFilter: 'blur(8px)',
            }}>
              <Brain size={22} color="white" />
            </div>
            <div>
              <p style={{ color: 'white', fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 18, lineHeight: 1.1 }}>CampusAI</p>
              <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: 11 }}>
                {role === 'admin' ? 'Admin / Faculty' : 'Student Portal'}
              </p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <SidebarNav items={navItems} />

        {/* User + Logout */}
        <div style={{ borderTop: '1px solid var(--border)', padding: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 12px', borderRadius: 'var(--radius)', background: 'var(--bg)', marginBottom: 8 }}>
            <div style={{
              width: 36, height: 36, borderRadius: '50%', flexShrink: 0,
              background: 'linear-gradient(135deg, var(--primary), var(--teal))',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              color: 'white', fontWeight: 700, fontSize: 13,
            }}>
              {getInitials(user?.name || 'User')}
            </div>
            <div style={{ overflow: 'hidden' }}>
              <p style={{ fontWeight: 600, fontSize: 13, color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {user?.name || 'User'}
              </p>
              <p style={{ fontSize: 11, color: 'var(--text-muted)' }}>{user?.department || ''}</p>
            </div>
          </div>
          <button
            id="sidebar-logout-btn"
            onClick={handleLogout}
            className="btn btn-ghost"
            style={{ width: '100%', justifyContent: 'flex-start', color: 'var(--error)', padding: '8px 12px' }}
          >
            <LogOut size={16} />
            Logout
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main style={{ marginLeft: 260, flex: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        {children}
      </main>
    </div>
  );
}
