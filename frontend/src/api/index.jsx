import axios from 'axios';

const request = axios.create({
  // baseURL: 'http://localhost:8080',
  baseURL: 'https://django-env.eba-i3yuiuiu.us-east-1.elasticbeanstalk.com/api',
  timeout: 60000,
});

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  config.headers.Authorization = `${token}`;
  config.headers['Content-Type'] = 'application/json';
  return config;
});

const api = {
  login: (data) => request.post('/auth/login/', data),
  register: (data) => request.post('/auth/register/', data),
  logout: () => request.post('/auth/logout/'),

  getServices: () => request.get('/services/'),
  getService: (id) => request.get(`/services/${id}/`),
  getBookings: () => request.get('/services/bookings/'),
  bookService: (data) => request.post('/services/book/', data),
  payService: (id) => request.post(`/services/pay/${id}/`),
  takenSchedules: () => request.get('/services/taken-schedules/'),

  getAdminBookings: () => request.get('/services/admin-bookings/'),
  nextStage: (id) => request.put(`/services/admin-booking/${id}/`),
};

export default api;