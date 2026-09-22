import { memo } from 'react';
import styles from './TimerCircle.module.css';

interface TimerCircleProps {
  timeLeft: number;
  totalDuration: number;
  label: string;
  size?: number;
  strokeWidth?: number;
}

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

export const TimerCircle = memo(function TimerCircle({
  timeLeft,
  totalDuration,
  label,
  size = 260,
  strokeWidth = 8,
}: TimerCircleProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = totalDuration > 0 ? timeLeft / totalDuration : 0;
  const dashOffset = circumference * (1 - progress);
  const center = size / 2;

  return (
    <div className={styles.wrapper} style={{ width: size, height: size }}>
      <svg
        className={styles.svg}
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        role="timer"
        aria-label={`${label}: ${formatTime(timeLeft)}`}
      >
        {/* Background circle */}
        <circle
          className={styles.track}
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
        />
        {/* Progress circle */}
        <circle
          className={styles.progress}
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          strokeLinecap="round"
          transform={`rotate(-90 ${center} ${center})`}
          style={{
            transition: 'stroke-dashoffset 1s linear',
          }}
        />
      </svg>
      <div className={styles.content}>
        <span className={styles.time}>{formatTime(timeLeft)}</span>
        <span className={styles.label}>{label}</span>
      </div>
    </div>
  );
});