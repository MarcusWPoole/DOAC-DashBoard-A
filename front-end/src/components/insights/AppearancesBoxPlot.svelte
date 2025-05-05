<script>
    import { onMount } from 'svelte';
    import Plotly from 'plotly.js-dist-min';
  
    let chartDiv;
    export let data = [];
  
    function renderBoxplot(data) {
      const grouped = {};
  
      for (const d of data) {
        const key = d.appearance_num;
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(d.subs_to_views_ratio);
      }
  
      const traces = Object.entries(grouped).map(([appearance, ratios]) => ({
        y: ratios,
        type: 'box',
        name: `#${appearance}`,
        boxpoints: 'all',
        jitter: 0.4,
        pointpos: -1.8,
        marker: { color: 'rgba(0,0,0,0.5)', size: 5 },
        fillcolor: 'rgba(124, 252, 0, 0.2)',
        line: { color: '#4ADE80' }
      }));
  
      Plotly.newPlot(chartDiv, traces, {
        title: 'Subs-to-Views Ratio by Appearance Number (Recurring Guests)',
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#CCCCCC', family: 'Inter' },
        xaxis: {
          title: 'Appearance Number',
          gridcolor: 'rgba(255, 255, 255, 0.05)'
        },
        yaxis: {
          title: 'Subscribers-to-Views Ratio',
          gridcolor: 'rgba(255, 255, 255, 0.05)'
        },
        margin: { t: 50, r: 30, b: 50, l: 60 },
        showlegend: false
      }, { responsive: true });
    }
  
    $: if (data.length > 0) renderBoxplot(data);
  </script>
  
  <div class="h-96">
    <div bind:this={chartDiv} class="w-full h-full"></div>
  </div>
  