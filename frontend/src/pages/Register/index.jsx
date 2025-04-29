import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import api from 'api';
import { useRequest } from 'hooks/useRequest';
import { Button } from 'components/Button';
import styles from './register.module.css';

const Register = () => {
  const navigate = useNavigate();
  const webcamRef = useRef(null);
  const [name, setName] = useState('');

  const capture = async () => await api.register({ image: webcamRef.current.getScreenshot() })

  const { doRequest, isLoading } = useRequest(capture, {
    onSuccess: ({ data }) => {
      console.log('Register successful:', data);
      navigate('/login');
    },
    onError: (error) => console.error('Register failed:', error),
  });

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
      <Button onClick={doRequest} isLoading={isLoading}>
        Register
      </Button>
    </div>
  );
};

export default Register;