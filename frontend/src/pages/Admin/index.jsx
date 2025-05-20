import { useEffect } from 'react';

import { useRequest } from 'hooks/useRequest';
import api from 'api'

import styles from './bookings.module.css'
import { ProgressBar } from 'components/ProgressBar';
import { Card } from 'components/Card';
import { Button } from 'components/Button';

function Admin() {
  const { doRequest: getBookings, data } = useRequest(api.getAdminBookings);

  const { doRequest: nextStage } = useRequest(api.nextStage, {
    onSuccess: () => getBookings(),
    onError: (error) => {
      console.log(error)
      alert('Error moving to next stage')
    }
  });

  useEffect(() => {
    getBookings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <main className={styles.bookings}>
      <h1>Admin Bookings</h1>

      {data?.bookings?.map((booking) => (
        <Card key={booking.id} className={styles.booking}>
          <h3>{booking.type}</h3>
          <ProgressBar
            labels={['Schedule', 'Payment', 'Repairing', 'Delivery']}
            currentIndex={booking.state}
            booking={booking}
          />

          <Button
            onClick={() => nextStage(booking.id)}
            disabled={booking.state === 2 || booking.state === 5}
          >
            Next Stage
          </Button>
        </Card>
      ))}
    </main>
  )
}

export default Admin