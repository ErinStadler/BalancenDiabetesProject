fetch('/entries')
.then((response) => response.json())
.then((responsejson) => {
    const data = responsejson.user_entries.map((entries) => ({
        x: entries.date,
        y: entries.bs,
    }));
    console.log(data)

new Chart(document.querySelector('#glucose_chart'), {
    type: 'line',
    data: {
        datasets: [
            {
                label: 'Blood Sugar Entries',
                data,
            },
        ],
    },
    options: {
        scales: {
          x: {
            type: 'time',
            time: {
              tooltipFormat: 'LLLL dd', 
              unit: 'day',
            },
          },
          y: {
                min: 40,
                max: 400,
              },
        },
      },
})
});