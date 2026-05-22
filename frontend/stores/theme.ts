import { defineStore } from 'pinia';

interface ThemeState {
  isDark: boolean;
}

export const useThemeStore = defineStore('theme', {
  state: (): ThemeState => ({
    isDark: true,
  }),

  actions: {
    toggle() {
      this.isDark = !this.isDark;
      if (process.client) {
        document.documentElement.classList.toggle('dark', this.isDark);
        localStorage.setItem('theme', this.isDark ? 'dark' : 'light');
      }
    },
    init() {
      if (process.client) {
        const saved = localStorage.getItem('theme');
        this.isDark = saved ? saved === 'dark' : true;
        document.documentElement.classList.toggle('dark', this.isDark);
      }
    },
  },
});
