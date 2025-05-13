import React, { useEffect } from 'react';
import { useRequest } from 'hooks/useRequest';
import api from 'api';

import styles from './progressbar.module.css'

export const ProgressBar = ({ labels, currentIndex, clickable=false, booking={} }) => {
  const { data, setData, doRequest } = useRequest(api.setBookingState);

  useEffect(() => {
    setData({state: currentIndex});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentIndex]);

  return (
    <div className={styles.progress}>
      {labels.map((label, index) => {
        let isError = data?.state === -1 && index === 0
        let isActive = index < data?.state - 1
        let isCurrent = index === data?.state - 1

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
                disabled={!clickable || isActive || isCurrent || data?.state === -1}
                onClick={() => doRequest({ booking_id: booking.id, state: index+1 })}
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