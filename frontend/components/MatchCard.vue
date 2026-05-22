<template>
  <NuxtLink :to="`/matches/${match.id}`" class="glass rounded-2xl p-5 block hover:glass-hover transition-all group">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <img v-if="match.league_logo" :src="match.league_logo" class="w-5 h-5 object-contain" alt="" />
        <span class="text-xs text-secondary font-medium">{{ match.league }}</span>
      </div>
      <span v-if="match.status === 'LIVE'" class="text-live text-xs font-bold neon-live flex items-center gap-1">
        <span class="w-1.5 h-1.5 rounded-full bg-live animate-pulse"/> LIVE {{ match.minute }}'
      </span>
      <span v-else-if="match.status === 'finished'" class="text-secondary text-xs font-medium">Завершен</span>
      <span v-else class="text-secondary text-xs font-medium">{{ formatTime(match.date) }}</span>
    </div>

    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3 flex-1">
        <img v-if="match.home_team.logo" :src="match.home_team.logo" class="w-8 h-8 object-contain" alt="" />
        <span class="font-semibold text-sm truncate">{{ match.home_team.name }}</span>
      </div>
      <div class="px-3 py-1 rounded-lg bg-white/5 font-bold text-lg mx-2 min-w-[48px] text-center">
        {{ match.home_team.score ?? '-' }} : {{ match.away_team.score ?? '-' }}
      </div>
      <div class="flex items-center gap-3 flex-1 justify-end">
        <span class="font-semibold text-sm truncate text-right">{{ match.away_team.name }}</span>
        <img v-if="match.away_team.logo" :src="match.away_team.logo" class="w-8 h-8 object-contain" alt="" />
      </div>
    </div>

    <div v-if="match.possession" class="mt-4">
      <div class="flex items-center justify-between text-xs text-secondary mb-1">
        <span>Владение</span>
        <span>{{ match.possession.home }}% — {{ match.possession.away }}%</span>
      </div>
      <div class="h-1.5 rounded-full bg-white/10 overflow-hidden flex">
        <div class="h-full bg-accent" :style="{ width: match.possession.home + '%' }"/>
        <div class="h-full bg-secondary" :style="{ width: match.possession.away + '%' }"/>
      </div>
    </div>

    <div v-if="match.events && match.events.length" class="mt-3 flex flex-wrap gap-2">
      <span v-for="(ev, i) in match.events.slice(0, 3)" :key="i" class="text-xs text-secondary flex items-center gap-1">
        {{ eventIcon(ev.type) }} {{ ev.time }} {{ ev.player }}
      </span>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { Match } from '~/types';
import { formatTime, eventIcon } from '~/utils/format';

defineProps<{ match: Match }>();
</script>
