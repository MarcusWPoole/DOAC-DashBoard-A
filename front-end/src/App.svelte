<script>
  import { onMount } from 'svelte';
  import Header from './components/Header.svelte';

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
</main>

<style>
  main {
    background-color: #121212;
    background-image: radial-gradient(circle at 25px 25px, rgba(255, 215, 0, 0.03) 2%, transparent 0%), 
                      radial-gradient(circle at 75px 75px, rgba(255, 215, 0, 0.02) 2%, transparent 0%);
    background-size: 100px 100px;
  }
</style>