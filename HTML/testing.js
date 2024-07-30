function fetchJSONData() {
    fetch('./predictions.json')
    .then((response) => JSON.parse())
    .then((json) => console.log(json[0]));
}
fetchJSONData()
