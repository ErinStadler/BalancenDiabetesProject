  document.getElementById("days_back_form").addEventListener("submit", (evt) => {
    evt.preventDefault();

    const daysBack = document.querySelector('#days_back').value;

    fetch('/blood_sugars_days_back', {
      method: 'POST',
      body: JSON.stringify({daysBack: daysBack}),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.json())
    .then((result) => {
      document.querySelector("#average").innerHTML = `Blood Sugar Average: ${result.average}`;
    });
  });