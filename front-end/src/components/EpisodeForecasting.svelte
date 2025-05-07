<script>
    import { onMount } from 'svelte';
    
    let formData = {
      episode_name: '',
      episode_description: '',
      guest: '',
      year: new Date().getFullYear(),
      month: new Date().getMonth() + 1,
      day_of_week: 1,
      days_since_first: 0
    };
  
    let prediction = null;
    let loading = false;
    let error = null;
  
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
  
    const days = [
      'Monday', 'Tuesday', 'Wednesday', 'Thursday',
      'Friday', 'Saturday', 'Sunday'
    ];
  
    async function getPrediction() {
      loading = true;
      error = null;
      
      try {
        // Placeholder for API call - will be implemented later
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Placeholder prediction data
        prediction = {
          views: 2500000,
          subscribersLost: 150,
          subscribersGained: 5000,
          likes: 125000,
          dislikes: 2500,
          averageViewPercentage: 72
        };
      } catch (err) {
        error = 'Failed to get prediction';
        console.error(err);
      } finally {
        loading = false;
      }
    }
  
    function formatNumber(num) {
      return new Intl.NumberFormat('en-US', {
        notation: 'compact',
        maximumFractionDigits: 1
      }).format(num);
    }
  </script>
  
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Episode Forecasting</h2>
    </div>
  
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Input Form -->
      <div class="lg:col-span-5">
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Episode Details</h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-400 mb-1">
                Episode Name
              </label>
              <input
                type="text"
                bind:value={formData.episode_name}
                class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]"
                placeholder="Enter episode name"
              />
            </div>
  
            <div>
              <label class="block text-sm font-medium text-gray-400 mb-1">
                Description
              </label>
              <textarea
                bind:value={formData.episode_description}
                class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm h-24 focus:outline-none focus:ring-1 focus:ring-[#FFD700]"
                placeholder="Enter episode description"
              ></textarea>
            </div>
  
            <div>
              <label class="block text-sm font-medium text-gray-400 mb-1">
                Guest
              </label>
              <input
                type="text"
                bind:value={formData.guest}
                class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]"
                placeholder="Enter guest name"
              />
            </div>
  
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-400 mb-1">
                  Year
                </label>
                <input
                  type="number"
                  bind:value={formData.year}
                  min="2020"
                  max="2030"
                  class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]"
                />
              </div>
  
              <div>
                <label class="block text-sm font-medium text-gray-400 mb-1">
                  Month
                </label>
                <select
                  bind:value={formData.month}
                  class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]"
                >
                  {#each months as month, i}
                    <option value={i + 1}>{month}</option>
                  {/each}
                </select>
              </div>
            </div>
  
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-400 mb-1">
                  Day of Week
                </label>
                <select
                  bind:value={formData.day_of_week}
                  class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]"
                >
                  {#each days as day, i}
                    <option value={i + 1}>{day}</option>
                  {/each}
                </select>
              </div>
  
              <div>
                <label class="block text-sm font-medium text-gray-400 mb-1">
                  Days Since First Episode
                </label>
                <input
                  type="number"
                  bind:value={formData.days_since_first}
                  min="0"
                  class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]"
                />
              </div>
            </div>
          </div>
  
          <div class="mt-6">
            <button
              class="btn btn-accent w-full"
              on:click={getPrediction}
              disabled={loading}
            >
              {#if loading}
                <span class="inline-block animate-spin mr-2">🔄</span>
                Generating Prediction...
              {:else}
                Generate Prediction
              {/if}
            </button>
          </div>
        </div>
      </div>
  
      <!-- Prediction Results -->
      <div class="lg:col-span-7">
        <div class="card h-full">
          <h3 class="text-lg font-semibold mb-6">Predicted Performance</h3>
  
          {#if error}
            <div class="bg-red-900/20 border border-red-500 rounded-lg p-4 text-red-400">
              {error}
            </div>
          {:else if !prediction}
            <div class="h-full flex items-center justify-center text-gray-400">
              Enter episode details and click "Generate Prediction" to see forecasted performance metrics
            </div>
          {:else}
            <div class="space-y-6">
              <!-- Views -->
              <div>
                <div class="flex justify-between mb-2">
                  <span class="text-sm font-medium text-gray-400">Predicted Views</span>
                  <span class="text-sm font-bold gold-accent">{formatNumber(prediction.views)}</span>
                </div>
                <div class="h-2 bg-[#2A2A2A] rounded-full overflow-hidden">
                  <div
                    class="h-full bg-[#FFD700]"
                    style="width: {(prediction.views / 5000000) * 100}%"
                  ></div>
                </div>
              </div>
  
              <!-- Subscriber Impact -->
              <div class="bg-[#2A2A2A] rounded-lg p-4">
                <h4 class="text-sm font-semibold mb-3">Subscriber Impact</h4>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-sm text-gray-400">Gained</p>
                    <p class="text-2xl font-bold text-green-500">
                      +{formatNumber(prediction.subscribersGained)}
                    </p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-400">Lost</p>
                    <p class="text-2xl font-bold text-red-500">
                      -{formatNumber(prediction.subscribersLost)}
                    </p>
                  </div>
                </div>
              </div>
  
              <!-- Engagement -->
              <div class="bg-[#2A2A2A] rounded-lg p-4">
                <h4 class="text-sm font-semibold mb-3">Engagement Metrics</h4>
                
                <div class="space-y-4">
                  <!-- Likes/Dislikes -->
                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-gray-400">Like Ratio</span>
                      <span class="font-semibold">
                        {Math.round((prediction.likes / (prediction.likes + prediction.dislikes)) * 100)}%
                      </span>
                    </div>
                    <div class="h-2 bg-[#1A1A1A] rounded-full overflow-hidden flex">
                      <div 
                        class="h-full bg-green-500"
                        style="width: {(prediction.likes / (prediction.likes + prediction.dislikes)) * 100}%"
                      ></div>
                      <div 
                        class="h-full bg-red-500"
                        style="width: {(prediction.dislikes / (prediction.likes + prediction.dislikes)) * 100}%"
                      ></div>
                    </div>
                    <div class="flex justify-between mt-2 text-sm">
                      <div class="text-green-500">
                        👍 {formatNumber(prediction.likes)}
                      </div>
                      <div class="text-red-500">
                        👎 {formatNumber(prediction.dislikes)}
                      </div>
                    </div>
                  </div>
  
                  <!-- Average View Duration -->
                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-gray-400">Average View Duration</span>
                      <span class="font-semibold">{prediction.averageViewPercentage}%</span>
                    </div>
                    <div class="h-2 bg-[#1A1A1A] rounded-full overflow-hidden">
                      <div 
                        class="h-full bg-blue-500"
                        style="width: {prediction.averageViewPercentage}%"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>