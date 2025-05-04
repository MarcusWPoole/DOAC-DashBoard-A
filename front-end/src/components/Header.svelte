<script>
  import { format } from 'date-fns';
  
  const today = format(new Date(), 'MMMM d, yyyy');
</script>

<header class="bg-[#1A1A1A] border-b border-[#2A2A2A] py-6">
  <div class="container mx-auto px-4">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
      <div>
        <h1 class="text-3xl font-bold text-white">
          <span class="gold-accent">Diary of a CEO</span> - Episode Analytics
        </h1>
        <p class="text-gray-400 mt-1">Interactive insights & guest strategy</p>
      </div>
      
      <div class="mt-4 md:mt-0">
        <div class="text-sm text-gray-400">
          <span>Last Updated: {today}</span>
        </div>
        <button class="btn btn-primary mt-2 text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh Data
        </button>
      </div>
    </div>
  </div>
</header>