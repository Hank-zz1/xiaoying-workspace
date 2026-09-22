import { useState, useCallback, useEffect } from 'react';
import { useTimer } from './hooks/useTimer';
import { useNotification } from './hooks/useNotification';
import { loadData, incrementCount, saveDuration } from './utils/storage';
import { TimerCircle } from './components/TimerCircle';
import { TimerControls } from './components/TimerControls';
import { DurationSelector } from './components/DurationSelector';
import { StatsPanel } from './components/StatsPanel';
import styles from './App.module.css';

export default function App() {
  const [data, setData] = useState(loadData);
  const [animKey, setAnimKey] = useState(0);
  const { notify, requestPermission } = useNotification();

  const handleWorkComplete = useCallback(() => {
    const updated = incrementCount();
    setData(updated);
    notify('该起来活动了! ', '起来走动走动，看看远方，放松一下眼睛和身体吧');
    setAnimKey((k) => k + 1);
  }, [notify]);

  const handleRestComplete = useCallback(() => {
    notify('休息时间结束', '可以继续下一轮工作了，加油！');
  }, [notify]);

  const timer = useTimer({
    initialDuration: data.duration,
    restDuration: 5 * 60,
    onWorkComplete: handleWorkComplete,
    onRestComplete: handleRestComplete,
  });

  const handleDurationChange = useCallback(
    (seconds: number) => {
      const updated = saveDuration(seconds);
      setData(updated);
      timer.reset(seconds);
    },
    [timer]
  );

  // Request notification permission on first user gesture
  useEffect(() => {
    const handler = () => {
      requestPermission();
      document.removeEventListener('click', handler);
    };
    document.addEventListener('click', handler, { once: true });
    return () => document.removeEventListener('click', handler);
  }, [requestPermission]);

  const statusLabel =
    timer.status === 'resting'
      ? '休息中'
      : timer.status === 'running'
      ? '专注中'
      : timer.status === 'paused'
      ? '已暂停'
      : '准备开始';

  return (
    <div className={styles.page}>
      <div className={styles.bgGradient} />
      <div className={styles.container}>
        {/* Header */}
        <header className={styles.header}>
          <h1 className={styles.title}>久坐提醒</h1>
          <p className={styles.subtitle}>保持健康工作节奏</p>
        </header>

        {/* Timer */}
        <div className={styles.timerSection} key={animKey}>
          <TimerCircle
            timeLeft={timer.timeLeft}
            totalDuration={timer.totalDuration}
            label={statusLabel}
          />
        </div>

        {/* Controls */}
        <TimerControls
          status={timer.status}
          isRunning={timer.isRunning}
          onStart={timer.start}
          onPause={timer.pause}
          onReset={() => timer.reset(data.duration)}
          onSkip={timer.skip}
        />

        {/* Duration selector */}
        {timer.status === 'idle' && (
          <DurationSelector
            value={data.duration}
            onChange={handleDurationChange}
            disabled={false}
          />
        )}

        {/* Stats */}
        <StatsPanel count={data.todayCount} totalDuration={data.duration} />
      </div>
    </div>
  );
}