const ctx = document.getElementById('myChart');




function chartbar(axis,ordonne, predictions){
  new Chart(ctx, {
  type: 'bar',
  data: {
    labels: axis,
    datasets: [
      {
      label: 'spent',
      data: ordonne,
      borderWidth: 1
    },
    {
      label: 'predictions',
      data: predictions,
      borderWidth: 1
    }

  ]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      },
      y1:{
        beginAtZero: true
      }
    }
  }
})};

chartbar(x,y, predictions)


