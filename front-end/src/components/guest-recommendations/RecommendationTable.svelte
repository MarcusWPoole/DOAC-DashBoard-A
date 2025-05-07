<script>
    export let recommendations = [];
    export let selectedGuest;
    export let selectGuest;
  </script>
  
  <div class="overflow-x-auto">
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Trend Score</th>
          <th>Past Engagement</th>
          <th>Match Score</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {#each recommendations as guest}
          <tr 
            class="hover:bg-[#2A2A2A] transition-colors cursor-pointer {guest.name === selectedGuest.name ? 'bg-[#2A2A2A]' : ''}"
            on:click={() => selectGuest(guest)}
          >
            <td>
              <div>
                <div class="font-medium">{guest.name}</div>
                <div class="text-xs text-gray-400">{guest.title}</div>
              </div>
            </td>
            <td>
              <div class="flex items-center">
                <span class="bg-[#2A2A2A] rounded-md px-2 py-1 text-xs font-medium mr-1">
                  {guest.trendScore}
                </span>
                
                <div class="w-16 bg-[#2A2A2A] h-1 rounded-full overflow-hidden">
                  <div 
                    class="bg-[#FFD700] h-full" 
                    style="width: {guest.trendScore}%">
                  </div>
                </div>
              </div>
            </td>
            <td>
              <div class="flex items-center">
                <span class="bg-[#2A2A2A] rounded-md px-2 py-1 text-xs font-medium mr-1">
                  {guest.pastEngagement}%
                </span>
                
                <div class="w-16 bg-[#2A2A2A] h-1 rounded-full overflow-hidden">
                  <div 
                    class="bg-[#3B82F6] h-full" 
                    style="width: {guest.pastEngagement}%">
                  </div>
                </div>
              </div>
            </td>
            <td>
              <span class="bg-[#1E3A8A] text-[#3B82F6] rounded-md px-2 py-1 text-xs font-medium">
                {guest.matchScore.toFixed(1)}
              </span>
            </td>
            <td>
              {#if guest.name === selectedGuest.name}
                <span class="gold-accent">•</span>
              {:else}
                <button class="text-xs text-blue-400 hover:underline">
                  View
                </button>
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>