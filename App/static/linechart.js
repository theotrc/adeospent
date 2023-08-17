const chartline = document.getElementById('lineChart');


const depenses = {
  labels: linex,
  data: liney
};




const chartline2 = new Chart(chartline, {
  type: 'line',
  data: {
    labels: depenses.labels,
    datasets: [
      {
        label: 'Dépenses passées',
        data: depenses.data,
        pointBackgroundColor:color_line
      },
      
    ]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

