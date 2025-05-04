<script>
    import { onMount } from 'svelte';
  
    // Local state for episodes and error
    let episodes = [];
    let error = null;
  
    onMount(async () => {
      try {
        const res = await fetch('http://127.0.0.1:8001/api/episodes');
        if (!res.ok) throw new Error(`Status ${res.status}`);
        episodes = await res.json();
      } catch (e) {
        error = e.message;
      }
    });
  </script>
  
  {#if error}
    <p class="text-red-600">Error loading episodes: {error}</p>
  {:else if episodes.length === 0}
    <p>Loading episodes…</p>
  {:else}
    <table class="min-w-full border">
      <thead>
        <tr class="bg-gray-100">
          <th class="px-4 py-2 border">#</th>
          <th class="px-4 py-2 border">Title</th>
          <th class="px-4 py-2 border">Guest</th>
          <th class="px-4 py-2 border">Date</th>
          <th class="px-4 py-2 border">Views</th>
        </tr>
      </thead>
      <tbody>
        {#each episodes as ep}
          <tr class="hover:bg-gray-50">
            <td class="px-4 py-2 border">{ep.episode}</td>
            <td class="px-4 py-2 border">{ep.title}</td>
            <td class="px-4 py-2 border">{ep.guest ?? '-'}</td>
            <td class="px-4 py-2 border">{ep.date}</td>
            <td class="px-4 py-2 border">{ep.views.toLocaleString()}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
  