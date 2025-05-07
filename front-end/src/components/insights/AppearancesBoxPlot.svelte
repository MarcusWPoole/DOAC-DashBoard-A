<script>
    import { onMount } from 'svelte';
    import Plotly from 'plotly.js-dist-min';
  
    let chartDiv;
    export let data = [];
  export let range = '12m'; // receive selected range from parent
  
    $: if (data.length > 0 && chartDiv) {
    Plotly.purge(chartDiv);
    renderBoxplot(data);
  }
  
    function renderBoxplot(data) {
      const grouped = {};
  
      for (const d of data) {
        const key = parseInt(d.appearance_num);
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(d.subs_to_views_ratio);
      }
  
      const sortedKeys = Object.keys(grouped).map(Number).sort((a, b) => a - b);
  
      const traces = sortedKeys.map(appearance => ({
        y: grouped[appearance],
        type: 'box',
        name: `${appearance}`,
        boxpoints: 'all',
        jitter: 0.3,
        pointpos: 0,
        marker: {
          color: '#CCCCCC',
          size: 6,
          line: { width: 0.5, color: '#444' }
        },
        fillcolor: 'rgba(34, 197, 94, 0.15)',
        line: { color: '#4ADE80' }
      }));
  
      Plotly.newPlot(chartDiv, traces, {
        title: 'Subs-to-Views Ratio by Number of Appearances by a Guest(Recurring Guests)',
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#CCCCCC', family: 'roboto' },
        xaxis: {
          title: {
            text: 'Number of Appearances',
            font: { color: '#CCCCCC' }
          },
          gridcolor: 'rgba(255, 255, 255, 0.05)',
          color: '#CCCCCC',
          tickmode: 'linear',
          tick0: 1,
          dtick: 1
        },
        yaxis: {
          title: {
            text: 'Subscribers-to-Views Ratio',
            font: { color: '#CCCCCC' }
          },
          gridcolor: 'rgba(255, 255, 255, 0.05)',
          color: '#CCCCCC'
        },
        margin: { t: 60, r: 40, b: 80, l: 90 },
        showlegend: false
      }, { responsive: true });
    }
  </script>
  
  <div class="h-[500px]">
    <div bind:this={chartDiv} class="w-full h-full"></div>
  </div>
  