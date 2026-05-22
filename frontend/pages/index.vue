<template>
  <div>
    <HeroSection />
    <LiveMatches :matches="liveMatches" />
    <section class="px-4 py-8">
      <h2 class="text-xl font-bold mb-6">Популярные лиги</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <LeagueCard v-for="league in leagues" :key="league.id" :league="league" />
      </div>
    </section>
    <section class="px-4 py-8">
      <h2 class="text-xl font-bold mb-6">Ближайшие матчи</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <MatchCard v-for="match in upcomingMatches" :key="match.id" :match="match" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useLiveMatches, useLeagues } from '~/composables/useApi';

const { data: liveData } = useLiveMatches();
const { data: leaguesData } = useLeagues();

const liveMatches = computed(() => liveData.value || []);
const leagues = computed(() => leaguesData.value || []);
const upcomingMatches = computed(() => {
  if (!liveData.value) return [];
  return liveData.value.filter(m => m.status === 'upcoming').slice(0, 3);
});
</script>
