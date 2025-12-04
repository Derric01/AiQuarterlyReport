import axios from 'axios';

// Use relative URLs in production, localhost in development
const api = axios.create({
  baseURL: import.meta.env.MODE === 'production' ? '' : 'http://localhost:8000',
  timeout: 60000, // 60 seconds for AI operations
});

// Data fetching
export const fetchData = async () => {
  const response = await api.get('/fetch');
  return response.data;
};

// Compute metrics
export const computeMetrics = async () => {
  const response = await api.get('/metrics');
  return response.data;
};

// Generate AI report
export const generateReport = async (metrics) => {
  const response = await api.post('/report-ai', { metrics });
  return response.data;
};

// Validate report
export const validateReport = async (report, metrics) => {
  const response = await api.post('/validate-ai', { report, metrics });
  return response.data;
};

// Get style score
export const getStyleScore = async (report) => {
  const response = await api.post('/style-score-ai', { report });
  return response.data;
};

export default api;