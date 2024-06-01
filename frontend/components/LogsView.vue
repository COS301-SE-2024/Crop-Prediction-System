
<template>
    <DataTable :value="entries">
        <template #header>
            <div class="flex flex-wrap align-items-center justify-between gap-2">
                <span class="text-xl text-900 font-bold">Data Entry Logs</span>
                <Button icon="pi pi-refresh" rounded raised />
            </div>
        </template>
        <Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header"></Column>
    </DataTable>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

class Entry {
    entry_id: number;
    created_at: Date;
    weather_temperature: number;
    weather_humidity: number;
    weather_uv: number;
    weather_rainfall: number;
    soil_moisture: number;
    soil_ph: number;
    soil_conductivity: number;
    is_manual: boolean;
    field_id: number;
};

const entries = ref<Entry[]>([]);
const columns = [
    { field: 'entry_id', header: 'Entry ID' },
    { field: 'created_at', header: 'Created At' },
    { field: 'weather_temperature', header: 'Temperature' },
    { field: 'weather_humidity', header: 'Humidity' },
    { field: 'weather_uv', header: 'UV Index' },
    { field: 'weather_rainfall', header: 'Rainfall' },
    { field: 'soil_moisture', header: 'Moisture' },
    { field: 'soil_ph', header: 'pH' },
    { field: 'soil_conductivity', header: 'Conductivity' },
    { field: 'is_manual', header: 'Manual Entry' },
    { field: 'field_id', header: 'Field ID' }
];

for (let i = 0; i < 100; i++) {
    entries.value.push({
        entry_id: i,
        created_at: new Date(),
        weather_temperature: parseFloat((Math.random() * 100).toFixed(2)),
        weather_humidity: parseFloat((Math.random() * 100).toFixed(2)),
        weather_uv: parseFloat((Math.random() * 10).toFixed(2)),
        weather_rainfall: parseFloat((Math.random() * 100).toFixed(2)),
        soil_moisture: parseFloat((Math.random() * 100).toFixed(2)),
        soil_ph: parseFloat((Math.random() * 14).toFixed(2)),
        soil_conductivity: parseFloat((Math.random() * 100).toFixed(2)),
        is_manual: Math.random() > 0.5,
        field_id: Math.floor(Math.random() * 10)
    });
}

</script>
