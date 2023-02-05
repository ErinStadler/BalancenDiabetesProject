document.querySelector("#oneDays").addEventListener("click", (evt) => {
    evt.preventDefaults;
  
    fetch("/dataOneButton")
    .then((response) => response.json())
    .then((jsonEntries) => {
      document.querySelector("#average").innerHTML = jsonEntries.average;
      })
    });
  
document.querySelector("#twoDays").addEventListener("click", (evt) => {
    evt.preventDefaults;
  
    fetch("/dataTwoButton")
    .then((response) => response.json())
    .then((jsonEntries) => {
      document.querySelector("#average").innerHTML = jsonEntries.average;
    })
  });
  
document.getElementById("sevenDays").addEventListener("click", (evt) => {
    evt.preventDefaults;
  
    fetch("/dataSevenButton")
    .then((response) => response.json())
    .then((jsonEntries) => {
      document.querySelector("#average").innerHTML = jsonEntries.average;
    })
  });
  
document.getElementById("fourteenDays").addEventListener("click", (evt) => {
    evt.preventDefaults;
  
    fetch("/dataFourteenButton")
    .then((response) => response.json())
    .then((jsonEntries) => {
      document.querySelector("#average").innerHTML = jsonEntries.average;
    })
  });
  
document.getElementById("thirtyDays").addEventListener("click", (evt) => {
    evt.preventDefaults;
  
    fetch("/dataThirtyButton")
    .then((response) => response.json())
    .then((jsonEntries) => {
        document.querySelector("#average").innerHTML = jsonEntries.average;
    })
  });
  
document.getElementById("sixtyDays").addEventListener("click", (evt) => {
    evt.preventDefaults;
  
    fetch("/dataSixtyButton")
    .then((response) => response.json())
    .then((jsonEntries) => {
        document.querySelector("#average").innerHTML = jsonEntries.average;
    })
  });
  
document.getElementById("ninetyDays").addEventListener("click", (evt) => {
    evt.preventDefaults;
  
    fetch("/dataNinetyButton")
    .then((response) => response.json())
    .then((jsonEntries) => {
        document.querySelector("#average").innerHTML = jsonEntries.average;
    })
  });