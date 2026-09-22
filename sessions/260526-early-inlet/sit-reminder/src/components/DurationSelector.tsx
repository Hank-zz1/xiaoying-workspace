import { memo } from 'react';
import styles from './DurationSelector.module.css';

interface DurationSelectorProps {
  value: number;
  onChange: (seconds: number) => void;
  disabled?: boolean;
}

const PRESETS = [
  { label: '25分', value: 25 },
  { label: '30分', value: 30 },
  { label: '45分', value: 45 },
  { label: '60分', value: 60 },
  { label: '90分', value: 90 },
];

export const DurationSelector = memo(function DurationSelector({
  value,
  onChange,
  disabled = false,
}: DurationSelectorProps) {
  const minutes = Math.round(value / 60);

  return (
    <div className={styles.wrapper}>
      <span className={styles.heading}>工作时长</span>
      <div className={styles.presets}>
        {PRESETS.map((p) => (
          <button
            key={p.value}
            className={`${styles.chip} ${p.value === minutes ? styles.active : ''}`}
            onClick={() => onChange(p.value * 60)}
            disabled={disabled}
          >
            {p.label}
          </button>
        ))}
      </div>
    </div>
  );
});