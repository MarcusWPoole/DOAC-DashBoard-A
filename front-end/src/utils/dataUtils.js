export function aggregateDataByMonth(episodeData) {
  // Group episodes by month
  const monthlyData = episodeData.reduce((result, episode) => {
    const date = new Date(episode.date);
    const monthYear = `${date.toLocaleString('default', { month: 'short' })} ${date.getFullYear()}`;
    
    if (!result[monthYear]) {
      result[monthYear] = {
        month: monthYear,
        views: 0,
        shares: 0,
        likes: 0,
        comments: 0,
        subscribers: 0
      };
    }
    
    result[monthYear].views += episode.views;
    result[monthYear].shares += episode.shares;
    result[monthYear].subscribers += episode.subsGained - episode.subsLost;
    
    return result;
  }, {});
  
  // Convert to array and sort by date
  return Object.values(monthlyData).sort((a, b) => {
    const [monthA, yearA] = a.month.split(' ');
    const [monthB, yearB] = b.month.split(' ');
    
    const dateA = new Date(`${monthA} 1, ${yearA}`);
    const dateB = new Date(`${monthB} 1, ${yearB}`);
    
    return dateA - dateB;
  });
}

export function calculateGrowthRate(current, previous) {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
}

export function formatNumber(num) {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num;
}