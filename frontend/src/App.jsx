import { BrowserRouter, Route, Routes, Navigate, Outlet } from 'react-router-dom';
import React from 'react';
import Home from 'pages/Home';
import Register from 'pages/Register';
import Login from 'pages/Login';

const isLoggedIn = () => !!localStorage.getItem('token');

const PrivateRoutes = () => {
  return isLoggedIn() ? <Outlet /> : <Navigate to='/login' replace />;
};

const PublicRoutes = () => {
  return isLoggedIn() ? <Navigate to='/' replace /> : <Outlet />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PrivateRoutes />}>
          <Route path='/' element={<Home />} />
        </Route>
        <Route element={<PublicRoutes />}>
          <Route path='/login' element={<Login />} />
          <Route path='/register' element={<Register />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App
