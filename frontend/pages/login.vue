<template>
  <div class="max-w-md mx-auto px-4 py-12">
    <div class="glass rounded-2xl p-8">
      <h1 class="text-2xl font-bold mb-6 text-center">Вход</h1>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm text-secondary mb-1">Email</label>
          <input v-model="email" type="email" required class="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-text outline-none focus:border-accent/50 transition-colors" />
        </div>
        <div>
          <label class="block text-sm text-secondary mb-1">Пароль</label>
          <input v-model="password" type="password" required class="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-text outline-none focus:border-accent/50 transition-colors" />
        </div>
        <button type="submit" class="w-full py-3 rounded-xl bg-accent text-bg font-bold hover:opacity-90 transition-opacity">
          Войти
        </button>
      </form>
      <p class="text-center text-sm text-secondary mt-4">
        Нет аккаунта? <NuxtLink to="/register" class="text-accent hover:underline">Зарегистрироваться</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';

const auth = useAuthStore();
const router = useRouter();
const email = ref('');
const password = ref('');

async function handleLogin() {
  await auth.login(email.value, password.value);
  router.push('/');
}
</script>
