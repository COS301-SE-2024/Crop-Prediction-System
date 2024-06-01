<template>
    <div>
        <div>
            <Chart type="polarArea" :data="chartData" :options="chartOptions" class="h-96" />
        </div>
    </div>
</template>

<script setup lang="ts">
import Chart from 'primevue/chart';
import Tag from 'primevue/tag';
import { ref, onMounted, defineProps } from "vue"

const props = defineProps({
    chartData: {
        type: Object,
        required: true
    }
});

onMounted(() => {
    chartData.value = setChartData();
    chartOptions.value = setChartOptions();
});

const chartData = ref();
const chartOptions = ref();
        
const setChartData = () => {
    const documentStyle = getComputedStyle(document.documentElement);

    return {
        labels: ['Moisture', 'Temperature', 'Humidity', 'Soil', 'Rainfall'],
        datasets: [
            {
                label: false,
                data: props.chartData,
                fill: true,
                backgroundColor: [
                    // moisture
                    'rgba(255, 99, 132, 0.2)',
                    // temperature
                    'rgba(54, 162, 235, 0.2)',
                    // humidity
                    'rgba(255, 206, 86, 0.2)',
                    // soil
                    'rgba(75, 192, 192, 0.2)',
                    // rainfall
                    'rgba(153, 102, 255, 0.2)'
                ],
                tension: 0.4
            }
        ]
    };
};
const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);

    return {
        maintainAspectRatio: false,
        responsive: true,
        width: 100,
        plugins: {
            legend: {
                display: false,
            }
        },
        scales: {
            x: {
                ticks: {
                    display: false
                },
                grid: {
                    display: false
                }
            },
            y: {
                ticks: {
                    display: false
                },
                grid: {
                    display: false
                }
            }
        }
    };
}
</script>