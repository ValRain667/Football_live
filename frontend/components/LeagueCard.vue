<template>
  <NuxtLink :to="`/leagues/${league.id}`" class="glass rounded-2xl p-6 flex items-center gap-4 hover:glass-hover transition-all group">
    <div class="w-14 h-14 rounded-xl bg-white/5 flex items-center justify-center shrink-0">
      <img v-if="league.logo" :src="league.logo" class="w-10 h-10 object-contain" alt="" />
      <span v-else class="text-xl font-bold text-accent">{{ league.name[0] }}</span>
    </div>
    <div>
      <h3 class="font-bold text-base group-hover:text-accent transition-colors">{{ league.name }}</h3>
      <p class="text-sm text-secondary">{{ league.country }}</p>
    </div>
    <svg class="w-5 h-5 text-secondary ml-auto group-hover:text-accent transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { League } from '~/types';
defineProps<{ league: League }>();
</script>
