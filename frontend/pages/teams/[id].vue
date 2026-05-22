<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div v-if="pending" class="text-center py-12 text-secondary">Загрузка...</div>
    <div v-else-if="team" class="space-y-6">
      <div class="glass rounded-2xl p-6 flex flex-col md:flex-row items-center gap-6">
        <img v-if="team.logo" :src="team.logo" class="w-24 h-24 object-contain" alt="" />
        <div class="text-center md:text-left">
          <h1 class="text-3xl font-bold">{{ team.name }}</h1>
          <p class="text-secondary mt-1">{{ team.country }} <span v-if="team.founded">· Основан {{ team.founded }}</span></p>
          <div class="flex flex-wrap gap-3 mt-3 justify-center md:justify-start">
            <span v-if="team.stadium" class="px-3 py-1 rounded-lg bg-white/5 text-xs text-secondary">🏟 {{ team.stadium }}</span>
            <span v-if="team.coach" class="px-3 py-1 rounded-lg bg-white/5 text-xs text-secondary">👔 {{ team.coach }}</span>
          </div>
        </div>
        <button
          @click="favorites.toggleTeam(team.id)"
          class="ml-auto px-4 py-2 rounded-xl text-sm font-medium transition-colors"
          :class="favorites.isTeamFavorite(team.id) ? 'bg-accent text-bg' : 'bg-white/5 text-secondary hover:bg-white/10'"
        >
          {{ favorites.isTeamFavorite(team.id) ? '★ В избранном' : '☆ В избранное' }}
        </button>
      </div>

      <div v-if="team.recent_matches && team.recent_matches.length" class="glass rounded-2xl p-6">
        <h2 class="font-bold text-lg mb-4">Последние матчи</h2>
        <div class="space-y-2">
          <div v-for="m in team.recent_matches" :key="m.id" class="flex items-center justify-between p-3 rounded-xl bg-white/[0.02]">
            <span class="text-sm">{{ m.opponent }}</span>
            <span class="font-bold text-sm">{{ m.score }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTeam } from '~/composables/useApi';
import { useFavoritesStore } from '~/stores/favorites';

const route = useRoute();
const teamId = computed(() => Number(route.params.id));
const favorites = useFavoritesStore();

const { data: team, pending } = useTeam(teamId);
</script>
