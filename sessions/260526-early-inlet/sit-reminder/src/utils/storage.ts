export interface StoredData {
  duration: number;
  todayCount: number;
  todayDate: string;
}

const STORAGE_KEY = 'sit-reminder';

const defaultData: StoredData = {
  duration: 45 * 60,
  todayCount: 0,
  todayDate: new Date().toDateString(),
};

function getToday(): string {
  return new Date().toDateString();
}

export function loadData(): StoredData {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...defaultData };
    const data: StoredData = JSON.parse(raw);
    if (data.todayDate !== getToday()) {
      return { duration: data.duration, todayCount: 0, todayDate: getToday() };
    }
    return data;
  } catch {
    return { ...defaultData };
  }
}

export function saveData(data: StoredData): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

export function incrementCount(): StoredData {
  const data = loadData();
  if (data.todayDate !== getToday()) {
    data.todayCount = 1;
    data.todayDate = getToday();
  } else {
    data.todayCount += 1;
  }
  saveData(data);
  return data;
}

export function saveDuration(duration: number): StoredData {
  const data = loadData();
  data.duration = duration;
  saveData(data);
  return data;
}