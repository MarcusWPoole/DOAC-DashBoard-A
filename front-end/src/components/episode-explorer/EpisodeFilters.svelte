<script>
    import { createEventDispatcher } from 'svelte';
  
    const dispatch = createEventDispatcher();
  
    // Props from parent
    export let dateRange = { start: null, end: null };
    export let selectedMetric;
    export let metricOptions = [];      // e.g. [{value:'views',label:'Views'},…]
    export let metricMin = 0;           // from API: true minimum for selectedMetric
    export let metricMax = 0;           // from API: true maximum for selectedMetric
  
    // Local slider state
    let rangeMin = metricMin;
    let rangeMax = metricMax;
  
    // Whenever the metric or its bounds change, re-set the sliders
    $: if (selectedMetric !== undefined) {
      rangeMin = metricMin;
      rangeMax = metricMax;
    }
  
    // Helpers to format/parse dates
    function formatDateValue(date) {
      if (!date) return '';
      const d = new Date(date);
      return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
    }
    function parseDateValue(val) {
      return val ? new Date(val) : null;
    }
  
    // Emit filterUpdate for parent to fetch new data
    function applyFilters() {
      dispatch('filterUpdate', {
        date_from: dateRange.start ? formatDateValue(dateRange.start) : undefined,
        date_to:   dateRange.end   ? formatDateValue(dateRange.end)   : undefined,
        metric:    selectedMetric,
        min_metric: rangeMin,
        max_metric: rangeMax
      });
    }
  
    function resetFilters() {
      dateRange = { start: null, end: null };
      selectedMetric = metricOptions[0]?.value;
      rangeMin = metricMin;
      rangeMax = metricMax;
      applyFilters();
    }
  </script>
  
  <div class="card p-4 space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Date From -->
      <div>
        <label class="block text-sm text-gray-400 mb-1">Date From</label>
        <input 
          type="date"
          bind:value={dateRange.start}
          on:change={() => dateRange.start = parseDateValue(dateRange.start)}
          class="w-full border rounded px-3 py-2 text-sm"
        />
      </div>
  
      <!-- Date To -->
      <div>
        <label class="block text-sm text-gray-400 mb-1">Date To</label>
        <input 
          type="date"
          bind:value={dateRange.end}
          on:change={() => dateRange.end = parseDateValue(dateRange.end)}
          class="w-full border rounded px-3 py-2 text-sm"
        />
      </div>
  
      <!-- Metric Selector -->
      <div>
        <label class="block text-sm text-gray-400 mb-1">Metric</label>
        <select
          bind:value={selectedMetric}
          class="w-full border rounded px-3 py-2 text-sm"
        >
          {#each metricOptions as opt}
            <option value={opt.value}>{opt.label}</option>
          {/each}
        </select>
      </div>
    </div>
  
    <!-- Metric Range Slider -->
    <div>
      <label class="block text-sm text-gray-400 mb-1">
        {metricOptions.find(o => o.value === selectedMetric)?.label}:
        {rangeMin.toLocaleString()} – {rangeMax.toLocaleString()}
      </label>
      <div class="flex space-x-2 items-center">
        <input
          type="range"
          min={metricMin}
          max={metricMax}
          step={(metricMax - metricMin) / 100 || 1}
          bind:value={rangeMin}
          class="flex-1 h-2"
        />
        <input
          type="range"
          min={metricMin}
          max={metricMax}
          step={(metricMax - metricMin) / 100 || 1}
          bind:value={rangeMax}
          class="flex-1 h-2"
        />
      </div>
    </div>
  
    <!-- Actions -->
    <div class="flex justify-end space-x-2">
      <button 
        class="btn btn-secondary px-4 py-2 text-sm"
        on:click={resetFilters}
      >
        Reset
      </button>
      <button 
        class="btn btn-primary px-4 py-2 text-sm"
        on:click={applyFilters}
      >
        Apply
      </button>
    </div>
  </div>
  