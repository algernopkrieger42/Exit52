import fs from "fs";
function displayPrediction() {
    document.getElementById("button").style.display = 'none';
    document.getElementById("float-container").style.display = 'block';
}

function todaysPrediction() { 
    fs.readFile("./predictions.json", 'utf8', (error, data) => {
        if (error){
            console.log(error);
            return;
        }
        var date = JSON.parse(data).Todays_Date;
        var prediction = JSON.parse(data).Todays_Prediction;
        var inches = "in";
        var output = date +  " " + prediction + inches;
        console.log(output);
        return output;
    })
}

function tomorrowsPrediction() { 
    fs.readFile("./predictions.json", 'utf8', (error, data) => {
        if (error){
            console.log(error);
            return;
        }
        var date = JSON.parse(data).Tomorrows_Date;
        var prediction = JSON.parse(data).Tomorrows_Prediction;
        var inches = "in";
        var output = date +  " " + prediction + inches;
        console.log(output);
        return output;
    })
}

function displayPredictions(){
    todaysPrediction();
    tomorrowsPrediction();
}


