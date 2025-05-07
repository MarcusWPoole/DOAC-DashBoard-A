<script>
    import { onMount } from 'svelte';
  
    let formData = {
      episode_name: '',
      episode_description: '',
      guest: '',
      release_date: new Date().toISOString().slice(0, 10)
    };
  
    let prediction = null;
    let loading = false;
    let error = null;
  
    // Reactive rounded value for average view percentage
    $: roundedAvg =
      prediction && typeof prediction.averageViewPercentage === 'number'
        ? Math.round(prediction.averageViewPercentage)
        : 0;
  
    // Checks for any empty required field
    $: fieldErrors = {
      episode_name:        !formData.episode_name.trim(),
      episode_description: !formData.episode_description.trim(),
      guest:               !formData.guest.trim(),
      release_date:        !formData.release_date
    };
  
    // Disables button if any field invalid
    $: isIncomplete = Object.values(fieldErrors).some(v => v);
  
    async function getPrediction() {
      loading = true;
      error = null;
      prediction = null;
  
      try {
        const resp = await fetch('http://localhost:8001/api/forecast', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            episode_name: formData.episode_name,
            episode_description: formData.episode_description,
            guest: formData.guest,
            release_date: formData.release_date
          })
        });
  
        if (!resp.ok) {
          const errBody = await resp.json().catch(() => ({}));
          throw new Error(errBody.detail || resp.statusText);
        }
  
        prediction = await resp.json();
      } catch (err) {
        console.error(err);
        error = 'Failed to get prediction: ' + err.message;
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
            <!-- Episode Name -->
            <div>
              <label class="block text-sm font-medium text-gray-400 mb-1">
                Episode Name
              </label>
              <input
                type="text"
                bind:value={formData.episode_name}
                class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]
                       border {fieldErrors.episode_name ? 'border-red-500' : 'border-transparent'}"
                placeholder="Enter episode name"
              />
              {#if fieldErrors.episode_name}
                <p class="text-red-500 text-xs mt-1">Episode name is required.</p>
              {/if}
            </div>
  
            <!-- Description -->
            <div>
              <label class="block text-sm font-medium text-gray-400 mb-1">
                Description
              </label>
              <textarea
                bind:value={formData.episode_description}
                class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm h-24 focus:outline-none focus:ring-1 focus:ring-[#FFD700]
                       border {fieldErrors.episode_description ? 'border-red-500' : 'border-transparent'}"
                placeholder="Enter episode description"
              ></textarea>
              {#if fieldErrors.episode_description}
                <p class="text-red-500 text-xs mt-1">Description is required.</p>
              {/if}
            </div>
  
            <!-- Guest -->
            <div>
              <label class="block text-sm font-medium text-gray-400 mb-1">
                Guest
              </label>
              <input
                type="text"
                bind:value={formData.guest}
                class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]
                       border {fieldErrors.guest ? 'border-red-500' : 'border-transparent'}"
                placeholder="Enter guest name"
              />
              {#if fieldErrors.guest}
                <p class="text-red-500 text-xs mt-1">Guest name is required.</p>
              {/if}
            </div>
  
            <!-- Release Date -->
            <div>
              <label class="block text-sm font-medium text-gray-400 mb-1">
                Release Date
              </label>
              <input
                type="date"
                bind:value={formData.release_date}
                class="w-full bg-[#2A2A2A] rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#FFD700]
                       border {fieldErrors.release_date ? 'border-red-500' : 'border-transparent'}"
              />
              {#if fieldErrors.release_date}
                <p class="text-red-500 text-xs mt-1">Release date is required.</p>
              {/if}
            </div>
          </div>
  
          <div class="mt-6">
            <button
              class="btn btn-accent w-full"
              on:click={getPrediction}
              disabled={loading || isIncomplete}
            >
              {#if loading}
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
  
              <!-- Engagement Metrics -->
              <div class="bg-[#2A2A2A] rounded-lg p-4">
                <h4 class="text-sm font-semibold mb-3">Engagement Metrics</h4>
                
                <!-- Like Ratio -->
                <div class="space-y-4">
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
                        {formatNumber(prediction.likes)}
                      </div>
                      <div class="text-red-500">
                        {formatNumber(prediction.dislikes)}
                      </div>
                    </div>
                  </div>
  
                  <!-- Average View Percentage -->
                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-gray-400">Average View Percentage</span>
                      <span class="font-semibold">{roundedAvg}%</span>
                    </div>
                    <div class="h-2 bg-[#1A1A1A] rounded-full overflow-hidden">
                      <div 
                        class="h-full bg-blue-500"
                        style="width: {roundedAvg}%"
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
  
  <style>
    /* Ensure the dynamic border classes work */
    .border-transparent { border-width: 1px; }
    .border-red-500  { border-width: 1px; }
  </style>
  