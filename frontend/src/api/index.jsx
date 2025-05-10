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
  getUser: () => request.get('/user'),
  login: (data) => request.post('/force_login', data),
  register: (data) => request.post('/force_register', data),
  logout: () => request.post('/logout'),

  getServices: () => request.get('/services'),
  getService: (id) => request.get(`/services/${id}`),
  bookService: (data) => request.post('/book-service', data),
  getBookings: () => request.get('/bookings'),
};

export default api;