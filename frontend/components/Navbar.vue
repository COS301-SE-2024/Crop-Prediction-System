<template>
  <nav class="p-2 h-[65px] z-50 w-full shadow-md">
    <div class="flex justify-between items-center h-full">
      <Sidebar />
      <img src="../assets/logo.png" alt="Logo" class="h-full object-cover self-center" />
      <div class="flex flex-row items-center gap-4">
        <i class="pi pi-bell" style="font-size: 1.5rem"></i>
        <i class="pi pi-user" style="font-size: 1.5rem"><i>
            <i class="pi pi-cog" style="font-size: 1.5rem"></i>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import Sidebar from "../components/Sidebar.vue";
</script>
