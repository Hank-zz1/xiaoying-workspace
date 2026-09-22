import { memo } from 'react';
import styles from './StatsPanel.module.css';

interface StatsPanelProps {
  count: number;
  totalDuration: number;
}

export const StatsPanel = memo(function StatsPanel({
  count,
  totalDuration,
}: StatsPanelProps) {
  const hours = totalDuration > 0 ? totalDuration / 3600 : 0;
  const totalFocus = hours * count;

  return (
    <div className={styles.panel}>
      <div className={styles.stat}>
        <span className={styles.value}>{count}</span>
        <span className={styles.unit}>次</span>
        <span className={styles.desc}>今日起立</span>
      </div>
      <div className={styles.divider} />
      <div className={styles.stat}>
        <span className={styles.value}>{totalFocus.toFixed(1)}</span>
        <span className={styles.unit}>小时</span>
        <span className={styles.desc}>累计专注</span>
      </div>
    </div>
  );
});