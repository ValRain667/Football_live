<template>
  <Teleport to="body">
    <div v-if="modelValue" class="fixed inset-0 z-[60] flex items-start justify-center pt-24 bg-black/60 backdrop-blur-sm" @click="emit('update:modelValue', false)">
      <div class="w-full max-w-2xl mx-4 glass rounded-2xl p-4" @click.stop>
        <div class="flex items-center gap-3 mb-4">
          <svg class="w-5 h-5 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input
            v-model="query"
            type="text"
            placeholder="Поиск команд, лиг, игроков..."
            class="flex-1 bg-transparent text-text placeholder-secondary outline-none text-lg"
            autofocus
          />
          <button @click="emit('update:modelValue', false)" class="text-secondary hover:text-text">Esc</button>
        </div>

        <div v-if="loading" class="text-secondary text-sm py-8 text-center">Поиск...</div>
        <div v-else-if="results.length === 0 && query" class="py-8 text-center">
          <p class="text-text font-semibold">Ничего не найдено</p>
          <p class="text-secondary text-sm mt-1">Попробуйте изменить поисковый запрос</p>
        </div>
        <div v-else class="space-y-2 max-h-96 overflow-auto">
          <NuxtLink
            v-for="r in results"
            :key="r.id"
            :to="r.link"
            class="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors"
            @click="emit('update:modelValue', false)"
          >
            <img v-if="r.logo" :src="r.logo" class="w-8 h-8 object-contain" alt="" />
            <div>
              <p class="font-medium text-sm">{{ r.name }}</p>
              <p class="text-xs text-secondary">{{ r.type }}</p>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { debounce } from '~/utils/debounce';

const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits<{ (e: 'update:modelValue', v: boolean): void }>();

const query = ref('');
const results = ref<any[]>([]);
const loading = ref(false);

const search = debounce(async () => {
  if (!query.value.trim()) { results.value = []; return; }
  loading.value = true;
  const { footballApi } = await import('~/services/football');
  const teams = await footballApi.getTeams(query.value);
  results.value = teams.map((t) => ({ id: t.id, name: t.name, logo: t.logo, type: 'Команда', link: `/teams/${t.id}` }));
  loading.value = false;
}, 300);

watch(query, search);
</script>
