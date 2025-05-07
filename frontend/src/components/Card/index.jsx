import React from 'react';
import styles from './card.module.css';

export const Card = ({ children, className = '' }) => {
  return (
    <div className={`${styles.card} ${className}`}>
      {children}
    </div>
  );
};