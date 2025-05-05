<script>
    import { onMount } from 'svelte';
    import Plotly from 'plotly.js-dist-min';
  
    export let data = [];
    let chartDiv;
  
    $: if (data.length > 0) renderScatter();
  
    function renderScatter() {
      const views = data.map(d => d.views);
      const durations = data.map(d => d.averageViewDuration);
      const labels = data.map(d => `${d.episode}: ${d.title}`);
      const categories = [...new Set(data.map(d => d.content_efficiency))];
      const colors = [
        '#10B981', '#3B82F6', '#F59E0B', '#EF4444'
      ];
  
      const traces = categories.map((category, i) => {
        const filtered = data.filter(d => d.content_efficiency === category);
        return {
          x: filtered.map(d => d.views),
          y: filtered.map(d => d.averageViewDuration),
          text: filtered.map(d => `${d.episode}: ${d.title}`),
          mode: 'markers',
          type: 'scatter',
          name: category,
          marker: {
            size: 10,
            color: colors[i % colors.length],
            opacity: 0.8,
            line: { width: 0.5, color: '#000' }
          },
          hoverinfo: 'text'
        };
      });
  
      const viewsMedian = median(views);
      const durationMedian = median(durations);
  
      const shapes = [
        {
          type: 'line',
          x0: viewsMedian,
          x1: viewsMedian,
          y0: Math.min(...durations),
          y1: Math.max(...durations),
          line: {
            dash: 'dot',
            color: 'gray',
            width: 1
          }
        },
        {
          type: 'line',
          x0: Math.min(...views),
          x1: Math.max(...views),
          y0: durationMedian,
          y1: durationMedian,
          line: {
            dash: 'dot',
            color: 'gray',
            width: 1
          }
        }
      ];
  
      Plotly.newPlot(chartDiv, traces, {
        title: 'Content Efficiency: Views vs Avg. View Duration',
        xaxis: {
          title: 'Views (log scale)',
          type: 'log',
          gridcolor: 'rgba(255, 255, 255, 0.05)',
          color: '#CCCCCC'
        },
        yaxis: {
          title: 'Average View Duration (sec)',
          gridcolor: 'rgba(255, 255, 255, 0.05)',
          color: '#CCCCCC'
        },
        shapes,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#CCCCCC', family: 'Inter' },
        margin: { t: 50, r: 20, b: 50, l: 60 },
        legend: {
          x: 1,
          y: 1,
          bgcolor: 'transparent'
        }
      }, { responsive: true });
    }
  
    function median(arr) {
      const sorted = [...arr].sort((a, b) => a - b);
      const mid = Math.floor(sorted.length / 2);
      return sorted.length % 2 !== 0
        ? sorted[mid]
        : (sorted[mid - 1] + sorted[mid]) / 2;
    }
  </script>
  
  <div class="h-96">
    <div bind:this={chartDiv} class="w-full h-full"></div>
  </div>
  