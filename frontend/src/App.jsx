import { BrowserRouter, Route, Routes, Navigate, Outlet } from 'react-router-dom';
import React from 'react';
import Home from 'pages/Home';
import Sign from 'pages/Sign';
import { Skeleton } from 'components/Skeleton';
import { Navbar } from 'components/Navbar';

const isLoggedIn = () => !!localStorage.getItem('token');

const PrivateRoutes = () => {
  return isLoggedIn() ? <Outlet /> : <Navigate to='/sign' replace />;
};

const PublicRoutes = () => {
  return isLoggedIn() ? <Navigate to='/' replace /> : <Outlet />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PrivateRoutes />}>
          <Route element={
            <Skeleton>
              <Navbar />
              <Outlet />
            </Skeleton>
          }>
            <Route path='/' element={<Home />} />
          </Route>
        </Route>
        <Route element={<PublicRoutes />}>
          <Route path='/sign' element={<Sign />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App
