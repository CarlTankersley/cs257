/* Soren DeHaan and Carl Tankersley
 * 15 November 2021
 * CS 257 - Software Design
 */

window.onload = initialize;

function initialize() {
    let element = document.getElementById('random_speaker_button');
    if (element) {
        element.onclick = onRandomSpeakerButton;
    }
}

function getAPIBaseURL() {
    let baseURL = window.location.protocol
        + '//' + window.location.hostname
        + ':' + window.location.port
        + '/api';
    return baseURL;
}

function onRandomSpeakerButton() {
    let url = getAPIBaseURL() + '/random/';

    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (speaker) {
            let str = '';
            str += '<h2>' + speaker['name']
                + ': ' + speaker['title']
                + '</h2>';
            let newHTML = document.getElementById('random_speaker');
            if (newHTML) {
                newHTML.innerHTML = str;
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}