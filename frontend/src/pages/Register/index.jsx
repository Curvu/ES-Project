import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import styles from './register.module.css';
import { api } from 'api';

const Register = () => {
  const webcamRef = useRef(null);
  const [name, setName] = useState('');

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    console.log(imageSrc);

    api.register({ image: imageSrc, name })
      .then((response) => {
        console.log('Registration successful:', response);
      })
      .catch((error) => {
        console.error('Registration failed:', error);
      });
  };

  return (
    <div className={styles.container}>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your name"
        className={styles.input}
      />
      <button onClick={capture}>Register</button>
    </div>
  );
};

export default Register;