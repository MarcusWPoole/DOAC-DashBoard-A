<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
  
    export let topicData = [];
    export let range = 'all';
    let canvas;
    let chart;
  
    function createChart() {
      if (!topicData.length) return;
      if (chart) chart.destroy();
  
      chart = new Chart(canvas, {
        type: 'bubble',
        data: {
          datasets: [{
            label: 'Topic Performance',
            data: topicData.map((d, i) => ({
              x: +d.avg_engagement,
              y: +(d.avg_views / 1_000_000).toFixed(2),
              r: Math.sqrt(d.episode_count) * 4,
              topic: d.topic
            })),
            backgroundColor: topicData.map((_, i) => {
              const colors = [
                'rgba(255, 215, 0, 0.7)',
                'rgba(59, 130, 246, 0.7)',
                'rgba(239, 68, 68, 0.7)',
                'rgba(16, 185, 129, 0.7)',
                'rgba(217, 70, 239, 0.7)',
                'rgba(245, 158, 11, 0.7)',
                'rgba(255, 99, 132, 0.7)',
                'rgba(75, 192, 192, 0.7)'
              ];
              return colors[i % colors.length];
            }),
            borderColor: 'rgba(255, 255, 255, 0.4)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#1A1A1A',
              titleColor: '#FFD700',
              bodyColor: '#FFFFFF',
              borderColor: '#2A2A2A',
              borderWidth: 1,
              padding: 10,
              callbacks: {
                title: items => items[0].raw.topic,
                label: ctx => [
                  `Engagement: ${ctx.raw.x.toFixed(1)}%`,
                  `Avg Views: ${ctx.raw.y.toFixed(2)}M`,
                  `Episodes: ${ctx.raw.r ? Math.round((ctx.raw.r/4)**2) : 0}`
                ]
              }
            }
          },
          scales: {
            x: {
              min: 10,
              max: 30,
              title: { display: true, text: 'Engagement %', color: '#CCCCCC' },
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#CCCCCC' }
            },
            y: {
              beginAtZero: true,
              title: { display: true, text: 'Avg Views (millions)', color: '#CCCCCC' },
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#CCCCCC' }
            }
          }
        }
      });
    }
  
    onMount(createChart);
    $: topicData, createChart();
  </script>
  
  <div class="h-64 bg-transparent">
    <canvas bind:this={canvas}></canvas>
  </div>
  
  <div class="mt-4 text-xs text-gray-400">
    <p class="mb-1">Bubble size represents number of episodes on the topic</p>
    <div class="grid grid-cols-2 gap-2">
      {#each topicData as item, idx}
        <div class="flex items-center">
          <span
            class="w-2 h-2 rounded-full inline-block mr-1"
            style="background-color: {[
              'rgba(255, 215, 0, 0.7)',
              'rgba(59, 130, 246, 0.7)',
              'rgba(239, 68, 68, 0.7)',
              'rgba(16, 185, 129, 0.7)',
              'rgba(217, 70, 239, 0.7)',
              'rgba(245, 158, 11, 0.7)',
              'rgba(255, 99, 132, 0.7)',
              'rgba(75, 192, 192, 0.7)'
            ][idx % 8]}"
          ></span>
          {item.topic}
        </div>
      {/each}
    </div>
  </div>