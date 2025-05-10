import { BrowserRouter, Route, Routes, Navigate, Outlet } from 'react-router-dom';
import React from 'react';
import Home from 'pages/Home';
import Sign from 'pages/Sign';
import Service from 'pages/Service';
import Bookings from 'pages/Bookings';
import { Skeleton } from 'components/Skeleton';
import { Navbar } from 'components/Navbar';

const isLoggedIn = () => !!localStorage.getItem('token');

const PrivateRoutes = () => {
  return isLoggedIn() ? <Outlet /> : <Navigate to='/sign' replace />;
};

const LoggedOutRoutes = () => {
  return isLoggedIn() ? <Navigate to='/' replace /> : <Outlet />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='*' element={<Navigate to='/' replace />} />
        <Route element={
          <Skeleton>
            <Navbar />
            <Outlet />
          </Skeleton>
        }>
          <Route path='/' element={<Home />} />

          <Route element={<PrivateRoutes />}>
            <Route path='/book/:service' element={<Service />} />
            <Route path='/my-bookings' element={<Bookings />} />
          </Route>

          <Route element={<LoggedOutRoutes />}>
            <Route path='/sign' element={<Sign />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App
