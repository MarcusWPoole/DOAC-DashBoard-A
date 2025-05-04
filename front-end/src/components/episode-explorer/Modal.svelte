<script>
    export let show = false;
    export let episode = null;
    export let formatNumber = n => n;
    export let formatDate = s => s;
  
    function closeModal() {
      show = false;
    }
  
    function handleBackdropClick(event) {
      if (event.target === event.currentTarget) {
        closeModal();
      }
    }
  
    function handleKeydown(event) {
      if (event.key === 'Escape') {
        closeModal();
      }
    }

      // Calculate like ratio
  $: likeRatio = episode ? Math.round((episode.likes / (episode.likes + episode.dislikes)) * 100) : 0;
  </script>

  <svelte:window on:keydown={handleKeydown}/>
  
  
  {#if show}
  <div 
  class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
  on:click={handleBackdropClick}
>
  <div class="bg-[#1A1A1A] rounded-xl shadow-2xl w-full max-w-2xl border border-[#2A2A2A] overflow-hidden">
    <!-- Header with Thumbnail -->
    <div class="p-6 border-b border-[#2A2A2A]">
      <div class="flex gap-6">
        <div class="w-32 h-32 bg-gradient-to-br from-[#2A2A2A] to-[#1A1A1A] rounded-lg flex items-center justify-center relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
          <img 
            src={episode.thumbnail} 
            alt={`Episode ${episode.episode} thumbnail`}
            class="w-full h-full object-cover"
            onerror="this.style.display='none';this.nextElementSibling.style.display='flex';"
          />
          <div class="hidden absolute inset-0 items-center justify-center">
            <span class="text-4xl">🎙️</span>
          </div>
        </div>
        
        <div class="flex-1">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-2xl font-bold">Episode #{episode.episode}</h3>
              <p class="text-gray-400 mt-1">{formatDate(episode.date)}</p>
            </div>
            <button 
              class="text-gray-400 hover:text-white transition-colors"
              on:click={closeModal}
            >
              ✕
            </button>
          </div>
        </div>
      </div>
    </div>
        
        <!-- Content -->
        <div class="p-6 space-y-6">
          <div>
            <h4 class="text-xl font-bold mb-2">{episode.title}</h4>
            {#if episode.guest}
              <p class="text-[#FFD700]">Guest: {episode.guest}</p>
            {/if}
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <!-- Performance -->
            <div class="bg-[#2A2A2A] rounded-lg p-4">
              <h5 class="text-sm font-semibold text-gray-400 mb-3">Performance</h5>
              <div class="space-y-3">
                <div>
                  <p class="text-sm text-gray-400">Views</p>
                  <p class="text-xl font-bold">{formatNumber(episode.views)}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-400">Shares</p>
                  <p class="text-xl font-bold">{formatNumber(episode.shares)}</p>
                </div>
              </div>
            </div>
            
            <!-- Engagement -->
            <div class="bg-[#2A2A2A] rounded-lg p-4">
              <h5 class="text-sm font-semibold text-gray-400 mb-3">Engagement</h5>
              <div class="space-y-3">
                <div>
                  <p class="text-sm text-gray-400">Watch %</p>
                  <p class="text-xl font-bold">{episode.avgViewDuration}%</p>
                </div>
                <div>
                  <p class="text-sm text-gray-400">Subs Gained</p>
                  <p class="text-xl font-bold text-green-500">+{formatNumber(episode.subsGained)}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-400">Subs Lost</p>
                  <p class="text-xl font-bold text-red-500">-{formatNumber(episode.subsLost)}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Likes & Dislikes Section -->
        <div class="mt-4 bg-[#2A2A2A] rounded-lg p-4">
            <h5 class="text-sm font-semibold text-gray-400 mb-3">Audience Reception</h5>
            
            <div class="flex items-center space-x-4">
              <div class="flex-1">
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-400">Like Ratio</span>
                  <span class="font-semibold">{likeRatio}%</span>
                </div>
                <div class="h-2 bg-[#1A1A1A] rounded-full overflow-hidden flex">
                  <div 
                    class="h-full bg-green-500" 
                    style="width: {likeRatio}%"
                  ></div>
                  <div 
                    class="h-full bg-red-500" 
                    style="width: {100 - likeRatio}%"
                  ></div>
                </div>
              </div>
              
              <div class="flex space-x-4 text-sm">
                <div class="text-center">
                  <div class="flex items-center space-x-1 text-green-500">
                    <span>👍</span>
                    <span class="font-bold">{formatNumber(episode.likes)}</span>
                  </div>
                  <p class="text-gray-400 text-xs mt-1">Likes</p>
                </div>
                
                <div class="text-center">
                  <div class="flex items-center space-x-1 text-red-500">
                    <span>👎</span>
                    <span class="font-bold">{formatNumber(episode.dislikes)}</span>
                  </div>
                  <p class="text-gray-400 text-xs mt-1">Dislikes</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Progress Bars -->
          <div class="space-y-4">
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-400">Watch %</span>
                <span class="font-semibold">{episode.avgViewDuration}%</span>
              </div>
              <div class="h-2 bg-[#2A2A2A] rounded-full overflow-hidden">
                <div class="h-full bg-[#FFD700]" style="width: {episode.avgViewDuration}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-400">Net Subscriber Growth</span>
                <span class="font-semibold">
                  {Math.round((1 - episode.subsLost/episode.subsGained) * 100)}%
                </span>
              </div>
              <div class="h-2 bg-[#2A2A2A] rounded-full overflow-hidden">
                <div 
                  class="h-full bg-green-500" 
                  style="width: {Math.round((1 - episode.subsLost/episode.subsGained) * 100)}%"
                ></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Footer -->
        <div class="p-6 border-t border-[#2A2A2A] bg-[#2A2A2A] flex justify-end space-x-3">
          <button class="btn btn-secondary" on:click={closeModal}>Close</button>
          <button class="btn btn-accent">Export Data</button>
        </div>
      </div>
    </div>
  {/if}
  