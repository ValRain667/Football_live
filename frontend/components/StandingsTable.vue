<template>
  <div class="glass rounded-2xl overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-white/5 text-secondary text-xs uppercase tracking-wider">
            <th class="px-4 py-3 text-left w-12">#</th>
            <th class="px-4 py-3 text-left">Команда</th>
            <th class="px-4 py-3 text-center w-12">И</th>
            <th class="px-4 py-3 text-center w-12">В</th>
            <th class="px-4 py-3 text-center w-12">Н</th>
            <th class="px-4 py-3 text-center w-12">П</th>
            <th class="px-4 py-3 text-center w-16">Голы</th>
            <th class="px-4 py-3 text-center w-12">+/-</th>
            <th class="px-4 py-3 text-center w-12">О</th>
            <th class="px-4 py-3 text-center">Форма</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in standings"
            :key="row.team.id"
            class="border-b border-white/5 hover:bg-white/[0.02] transition-colors"
            :class="zoneClass(row.position)"
          >
            <td class="px-4 py-3 font-medium">{{ row.position }}</td>
            <td class="px-4 py-3">
              <NuxtLink :to="`/teams/${row.team.id}`" class="flex items-center gap-2 hover:text-accent transition-colors">
                <img v-if="row.team.logo" :src="row.team.logo" class="w-6 h-6 object-contain" alt="" />
                <span class="font-medium truncate">{{ row.team.name }}</span>
              </NuxtLink>
            </td>
            <td class="px-4 py-3 text-center text-secondary">{{ row.played }}</td>
            <td class="px-4 py-3 text-center text-secondary">{{ row.won }}</td>
            <td class="px-4 py-3 text-center text-secondary">{{ row.draw }}</td>
            <td class="px-4 py-3 text-center text-secondary">{{ row.lost }}</td>
            <td class="px-4 py-3 text-center text-secondary">{{ row.goals_for }}:{{ row.goals_against }}</td>
            <td class="px-4 py-3 text-center" :class="row.goal_difference > 0 ? 'text-accent' : 'text-secondary'">
              {{ row.goal_difference > 0 ? '+' : '' }}{{ row.goal_difference }}
            </td>
            <td class="px-4 py-3 text-center font-bold">{{ row.points }}</td>
            <td class="px-4 py-3 text-center">
              <div class="flex justify-center gap-1">
                <span
                  v-for="(f, i) in row.form"
                  :key="i"
                  class="w-5 h-5 rounded text-[10px] font-bold flex items-center justify-center"
                  :class="f === 'W' ? 'bg-accent/20 text-accent' : f === 'D' ? 'bg-white/10 text-secondary' : 'bg-live/20 text-live'"
                >
                  {{ f }}
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Standing } from '~/types';
defineProps<{ standings: Standing[] }>();

function zoneClass(pos: number) {
  if (pos <= 4) return 'border-l-2 border-l-accent/40';
  if (pos >= 18) return 'border-l-2 border-l-live/40';
  return '';
}
</script>
