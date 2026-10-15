import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Auth ──────────────────────────────────────────────────────────────────────
export const loginUser = (email, password, role) =>
  api.post('/api/login', {
    email: email.trim().toLowerCase(),
    password: password.trim(),
    role: role.trim().toLowerCase()
  }).then(r => r.data);

// ── Dashboard Stats ───────────────────────────────────────────────────────────
export const getDashboardStats = () =>
  api.get('/api/dashboard/stats').then(r => r.data);

export const getDepartmentStats = () =>
  api.get('/api/dashboard/department-stats').then(r => r.data);

// ── NLP Query (Carries role and student_id) ───────────────────────────────────
export const processQuery = (query, student_id = null, role = 'admin') =>
  api.post('/api/query', { query, student_id, role }).then(r => r.data);

// ── Student ───────────────────────────────────────────────────────────────────
export const getStudentProfile = (id) =>
  api.get(`/api/student/${id}/profile`).then(r => r.data);

export const getStudentAcademics = (id) =>
  api.get(`/api/student/${id}/academics`).then(r => r.data);

export const getStudentAttendance = (id) =>
  api.get(`/api/student/${id}/attendance`).then(r => r.data);

export const getStudentFees = (id) =>
  api.get(`/api/student/${id}/fees`).then(r => r.data);

export const getStudentScholarships = (id) =>
  api.get(`/api/student/${id}/scholarships`).then(r => r.data);

export const getStudentSuggestions = (id) =>
  api.get(`/api/student/${id}/suggestions`).then(r => r.data);

// ── Documents ─────────────────────────────────────────────────────────────────
export const searchDocuments = (query, top_k = 5) =>
  api.post('/api/documents/search', { query, top_k }).then(r => r.data);

export const listDocuments = () =>
  api.get('/api/documents').then(r => r.data);

// ── Information Retrieval Recommendation & Search ─────────────────────────────
export const getRecommendedScholarships = (studentId, query = '', top_k = 12) =>
  api.post('/api/recommendations/scholarships', { student_id: studentId, query, top_k }).then(r => r.data);

export const getRecommendedInternships = (studentId, query = '', top_k = 12) =>
  api.post('/api/recommendations/internships', { student_id: studentId, query, top_k }).then(r => r.data);

export const searchScholarshipsAdmin = (query = '', min_amount = null, top_k = 30) =>
  api.post('/api/scholarships/search', { query, min_amount, top_k }).then(r => r.data);

export const searchInternshipsAdmin = (query = '', domain = null, top_k = 30) =>
  api.post('/api/internships/search', { query, domain, top_k }).then(r => r.data);

export const listScholarships = () =>
  api.get('/api/scholarships').then(r => r.data);

// ── External (Crawled / Knowledge Base) ────────────────────────────────────────
export const getExternalScholarships = () =>
  api.get('/api/external/scholarships').then(r => r.data);

export const getExternalInternships = () =>
  api.get('/api/external/internships').then(r => r.data);

export const getExternalAnnouncements = () =>
  api.get('/api/external/announcements').then(r => r.data);

export const searchExternal = (query, category = null, top_k = 10) =>
  api.post('/api/external/search', { query, category, top_k }).then(r => r.data);

// ── Utilities ─────────────────────────────────────────────────────────────────
export const listDepartments = () =>
  api.get('/api/departments').then(r => r.data);

export const listInternships = () =>
  api.get('/api/internships').then(r => r.data);

export const getSampleQueries = () =>
  api.get('/api/sample-queries').then(r => r.data);

export const healthCheck = () =>
  api.get('/api/health').then(r => r.data);

export default api; 