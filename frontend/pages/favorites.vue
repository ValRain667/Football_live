<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Избранное</h1>
    <div v-if="favorites.teams.length === 0 && favorites.matches.length === 0" class="text-center py-12">
      <p class="text-text font-semibold">Нет избранного</p>
      <p class="text-secondary text-sm mt-1">Добавьте команды и матчи в избранное</p>
    </div>
    <div v-else class="space-y-8">
      <div v-if="favorites.teams.length">
        <h2 class="text-lg font-bold mb-4">Команды</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <TeamCard v-for="team in favoriteTeams" :key="team.id" :team="team" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useFavoritesStore } from '~/stores/favorites';
import { useTeams } from '~/composables/useApi';

const favorites = useFavoritesStore();
const { data: allTeams } = useTeams();

const favoriteTeams = computed(() => {
  if (!allTeams.value) return [];
  return allTeams.value.filter(t => favorites.teams.includes(t.id));
});
</script>
