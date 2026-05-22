<template>
  <section class="relative overflow-hidden rounded-3xl mx-4 mt-6 p-8 md:p-12 min-h-[320px] flex flex-col justify-center">
    <div class="absolute inset-0 bg-gradient-to-br from-accent/10 to-transparent"/>
    <div class="absolute inset-0 glass rounded-3xl"/>
    <div class="relative z-10 max-w-2xl">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-live/10 border border-live/20 mb-4">
        <span class="w-2 h-2 rounded-full bg-live animate-pulse"/>
        <span class="text-live text-xs font-semibold uppercase tracking-wider">Live Matches</span>
      </div>
      <h1 class="text-4xl md:text-5xl font-extrabold leading-tight mb-4">
        Football <span class="text-accent neon-accent">Live Hub</span>
      </h1>
      <p class="text-secondary text-lg mb-6 max-w-lg">
        Live scores, standings, team stats and match analytics from top leagues around the world.
      </p>
      <div class="flex gap-3">
        <NuxtLink to="/live" class="px-6 py-3 rounded-xl bg-accent text-bg font-bold hover:opacity-90 transition-opacity">
          Смотреть Live
        </NuxtLink>
        <NuxtLink to="/matches" class="px-6 py-3 rounded-xl bg-white/5 font-medium hover:bg-white/10 transition-colors">
          Расписание
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
