import React from 'react';
import styles from './skeleton.module.css';

export const Skeleton = ({ children }) => {
  return (
    <div className={styles.skeleton}>
      {children}
    </div>
  );
};