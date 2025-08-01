import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaHome, FaTools, FaBoxOpen, FaUserShield } from 'react-icons/fa';
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
    onFinally: () => {
      logout();
      navigate('/sign');
    }
  })

  return (
    <nav className={styles.navbar}>
      <Link to='/' className={styles.title}>
        <span>PrimeTech</span>
        <span>Repairs</span>
      </Link>
      <ul className={styles.links}>
        <Link to='/' className={styles.link}>
          <FaHome />
          <span>Home</span>
        </Link>
        <Link to='/my-bookings' className={styles.link}>
          <FaBoxOpen />
          <span>My Bookings</span>
        </Link>
        {user?.is_admin && (
          <Link to='/admin' className={styles.link}>
            <FaUserShield />
            <span>Admin</span>
          </Link>
        )}
      </ul>
      <div>
        {user ? (
          <Button onClick={doLogout}>
            <span>{user.username}</span>
            <IoLogOutOutline />
          </Button>
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