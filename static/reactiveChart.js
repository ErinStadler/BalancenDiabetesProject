fetch('/entries')
.then((response) => response.json())
.then((responsejson) => {
    const data = responsejson.all_bs_dates.map((entries) => ({
        x: entries.date,
        y: entries.bs,
    }));
    const data1 = responsejson.one_bs_date.map((entries) => ({
      x: entries.date,
      y: entries.bs,
    }));
    const data2 = responsejson.two_bs_dates.map((entries) => ({
      x: entries.date,
      y: entries.bs,
    }));
    const data7 = responsejson.seven_bs_dates.map((entries) => ({
      x: entries.date,
      y: entries.bs,
    }));
    const data14 = responsejson.fourteen_bs_dates.map((entries) => ({
      x: entries.date,
      y: entries.bs,
    }));
    const data30 = responsejson.thirty_bs_dates.map((entries) => ({
      x: entries.date,
      y: entries.bs,
    }));
    const data60 = responsejson.sixty_bs_dates.map((entries) => ({
      x: entries.date,
      y: entries.bs,
    }));
    const data90 = responsejson.ninety_bs_dates.map((entries) => ({
      x: entries.date,
      y: entries.bs,
    }));

new Chart(document.querySelector('#glucose_chart'), {
    type: 'line',
    data: {
        datasets: [
            {
                label: 'All Blood Sugar Entries',
                data: data,
            },
            {
              label: 'Last Day Blood Sugar Entries',
              data: data1,
            },
            {
              label: 'Last Two Days Blood Sugar Entries',
              data: data2,
            },
            {
              label: 'Last Seven Days Blood Sugar Entries',
              data: data7,
            },
            {
              label: 'Last Fourteen Days Blood Sugar Entries',
              data: data14,
            },
            {
              label: 'Last Thirty Days Blood Sugar Entries',
              data: data30,
            },
            {
              label: 'Last Sixty Days Blood Sugar Entries',
              data: data60,
            },
            {
              label: 'Last Ninety Days Blood Sugar Entries',
              data: data90,
            },
        ],
    },
    options: {
        responsive: true,
        plugins: {
          Legend: {
            position: 'top',
          },
          Title: {
            Display: true,
            text: 'Current Entries'
          }
        },
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