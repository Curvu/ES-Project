import { useEffect } from 'react';

import { useRequest } from 'hooks/useRequest';
import api from 'api'

import styles from './bookings.module.css'
import { ProgressBar } from 'components/ProgressBar';
import { Card } from 'components/Card';

function Bookings() {
  const { doRequest: getBookings, data } = useRequest(api.getBookings);

  useEffect(() => {
    getBookings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  console.log(data)

  return (
    <main className={styles.bookings}>
      <h1>Bookings</h1>

      {data?.bookings?.map((booking) => (
        <Card key={booking.id} className={styles.booking}>
          <h3>{booking.service_type}</h3>
          <ProgressBar labels={['Scheduled', 'Repairing', 'Waiting for Pickup', 'Finished']} currentIndex={booking.service_state} />

          {/* TODO: if service_state > 1 then show pay button, also change card if state is -1 */}
        </Card>
      ))}
    </main>
  )
}

export default Bookings