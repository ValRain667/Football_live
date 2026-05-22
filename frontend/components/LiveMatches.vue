<template>
  <section class="px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-live animate-pulse"/>
        Live Matches
      </h2>
      <NuxtLink to="/live" class="text-accent text-sm font-medium hover:underline">Все live матчи →</NuxtLink>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <MatchCard v-for="match in matches" :key="match.id" :match="match" />
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Match } from '~/types';
defineProps<{ matches: Match[] }>();
</script>
