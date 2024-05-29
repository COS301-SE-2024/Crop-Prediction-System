<template>
  <div>
    <header>
      <Navbar />
    </header>
  </div>

  <div>
    <slot />
  </div>
</template>

<script setup lang="ts">
import Navbar from "~/components/Navbar.vue"
</script>
