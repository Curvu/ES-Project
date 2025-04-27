import axios from 'axios';

const getAxiosInstance = (type) => {
  const axiosInstance = axios.create({
    baseURL: 'http://localhost:8080',
    timeout: 15000,
  });

  axiosInstance.interceptors.request.use((config) => {
    // const token = localStorage.getItem('token');
    // config.headers.Authorization = `${token}`;
    config.headers['Content-Type'] =
      type === 'json' ? 'application/json' : 'multipart/form-data';
    return config;
  });

  return axiosInstance;
};

const request = getAxiosInstance('json');

export const api = {
  login: (data) => request.post('/login', data),
  register: (data) => request.post('/register', data),
};