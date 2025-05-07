<script>
  import { onMount } from 'svelte';
  import Header          from './components/Header.svelte';
  import Navigation      from './components/Navigation.svelte';
  import EpisodeExplorer from './components/EpisodeExplorer.svelte';
  import InsightfulTrends from './components/InsightfulTrends.svelte';
  import SummaryCards    from './components/SummaryCards.svelte';
  import GuestRecommendations from './components/GuestRecommendations.svelte';
  import EpisodeForecasting from './components/EpisodeForecasting.svelte';

  let activeTab  = 'episode-explorer';
  let isLoading  = true;
  let summary    = null;     // will hold the summary-cards data
  let episodes   = [];       // still used by EpisodeExplorer

  onMount(async () => {
    try {
      const [summaryRes, episodesRes] = await Promise.all([
        fetch('http://localhost:8001/api/episodes/summary'),
        fetch('http://localhost:8001/api/episodes')
      ]);

      if (!summaryRes.ok || !episodesRes.ok) throw new Error('API error');

      summary  = await summaryRes.json();
      episodes = (await episodesRes.json()).episodes;
    } catch (err) {
      console.error(err);
    } finally {
      isLoading = false;
    }
  });

  const setActiveTab = tab => (activeTab = tab);
</script>

<main class="min-h-screen pb-12">
  <Header />

  <div class="container mx-auto px-4 mt-8">
    {#if summary}
      <SummaryCards {summary} />
    {/if}

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
            <EpisodeExplorer {episodes} />
            {:else if activeTab === 'insightful-trends'}
            <InsightfulTrends {episodes} />
            {:else if activeTab === 'guest-recommendations'}
            <GuestRecommendations />
            {:else if activeTab === 'episode-forecasting'}
            <EpisodeForecasting />
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