<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Матчи</h1>
    <div class="flex gap-2 mb-6 overflow-x-auto pb-2">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        @click="activeTab = tab.value"
        class="px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-colors"
        :class="activeTab === tab.value ? 'bg-accent text-bg' : 'bg-white/5 text-secondary hover:bg-white/10'"
      >
        {{ tab.label }}
      </button>
    </div>
    <div v-if="pending" class="text-center py-12 text-secondary">Загрузка...</div>
    <div v-else-if="filteredMatches.length === 0" class="text-center py-12">
      <p class="text-text font-semibold">Нет матчей</p>
      <p class="text-secondary text-sm mt-1">Попробуйте изменить фильтр</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <MatchCard v-for="match in filteredMatches" :key="match.id" :match="match" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMatches } from '~/composables/useApi';
import type { Match } from '~/types';

const activeTab = ref('all');
const tabs = [
  { label: 'Все', value: 'all' },
  { label: 'Live', value: 'live' },
  { label: 'Завершенные', value: 'finished' },
  { label: 'Предстоящие', value: 'upcoming' },
];

const { data: matches, pending } = useMatches();

const filteredMatches = computed<Match[]>(() => {
  const list = matches.value || [];
  if (activeTab.value === 'all') return list;
  if (activeTab.value === 'live') return list.filter(m => m.status === 'LIVE');
  if (activeTab.value === 'finished') return list.filter(m => m.status === 'finished');
  if (activeTab.value === 'upcoming') return list.filter(m => m.status === 'upcoming');
  return list;
});
</script>
