const chartline = document.getElementById('lineChart');




function chartbar(axis,ordonne, plafond){
  new Chart(chartline, {
  type: 'line',
  data: {
    labels: axis,
    datasets: [
      {
      label: 'depense du budget',
      data: ordonne,
      borderWidth: 1
    },
    {
        label: "budget de l'annee",
        data:plafond ,
        borderWidth: 1
      },
  ]
  },
  options: {
    scales: {
      y: {
        beginAtZero: false
      },
      y1: {
        beginAtZero: false
      },
    }
  }
})};

chartbar(linex, liney, plafond)