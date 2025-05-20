import { useEffect } from 'react';

import { useRequest } from 'hooks/useRequest';
import { ProgressBar } from 'components/ProgressBar';
import { Card } from 'components/Card';
import { Button } from 'components/Button';
import api from 'api'

import styles from './bookings.module.css'

function Bookings() {
  const { doRequest: getBookings, data, isLoading: isLoading2 } = useRequest(api.getBookings);

  const { doRequest: payService, isLoading } = useRequest(api.payService, {
    onSuccess: () => getBookings(),
  });

  useEffect(() => {
    getBookings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <main className={styles.bookings}>
      <h1>Bookings</h1>

      {data?.bookings?.map((booking) => (
        <Card key={booking.id} className={styles.booking}>
          <div>
            <h3>{booking.type}</h3>
            <Button
              className={styles.button}
              onClick={() => payService(booking.id)}
              disabled={!booking?.can_pay || isLoading || isLoading2}
            >
              Pay
            </Button>
            {booking.paid ? 'Paid' : 'Not Paid'}
          </div>
          <ProgressBar
            labels={['Schedule', 'Payment', 'Repairing', 'Delivery']}
            currentIndex={parseInt(booking.state)}
          />
        </Card>
      ))}
    </main>
  )
}

export default Bookings