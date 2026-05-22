<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div v-if="pending" class="text-center py-12 text-secondary">Загрузка...</div>
    <div v-else-if="league" class="space-y-8">
      <div class="glass rounded-2xl p-6 flex items-center gap-4">
        <img v-if="league.logo" :src="league.logo" class="w-16 h-16 object-contain" alt="" />
        <div>
          <h1 class="text-2xl font-bold">{{ league.name }}</h1>
          <p class="text-secondary">{{ league.country }}</p>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold mb-4">Турнирная таблица</h2>
        <StandingsTable :standings="standings" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useLeague, useStandings } from '~/composables/useApi';

const route = useRoute();
const leagueId = computed(() => Number(route.params.id));

const { data: league, pending: leaguePending } = useLeague(leagueId);
const { data: standings, pending: standingsPending } = useStandings(leagueId);

const pending = computed(() => leaguePending.value || standingsPending.value);
</script>
