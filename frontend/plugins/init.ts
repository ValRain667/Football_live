import { useAuthStore } from '~/stores/auth';
import { useThemeStore } from '~/stores/theme';
import { useFavoritesStore } from '~/stores/favorites';

export default defineNuxtPlugin(() => {
  useAuthStore().init();
  useThemeStore().init();
  useFavoritesStore().init();
});
