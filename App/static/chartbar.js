// const ctx = document.getElementById('myChart');




// function chartbar(axis,ordonne, axis_pred, ordonne_pred){
//   new Chart(ctx, {
//   type: 'bar',
//   data: {
//     labels: axis,
//     datasets: [
//       {
//       label: 'depense par mois',
//       data: ordonne,
//       borderWidth: 1
//     }
//   ]
//   },
//   data: {
//     labels: axis_pred,
//     datasets: [
//       {
//       label: 'depense par mois',
//       data: ordonne_pred,
//       borderWidth: 1
//     }
//   ]
//   },
//   options: {
//     scales: {
//       y: {
//         beginAtZero: true
//       }
//     }
//   }
// })};

// chartbar(x,y, x_pred, y_pred);


const depensesPasses = {
  labels: x_pred,
  data: y
};

const predictionsDepenses = {
  labels: x_pred,
  data: y_pred
};
// const depensesPasses = {
//   labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov"],
//   data: [1000, 1500, 1200, 1800, 2000, 1700, 1900, 2100, 2200, 2300, 2000, 1800]
// };

// const predictionsDepenses = {
//   labels: ["Mai", "dec"],
//   data: [2200, 2903]
// };

const ctx = document.getElementById('myChart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: depensesPasses.labels,
    datasets: [
      {
        label: 'Dépenses passées',
        data: depensesPasses.data,
        backgroundColor: 'rgba(54, 162, 235, 0.5)'
      },
      {
        label: 'Prédictions de dépenses',
        data: depensesPasses.labels.map((label) => {
          const predictionIndex = predictionsDepenses.labels.indexOf(label);
          return (predictionIndex !== -1) ? predictionsDepenses.data[predictionIndex] : null;
        }),
        backgroundColor: 'rgba(255, 99, 132, 0.5)'
      }
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
