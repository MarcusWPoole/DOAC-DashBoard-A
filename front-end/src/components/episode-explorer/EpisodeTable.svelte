<script>
    import { format } from 'date-fns';
  
    export let data = [];
    export let sortField = 'views';
    export let sortDirection = 'desc';
    export let onSort = () => {};
  
    // Toggle sort or change field
    function handleSort(field) {
      const newDir = field === sortField && sortDirection === 'desc' ? 'asc' : 'desc';
      onSort(field, newDir);
    }
  
    // Format large numbers
    function formatNumber(num) {
      if (num >= 1_000_000) return (num/1_000_000).toFixed(1)+'M';
      if (num >=   1_000) return (num/1_000).toFixed(1)+'K';
      return num.toString();
    }
  
    // Format date strings
    function formatDate(dateStr) {
      return format(new Date(dateStr), 'MMM d, yyyy');
    }
  </script>
  
  <div class="overflow-x-auto">
    <table class="min-w-full text-left">
      <thead class="bg-gray-800 text-gray-200">
        <tr>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('episode')}>
            #
            {#if sortField==='episode'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
          <th class="px-4 py-2">Title</th>
          <th class="px-4 py-2">Guest</th>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('date')}>
            Date
            {#if sortField==='date'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('views')}>
            Views
            {#if sortField==='views'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('shares')}>
            Shares
            {#if sortField==='shares'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('likes')}>
            Likes
            {#if sortField==='likes'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('dislikes')}>
            Dislikes
            {#if sortField==='dislikes'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('avgViewDuration')}>
            Watch %
            {#if sortField==='avgViewDuration'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('subsGained')}>
            Subs Gained
            {#if sortField==='subsGained'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
          <th class="px-4 py-2 cursor-pointer" on:click={() => handleSort('subsLost')}>
            Subs Lost
            {#if sortField==='subsLost'}<span>{sortDirection==='desc'?' ↓':' ↑'}</span>{/if}
          </th>
        </tr>
      </thead>
      <tbody class="text-gray-100">
        {#if data.length === 0}
          <tr>
            <td colspan="11" class="py-8 text-center">No episodes match your filters</td>
          </tr>
        {:else}
          {#each data as ep}
            <tr class="hover:bg-gray-700 transition-colors">
              <td class="px-4 py-2">#{ep.episode}</td>
              <td class="px-4 py-2 max-w-xs truncate" title={ep.title}>{ep.title}</td>
              <td class="px-4 py-2">{ep.guest || 'N/A'}</td>
              <td class="px-4 py-2">{formatDate(ep.date)}</td>
              <td class="px-4 py-2">{formatNumber(ep.views)}</td>
              <td class="px-4 py-2">{formatNumber(ep.shares)}</td>
              <td class="px-4 py-2">{formatNumber(ep.likes)}</td>
              <td class="px-4 py-2">{formatNumber(ep.dislikes)}</td>
              <td class="px-4 py-2">{ep.avgViewDuration}%</td>
              <td class="px-4 py-2">{formatNumber(ep.subsGained)}</td>
              <td class="px-4 py-2">{formatNumber(ep.subsLost)}</td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
  