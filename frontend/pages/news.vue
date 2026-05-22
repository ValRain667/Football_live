<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Новости</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <article v-for="i in 6" :key="i" class="glass rounded-2xl overflow-hidden hover:glass-hover transition-all group">
        <div class="h-40 bg-gradient-to-br from-accent/10 to-transparent"/>
        <div class="p-5">
          <div class="flex items-center gap-2 text-xs text-secondary mb-2">
            <span>22 мая 2026</span>
            <span>·</span>
            <span>Футбол</span>
          </div>
          <h3 class="font-bold text-base mb-2 group-hover:text-accent transition-colors">
            Главные новости футбола {{ i }}
          </h3>
          <p class="text-sm text-secondary line-clamp-3">
            Последние события из мира футбола: трансферы, результаты матчей и аналитика ведущих турниров.
          </p>
        </div>
      </article>
    </div>
  </div>
</template>
