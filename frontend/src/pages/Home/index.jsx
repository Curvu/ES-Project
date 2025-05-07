import { Button } from 'components/Button'
import styles from './home.module.css'
import { Card } from 'components/Card'

function Home() {
  return (
    <main className={styles.home}>
      <section>
        <h2>Services</h2>
        <ul>
          <Card className={styles.card}>
            <h3>Service 1</h3>
            <p>Description of Service 1</p>
            <div className={styles.bot}>
              <span className={styles.price}>100€</span>
              <Button onClick={() => alert('Service 1 clicked!')}>Schedule</Button>
            </div>
          </Card>
        </ul>
      </section>
    </main>
  )
}

export default Home