'use client';

import styles from './page.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <h1>Welcome to Paper Betting</h1>
      <div className={styles.buttonContainer}>
        <a 
          href="/login"
          className={styles.button}
        >
          Existing User? Login Here
        </a>
        <a 
          href="/register"
          className={styles.button}
        >
          New User? Create Your Account Here
        </a>
      </div>
    </div>
  );
} 