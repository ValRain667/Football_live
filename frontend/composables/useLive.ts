import { ref, onMounted, onUnmounted } from 'vue';
import type { Match } from '~/types';

export function useLiveSocket() {
  const liveMatches = ref<Match[]>([]);
  const connected = ref(false);
  let ws: WebSocket | null = null;

  onMounted(() => {
    const url = useRuntimeConfig().public.apiUrl?.replace('http', 'ws') || 'ws://localhost:8000';
    ws = new WebSocket(`${url}/api/ws/live`);
    ws.onopen = () => { connected.value = true; };
    ws.onmessage = (event) => {
      liveMatches.value = JSON.parse(event.data);
    };
    ws.onclose = () => { connected.value = false; };
  });

  onUnmounted(() => {
    ws?.close();
  });

  return { liveMatches, connected };
}
