import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Eye, EyeOff, Shield, GraduationCap, LogIn, AlertCircle, Building2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { loginUser } from '../services/api';

export default function LoginPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { login, isAuthenticated, user } = useAuth();

  const [role, setRole] = useState(searchParams.get('role') || 'admin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Redirect if already logged in
  useEffect(() => {
    if (isAuthenticated && user) {
      navigate(user.role === 'admin' ? '/admin/dashboard' : '/student/dashboard');
    }
  }, [isAuthenticated, user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) {
      setError('Please fill in all fields.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const data = await loginUser(email.trim(), password.trim(), role);
      if (data.success) {
        login(data);
        navigate(data.role === 'admin' ? '/admin/dashboard' : '/student/dashboard');
      }
    } catch (err) {
      const msg = err?.response?.data?.detail || 'Invalid credentials. Please check your role, email, and password.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      width: '100%',
      display: 'flex',
      flexWrap: 'wrap',
      backgroundColor: '#0f172a',
      fontFamily: 'var(--font-sans)',
      overflowX: 'hidden'
    }}>
      {/* ── LEFT SIDE: Full-height Hero & Imagery ── */}
      <div style={{
        flex: '1 1 500px',
        minHeight: '400px',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: 'clamp(32px, 5vw, 64px)',
        backgroundImage: 'url("https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1600&q=80")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}>
        {/* Dark readability overlay with blue/teal gradient accent */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 58, 138, 0.88) 50%, rgba(13, 148, 136, 0.85) 100%)',
          zIndex: 1,
        }} />

        {/* Brand Header */}
        <div style={{ position: 'relative', zIndex: 2, display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{
            width: 44,
            height: 44,
            background: 'linear-gradient(135deg, var(--primary), var(--teal))',
            borderRadius: 12,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 8px 16px rgba(0,0,0,0.25)'
          }}>
            <Building2 size={24} color="#ffffff" />
          </div>
          <div>
            <span style={{
              fontFamily: 'var(--font-display)',
              fontWeight: 800,
              fontSize: 22,
              color: '#ffffff',
              letterSpacing: '-0.5px'
            }}>
              College ERP
            </span>
          </div>
        </div>

        {/* Center/Bottom Highlight Content */}
        <div style={{ position: 'relative', zIndex: 2, maxWidth: 540, margin: '40px 0' }}>
          <span style={{
            display: 'inline-block',
            padding: '6px 14px',
            background: 'rgba(255, 255, 255, 0.12)',
            backdropFilter: 'blur(8px)',
            borderRadius: 99,
            fontSize: 13,
            fontWeight: 600,
            color: '#99f6e4',
            marginBottom: 20,
            border: '1px solid rgba(255, 255, 255, 0.2)'
          }}>
            Welcome to the Campus Portal
          </span>

          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(32px, 4vw, 48px)',
            fontWeight: 800,
            lineHeight: 1.15,
            color: '#ffffff',
            letterSpacing: '-1px',
            marginBottom: 16
          }}>
            College ERP Management System
          </h1>

          <p style={{
            fontSize: 'clamp(15px, 1.8vw, 18px)',
            color: '#e2e8f0',
            lineHeight: 1.6,
            maxWidth: 480
          }}>
            Secure portal for students, faculty and administrators.
          </p>
        </div>

        {/* Left Footer info badge */}
        <div style={{ position: 'relative', zIndex: 2 }}>
          <p style={{ fontSize: 13, color: 'rgba(255, 255, 255, 0.65)' }}>
            Empowering institutional administration and academic excellence.
          </p>
        </div>
      </div>

      {/* ── RIGHT SIDE: Modern Glass-Card Form ── */}
      <div style={{
        flex: '1 1 450px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 'clamp(24px, 4vw, 48px)',
        background: 'linear-gradient(135deg, #f0fdfa 0%, #f0f9ff 50%, #eff6ff 100%)',
        position: 'relative'
      }}>
        {/* Soft background glow dots */}
        <div style={{
          position: 'absolute',
          width: 320,
          height: 320,
          background: 'radial-gradient(circle, rgba(13,148,136,0.15) 0%, transparent 70%)',
          top: 0,
          right: 0,
          borderRadius: '50%'
        }} />

        {/* Glass Card Container */}
        <div style={{
          width: '100%',
          maxWidth: 460,
          background: 'rgba(255, 255, 255, 0.90)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          borderRadius: 24,
          padding: 'clamp(28px, 4vw, 40px)',
          boxShadow: '0 20px 40px -15px rgba(30, 64, 175, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.8)',
          position: 'relative',
          zIndex: 2
        }}>
          <div style={{ marginBottom: 20 }}>
            <h2 style={{
              fontFamily: 'var(--font-display)',
              fontWeight: 800,
              fontSize: 26,
              color: 'var(--text-primary)',
              marginBottom: 4
            }}>
              College ERP
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>
              Sign in to your {role === 'admin' ? 'Faculty / Admin' : 'Student'} account
            </p>
          </div>

          {/* ── VISIBLE ROLE SELECTOR ── */}
          <div style={{
            display: 'flex',
            background: '#e2e8f0',
            padding: 4,
            borderRadius: 12,
            marginBottom: 20,
            border: '1px solid #cbd5e1'
          }}>
            <button
              type="button"
              id="role-admin-btn"
              onClick={() => { setRole('admin'); setError(''); }}
              style={{
                flex: 1,
                padding: '10px 14px',
                borderRadius: 8,
                border: 'none',
                cursor: 'pointer',
                fontSize: 13,
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 8,
                background: role === 'admin' ? '#ffffff' : 'transparent',
                color: role === 'admin' ? '#1e40af' : '#64748b',
                boxShadow: role === 'admin' ? '0 2px 8px rgba(0,0,0,0.12)' : 'none',
                transition: 'all 0.2s ease',
              }}
            >
              <Shield size={16} />
              Admin / Faculty
            </button>

            <button
              type="button"
              id="role-student-btn"
              onClick={() => { setRole('student'); setError(''); }}
              style={{
                flex: 1,
                padding: '10px 14px',
                borderRadius: 8,
                border: 'none',
                cursor: 'pointer',
                fontSize: 13,
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 8,
                background: role === 'student' ? '#ffffff' : 'transparent',
                color: role === 'student' ? '#0d9488' : '#64748b',
                boxShadow: role === 'student' ? '0 2px 8px rgba(0,0,0,0.12)' : 'none',
                transition: 'all 0.2s ease',
              }}
            >
              <GraduationCap size={16} />
              Student
            </button>
          </div>

          {/* Error message */}
          {error && (
            <div style={{
              display: 'flex',
              gap: 10,
              alignItems: 'flex-start',
              padding: '12px 14px',
              marginBottom: 18,
              background: '#fef2f2',
              borderRadius: 10,
              border: '1px solid #fecaca',
            }}>
              <AlertCircle size={16} color="#ef4444" style={{ flexShrink: 0, marginTop: 2 }} />
              <p style={{ fontSize: 13, color: '#dc2626', margin: 0 }}>{error}</p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {/* Username / Email field */}
            <div>
              <label
                htmlFor="login-username"
                style={{
                  display: 'block',
                  fontSize: 13,
                  fontWeight: 600,
                  color: 'var(--text-primary)',
                  marginBottom: 6
                }}
              >
                {role === 'admin' ? 'Faculty / Admin Email' : 'Student Email'}
              </label>
              <input
                id="login-username"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder={role === 'admin' ? 'amit.chauhan32@campusai.edu.in' : 'aditi.gupta5140@student.campusai.edu.in'}
                className="input"
                required
                autoComplete="email"
                style={{
                  width: '100%',
                  padding: '12px 14px',
                  borderRadius: 10,
                  border: '1px solid #cbd5e1',
                  background: '#ffffff',
                  fontSize: 14,
                  outline: 'none',
                  transition: 'border-color 0.2s',
                }}
              />
            </div>

            {/* Password field */}
            <div>
              <label
                htmlFor="login-password"
                style={{
                  display: 'block',
                  fontSize: 13,
                  fontWeight: 600,
                  color: 'var(--text-primary)',
                  marginBottom: 6
                }}
              >
                Password
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  id="login-password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="input"
                  required
                  autoComplete="current-password"
                  style={{
                    width: '100%',
                    padding: '12px 42px 12px 14px',
                    borderRadius: 10,
                    border: '1px solid #cbd5e1',
                    background: '#ffffff',
                    fontSize: 14,
                    outline: 'none',
                    transition: 'border-color 0.2s',
                  }}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: 12,
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    color: 'var(--text-muted)',
                    display: 'flex',
                    alignItems: 'center',
                    padding: 0
                  }}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* Remember Me & Help */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, color: 'var(--text-secondary)', cursor: 'pointer' }}>
                <input
                  id="remember-me"
                  type="checkbox"
                  checked={rememberMe}
                  onChange={e => setRememberMe(e.target.checked)}
                  style={{ width: 16, height: 16, accentColor: 'var(--primary)', cursor: 'pointer' }}
                />
                Remember me
              </label>
              <button
                type="button"
                id="forgot-password-btn"
                style={{
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: 13,
                  color: 'var(--primary)',
                  fontWeight: 600
                }}
                onClick={() => alert('Please contact the college ERP administration office to reset your credentials.')}
              >
                Need Help?
              </button>
            </div>

            {/* Login button */}
            <button
              id="login-submit-btn"
              type="submit"
              disabled={loading}
              className="btn btn-primary"
              style={{
                width: '100%',
                justifyContent: 'center',
                padding: '13px',
                fontSize: 15,
                fontWeight: 600,
                borderRadius: 10,
                marginTop: 6,
                background: role === 'admin'
                  ? 'linear-gradient(135deg, var(--primary), #2563eb)'
                  : 'linear-gradient(135deg, var(--teal), #0d9488)',
                border: 'none',
                color: '#ffffff',
                cursor: loading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                boxShadow: '0 4px 14px rgba(30, 64, 175, 0.25)',
                transition: 'opacity 0.2s ease',
              }}
            >
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span className="spinner" style={{ width: 18, height: 18 }} />
                  Signing in…
                </span>
              ) : (
                <>
                  <LogIn size={18} />
                  Login as {role === 'admin' ? 'Faculty / Admin' : 'Student'}
                </>
              )}
            </button>
          </form>

          {/* Footer note */}
          <div style={{
            marginTop: 20,
            padding: '12px 14px',
            background: 'rgba(248, 250, 252, 0.9)',
            borderRadius: 10,
            border: '1px solid rgba(226, 232, 240, 0.8)',
            textAlign: 'center'
          }}>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', margin: 0 }}>
              {role === 'admin'
                ? 'Faculty login uses @campusai.edu.in'
                : 'Student login uses @student.campusai.edu.in'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}