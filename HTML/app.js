function displayPrediction() {
    document.getElementById("button").style.display = 'none';
    document.getElementById("float-container").style.display = 'block';
}

function readJSON() {
    fetch('predictions.json')
    .then(response => response.json())
    var mydata = JSON.parse(response);
    var date = mydata[0].Todays_Date;
    var statment = date.concat(' ',mydata[0].Todays_Prediction);
}

