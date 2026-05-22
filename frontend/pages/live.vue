<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6 flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-live animate-pulse"/>
      Live Матчи
    </h1>
    <div v-if="pending" class="text-center py-12 text-secondary">Загрузка...</div>
    <div v-else-if="!matches || matches.length === 0" class="text-center py-12">
      <p class="text-text font-semibold">Нет live матчей</p>
      <p class="text-secondary text-sm mt-1">Возвращайтесь позже</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <MatchCard v-for="match in matches" :key="match.id" :match="match" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useLiveMatches } from '~/composables/useApi';
const { data: matches, pending } = useLiveMatches();
</script>
