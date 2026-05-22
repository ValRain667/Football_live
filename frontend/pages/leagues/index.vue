<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Лиги</h1>
    <div v-if="pending" class="text-center py-12 text-secondary">Загрузка...</div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <LeagueCard v-for="league in leagues" :key="league.id" :league="league" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useLeagues } from '~/composables/useApi';
const { data: leagues, pending } = useLeagues();
</script>
