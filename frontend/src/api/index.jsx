import axios from 'axios';

const getAxiosInstance = (type) => {
  const axiosInstance = axios.create({
    baseURL: 'http://localhost:8080',
    timeout: 60000,
  });

  axiosInstance.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    config.headers.Authorization = `${token}`;
    config.headers['Content-Type'] =
      type === 'json' ? 'application/json' : 'multipart/form-data';
    return config;
  });

  return axiosInstance;
};

const request = getAxiosInstance('json');

const api = {
  login: (data) => request.post('/auth/login/', data),
  register: (data) => request.post('/auth/register/', data),
  logout: () => request.post('/auth/logout/'),

  getServices: () => request.get('/services/'),
  getService: (id) => request.get(`/services/${id}/`),
  getBookings: () => request.get('/services/bookings/'),
  bookService: (data) => request.post('/services/book/', data),
  payService: (id) => request.post(`/services/pay/${id}/`),

  getAdminBookings: () => request.get('/services/admin-bookings/'),
  setBookingState: (data) => request.put('/services/admin-booking/', data),
};

export default api;