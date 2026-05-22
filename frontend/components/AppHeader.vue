<template>
  <header class="fixed top-0 left-0 right-0 z-50 glass border-b border-white/5">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <NuxtLink to="/" class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-full bg-accent flex items-center justify-center">
          <span class="text-bg font-bold text-sm">FL</span>
        </div>
        <span class="font-bold text-lg tracking-tight">Football Live Hub</span>
      </NuxtLink>

      <nav class="hidden md:flex items-center gap-6 text-sm font-medium text-secondary">
        <NuxtLink to="/" class="hover:text-text transition-colors">Главная</NuxtLink>
        <NuxtLink to="/matches" class="hover:text-text transition-colors">Матчи</NuxtLink>
        <NuxtLink to="/live" class="hover:text-text transition-colors flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-live animate-pulse"/>
          Live
        </NuxtLink>
        <NuxtLink to="/leagues" class="hover:text-text transition-colors">Лиги</NuxtLink>
        <NuxtLink to="/teams" class="hover:text-text transition-colors">Команды</NuxtLink>
        <NuxtLink to="/standings/39" class="hover:text-text transition-colors">Таблицы</NuxtLink>
        <NuxtLink to="/favorites" class="hover:text-text transition-colors">Избранное</NuxtLink>
        <NuxtLink to="/profile" class="hover:text-text transition-colors">Профиль</NuxtLink>
      </nav>

      <div class="flex items-center gap-3">
        <button @click="showSearch = true" class="p-2 rounded-lg hover:bg-white/5 transition-colors" aria-label="Поиск">
          <svg class="w-5 h-5 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </button>
        <ThemeToggle />
        <NuxtLink v-if="!auth.isAuthenticated" to="/login" class="hidden sm:inline-flex px-4 py-2 rounded-lg bg-accent text-bg font-semibold text-sm hover:opacity-90 transition-opacity">
          Войти
        </NuxtLink>
        <button v-else @click="auth.logout" class="hidden sm:inline-flex px-4 py-2 rounded-lg bg-white/5 text-sm font-medium hover:bg-white/10 transition-colors">
          Выйти
        </button>
      </div>
    </div>

    <SearchModal v-model="showSearch" />
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';

const auth = useAuthStore();
const showSearch = ref(false);
</script>
