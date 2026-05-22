<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Турнирная таблица</h1>
    <div v-if="pending" class="text-center py-12 text-secondary">Загрузка...</div>
    <StandingsTable v-else :standings="standings" />
  </div>
</template>

<script setup lang="ts">
import { useStandings } from '~/composables/useApi';

const route = useRoute();
const leagueId = computed(() => Number(route.params.leagueId));

const { data: standings, pending } = useStandings(leagueId);
</script>
