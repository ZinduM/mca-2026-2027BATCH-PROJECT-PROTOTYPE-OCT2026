// Format number with commas
export const formatNumber = (n) =>
  n !== undefined && n !== null ? Number(n).toLocaleString('en-IN') : '—';

// Format currency
export const formatCurrency = (n) =>
  n !== undefined && n !== null
    ? `₹${Number(n).toLocaleString('en-IN')}`
    : '—';

// Format percentage
export const formatPercent = (n, decimals = 1) =>
  n !== undefined && n !== null ? `${Number(n).toFixed(decimals)}%` : '—';

// Truncate long strings
export const truncate = (str, len = 80) =>
  str && str.length > len ? str.slice(0, len) + '…' : str;

// Capitalize first letter
export const capitalize = (str) =>
  str ? str.charAt(0).toUpperCase() + str.slice(1) : '';

// Get initials from name
export const getInitials = (name) =>
  name
    ? name
        .split(' ')
        .map((w) => w[0])
        .join('')
        .slice(0, 2)
        .toUpperCase()
    : '?';

// Attendance color
export const attendanceColor = (pct) => {
  if (pct >= 85) return '#10b981';
  if (pct >= 75) return '#f59e0b';
  return '#ef4444';
};

// Grade color
export const gradeColor = (grade) => {
  const map = {
    'O': '#10b981', 'A+': '#10b981', 'A': '#3b82f6',
    'B+': '#6366f1', 'B': '#8b5cf6', 'C': '#f59e0b',
    'F': '#ef4444',
  };
  return map[grade] || '#64748b';
};

// Format date
export const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
};
