import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';

// Pages
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';

// Admin pages
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminQueryPage from './pages/admin/AdminQueryPage';
import DocumentSearchPage from './pages/admin/DocumentSearchPage';
import ScholarshipsPage from './pages/admin/ScholarshipsPage';
import AdminProfile from './pages/admin/AdminProfile';
import AdminSettings from './pages/admin/AdminSettings';

// Student pages
import StudentDashboard from './pages/student/StudentDashboard';
import StudentQueryPage from './pages/student/StudentQueryPage';
import StudentDocumentSearch from './pages/student/StudentDocumentSearch';
import StudentScholarships from './pages/student/StudentScholarships';
import StudentProfile from './pages/student/StudentProfile';
import StudentSettings from './pages/student/StudentSettings';

// Protected route wrapper
function RequireAuth({ children, allowedRole }) {
  const { user, isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (allowedRole && user?.role !== allowedRole) {
    return <Navigate to={user?.role === 'admin' ? '/admin/dashboard' : '/student/dashboard'} replace />;
  }
  return children;
}

function AppRoutes() {
  const { user, isAuthenticated } = useAuth();

  return (
    <Routes>
      {/* Default route opens login directly */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />

      {/* Admin/Faculty routes */}
      <Route path="/admin/dashboard" element={<RequireAuth allowedRole="admin"><AdminDashboard /></RequireAuth>} />
      <Route path="/admin/query" element={<RequireAuth allowedRole="admin"><AdminQueryPage /></RequireAuth>} />
      <Route path="/admin/documents" element={<RequireAuth allowedRole="admin"><DocumentSearchPage /></RequireAuth>} />
      <Route path="/admin/scholarships" element={<RequireAuth allowedRole="admin"><ScholarshipsPage /></RequireAuth>} />
      <Route path="/admin/profile" element={<RequireAuth allowedRole="admin"><AdminProfile /></RequireAuth>} />
      <Route path="/admin/settings" element={<RequireAuth allowedRole="admin"><AdminSettings /></RequireAuth>} />

      {/* Student routes */}
      <Route path="/student/dashboard" element={<RequireAuth allowedRole="student"><StudentDashboard /></RequireAuth>} />
      <Route path="/student/query" element={<RequireAuth allowedRole="student"><StudentQueryPage /></RequireAuth>} />
      <Route path="/student/documents" element={<RequireAuth allowedRole="student"><StudentDocumentSearch /></RequireAuth>} />
      <Route path="/student/scholarships" element={<RequireAuth allowedRole="student"><StudentScholarships /></RequireAuth>} />
      <Route path="/student/profile" element={<RequireAuth allowedRole="student"><StudentProfile /></RequireAuth>} />
      <Route path="/student/settings" element={<RequireAuth allowedRole="student"><StudentSettings /></RequireAuth>} />

      {/* Redirect /dashboard to role-based dashboard */}
      <Route path="/dashboard" element={
        isAuthenticated
          ? <Navigate to={user?.role === 'admin' ? '/admin/dashboard' : '/student/dashboard'} replace />
          : <Navigate to="/login" replace />
      } />

      {/* 404 */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}