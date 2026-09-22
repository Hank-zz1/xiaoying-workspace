import { memo } from 'react';
import type { TimerStatus } from '../hooks/useTimer';
import styles from './TimerControls.module.css';

interface TimerControlsProps {
  status: TimerStatus;
  isRunning: boolean;
  onStart: () => void;
  onPause: () => void;
  onReset: () => void;
  onSkip: () => void;
}

export const TimerControls = memo(function TimerControls({
  status,
  isRunning,
  onStart,
  onPause,
  onReset,
  onSkip,
}: TimerControlsProps) {
  const isIdle = status === 'idle';
  const isPaused = status === 'paused';
  const isActive = status === 'running' || status === 'resting';

  return (
    <div className={styles.controls}>
      {/* Main play/pause button */}
      {!isActive ? (
        <button className={`${styles.btn} ${styles.primary}`} onClick={onStart}>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z" />
          </svg>
          {isPaused ? '继续' : '开始'}
        </button>
      ) : (
        <button className={`${styles.btn} ${styles.primary}`} onClick={onPause}>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
          </svg>
          暂停
        </button>
      )}

      {/* Skip button */}
      {isActive && (
        <button className={`${styles.btn} ${styles.secondary}`} onClick={onSkip}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z" />
          </svg>
          跳过
        </button>
      )}

      {/* Reset button */}
      {!isIdle && (
        <button className={`${styles.btn} ${styles.ghost}`} onClick={onReset}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.65 6.35A7.958 7.958 0 0012 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0112 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" />
          </svg>
          重置
        </button>
      )}
    </div>
  );
});