import React from 'react';
import styles from './button.module.css';

export const Button = ({ children, onClick, disabled = false, isLoading = false, className = '' }) => {
  return (
    <button className={`${styles.button} ${className}`} onClick={onClick} disabled={disabled || isLoading}>
      {!isLoading ? children : <span>Loading...</span>}
    </button>
  );
};