//import fs from 'fs';
//import fs from 'fs';

var date;
var prediction;
var inches;
var output;
var data;

export async function displayPrediction() {
    document.getElementById("loadingWindow").style.display = 'none';
    document.getElementById("float-container").style.display = 'flex';
    document.getElementById("infoButton").style.display = 'flex'

}

export async function displayInfo(){
    document.getElementById("infoButton").style.display = 'none';
    document.getElementById("infoAsButton").style.display = 'flex';
}

export async function hideInfo(){
    document.getElementById("infoAsButton").style.display = 'none';
    document.getElementById("infoButton").style.display = 'flex';
}

function todaysPrediction(json) { 
    var date = json.Todays_Date;
    var prediction = json.Todays_Prediction;
    var inches = " inches";
    var output = date +  "\n" + prediction + inches;
    console.log(output);
    document.getElementById("box1").innerHTML = output;
    return output;
}

function tomorrowsPrediction(json) { 
    var date = json.Tomorrows_Date;
    var prediction = json.Tomorrows_Prediction;
    var inches = " inches";
    var output = date +  "\n" + prediction + inches;
    document.getElementById("box2").innerHTML = output;
    return output;
}

async function fetchAPI() {
    try {
        const response = await fetch('https://enabled-needed-kitten.ngrok-free.app/predictions.json', {
            headers: {
                'bypass-tunnel-reminder': 'bypass', // Include if required by your Express server
            },
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const text = await response.text();//show text
        console.log("Raw response:", text);
        const data = await response.json(); // Parse the JSON data
        return data; // Return the parsed data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        throw error; // Rethrow the error to handle it outside the function
    }
}

function setInfo() {
    
    var info = "This site was built as a way to share independently formulated snowfall predictions for Snoqualmie Pass";
    var info2 = " in an effort to improve upon predictions provided by traditional sources";
    var fullInfo = info + info2;
    document.getElementById("infoAsButton").innerHTML = fullInfo;
}

try {
    document.getElementById("errorWindow").style.display = 'none';
    data = await fetchAPI(); // Wait for the fetchAPI promise to resolve and save the data to a variable

    todaysPrediction(data);
    tomorrowsPrediction(data);
    setInfo()
    displayPrediction()
} catch (error) {
    console.error('Error:', error);
    document.getElementById("errorWindow").style.display = 'block';
}



