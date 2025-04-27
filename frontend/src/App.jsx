import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React from 'react';
import Home from 'pages/Home';
import Register from 'pages/Register';
import Login from 'pages/Login';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="*" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App
