import React from 'react';

import styles from './progressbar.module.css'

export const ProgressBar = ({ labels, currentIndex }) => {
  return (
    <div className={styles.progress}>
      {labels.map((label, index) => {
        let isError = currentIndex === -1 && index === 0
        let isActive = index < currentIndex - 1
        let isCurrent = index === currentIndex - 1

        return (
          <React.Fragment key={label}>
            <div
              className={[
                styles.progressItem,
                isActive && styles.active,
                isCurrent && styles.current,
                isError && styles.error,
              ].filter(Boolean).join(' ')}
            >
              <button className={styles.index}>{index + 1}</button>
              <span className={styles.label}>{label}</span>
            </div>
            {index < labels.length - 1 && (
              <div className={`${styles.lineWrapper} ${isActive ? styles.active : ''}`}>
                <div className={styles.line} />
                <span className={styles.lineLabel}>invisible</span>
              </div>
            )}
          </React.Fragment>
        )
      })}
    </div>
  )
}