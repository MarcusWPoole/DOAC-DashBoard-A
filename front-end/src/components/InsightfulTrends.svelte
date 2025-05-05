<script>
    import { onMount } from 'svelte';
    import SeasonalityChart from './insights/SeasonalityChart.svelte';
    import GuestBoxplot from './insights/AppearancesBoxPlot.svelte';
    import SubGainBarChart from './insights/SubGainBarChart.svelte';
    import ContentEfficiencyScatter from './insights/ContentEfficiencyScatter.svelte';

  
    let seasonalityData = [];
    let guestBoxplotData = [];
    let correlationData = [];
    let contentEfficiencyData = [];


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
  
onMount(() => {
  fetchSeasonality(activeRange);
  fetchContentEfficiency(activeRange);
  fetchGuestBoxplotData(activeRange);
  fetchCorrelationData(activeRange);
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
};



    const keyFindings = [
      {
        title: 'Lorem ipsum dolor sit.',
        description: '  Lorem, ipsum dolor sit amet consectetur adipisicing elit. Vel at ipsam ullam est nihil quia quo voluptatem! Quibusdam aut perspiciatis corporis, ex eum voluptas ullam iure aspernatur, recusandae deserunt quam.'
      },
      {
        title: 'Lorem ipsum dolor sit.',
        description: '  Lorem, ipsum dolor sit amet consectetur adipisicing elit. Vel at ipsam ullam est nihil quia quo voluptatem! Quibusdam aut perspiciatis corporis, ex eum voluptas ullam iure aspernatur, recusandae deserunt quam.'
      },
      {
        title: 'Lorem ipsum dolor sit.',
        description: '  Lorem, ipsum dolor sit amet consectetur adipisicing elit. Vel at ipsam ullam est nihil quia quo voluptatem! Quibusdam aut perspiciatis corporis, ex eum voluptas ullam iure aspernatur, recusandae deserunt quam.'
      },
      {
        title: 'Lorem ipsum dolor sit.',
        description: '  Lorem, ipsum dolor sit amet consectetur adipisicing elit. Vel at ipsam ullam est nihil quia quo voluptatem! Quibusdam aut perspiciatis corporis, ex eum voluptas ullam iure aspernatur, recusandae deserunt quam.'
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
    </div>
    </div>

    <div class="card mt-6">
        <h3 class="text-lg font-semibold mb-4">Content Efficiency Quadrant</h3>
        <p class="text-sm text-gray-400 mb-4">Based on view count vs. average watch duration</p>
        <ContentEfficiencyScatter data={contentEfficiencyData} range={activeRange} />
      </div>
    
    <div class="card mt-6">
      <h3 class="text-lg font-semibold mb-4">Executive Summary</h3>
      
      <div class="prose prose-sm text-gray-300 max-w-none">
        <p>
          Analysis of The Diary of a CEO podcast over the past 12 months reveals several actionable insights:
        </p>
        
        <ol class="list-decimal pl-5 space-y-2 mt-3">
          <li>
            <strong class="text-white">Lorem ipsum dolor sit amet consectetur adipisicing elit. Facere, autem!</strong> 
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Repudiandae maxime iste velit quaerat natus dolor alias fuga! Fugiat cumque, quod dicta, consectetur nisi nobis sequi natus quidem eum culpa cum.
          </li>
          
          <li>
            <strong class="text-white">Lorem ipsum dolor sit amet consectetur adipisicing elit. Facere, autem!</strong> 
           Lorem ipsum dolor sit amet consectetur, adipisicing elit. Maiores, accusantium debitis porro amet, aperiam quo fugit aliquam, at neque esse excepturi minus accusamus dignissimos delectus voluptate reiciendis nesciunt sequi! Perferendis!
          </li>
          
          <li>
            <strong class="text-white">Lorem ipsum dolor sit amet.</strong> 
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ut adipisci consequatur consequuntur dolorem necessitatibus soluta esse possimus doloremque, veritatis repellendus ratione corrupti quas autem impedit magnam, recusandae tempora beatae veniam.
          </li>
          
          <li>
            <strong class="text-white">Lorem ipsum dolor sit amet.</strong> 
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt aspernatur ea porro inventore eum et, quam atque minima, necessitatibus laborum sint explicabo totam provident eos. Enim architecto quisquam ad! Deserunt?.
          </li>
        </ol>
      </div>
    </div>
  </div>