<!-- components/HelloWorld.vue -->
<template>
  <div class="hello-world">
    <FileUpload mode="basic" name="demo[]" url="/api/upload" accept="image/*" :maxFileSize="1000000" @upload="onUpload"
      :auto="true" chooseLabel="Browse" />
    <Calendar v-model="buttondisplay" showIcon />
  </div>
</template>

<script setup lang="ts">
// You can add any script here if needed
import FileUpload from 'primevue/fileupload';
</script>

<style scoped>
/* You can add scoped styles here if needed */
</style>

