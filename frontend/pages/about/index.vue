
<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <h1 class="text-4xl font-bold text-pink">This is the SECOND about page!</h1>
    <NuxtLink to="/" class="text-2xl font-bold text-black hover:underline">Go to Home</NuxtLink>
    <HelloWorld />
  </div>
</template>

<script setup lang="ts">
import HelloWorld from '../../components/HelloWorld.vue';
</script>
