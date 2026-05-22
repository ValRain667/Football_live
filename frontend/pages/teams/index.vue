<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">Команды</h1>
    <div class="flex gap-2 mb-6">
      <input
        v-model="search"
        type="text"
        placeholder="Поиск команд..."
        class="flex-1 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-text placeholder-secondary outline-none focus:border-accent/50 transition-colors"
      />
    </div>
    <div v-if="pending" class="text-center py-12 text-secondary">Загрузка...</div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <TeamCard v-for="team in teams" :key="team.id" :team="team" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTeams } from '~/composables/useApi';
const search = ref('');
const { data: teams, pending } = useTeams(search);
</script>
