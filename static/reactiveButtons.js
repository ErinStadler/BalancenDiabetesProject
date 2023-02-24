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
  
let calories = 0
let carbs = 0

  document.getElementById("add_food_to_calc").addEventListener("submit", (evt) => {
    evt.preventDefault();

    const foodToAdd = document.querySelector('#foodToAdd').value;

    fetch('/add_food', {
      method: 'POST',
      body: JSON.stringify({foodToAdd: foodToAdd}),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.json())
    .then((result) => {
      calories += result.calories
      carbs += result.carbs
      document.querySelector('#foodsAdded').insertAdjacentHTML('beforeend', `<li>${result.name, result.serving, result.calories, result.carbs}</li>`);
    });
  });

  document.querySelector("#calculate").addEventListener("click", (evt) => {
    evt.preventDefault();

    const ul = document.querySelector("ul");

    while (ul.firstChild) {
      ul.firstChild.remove();
    }

    document.querySelector("#totals").innerHTML = `Total Calories: ${calories}, Total Carbs: ${carbs}`
  })