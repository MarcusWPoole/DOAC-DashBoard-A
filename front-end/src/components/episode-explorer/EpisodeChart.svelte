<script>
    import { onMount, afterUpdate } from 'svelte';
    import Chart from 'chart.js/auto';
    
    export let chartData;
    
    let canvas;
    let chart;
    
    onMount(() => {
      // Create the chart instance
      chart = new Chart(canvas, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
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
              grid: {
                color: 'rgba(255, 255, 255, 0.05)'
              },
              ticks: {
                color: '#CCCCCC'
              }
            },
            y: {
              grid: {
                color: 'rgba(255, 255, 255, 0.05)'
              },
              ticks: {
                color: '#CCCCCC'
              }
            }
          }
        }
      });
    });
    
    afterUpdate(() => {
      // Update the chart when data changes
      if (chart && chartData) {
        chart.data = chartData;
        chart.update();
      }
    });
  </script>
  
  <div class="h-64">
    <canvas bind:this={canvas}></canvas>
  </div>