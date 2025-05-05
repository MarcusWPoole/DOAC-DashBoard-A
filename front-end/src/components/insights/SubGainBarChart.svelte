<script>
    import { onMount, afterUpdate } from 'svelte';
    import Chart from 'chart.js/auto';
  
    export let target = 'subscribersGained';
    export let correlationData = [];
  
    let canvas;
    let chart;
  
    // Prepare the chart dataset
    function formatChartData(data) {
      const sorted = data
        .filter(d => d.target === target)
        .sort((a, b) => a.pearson_r - b.pearson_r);
  
      return {
        labels: sorted.map(d => d.kpi),
        datasets: [
          {
            label: `Correlation with ${target}`,
            data: sorted.map(d => d.pearson_r),
            backgroundColor: sorted.map(d => d.pearson_r > 0 ? '#22C55E' : '#EF4444')
          }
        ]
      };
    }
  
    // Render chart initially
    onMount(() => {
      const chartData = formatChartData(correlationData);
      chart = new Chart(canvas, {
        type: 'bar',
        data: chartData,
        options: {
          indexAxis: 'y',
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
              displayColors: false
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#CCCCCC' },
              title: {
                display: true,
                text: 'Pearson r',
                color: '#CCCCCC'
              }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#CCCCCC' }
            }
          }
        }
      });
    });
  
    // Update on prop change
    afterUpdate(() => {
      if (chart && correlationData.length) {
        chart.data = formatChartData(correlationData);
        chart.update();
      }
    });
  </script>
  
  <div class="h-96">
    <canvas bind:this={canvas}></canvas>
  </div>