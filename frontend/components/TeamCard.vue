<template>
  <NuxtLink :to="`/teams/${team.id}`" class="glass rounded-2xl p-5 flex items-center gap-4 hover:glass-hover transition-all group">
    <div class="w-14 h-14 rounded-xl bg-white/5 flex items-center justify-center shrink-0">
      <img v-if="team.logo" :src="team.logo" class="w-10 h-10 object-contain" alt="" />
      <span v-else class="text-xl font-bold text-accent">{{ team.name[0] }}</span>
    </div>
    <div class="flex-1 min-w-0">
      <h3 class="font-bold text-base group-hover:text-accent transition-colors truncate">{{ team.name }}</h3>
      <p class="text-sm text-secondary">{{ team.country }} <span v-if="team.founded">· {{ team.founded }}</span></p>
    </div>
    <svg class="w-5 h-5 text-secondary group-hover:text-accent transition-colors shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { Team } from '~/types';
defineProps<{ team: Team }>();
</script>
