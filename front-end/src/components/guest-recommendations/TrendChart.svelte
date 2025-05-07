<script>
    import { onMount, afterUpdate } from 'svelte';
    import Chart from 'chart.js/auto';
    
    export let guest;
    
    let canvas;
    let chart;
    
    function createChart() {
      if (chart) chart.destroy();
      
      chart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: guest.trendData.map(d => d.date),
          datasets: [{
            label: 'Google Trend Score',
            data: guest.trendData.map(d => d.value),
            borderColor: '#FFD700',
            backgroundColor: 'rgba(255, 215, 0, 0.1)',
            tension: 0.4,
            fill: true
          }]
        },
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
              padding: 10
            },
            title: {
              display: true,
              text: '90-Day Trend Activity',
              color: '#CCCCCC',
              font: {
                size: 12
              }
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              },
              ticks: {
                display: false
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
    }
    
    onMount(() => {
      createChart();
    });
    
    afterUpdate(() => {
      createChart();
    });
  </script>
  
  <div class="h-32">
    <canvas bind:this={canvas}></canvas>
  </div>