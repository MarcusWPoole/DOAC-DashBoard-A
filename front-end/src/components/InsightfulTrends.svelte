<script>
    import { onMount } from 'svelte';
    import SeasonalityChart from './insights/SeasonalityChart.svelte';
    import GuestBoxplot from './insights/AppearancesBoxPlot.svelte';
    import SubGainBarChart from './insights/SubGainBarChart.svelte';
    import ContentEfficiencyScatter from './insights/ContentEfficiencyScatter.svelte';
    import TopicPerformance from './insights/TopicPerformance.svelte'

  
    let seasonalityData = [];
    let guestBoxplotData = [];
    let correlationData = [];
    let contentEfficiencyData = [];
    let topicData = [];


    let activeRange = 'all'; // default
  
    async function fetchSeasonality(range) {
      const now = new Date();
      let dateFrom;
  
      if (range === '6m') {
        dateFrom = new Date(now.setMonth(now.getMonth() - 6));
      } else if (range === '12m') {
        dateFrom = new Date(now.setMonth(now.getMonth() - 12));
      } else {
        dateFrom = null; 
      }
  
      const url = new URL('http://localhost:8001/api/episodes');
      if (dateFrom) {
        url.searchParams.append('date_from', dateFrom.toISOString().slice(0, 10));
      }
  
      const res = await fetch(url);
      const json = await res.json();
  
      const grouped = json.episodes.reduce((acc, ep) => {
        const date = new Date(ep.date);
        const month = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        if (!acc[month]) acc[month] = { month, views: 0, subscribers: 0 };
        acc[month].views += ep.views;
        acc[month].subscribers += ep.subsGained;
        return acc;
      }, {});
      seasonalityData = Object.values(grouped).sort((a, b) => new Date(a.month) - new Date(b.month));
    }

async function fetchContentEfficiency(range) {
  const url = new URL('http://localhost:8001/api/episodes/content-efficiency');
  if (range !== 'all') {
    const months = range === '6m' ? 6 : 12;
    const fromDate = new Date();
    fromDate.setMonth(fromDate.getMonth() - months);
    url.searchParams.append('date_from', fromDate.toISOString().split('T')[0]);
  }
  const res = await fetch(url);
  contentEfficiencyData = await res.json();
}

async function fetchGuestBoxplotData(range) {
  const url = new URL('http://localhost:8001/api/episodes/guest-recurring');
  if (range !== 'all') {
    const months = range === '6m' ? 6 : 12;
    const fromDate = new Date();
    fromDate.setMonth(fromDate.getMonth() - months);
    url.searchParams.append('date_from', fromDate.toISOString().split('T')[0]);
  }
  const res = await fetch(url);
  guestBoxplotData = await res.json();
}

async function fetchCorrelationData(range) {
  const url = new URL('http://localhost:8001/api/episodes/correlation');
  if (range !== 'all') {
    const months = range === '6m' ? 6 : 12;
    const fromDate = new Date();
    fromDate.setMonth(fromDate.getMonth() - months);
    url.searchParams.append('date_from', fromDate.toISOString().split('T')[0]);
  }
  const res = await fetch(url);
  correlationData = await res.json();
}

async function fetchTopicData(range) {
   const url = new URL('http://localhost:8001/api/topics/performance');
   if (range !== 'all') {
     const months = range === '6m' ? 6 : 12;
     const fromDate = new Date();
     fromDate.setMonth(fromDate.getMonth() - months);
     url.searchParams.append('date_from', fromDate.toISOString().split('T')[0]);
   }
   const res = await fetch(url);
   topicData = await res.json();
}
  
onMount(() => {
  fetchSeasonality(activeRange);
  fetchContentEfficiency(activeRange);
  fetchGuestBoxplotData(activeRange);
  fetchCorrelationData(activeRange);
  fetchTopicData(activeRange);
});

$: btnClasses = (range) =>
    `btn text-sm ${
      activeRange === range ? 'bg-[#FFD700] text-black' : 'btn-primary'
    }`;


const setRange = (range) => {
    activeRange = range;
    fetchSeasonality(range);
    fetchContentEfficiency(range);
    fetchGuestBoxplotData(range);
    fetchCorrelationData(range);
    fetchTopicData(range);
};



    const keyFindings = [
      {
        title: 'Focus on loyalty.',
        description: 'While visibility is important, to improve net subscriber growth the focus should be on what converts into loyalty.'
      },
      {
        title: 'Returning Guests',
        description: 'Guests generate the highest subscriber-to-views ratio on their first or second appearance. Impact declines sharply with each additional return, indicating diminishing returns from repeat guests.'
      },
      {
        title: 'Changing Seasons.',
        description: 'Strong seasonal spikes in both views and new subscribers occur consistently around Q1 and Q3 each year. Engagement peaks in early spring and late summer, indicating optimal windows for high-impact content drops. As well as increased promotion efforts during those dips'
      },
      {
        title: 'Hidden Gems',
        description: "Episodes in the blue quadrant (High Attention, Low Exposure) are hidden gems, They deliver strong viewer engagement but haven't reached wide audiences. These should be prioritised for re-promotion or reposting to maximise ROI."
      }
    ];
  </script>

  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Insightful Trends</h2>
      <div class="flex space-x-2">
        <!-- 6-month button -->
        <button
          class={btnClasses('6m')}
          on:click={() => setRange('6m')}>
          Last 6 Months
        </button>
      
        <!-- 12-month button -->
        <button
          class={btnClasses('12m')}
          on:click={() => setRange('12m')}>
          Last 12 Months
        </button>
      
        <!-- All-time button -->
        <button
          class={btnClasses('all')}
          on:click={() => setRange('all')}>
          All Time
        </button>
      </div>
      
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="card lg:col-span-2">
        <h3 class="text-lg font-semibold mb-4">Seasonality Analysis</h3>
        <p class="text-sm text-gray-400 mb-4">Monthly view patterns show strong seasonal trends</p>
        <SeasonalityChart data={seasonalityData}/>
      </div>
      
      <div class="card">
        <h3 class="text-lg font-semibold mb-4">Key Findings</h3>
        <div class="space-y-4">
          {#each keyFindings as finding}
            <div class="pb-3 border-b border-[#2A2A2A] last:border-0 last:pb-0">
              <h4 class="text-sm font-semibold gold-accent">{finding.title}</h4>
              <p class="text-sm mt-1 text-gray-300">{finding.description}</p>
            </div>
          {/each}
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
      <div class="card">
        <h3 class="text-lg font-semibold mb-4">Engagement vs Churn Correlation</h3>
        <p class="text-sm text-gray-400 mb-4">Correlation between engagement metrics and subscriber churn</p>
        <div class="card mt-6">
            <h3 class="text-lg font-semibold mb-4">What Drives Subscriber Changes</h3>
            <p class="text-sm text-gray-400 mb-4">Strong correlation signals to subscriber gains/losses</p>
            <SubGainBarChart target="subscribersGained" correlationData={correlationData} range={activeRange} />
          </div>
          
          <div class="card mt-6">
            <h3 class="text-lg font-semibold mb-4">What Causes Subscriber Loss</h3>
            <p class="text-sm text-gray-400 mb-4">Negative drivers of subscriber churn</p>
            <SubGainBarChart target="subscribersLost" correlationData={correlationData} range={activeRange} />
          </div>
      </div>
      
      <div class="card">
        <div class="card mt-6">
        <h3 class="text-lg font-semibold mb-4">Returning Guests Analysis</h3>
        <p class="text-sm text-gray-400 mb-4">Correlation between number of appearances for a guest and views to subscribers ratio</p>
        <GuestBoxplot data={guestBoxplotData} range={activeRange} />
      </div>
      <div class="card mt-6">
        <h3 class="text-lg font-semibold mb-4">Topic Performance</h3>
        <p class="text-sm text-gray-400 mb-4">Visualisation of the performance of topics on views and engagement</p>
        <TopicPerformance topicData={topicData} range={activeRange}/>
      </div>
    </div>
    </div>

    <div class="card mt-6">
        <h3 class="text-lg font-semibold mb-4">Content Efficiency Quadrant</h3>
        <p class="text-sm text-gray-400 mb-4">Based on view count vs. average watch duration</p>
        <ContentEfficiencyScatter data={contentEfficiencyData} range={activeRange} />
      </div>
    
 
  </div>