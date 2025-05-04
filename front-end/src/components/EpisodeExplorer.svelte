<script>
    import { onMount } from 'svelte';
    import EpisodeFilters from './episode-explorer/EpisodeFilters.svelte';
    import EpisodeTable   from './episode-explorer/EpisodeTable.svelte';
    import EpisodeChart   from './episode-explorer/EpisodeChart.svelte';
  
    // All episodes (unfiltered) & filtered results
    let episodeData = [];
    let filteredData = [];
  
    // Error/loading
    let error = null;
    let loading = true;
  
    // Filter state
    let dateRange     = { start: null, end: null };
    let metricOptions = [
      { value: 'views',           label: 'Views' },
      { value: 'shares',          label: 'Shares' },
      { value: 'likes',           label: 'Likes' },
      { value: 'dislikes',        label: 'Dislikes' },
      { value: 'avgViewDuration', label: 'Watch %' },
      { value: 'subsGained',      label: 'Subs Gained' },
      { value: 'subsLost',        label: 'Subs Lost' }
    ];
    let selectedMetric = 'views';
  
    // Metric slider bounds
    let metricMin = 0;
    let metricMax = 0;
    // Current slider values
    let rangeMin = 0;
    let rangeMax = 0;
  
    // Sort state
    let sortField     = 'date';
    let sortDirection = 'desc';
  
    // Chart data
    let chartData = { labels: [], datasets: [] };
  
    // Helper: format dates for querystring
    const fmt = d => d?.toISOString().split('T')[0];
  
    // 1) On mount: fetch unfiltered episodes + metric bounds
    onMount(async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8001/api/episodes?metric=${selectedMetric}`, { mode: 'cors' });
        if (!res.ok) throw new Error(res.statusText);
        const json = await res.json();
        episodeData   = json.episodes;
        filteredData  = json.episodes;
        metricMin     = json.metricMin;
        metricMax     = json.metricMax;
        rangeMin      = metricMin;
        rangeMax      = metricMax;
        updateChartData();
      } catch (e) {
        error = e.message;
      } finally {
        loading = false;
      }
    });
  
    // 2) When filters change, re-fetch
    async function applyFilters({ dateRange: dr, viewsRange, metric }) {
      dateRange      = dr;
      selectedMetric = metric;
      rangeMin       = viewsRange.min;
      rangeMax       = viewsRange.max;
  
      const url = new URL('http://127.0.0.1:8001/api/episodes');
      if (dateRange.start)   url.searchParams.set('date_from', fmt(dateRange.start));
      if (dateRange.end)     url.searchParams.set('date_to',   fmt(dateRange.end));
      url.searchParams.set('metric',     selectedMetric);
      url.searchParams.set('min_metric', rangeMin);
      url.searchParams.set('max_metric', rangeMax);
  
      loading = true;
      try {
        const res  = await fetch(url.toString(), { mode: 'cors' });
        if (!res.ok) throw new Error(res.statusText);
        const json = await res.json();
        filteredData = json.episodes;
        // update bounds (in case after date/guest filtering they shift)
        metricMin = json.metricMin;
        metricMax = json.metricMax;
        updateChartData();
      } catch (e) {
        error = e.message;
      } finally {
        loading = false;
      }
    }
  
    // 3) Sorting helper
    function sortData(field, direction) {
      sortField     = field;
      sortDirection = direction;
      filteredData = filteredData.slice().sort((a, b) => {
        let av = a[field], bv = b[field];
        if (field === 'date') {
          av = new Date(av);
          bv = new Date(bv);
        } else {
          av = Number(av);
          bv = Number(bv);
        }
        return direction === 'asc' ? (av > bv ? 1 : -1) : (bv > av ? 1 : -1);
      });
    }
  
    // 4) Build chart data from filtered & sorted episodes
    function updateChartData() {
      const top = filteredData
        .slice()
        .sort((a, b) => Number(b[selectedMetric]) - Number(a[selectedMetric]))
        .slice(0, 10);
      chartData = {
        labels: top.map(ep => `#${ep.episode}`),
        datasets: [{
          label: metricOptions.find(o => o.value === selectedMetric).label,
          data: top.map(ep => {
            const val = ep[selectedMetric];
            if (selectedMetric === 'views') return val / 1e6;
            if (selectedMetric === 'shares') return val / 1e3;
            return val;
          }),
          backgroundColor: 'rgba(255,215,0,0.7)',
          borderColor:     '#FFD700',
          borderWidth:     1
        }]
      };
    }
  </script>
  
  {#if loading}
    <p>Loading…</p>
  {:else if error}
    <p class="text-red-600">Error: {error}</p>
  {:else}
    <div class="flex justify-between mb-6">
      <h2 class="text-2xl font-bold">Episode Explorer</h2>
      <!-- Export button etc. -->
    </div>
  
    <!-- Filters (date range + metric selector + metric-range sliders) -->
    <EpisodeFilters
      {dateRange}
      minMetric={metricMin}
      maxMetric={metricMax}
      {selectedMetric}
      metricOptions={metricOptions}
      on:filterUpdate={e => applyFilters(e.detail)}
    />
  
    <div class="grid lg:grid-cols-2 gap-6 mt-6">
      <div class="card">
        <h3 class="mb-4 text-lg font-semibold">
          Top Episodes by {metricOptions.find(o => o.value === selectedMetric).label}
        </h3>
        <EpisodeChart {chartData} />
      </div>
      <div class="card">
        <h3 class="mb-4 text-lg font-semibold">Key Insights</h3>
        <!-- static or dynamic insights -->
      </div>
    </div>
  
    <div class="card mt-6">
      <div class="flex justify-between mb-4">
        <h3 class="text-lg font-semibold">Episode List</h3>
        <p class="text-sm text-gray-400">
          Showing {filteredData.length} of {episodeData.length} episodes
        </p>
      </div>
      <EpisodeTable
        data={filteredData}
        {sortField}
        {sortDirection}
        onSort={sortData}
      />
    </div>
  {/if}
  