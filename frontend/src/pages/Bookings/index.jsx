import { useEffect, useState } from 'react';

import { useRequest } from 'hooks/useRequest';
import { ProgressBar } from 'components/ProgressBar';
import { Card } from 'components/Card';
import { Button } from 'components/Button';
import api from 'api'

import styles from './bookings.module.css'

function Bookings() {
  const [paidServiceIds, setPaidServiceIds] = useState([]);

  const { doRequest: getBookings, data } = useRequest(api.getBookings);

  const { doRequest: payService, isLoading } = useRequest(api.payService, {
    onSuccess: (data) => setPaidServiceIds((prev) => [...prev, data.id]),
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
              disabled={!booking?.can_pay || paidServiceIds.includes(booking.id) || isLoading}
            >
              Pay
            </Button>
            {booking.paid ? 'Paid' : 'Not Paid'}
          </div>
          <ProgressBar
            labels={['Scheduled', 'Repairing', 'Waiting for Pickup', 'Delivered']}
            currentIndex={parseInt(booking.state)}
          />
        </Card>
      ))}
    </main>
  )
}

export default Bookings