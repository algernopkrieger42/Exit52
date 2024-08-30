//import fs from 'fs';
//import fs from 'fs';

var date;
var prediction;
var inches;
var output;
var data;

export async function displayPrediction() {
    document.getElementById("button").style.display = 'none';
    document.getElementById("float-container").style.display = 'block';
}

export function todaysPrediction(json) { 
    var date = json.Todays_Date;
    var prediction = json.Todays_Prediction;
    var inches = " inches";
    var output = date +  " " + prediction + inches;
    console.log(output);
    document.getElementById("box1").innerHTML = output;
    return output;
}

function tomorrowsPrediction(json) { 
    var date = json.Tomorrows_Date;
    var prediction = json.Tomorrows_Prediction;
    var inches = " inches";
    var output = date +  " " + prediction + inches;
    document.getElementById("box2").innerHTML = output;
    return output;
}

async function fetchAPI() {
    try {
        const response = await fetch('https://plenty-deer-rush.loca.lt/predictions.json');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json(); // Parse the JSON data
        return data; // Return the parsed data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        throw error; // Rethrow the error to handle it outside the function
    }
}

try {
    data = await fetchAPI(); // Wait for the fetchAPI promise to resolve and save the data to a variable

    todaysPrediction(data); // Example function call
    tomorrowsPrediction(data);
} catch (error) {
    console.error('Error:', error);
}


