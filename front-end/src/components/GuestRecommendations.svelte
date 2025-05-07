<script>
    import RecommendationTable from './guest-recommendations/RecommendationTable.svelte';
    import TrendChart from './guest-recommendations/TrendChart.svelte';
    import { guestRecommendations } from '../data/dummyData.js'
    
    let selectedGuest = guestRecommendations[0];
    
    function selectGuest(guest) {
      selectedGuest = guest;
    }
  </script>
  
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Guest Recommendations</h2>
      
      <div>
        <button class="btn btn-primary text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh Suggestions
        </button>
      </div>
    </div>
    
    <div class="card mb-6">
      <h3 class="text-lg font-semibold mb-2">How Our Recommendations Work</h3>
      <p class="text-sm text-gray-300">
        Our AI-powered recommendation engine analyzes multiple data sources to identify potential high-impact guests for your podcast:
      </p>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        <div class="bg-[#2A2A2A] p-4 rounded-md">
          <h4 class="text-sm font-semibold gold-accent mb-2">Trend Analysis</h4>
          <p class="text-xs text-gray-300">
            We analyze Google Trends data for the past 90 days to identify individuals gaining popularity in relevant topics.
          </p>
        </div>
        
        <div class="bg-[#2A2A2A] p-4 rounded-md">
          <h4 class="text-sm font-semibold gold-accent mb-2">Historical Engagement</h4>
          <p class="text-xs text-gray-300">
            We evaluate similar guest profiles from your past episodes to predict potential audience engagement.
          </p>
        </div>
        
        <div class="bg-[#2A2A2A] p-4 rounded-md">
          <h4 class="text-sm font-semibold gold-accent mb-2">Audience Alignment</h4>
          <p class="text-xs text-gray-300">
            We match potential guests with your audience demographics and interests to ensure relevance.
          </p>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <div class="lg:col-span-7">
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Recommended Guests</h3>
          <RecommendationTable 
            recommendations={guestRecommendations} 
            selectedGuest={selectedGuest}
            {selectGuest}
          />
        </div>
      </div>
      
      <div class="lg:col-span-5">
        <div class="card h-full">
          <h3 class="text-lg font-semibold">{selectedGuest.name}</h3>
          <p class="text-sm text-gray-400">{selectedGuest.title}</p>
          
          <div class="mt-4">
            <TrendChart guest={selectedGuest} />
          </div>
          
          <h4 class="text-sm font-semibold mt-6 mb-2">Why This Guest?</h4>
          <p class="text-sm text-gray-300">{selectedGuest.justification}</p>
          
          <div class="mt-6 pt-4 border-t border-[#2A2A2A]">
            <h4 class="text-sm font-semibold mb-2">Potential Topics</h4>
            <div class="flex flex-wrap gap-2">
              {#each selectedGuest.topics as topic}
                <span class="bg-[#2A2A2A] text-xs px-3 py-1 rounded-full">{topic}</span>
              {/each}
            </div>
          </div>
          
          <div class="mt-6 pt-4 border-t border-[#2A2A2A] flex">
            <button class="btn btn-primary text-sm flex-1 mr-2">Save for Later</button>
            <button class="btn btn-accent text-sm flex-1">Contact</button>
          </div>
        </div>
      </div>
    </div>
  </div>