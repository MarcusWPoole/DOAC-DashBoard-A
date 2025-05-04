// Generate sample episode data
const generateEpisodeData = () => {
  const episodes = [];
  const startDate = new Date(2023, 0, 1); // Start from January 1, 2023
  
  const guests = [
    'Elon Musk', 'Mark Cuban', 'Sara Blakely', 'Peter Thiel', 'Ray Dalio',
    'Gary Vaynerchuk', 'Brené Brown', 'Simon Sinek', 'Tim Ferriss', 'Arianna Huffington',
    'Naval Ravikant', 'Ryan Holiday', 'Robert Kiyosaki', 'Marie Forleo', 'Andy Frisella'
  ];
  
  const titles = [
    'Building Resilience in Challenging Times',
    'The Art of Self-Discipline and Focus',
    'From Zero to Billion: The Untold Story',
    'Leadership Principles That Transform Organizations',
    'The Future of Technology and Its Impact',
    'Mental Health and High Performance',
    'Scaling Your Business Without Burning Out',
    'Financial Freedom: Strategies That Work',
    'The Science of Habits and Behavior Change',
    'Inside the Mind of Successful Entrepreneurs'
  ];
  
  for (let i = 1; i <= 50; i++) {
    // Generate a date by adding days
    const date = new Date(startDate);
    date.setDate(date.getDate() + (i * 7)); // Weekly episodes
    
    // Randomly select a guest (or no guest for some episodes)
    const hasGuest = Math.random() > 0.2; // 80% chance of having a guest
    const guest = hasGuest ? guests[Math.floor(Math.random() * guests.length)] : null;
    
    // Generate view count (more recent episodes tend to have fewer views)
    const recencyFactor = 1 - ((new Date() - date) / (new Date() - startDate));
    const viewBase = 1000000 + Math.random() * 5000000; // Between 1M and 6M
    const views = Math.round(viewBase * (0.5 + Math.random() * 0.5) * (recencyFactor * 0.5 + 0.5));
    
    // Generate share count (correlated with views)
    const shareRate = 0.01 + Math.random() * 0.04; // Between 1% and 5%
    const shares = Math.round(views * shareRate);
    
    // Generate other metrics
    const avgViewDuration = Math.round(50 + Math.random() * 40); // Between 50% and 90%
    const subsGained = Math.round(views * (0.001 + Math.random() * 0.009)); // Between 0.1% and 1%
    const subsLost = Math.round(subsGained * (0.1 + Math.random() * 0.3)); // Between 10% and 40% of gained
    
    episodes.push({
      episode: i,
      title: titles[Math.floor(Math.random() * titles.length)],
      guest,
      date: date.toISOString().split('T')[0],
      views,
      shares,
      avgViewDuration,
      subsGained,
      subsLost
    });
  }
  
  // Sort by episode number (descending)
  return episodes.sort((a, b) => b.episode - a.episode);
};

// Generate guest recommendations data
const generateGuestRecommendations = () => {
  const guests = [
    {
      name: 'Sam Altman',
      title: 'CEO, OpenAI',
      trendScore: 86,
      pastEngagement: 92,
      matchScore: 9.2,
      justification: 'As the CEO of OpenAI, Sam represents the cutting edge of AI technology, which is highly relevant to your entrepreneurship-focused audience. His recent public appearances have generated significant engagement, and his insights on the future of AI in business would align perfectly with your podcast format.',
      topics: ['Artificial Intelligence', 'Startups', 'Innovation', 'Future of Work'],
      trendData: generateTrendData(86)
    },
    {
      name: 'Whitney Wolfe Herd',
      title: 'Founder & CEO, Bumble',
      trendScore: 78,
      pastEngagement: 85,
      matchScore: 8.7,
      justification: 'Whitney\'s journey building Bumble into a multi-billion dollar company resonates with your audience\'s interest in entrepreneurial journeys. Her focus on female empowerment and building mission-driven companies would create compelling content for your listeners.',
      topics: ['Female Leadership', 'Tech Industry', 'Company Culture', 'Work-Life Balance'],
      trendData: generateTrendData(78)
    },
    {
      name: 'Alex Hormozi',
      title: 'Founder, Acquisition.com',
      trendScore: 92,
      pastEngagement: 81,
      matchScore: 8.9,
      justification: 'Alex has been experiencing a significant surge in popularity due to his no-nonsense business advice and content. His expertise in scaling businesses and creating profitable systems would provide actionable value to your entrepreneurial audience.',
      topics: ['Business Growth', 'Sales Systems', 'Wealth Building', 'Entrepreneurship'],
      trendData: generateTrendData(92)
    },
    {
      name: 'Melinda French Gates',
      title: 'Co-Chair, Bill & Melinda Gates Foundation',
      trendScore: 72,
      pastEngagement: 88,
      matchScore: 8.3,
      justification: 'Melinda\'s philanthropic work and insights on global challenges would add a unique perspective to your podcast. Guests focused on impact and purpose-driven leadership have historically performed well with your audience.',
      topics: ['Philanthropy', 'Global Health', 'Women\'s Rights', 'Leadership'],
      trendData: generateTrendData(72)
    },
    {
      name: 'Andrew Huberman',
      title: 'Neuroscientist, Stanford University',
      trendScore: 89,
      pastEngagement: 90,
      matchScore: 9.1,
      justification: 'Andrew\'s ability to translate complex neuroscience into practical advice for performance, sleep, and mental health has made him incredibly popular. His scientific approach to optimal performance would resonate with your high-achieving audience.',
      topics: ['Neuroscience', 'Peak Performance', 'Mental Health', 'Habits'],
      trendData: generateTrendData(89)
    },
    {
      name: 'Rihanna',
      title: 'Entrepreneur & Artist, Fenty',
      trendScore: 95,
      pastEngagement: 79,
      matchScore: 8.5,
      justification: 'Beyond her music career, Rihanna\'s success building the Fenty empire makes her a compelling business figure. Her journey from artist to billionaire entrepreneur offers valuable insights on brand building and industry disruption.',
      topics: ['Entrepreneurship', 'Brand Building', 'Fashion Industry', 'Creative Leadership'],
      trendData: generateTrendData(95)
    }
  ];
  
  return guests;
};

// Generate trend data for guest recommendations
function generateTrendData(peakValue) {
  const data = [];
  const days = 90;
  
  // Generate random trend data with an overall upward trend
  for (let i = 0; i < days; i++) {
    const baseValue = 20 + (peakValue - 20) * (i / days);
    const randomFactor = 0.7 + Math.random() * 0.6; // Random between 0.7 and 1.3
    const value = Math.min(100, Math.round(baseValue * randomFactor));
    
    // Format date
    const date = new Date();
    date.setDate(date.getDate() - (days - i));
    const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    
    data.push({ date: dateStr, value });
  }
  
  return data;
}

export const episodeData = generateEpisodeData();
export const guestRecommendations = generateGuestRecommendations();