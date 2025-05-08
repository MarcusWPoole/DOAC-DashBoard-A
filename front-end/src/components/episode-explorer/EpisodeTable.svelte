<script>
    import { format } from 'date-fns';
    import Modal from './Modal.svelte';
  
    export let data = [];
    export let sortField = 'views';
    export let sortDirection = 'desc';
    export let onSort = () => {};
  
    // Pagination props
    export let currentPage = 1;
    export let itemsPerPage = 10;
    export let onPageChange = () => {};
  
    // Derived values
    $: totalPages = Math.max(1, Math.ceil(data.length / itemsPerPage));
    $: if (currentPage > totalPages) onPageChange(totalPages);
  
    // Paginated data
    $: paginatedData = data.slice(
      (currentPage - 1) * itemsPerPage,
      currentPage * itemsPerPage
    );
  
    // Build standard UX pagination with ellipses
    function makePages(cur, total) {
      const delta = 2; // pages around current
      if (total <= 5) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }
      const pages = [1];
      const left = Math.max(2, cur - delta);
      const right = Math.min(total - 1, cur + delta);
      if (left > 2) pages.push('...');
      for (let i = left; i <= right; i++) {
        pages.push(i);
      }
      if (right < total - 1) pages.push('...');
      pages.push(total);
      return pages;
    }
    $: pagesToShow = makePages(currentPage, totalPages);
  
    // Modal state
    let showModal = false;
    let selectedEpisode = null;
  
    // Sorting handler
    function handleSort(field) {
      const newDir = field === sortField && sortDirection === 'desc' ? 'asc' : 'desc';
      onSort(field, newDir);
    }
  
    // Formatting helpers
    const formatNumber = n => {
      if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
      if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
      return n.toString();
    };
    const formatDate = s => format(new Date(s), 'MMM d, yyyy');
  
    function selectEpisode(ep) {
      selectedEpisode = ep;
      showModal = true;
    }
  
    function changePage(page) {
      if (page === '...' || page < 1 || page > totalPages || page === currentPage) return;
      onPageChange(page);
    }

    function handleExport() {
  const headers = ['Episode', 'Title', 'Guest', 'Date', 'Views'];
  const rows = data.map(ep => [
    ep.episode,
    `"${ep.title.replace(/"/g, '""')}"`, // escape quotes
    ep.guest || 'N/A',
    formatDate(ep.date),
    ep.views
  ]);

  const csvContent = [headers, ...rows]
    .map(row => row.join(','))
    .join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', 'episodes.csv');
  link.click();
}
  </script>
  <div class="mb-4 flex justify-end">
    <button class="btn btn-accent" on:click={handleExport}>Export Data</button>
  </div>
  
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
          <th class="px-2 py-3 cursor-pointer" on:click={() => handleSort('episode')}># {sortField === 'episode' ? (sortDirection === 'desc' ? '↓' : '↑') : ''}</th>
          <th class="px-2 py-3">Img</th>
          <th class="px-3 py-3 cursor-pointer" on:click={() => handleSort('title')}>Title {sortField === 'title' ? (sortDirection === 'desc' ? '↓' : '↑') : ''}</th>
          <th class="px-3 py-3 cursor-pointer" on:click={() => handleSort('guest')}>Guest {sortField === 'guest' ? (sortDirection === 'desc' ? '↓' : '↑') : ''}</th>
          <th class="px-3 py-3 cursor-pointer" on:click={() => handleSort('date')}>Date {sortField === 'date' ? (sortDirection === 'desc' ? '↓' : '↑') : ''}</th>
          <th class="px-2 py-3 cursor-pointer" on:click={() => handleSort('views')}>Views {sortField === 'views' ? (sortDirection === 'desc' ? '↓' : '↑') : ''}</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-700 text-gray-100">
        {#if paginatedData.length === 0}
          <tr><td colspan="6" class="py-8 text-center">No episodes match your filters</td></tr>
        {:else}
          {#each paginatedData as ep}
            <tr class="hover:bg-gray-700 cursor-pointer" on:click={() => selectEpisode(ep)}>
              <td class="px-2 py-2 text-center">#{ep.episode}</td>
              <td class="px-2 py-2"><img src={ep.thumbnail} alt="" class="w-full h-full object-cover" /></td>
              <td class="px-3 py-2"><div class="line-clamp-2">{ep.title}</div></td>
              <td class="px-3 py-2 truncate">{ep.guest || 'N/A'}</td>
              <td class="px-3 py-2">{formatDate(ep.date)}</td>
              <td class="px-2 py-2 text-right">{formatNumber(ep.views)}</td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  
    <!-- Pagination controls -->
    <div class="mt-6 flex items-center justify-between">
      <div class="ml-1 text-sm text-gray-400">
        Showing {(currentPage - 1) * itemsPerPage + 1} to {Math.min(currentPage * itemsPerPage, data.length)} of {data.length} episodes
      </div>
      <div class="flex items-center space-x-2">
        <button
          class="btn btn-primary text-sm px-3 py-1 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={currentPage === 1}
          on:click={() => changePage(currentPage - 1)}>
          Previous
        </button>
  
        {#each pagesToShow as p}
          {#if p === '...'}
            <span class="text-gray-400 px-2">…</span>
          {:else}
            <button
              class="btn text-sm px-3 py-1"
              class:btn-accent={currentPage === p}
              class:btn-primary={currentPage !== p}
              on:click={() => changePage(p)}>
              {p}
            </button>
          {/if}
        {/each}
  
        <button
          class="btn btn-primary text-sm px-3 py-1 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={currentPage === totalPages}
          on:click={() => changePage(currentPage + 1)}>
          Next
        </button>
      </div>
    </div>
  </div>
  
  {#if showModal && selectedEpisode}
    <Modal bind:show={showModal} episode={selectedEpisode} {formatNumber} {formatDate} />
  {/if}
  
  <style>
    .line-clamp-2 {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  </style>
  