<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
  
    export let data = [];
    let canvas;
    let chart;
  
    function renderChart() {
      if (!canvas || data.length === 0) return;
  
      if (chart) chart.destroy();
  
      chart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: data.map(d => d.month),
          datasets: [
            {
              label: 'Views (millions)',
              data: data.map(d => d.views / 1e6),
              borderColor: '#FFD700',
              backgroundColor: 'rgba(255, 215, 0, 0.1)',
              tension: 0.4,
              fill: true,
              yAxisID: 'y1'
            },
            {
              label: 'New Subscribers (millions)',
              data: data.map(d => d.subscribers / 1e6),
              borderColor: '#3B82F6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              tension: 0.4,
              fill: true,
              yAxisID: 'y2'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: '#CCCCCC',
                font: {
                  family: 'roboto'
                }
              }
            },
            tooltip: {
              backgroundColor: '#1A1A1A',
              titleColor: '#FFD700',
              bodyColor: '#FFFFFF',
              borderColor: '#2A2A2A',
              borderWidth: 1,
              padding: 10
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#CCCCCC' }
            },
            y1: {
              type: 'linear',
              position: 'left',
              title: {
                display: true,
                text: 'Views (millions)',
                color: '#FFD700'
              },
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: {
                color: '#FFD700',
                callback: (value) => `${value}M`
              }
            },
            y2: {
              type: 'linear',
              position: 'right',
              title: {
                display: true,
                text: 'Subscribers (millions)',
                color: '#3B82F6'
              },
              grid: { drawOnChartArea: false },
              ticks: {
                color: '#3B82F6',
                callback: (value) => `${value}M`
              }
            }
          }
        }
      });
    }
  
    onMount(() => {
      if (data.length > 0) renderChart();
    });
  
    $: if (data.length > 0) renderChart();
  </script>
  
  <div class="h-[30rem]">
    <canvas bind:this={canvas}></canvas>
  </div>
  