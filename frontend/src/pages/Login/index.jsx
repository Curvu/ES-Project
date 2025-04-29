import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import { Button } from 'components/Button';
import { useRequest } from 'hooks/useRequest';
import api from 'api';
import styles from './login.module.css';

const Login = () => {
  const navigate = useNavigate();
  const webcamRef = useRef(null);

  const capture = async () => await api.login({ image: webcamRef.current.getScreenshot() })

  const { doRequest, isLoading } = useRequest(capture, {
    onSuccess: ({ data }) => {
      console.log('Login successful:', data);
      localStorage.setItem('token', data.token);
      navigate('/');
    },
    onError: (error) => console.error('Login failed:', error),
  });

  return (
    <div className={styles.container}>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      <Button onClick={doRequest} isLoading={isLoading}>
        Login
      </Button>
    </div>
  );
};

export default Login;