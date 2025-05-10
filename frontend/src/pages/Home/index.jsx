import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { Button } from 'components/Button'
import { Card } from 'components/Card'
import { useRequest } from 'hooks/useRequest';
import api from 'api'

import styles from './home.module.css'

function Home() {
  const navigate = useNavigate();

  const { doRequest: getServices, data } = useRequest(api.getServices, {
    onSuccess: (data) => console.log('Services:', data),
  });

  useEffect(() => {
    getServices();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className={styles.home}>
      <section>
        <h2>Services</h2>
        <ul>
          {data?.services?.map((service, idx) => (
            <Card key={`${service.id}-${idx}`} className={styles.card}>
              <h3>{service.name}</h3>
              <p>Description of the service lollol</p>
              <div className={styles.bot}>
                <span className={styles.price}>{service.price}€</span>
                <Button
                  onClick={() => navigate(`/book/${service.id}`, { state: { service } })}
                  disabled={!service.can_book}
                >
                  Book
                </Button>
              </div>
            </Card>
          ))}
          {!data && (
            <div className={styles.noServices}>
              <h3>No services available</h3>
              <p>Please check back later or log in.</p>
            </div>
          )}
        </ul>
      </section>
    </main>
  )
}

export default Home