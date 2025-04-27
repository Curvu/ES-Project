import React, { useRef } from 'react';
import Webcam from 'react-webcam';
import styles from './login.module.css';
import { api } from 'api';

const Login = () => {
  const webcamRef = useRef(null);

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    console.log(imageSrc);

    api.login({ image: imageSrc })
      .then((response) => {
        console.log('Login successful:', response.data);
        // Handle successful login (e.g., redirect to another page)
      })
      .catch((error) => {
        console.error('Login failed:', error);
        // Handle login failure (e.g., show an error message)
      });
  };

  return (
    <div className={styles.container}>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      <button onClick={capture}>Login</button>
    </div>
  );
};

export default Login;