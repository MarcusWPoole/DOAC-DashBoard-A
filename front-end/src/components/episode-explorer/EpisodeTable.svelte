<script>
    import { format } from 'date-fns';
    import Modal from './Modal.svelte';
  
    export let data = [];
    export let sortField = 'views';
    export let sortDirection = 'desc';
    export let onSort = () => {};
  
    // Modal state
    let showModal = false;
    let selectedEpisode = null;
  
    // Sorting
    function handleSort(field) {
      const newDir = field === sortField && sortDirection === 'desc' ? 'asc' : 'desc';
      onSort(field, newDir);
    }
  
    // Helpers
    const formatNumber = n => {
      if (n >= 1e6) return (n/1e6).toFixed(1)+'M';
      if (n >= 1e3) return (n/1e3).toFixed(1)+'K';
      return n.toString();
    };
    const formatDate = s => format(new Date(s), 'MMM d, yyyy');
  
    // Row click → open modal
    function selectEpisode(ep) {
      selectedEpisode = ep;
      showModal = true;
    }

    function handleRowClick(episode) {
    selectedEpisode = episode;
    showModal = true;
  }
  </script>
  
  <div class="overflow-x-auto border rounded-lg">
    <table class="min-w-full table-fixed">
      <colgroup>
        <col style="width:48px" />
        <col style="width:56px" />
        <col style="width:240px" />
        <col style="width:140px" />
        <col style="width:120px" />
        <col style="width:96px" />
      </colgroup>
      <thead class="sticky top-0 bg-gray-800 text-gray-200">
        <tr>
          <th class="px-2 py-3 cursor-pointer" on:click={() => handleSort('episode')}>
            # {sortField==='episode'?(sortDirection==='desc'?'↓':'↑'):''}
          </th>
          <th class="px-2 py-3">Img</th>
          <th class="px-3 py-3 cursor-pointer" on:click={() => handleSort('title')}>
            Title {sortField==='title'?(sortDirection==='desc'?'↓':'↑'):''}
          </th>
          <th class="px-3 py-3 cursor-pointer" on:click={() => handleSort('guest')}>
            Guest {sortField==='guest'?(sortDirection==='desc'?'↓':'↑'):''}
          </th>
          <th class="px-3 py-3 cursor-pointer" on:click={() => handleSort('date')}>
            Date {sortField==='date'?(sortDirection==='desc'?'↓':'↑'):''}
          </th>
          <th class="px-2 py-3 cursor-pointer" on:click={() => handleSort('views')}>
            Views {sortField==='views'?(sortDirection==='desc'?'↓':'↑'):''}
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-700 text-gray-100">
        {#if data.length === 0}
          <tr><td colspan="6" class="py-8 text-center">No episodes match your filters</td></tr>
        {:else}
          {#each data as ep}
            <tr class="hover:bg-gray-700 cursor-pointer" on:click={() => selectEpisode(ep)}>
              <td class="px-2 py-2 text-center">#{ep.episode}</td>
              <td class="px-2 py-2">
                <img src={ep.thumbnail} alt="" class="w-full h-full object-cover" />
              </td>
              <td class="px-3 py-2">
                <div class="line-clamp-2">{ep.title}</div>
              </td>
              <td class="px-3 py-2 truncate">{ep.guest || 'N/A'}</td>
              <td class="px-3 py-2">{formatDate(ep.date)}</td>
              <td class="px-2 py-2 text-right">{formatNumber(ep.views)}</td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
  
  <!-- Episode details modal -->
  {#if showModal && selectedEpisode}
  <Modal bind:show={showModal} episode={selectedEpisode} {formatNumber} {formatDate} />
{/if}
  
  <style>
    /* Two-line clamp for titles */
    .line-clamp-2 {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  </style>
  