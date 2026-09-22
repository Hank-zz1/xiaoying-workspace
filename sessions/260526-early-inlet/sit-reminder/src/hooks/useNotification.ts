import { useCallback, useRef } from 'react';

export function useNotification() {
  const permissionRef = useRef<NotificationPermission>('default');

  const requestPermission = useCallback(async (): Promise<boolean> => {
    if (!('Notification' in window)) return false;
    if (Notification.permission === 'granted') {
      permissionRef.current = 'granted';
      return true;
    }
    const result = await Notification.requestPermission();
    permissionRef.current = result;
    return result === 'granted';
  }, []);

  const notify = useCallback(
    (title: string, body: string, icon?: string) => {
      if (!('Notification' in window)) return;
      if (Notification.permission === 'granted') {
        new Notification(title, { body, icon, tag: 'sit-reminder' });
      } else if (Notification.permission === 'default') {
        requestPermission().then((granted) => {
          if (granted) {
            new Notification(title, { body, icon, tag: 'sit-reminder' });
          }
        });
      }
    },
    [requestPermission]
  );

  return { notify, requestPermission };
}