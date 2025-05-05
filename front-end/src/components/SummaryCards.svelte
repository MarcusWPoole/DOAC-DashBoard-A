<script>
    export let summary = {
      totalEpisodes: 0,
      totalViews:    0,
      avgViewMin:    0,
      topEpisode:    { episode: 0, title: '', views: 0 },
      topGuest:      { name: null, views: 0 }
    };
  </script>
  
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6 slide-in">
    <!-- Total Episodes -->
    <div class="card">
      <h3 class="text-sm text-gray-400 uppercase">Total Episodes</h3>
      <p class="text-3xl font-bold mt-2">{summary.totalEpisodes}</p>
      <p class="text-sm text-gray-400 mt-1">episodes produced</p>
    </div>
  
    <!-- Average View Duration -->
    <div class="card">
      <h3 class="text-sm text-gray-400 uppercase">Avg Duration</h3>
      <p class="text-3xl font-bold mt-2">
        {summary.avgViewMin.toFixed(1)}&nbsp;min
      </p>
      <p class="text-sm text-gray-400 mt-1">average watch time</p>
    </div>
  
    <!-- Total Views -->
    <div class="card">
      <h3 class="text-sm text-gray-400 uppercase">Total Views</h3>
      <p class="text-accent text-3xl font-bold mt-2">
        {(summary.totalViews / 1_000_000).toFixed(1)} M
      </p>
      <p class="text-sm text-gray-400 mt-1">cumulative views</p>
    </div>
  
    <!-- Top Guest -->
    <div class="card">
      <h3 class="text-sm text-gray-400 uppercase">Top Guest</h3>
      <p class="text-3xl font-bold mt-2 truncate" title={summary.topGuest.name}>
        {summary.topGuest.name ?? '—'}
      </p>
      <p class="text-sm text-gray-400 mt-1">highest engagement</p>
    </div>
  
    <!-- Top Episode -->
    <div class="card">
      <h3 class="text-sm text-gray-400 uppercase">Top Episode</h3>
      <p class="text-3xl font-bold mt-2 truncate" title={summary.topEpisode.title}>
        #{summary.topEpisode.episode}
      </p>
      <p class="text-sm text-gray-400 mt-1">
        {(summary.topEpisode.views / 1_000_000).toFixed(1)} M views
      </p>
    </div>
  </div>
  