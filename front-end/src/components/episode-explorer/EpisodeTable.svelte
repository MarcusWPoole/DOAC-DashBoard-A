<script>
    import { format } from 'date-fns';
    
    export let data = [];
    export let sortField = 'views';
    export let sortDirection = 'desc';
    export let onSort;
    
    function handleSort(field) {
      const newDirection = field === sortField && sortDirection === 'desc' ? 'asc' : 'desc';
      onSort(field, newDirection);
    }
    
    function formatNumber(num) {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
      }
      return num;
    }
    
    function formatDate(dateStr) {
      const date = new Date(dateStr);
      return format(date, 'MMM d, yyyy');
    }
  </script>
  
  <div class="overflow-x-auto">
    <table>
      <thead>
        <tr>
          <th>Episode</th>
          <th>Title</th>
          <th>Guest</th>
          <th>
            <button 
              class="flex items-center" 
              on:click={() => handleSort('date')}
            >
              Date
              {#if sortField === 'date'}
                <span class="ml-1">{sortDirection === 'desc' ? '↓' : '↑'}</span>
              {/if}
            </button>
          </th>
          <th>
            <button 
              class="flex items-center" 
              on:click={() => handleSort('views')}
            >
              Views
              {#if sortField === 'views'}
                <span class="ml-1">{sortDirection === 'desc' ? '↓' : '↑'}</span>
              {/if}
            </button>
          </th>
          <th>
            <button 
              class="flex items-center" 
              on:click={() => handleSort('shares')}
            >
              Shares
              {#if sortField === 'shares'}
                <span class="ml-1">{sortDirection === 'desc' ? '↓' : '↑'}</span>
              {/if}
            </button>
          </th>
          <th>
            <button 
              class="flex items-center" 
              on:click={() => handleSort('avgViewDuration')}
            >
              Watch %
              {#if sortField === 'avgViewDuration'}
                <span class="ml-1">{sortDirection === 'desc' ? '↓' : '↑'}</span>
              {/if}
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        {#if data.length === 0}
          <tr>
            <td colspan="7" class="text-center py-8">No episodes match your filters</td>
          </tr>
        {:else}
          {#each data as episode}
            <tr class="hover:bg-[#2A2A2A] transition-colors">
              <td>#{episode.episode}</td>
              <td class="max-w-xs truncate" title={episode.title}>
                {episode.title}
              </td>
              <td>{episode.guest || 'N/A'}</td>
              <td>{formatDate(episode.date)}</td>
              <td>{formatNumber(episode.views)}</td>
              <td>{formatNumber(episode.shares)}</td>
              <td>{episode.avgViewDuration}%</td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>