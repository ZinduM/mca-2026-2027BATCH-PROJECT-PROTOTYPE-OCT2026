import { AlertTriangle, Info, CheckCircle, XCircle, X } from 'lucide-react';
import { useState } from 'react';

const icons = {
  error:   { Icon: XCircle,       bg: '#fef2f2', border: '#fecaca', text: '#dc2626', iconColor: '#ef4444' },
  warning: { Icon: AlertTriangle, bg: '#fffbeb', border: '#fde68a', text: '#b45309', iconColor: '#f59e0b' },
  success: { Icon: CheckCircle,   bg: '#f0fdf4', border: '#bbf7d0', text: '#15803d', iconColor: '#10b981' },
  info:    { Icon: Info,          bg: '#eff6ff', border: '#bfdbfe', text: '#1d4ed8', iconColor: '#3b82f6' },
};

export default function Alert({ type = 'info', title, message, dismissible = true, className = '' }) {
  const [visible, setVisible] = useState(true);
  if (!visible) return null;

  const { Icon, bg, border, text, iconColor } = icons[type] || icons.info;

  return (
    <div
      className={`animate-fade-in ${className}`}
      style={{
        display: 'flex',
        gap: 12,
        padding: '14px 16px',
        borderRadius: 'var(--radius)',
        background: bg,
        border: `1px solid ${border}`,
        color: text,
      }}
    >
      <Icon size={20} color={iconColor} style={{ flexShrink: 0, marginTop: 1 }} />
      <div style={{ flex: 1 }}>
        {title && <p style={{ fontWeight: 600, marginBottom: 2 }}>{title}</p>}
        <p style={{ fontSize: 14 }}>{message}</p>
      </div>
      {dismissible && (
        <button
          onClick={() => setVisible(false)}
          style={{ background: 'none', border: 'none', cursor: 'pointer', color: text, padding: 2 }}
        >
          <X size={16} />
        </button>
      )}
    </div>
  );
}
