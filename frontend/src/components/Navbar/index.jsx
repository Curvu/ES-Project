import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaHome, FaTools, FaBoxOpen } from 'react-icons/fa';
import { IoLogOutOutline } from 'react-icons/io5';
import { Button } from 'components/Button';
import { useRequest } from 'hooks/useRequest';
import api from 'api';
import styles from './navbar.module.css';

export const Navbar = () => {
  const navigate = useNavigate()

  const { doRequest: logout } = useRequest(api.logout, {
    onSuccess: () => {
      localStorage.removeItem('token');
      navigate('/login');
    },
    onError: (err) => console.log('err', err)
  })

  return (
    <nav className={styles.navbar}>
      <div className={styles.topbar}>
        <h1 className={styles.title}>PrimeTech Repairs</h1>
        <ul className={styles.links}>
          <Link to='/' className={styles.link}>
            <FaHome />
            <span>Home</span>
          </Link>
          <Link to='/repair' className={styles.link}>
            <FaTools />
            <span>Repair</span>
          </Link>
          <Link to='/my-services' className={styles.link}>
            <FaBoxOpen />
            <span>My Services</span>
          </Link>
        </ul>
      </div>
      <Button onClick={logout}>
        <IoLogOutOutline />
        <span>Log Out</span>
      </Button>
    </nav>
  );
};