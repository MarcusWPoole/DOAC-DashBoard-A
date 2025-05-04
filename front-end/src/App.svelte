<script>
  import { onMount } from 'svelte';
  import Header from './components/Header.svelte';
  import Navigation from './components/Navigation.svelte';
  import EpisodeExplorer from './components/EpisodeExplorer.svelte';

  let activeTab = 'episode-explorer';
  let isLoading = true;

  function setActiveTab(tab) {
    activeTab = tab;
  }

  onMount(() => {
    // Simulate data loading
    setTimeout(() => {
      isLoading = false;
    }, 1000);
  });
</script>

<main class="min-h-screen pb-12">
  <Header />

  <div class="container mx-auto px-4 mt-8">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-8">
      <div class="lg:col-span-3">
        <Navigation {activeTab} {setActiveTab} />
      </div>

      <div class="lg:col-span-9 fade-in">
        {#if isLoading}
          <div class="flex justify-center items-center h-64">
            <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-[#FFD700]"></div>
          </div>
        {:else}
          {#if activeTab === 'episode-explorer'}
            <EpisodeExplorer />
          {:else if activeTab === 'insightful-trends'}
            <!-- TODO: Insights-->
          {:else if activeTab === 'guest-recommendations'}
            <!--TODO: Guest Recommender-->
          {/if}
        {/if}
      </div>
    </div>
  </div>
</main>

<style>
  main {
    background-color: #121212;
    background-image: radial-gradient(circle at 25px 25px, rgba(255, 215, 0, 0.03) 2%, transparent 0%), 
                      radial-gradient(circle at 75px 75px, rgba(255, 215, 0, 0.02) 2%, transparent 0%);
    background-size: 100px 100px;
  }
</style>