import { defineStore } from 'pinia';
import api from '~/services/api';
import type { User } from '~/types';

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    refreshToken: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email: string, password: string) {
      const { data } = await api.post('/auth/login', { email, password });
      this.token = data.access_token;
      this.refreshToken = data.refresh_token;
      if (process.client) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
      }
      await this.fetchUser();
    },

    async register(email: string, username: string, password: string) {
      await api.post('/auth/register', { email, username, password });
    },

    async fetchUser() {
      try {
        const { data } = await api.get('/auth/me');
        this.user = data;
      } catch {
        this.logout();
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.refreshToken = null;
      if (process.client) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    },

    init() {
      if (process.client) {
        const access = localStorage.getItem('access_token');
        const refresh = localStorage.getItem('refresh_token');
        if (access) {
          this.token = access;
          this.refreshToken = refresh;
          this.fetchUser();
        }
      }
    },
  },
});
