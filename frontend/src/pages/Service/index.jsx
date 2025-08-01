import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import DatePicker from 'react-datepicker';

import { Button } from 'components/Button'
import { useRequest } from 'hooks/useRequest';
import api from 'api'

import 'react-datepicker/dist/react-datepicker.css';
import styles from './service.module.css'

function Service() {
  const location = useLocation()
  const pathname = location.pathname.split('/')[2]
  const navigate = useNavigate()

  const getNextHour = () => {
    const now = new Date();
    now.setHours(now.getHours() + 1, 0, 0, 0);
    return now;
  }

  const [datetime, setDatetime] = useState(getNextHour());

  const { doRequest: getService, data, setData } = useRequest(api.getService);

  const { doRequest: bookService, isLoading } = useRequest(api.bookService, {
    onSuccess: () => navigate('/my-bookings'),
    onError: (error) => {
      console.log(error)
      alert('Error booking service')
    }
  });

  const { doRequest: getTakenSchedules, data: takenSchedules } = useRequest(api.takenSchedules)

  useEffect(() => {
    if (!location.state?.service) getService(pathname);
    else setData(location.state.service)
    getTakenSchedules()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const onSubmit = (e) => {
    e.preventDefault()

    const normalized = new Date(datetime)
    normalized.setMinutes(normalized.getMinutes(), 0, 0);

    const in1min = new Date();
    in1min.setMinutes(in1min.getMinutes() + 1);

    const booking = {
      service_id: data.id,
      datetime: normalized.toISOString(),
      // datetime: in1min.toISOString(), // this is for testing
    }
    console.log(booking)

    bookService(booking);
  }

  return (
    <main className={styles.service}>
      <h2>{data?.name}</h2>
      <p>{data?.price}€</p>
      <form className={styles.form}>
        <DatePicker
          selected={datetime}
          onChange={(date) => setDatetime(date)}
          showTimeSelect
          dateFormat="dd/MM HH:mm"
          timeFormat="HH:mm"
          timeIntervals={60}
          timeCaption="Hour"
          minDate={new Date()}
        />
        <Button className={styles.button} onClick={onSubmit} disabled={!data?.can_book || isLoading}>
          Book
        </Button>
      </form>

      <div className={styles.takenSchedules}>
        <h3>Taken schedules</h3>
        <ul>
          {takenSchedules?.schedules.map((schedule, idx) => (
            <li key={idx}>
              {schedule}
            </li>
          ))}
        </ul>
      </div>
    </main>
  )
}

export default Service