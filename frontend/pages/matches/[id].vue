<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div v-if="pending" class="text-center py-12 text-secondary">Загрузка...</div>
    <div v-else-if="match" class="space-y-6">
      <div class="glass rounded-2xl p-6 md:p-8">
        <div class="flex items-center justify-center gap-4 mb-6">
          <div class="flex flex-col items-center gap-2 flex-1">
            <img v-if="match.home_team.logo" :src="match.home_team.logo" class="w-16 h-16 object-contain" alt="" />
            <span class="font-bold text-center">{{ match.home_team.name }}</span>
          </div>
          <div class="text-center px-4">
            <div class="text-3xl font-extrabold">{{ match.home_team.score ?? '-' }} : {{ match.away_team.score ?? '-' }}</div>
            <div v-if="match.status === 'LIVE'" class="text-live text-sm font-bold neon-live mt-1">LIVE {{ match.minute }}'</div>
            <div v-else-if="match.status === 'finished'" class="text-secondary text-sm mt-1">Завершен</div>
            <div v-else class="text-secondary text-sm mt-1">{{ formatDate(match.date) }}</div>
          </div>
          <div class="flex flex-col items-center gap-2 flex-1">
            <img v-if="match.away_team.logo" :src="match.away_team.logo" class="w-16 h-16 object-contain" alt="" />
            <span class="font-bold text-center">{{ match.away_team.name }}</span>
          </div>
        </div>

        <div v-if="match.possession" class="mb-6">
          <div class="flex items-center justify-between text-sm text-secondary mb-2">
            <span>Владение мячом</span>
            <span>{{ match.possession.home }}% — {{ match.possession.away }}%</span>
          </div>
          <div class="h-2 rounded-full bg-white/10 overflow-hidden flex">
            <div class="h-full bg-accent" :style="{ width: match.possession.home + '%' }"/>
            <div class="h-full bg-secondary" :style="{ width: match.possession.away + '%' }"/>
          </div>
        </div>

        <div v-if="match.statistics" class="grid grid-cols-3 gap-4 text-center">
          <div v-for="(val, key) in match.statistics" :key="key" class="glass rounded-xl p-3">
            <p class="text-xs text-secondary uppercase mb-1">{{ key }}</p>
            <p class="font-bold">{{ val.home }} — {{ val.away }}</p>
          </div>
        </div>
      </div>

      <div v-if="match.events && match.events.length" class="glass rounded-2xl p-6">
        <h3 class="font-bold text-lg mb-4">События</h3>
        <div class="space-y-3">
          <div v-for="(ev, i) in match.events" :key="i" class="flex items-center gap-3 p-3 rounded-xl bg-white/[0.02]">
            <span class="text-sm font-mono text-secondary w-10">{{ ev.time }}</span>
            <span class="text-lg">{{ eventIcon(ev.type) }}</span>
            <span class="font-medium text-sm">{{ ev.player }}</span>
            <span class="text-xs text-secondary ml-auto">{{ ev.team }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMatch } from '~/composables/useApi';
import { formatDate, eventIcon } from '~/utils/format';

const route = useRoute();
const matchId = computed(() => Number(route.params.id));
const { data: match, pending } = useMatch(matchId);
</script>
