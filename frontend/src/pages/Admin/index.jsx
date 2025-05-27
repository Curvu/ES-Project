import { useEffect } from 'react';

import { useRequest } from 'hooks/useRequest';
import api from 'api'

import styles from './bookings.module.css'
import { ProgressBar } from 'components/ProgressBar';
import { Card } from 'components/Card';
import { Button } from 'components/Button';

function Admin() {
  const { doRequest: getBookings, data, isLoading: isLoading2 } = useRequest(api.getAdminBookings);

  const { doRequest: nextStage, isLoading } = useRequest(api.nextStage, {
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
          />

          <Button
            onClick={() => nextStage(booking.id)}
            disabled={[-1, 2, 5].includes(booking.state)}
            isLoading={isLoading || isLoading2}
          >
            Next Stage
          </Button>
        </Card>
      ))}
    </main>
  )
}

export default Admin