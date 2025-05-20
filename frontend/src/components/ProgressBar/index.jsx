import React from 'react';
import { useRequest } from 'hooks/useRequest';
import api from 'api';

import styles from './progressbar.module.css'

export const ProgressBar = ({ labels, currentIndex, clickable=false, booking={}, onSuccess=()=>{} }) => {
  const { doRequest } = useRequest(api.setBookingState, {
    onSuccess: () => onSuccess()
  });

  return (
    <div className={styles.progress}>
      {labels.map((label, index) => {
        let isError = currentIndex === -1 && index === 0
        let isActive = index < currentIndex - 1
        let isCurrent = index === currentIndex - 1
        let isLast = index === labels.length - 1 && !booking?.paid;

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
              <button
                className={styles.index}
                disabled={!clickable || isActive || isCurrent || currentIndex === -1 || isLast}
                onClick={() => doRequest({ service_id: booking.id, state: index+1 })}
              >{index + 1}</button>
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