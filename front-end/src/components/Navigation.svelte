<script>
    export let activeTab;
    export let setActiveTab;
  
    import IconHisto from "./IconHisto.svelte";
    import IconHonor from "./IconHonor.svelte";
    import IconTableCont from "./IconTableCont.svelte";
    
    const tabs = [
      { id: 'episode-explorer', label: 'Episode Explorer', icon: IconTableCont },
      { id: 'insightful-trends', label: 'Insightful Trends', icon: IconHisto },
      { id: 'guest-recommendations', label: 'Guest Recommendations', icon: IconHonor }
    ];
  </script>
  
  <div class="card">
    <h2 class="text-xl font-semibold mb-4">Navigation</h2>
  
    <nav>
      <ul class="space-y-2">
        {#each tabs as tab}
          <li>
            <button 
              class="w-full text-left px-4 py-3 rounded-md transition-colors hover:bg-[#2A2A2A] flex items-center
                    {activeTab === tab.id ? 'tab-active' : ''}"
              on:click={() => setActiveTab(tab.id)}
            >
              <span class="mr-3 text-xl w-9">
                <svelte:component this={tab.icon} />
              </span>
              <span class="font-medium">{tab.label}</span>
            </button>
          </li>
        {/each}
      </ul>
    </nav>
  
    <div class="mt-6 pt-6 border-t border-[#2A2A2A]">
      <h3 class="text-sm font-semibold text-gray-400 mb-3">ABOUT</h3>
      <p class="text-sm text-gray-300">
        This dashboard provides comprehensive analytics for The Diary of a CEO podcast, helping to track performance and discover insights for future episodes.
      </p>
    </div>
  </div>
  