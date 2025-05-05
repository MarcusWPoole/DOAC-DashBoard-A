<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
    import RangeSlider from 'svelte-range-slider-pips';
  
    const dispatch = createEventDispatcher();
  
    // Props from parent
    export let dateRange = { start: null, end: null };
    export let metric = ''; // incoming from parent
  export let metricOptions = [];


    let rangeValues = [0, 0];
    let boundsLoading = false;
    let error = null;
    let start = dateRange.start;
    let end = dateRange.end;
  
    // Track previous metric for reset logic
    let prevMetric = null;
  
    // Internal copies of bounds for slider use
    let internalMin = 0;
    let internalMax = 0;

    let lastLoadedMetric = null;
  
    // Fetch metric options on mount
    onMount(() => {
      loadMetrics();
    });
  
    async function loadMetrics() {
      try {
        const res = await fetch('http://127.0.0.1:8001/api/metrics');
        if (!res.ok) throw new Error(res.statusText);
        metricOptions = await res.json();
        await loadBounds(metric);
      } catch (err) {
        console.error('Failed to load metrics', err);
      }
    }
  
    async function loadBounds(m, force = false) {
  if (!force && m === lastLoadedMetric) return;

  boundsLoading = true;
  error = null;
  try {
    const res = await fetch(`http://127.0.0.1:8001/api/episodes/bounds?metric=${encodeURIComponent(m)}`);
    if (!res.ok) throw new Error(res.statusText);
    const { metricMin: min, metricMax: max } = await res.json();

    internalMin = min;
    internalMax = max;

    if (force || m !== prevMetric) {
      rangeValues = [min, max];
      prevMetric = m;
    }

    lastLoadedMetric = m;
  } catch (err) {
    console.error('Bounds error:', err);
    error = 'Failed to load bounds';
  } finally {
    boundsLoading = false;
  }
}

function onMetricChange(e) {
  metric = e.target.value;
  loadBounds(metric, true);
}



    function onStartChange(val) { start = val; }
    function onEndChange(val) { end = val; }
    function onSliderChange(e) { rangeValues = e.detail.values; }
  
    function resetFilters() {
  start = null;
  end = null;
  metric = metricOptions[0]?.value;
  loadBounds(metric, true);
}
  
    function applyAll() {
      if (!rangeValues || rangeValues.length < 2) return;
  
      dispatch('filterUpdate', {
        dateRange: { start, end },
        viewsRange: {
          min: rangeValues[0],
          max: rangeValues[1]
        },
        metric
      });
    }
  
    function parseDateValue(val) {
      return val ? new Date(val) : null;
    }
  </script>
  
  <div class="card p-4 space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div>
        <label for="start-date" class="block text-sm text-gray-400 mb-1">Date From</label>
        <input id="start-date" type="date" bind:value={start}
          on:change={() => onStartChange(parseDateValue(start))}
          class="bg-[#2A2A2A] rounded px-3 py-2 text-sm w-full focus:outline-none focus:ring-1 focus:ring-[#FFD700]" />
      </div>
      <div>
        <label for="end-date" class="block text-sm text-gray-400 mb-1">Date To</label>
        <input id="end-date" type="date" bind:value={end}
          on:change={() => onEndChange(parseDateValue(end))}
          class="bg-[#2A2A2A] rounded px-3 py-2 text-sm w-full focus:outline-none focus:ring-1 focus:ring-[#FFD700]" />
      </div>
      <div>
        <label class="block text-sm text-gray-400 mb-1">Metric</label>
        <select bind:value={metric} on:change={onMetricChange}
          class="bg-[#2A2A2A] rounded px-3 py-2 text-sm w-full focus:outline-none focus:ring-1 focus:ring-[#FFD700]">
          {#each metricOptions as opt}
            <option value={opt.value}>{opt.label}</option>
          {/each}
        </select>
      </div>
    </div>
  
    <div>
      <label class="block text-sm text-gray-400 mb-1">
        {metricOptions.find(o => o.value === metric)?.label}:
        {#if boundsLoading}
          Loading bounds...
        {:else if error}
          <span class="text-red-500">{error}</span>
        {:else}
          {rangeValues[0].toLocaleString()} – {rangeValues[1].toLocaleString()}
        {/if}
      </label>
      <RangeSlider
        min={internalMin}
        max={internalMax}
        step={(internalMax - internalMin) / 100 || 1}
        values={rangeValues}
        on:change={onSliderChange}
        disabled={boundsLoading}
        ariaLabel={[
          `${metricOptions.find(o => o.value === metric)?.label} minimum`,
          `${metricOptions.find(o => o.value === metric)?.label} maximum`
        ]}
      />
    </div>
  
    <div class="flex justify-end space-x-2">
      <button class="btn btn-secondary px-4 py-2 text-sm" on:click={resetFilters}>
        Reset
      </button>
      <button class="btn btn-primary px-4 py-2 text-sm" on:click={applyAll}>
        Apply
      </button>
    </div>
  </div>