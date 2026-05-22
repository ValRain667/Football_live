<template>
  <footer class="border-t border-white/5 mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-2">
        <div class="w-6 h-6 rounded-full bg-accent flex items-center justify-center">
          <span class="text-bg font-bold text-xs">FL</span>
        </div>
        <span class="font-semibold text-sm">Football Live Hub</span>
      </div>
      <p class="text-secondary text-xs">Live football scores, standings and statistics.</p>
      <div class="flex gap-4 text-xs text-secondary">
        <NuxtLink to="/" class="hover:text-text transition-colors">Главная</NuxtLink>
        <NuxtLink to="/matches" class="hover:text-text transition-colors">Матчи</NuxtLink>
        <NuxtLink to="/leagues" class="hover:text-text transition-colors">Лиги</NuxtLink>
      </div>
    </div>
  </footer>
</template>
