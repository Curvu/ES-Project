import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import api from 'api';
import { useRequest } from 'hooks/useRequest';
import { Button } from 'components/Button';
import styles from './sign.module.css';
import { useUser } from 'context/UserContext';

const Sign = () => {
  const navigate = useNavigate();
  const webcamRef = useRef(null);
  const [isLogin, setIsLogin] = useState(true);
  const [name, setName] = useState('');
  const [image, setImage] = useState(null);
  const [images, setImages] = useState([]);

  const { login } = useUser();

  const loginReq = async () =>  await api.login({ image });
  const registerReq = async () => await api.register({ name, images });

  const { doRequest: doSign, isLoading: isSigning } = useRequest(
    async () => isLogin ? loginReq() : registerReq(), {
      onSuccess: (data) => {
        localStorage.setItem('token', data.token);
        login(data.user);
        navigate('/');
      },
      onError: (err) => {
        console.error(err);
        alert('Error signing in');
      }
    }
  );

  const handleCapture = async () => {
    if (!webcamRef.current) return;

    const screenshot = webcamRef.current.getScreenshot();
    setImage(screenshot);

    if (isLogin) return;
    // Keep the last 5 images
    setImages((prev) => {
      const newImages = [...prev, screenshot];
      if (newImages.length > 5) newImages.shift();
      return newImages;
    });
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setImage(null);
    setName('');
    setImages([]);
  };

  const isButtonDisabled = isLogin
    ? !image
    : images.length < 5 || !name;

  return (
    <main className={styles.main}>
      <h1>{isLogin ? 'Login with Face' : 'Register with Face'}</h1>

      <div className={styles.webcamContainer}>
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          mirrored
          disablePictureInPicture
        />
        <button className={styles.captureButton} onClick={handleCapture}>
          <div className={styles.captureCircle}></div>
        </button>
      </div>

      {!isLogin && (
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your name"
          className={styles.input}
        />
      )}

      <Button onClick={doSign} isLoading={isSigning} disabled={isButtonDisabled}>
        {isLogin
          ? 'Login'
          : `Register (${images.length}/5)`}
      </Button>

      <Button onClick={toggleMode}>
        Switch to {isLogin ? 'Register' : 'Login'}
      </Button>
    </main>
  );
};

export default Sign;