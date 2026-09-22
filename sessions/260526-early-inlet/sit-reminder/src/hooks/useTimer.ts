import { useState, useRef, useCallback, useEffect } from 'react';

export type TimerStatus = 'idle' | 'running' | 'paused' | 'resting';

interface UseTimerOptions {
  initialDuration: number;
  restDuration?: number;
  onWorkComplete?: () => void;
  onRestComplete?: () => void;
  onTick?: (timeLeft: number, status: TimerStatus) => void;
}

interface UseTimerReturn {
  timeLeft: number;
  totalDuration: number;
  status: TimerStatus;
  isRunning: boolean;
  start: () => void;
  pause: () => void;
  reset: (newDuration?: number) => void;
  skip: () => void;
}

export function useTimer({
  initialDuration,
  restDuration = 5 * 60,
  onWorkComplete,
  onRestComplete,
  onTick,
}: UseTimerOptions): UseTimerReturn {
  const [totalDuration, setTotalDuration] = useState(initialDuration);
  const [timeLeft, setTimeLeft] = useState(initialDuration);
  const [status, setStatus] = useState<TimerStatus>('idle');
  const intervalRef = useRef<number | null>(null);

  const clearIntervalRef = useCallback(() => {
    if (intervalRef.current !== null) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  const stopTimer = useCallback(() => {
    clearIntervalRef();
  }, [clearIntervalRef]);

  const tick = useCallback(() => {
    setTimeLeft((prev) => {
      const next = prev - 1;
      if (next <= 0) {
        stopTimer();
        return 0;
      }
      return next;
    });
  }, [stopTimer]);

  // Notify parent of ticks
  useEffect(() => {
    onTick?.(timeLeft, status);
  }, [timeLeft, status, onTick]);

  // Handle completion
  useEffect(() => {
    if (timeLeft === 0 && status === 'running') {
      onWorkComplete?.();
      // Start rest mode
      setStatus('resting');
      setTimeLeft(restDuration);
      setTotalDuration(restDuration);
    }
    if (timeLeft === 0 && status === 'resting') {
      onRestComplete?.();
      setStatus('idle');
      setTimeLeft(initialDuration);
      setTotalDuration(initialDuration);
    }
  }, [timeLeft, status, restDuration, initialDuration, onWorkComplete, onRestComplete]);

  const start = useCallback(() => {
    clearIntervalRef();
    setStatus((prev) => {
      if (prev === 'paused' || prev === 'idle') {
        intervalRef.current = window.setInterval(tick, 1000);
        return prev === 'idle' && timeLeft === totalDuration ? 'running' : 'running';
      }
      return prev;
    });
    if (status === 'idle') {
      intervalRef.current = window.setInterval(tick, 1000);
    } else if (status === 'paused') {
      intervalRef.current = window.setInterval(tick, 1000);
    }
  }, [clearIntervalRef, tick, status, timeLeft, totalDuration]);

  // Re-build start to avoid status dependency issues
  const startTimer = useCallback(() => {
    stopTimer();
    if (timeLeft <= 0) return;
    intervalRef.current = window.setInterval(tick, 1000);
    setStatus((s) => (s === 'resting' ? 'resting' : 'running'));
  }, [stopTimer, tick, timeLeft]);

  const pause = useCallback(() => {
    stopTimer();
    setStatus('paused');
  }, [stopTimer]);

  const reset = useCallback(
    (newDuration?: number) => {
      stopTimer();
      const dur = newDuration ?? initialDuration;
      setTotalDuration(dur);
      setTimeLeft(dur);
      setStatus('idle');
    },
    [stopTimer, initialDuration]
  );

  const skip = useCallback(() => {
    stopTimer();
    if (status === 'running') {
      setTimeLeft(0);
    } else if (status === 'resting') {
      setTimeLeft(0);
    }
  }, [stopTimer, status]);

  // Sync initialDuration changes
  useEffect(() => {
    if (status === 'idle') {
      setTimeLeft(initialDuration);
      setTotalDuration(initialDuration);
    }
  }, [initialDuration, status]);

  return {
    timeLeft,
    totalDuration,
    status,
    isRunning: status === 'running' || status === 'resting',
    start: startTimer,
    pause,
    reset,
    skip,
  };
}