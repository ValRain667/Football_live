<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Профиль</h1>
    <div v-if="!auth.isAuthenticated" class="glass rounded-2xl p-8 text-center">
      <p class="text-secondary mb-4">Войдите, чтобы увидеть профиль</p>
      <NuxtLink to="/login" class="px-6 py-3 rounded-xl bg-accent text-bg font-bold inline-block">Войти</NuxtLink>
    </div>
    <div v-else-if="auth.user" class="space-y-4">
      <div class="glass rounded-2xl p-6 flex items-center gap-4">
        <div class="w-16 h-16 rounded-full bg-accent/20 flex items-center justify-center text-2xl font-bold text-accent">
          {{ auth.user.username[0]?.toUpperCase() }}
        </div>
        <div>
          <h2 class="text-xl font-bold">{{ auth.user.username }}</h2>
          <p class="text-secondary text-sm">{{ auth.user.email }}</p>
        </div>
      </div>
      <div class="glass rounded-2xl p-6">
        <h3 class="font-bold mb-3">Настройки</h3>
        <div class="flex items-center justify-between py-2">
          <span class="text-secondary">Тема</span>
          <button @click="theme.toggle()" class="text-sm text-accent">{{ theme.isDark ? 'Темная' : 'Светлая' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';
import { useThemeStore } from '~/stores/theme';

const auth = useAuthStore();
const theme = useThemeStore();

definePageMeta({ middleware: 'auth' });
</script>
