import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaHome, FaTools, FaBoxOpen } from 'react-icons/fa';
import { IoLogOutOutline, IoLogInOutline } from 'react-icons/io5';
import { Button } from 'components/Button';
import { useRequest } from 'hooks/useRequest';
import api from 'api';
import { useUser } from 'context/UserContext';
import styles from './navbar.module.css';

export const Navbar = () => {
  const navigate = useNavigate()

  const { user, logout } = useUser();

  const { doRequest: doLogout } = useRequest(api.logout, {
    onSuccess: () => {
      localStorage.removeItem('token');
      logout();
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
          <Link to='/book-a-repair' className={styles.link}>
            <FaTools />
            <span>Book a Repair</span>
          </Link>
          <Link to='/my-repairs' className={styles.link}>
            <FaBoxOpen />
            <span>My Repairs</span>
          </Link>
        </ul>
      </div>
      <div className={styles.bottom}>
        {user ? (
          <>
            <span>{user.username}</span>
            <Button onClick={doLogout}>
              <IoLogOutOutline />
              <span>Log Out</span>
            </Button>
          </>
        ) : (
          <Link to='/sign' className={styles.link}>
            <IoLogInOutline />
            <span>Log In</span>
          </Link>
        )}
      </div>
    </nav>
  );
};