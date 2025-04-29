import { useEffect } from 'react'
import reactLogo from 'assets/react.svg'
import viteLogo from '/vite.svg'
import { Button } from 'components/Button'
import './home.css'
import { useRequest } from 'hooks/useRequest'
import api from 'api'

function Home() {
  const { doRequest: doRequestWithToken } = useRequest(api.hello_world_with_token, {
    onSuccess: (res) => console.log('res_wt', res),
    onError: (err) => console.log('err_wt', err)
  })
  const { doRequest } = useRequest(api.hello_world, {
    onSuccess: (res) => console.log('res', res),
    onError: (err) => console.log('err', err)
  })

  useEffect(() => {
    doRequest()
    doRequestWithToken()
    // eslint-disable-next-line
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <Button onClick={() => localStorage.removeItem('token')}>
        Clear token
      </Button>
    </>
  )
}

export default Home