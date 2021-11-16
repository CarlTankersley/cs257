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

function search_speaker() {
    let input = document.getElementById('speaker_search').value;
    let url = getAPIBaseURL() + '/speakers/';
    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(speakers) {
        let newHTML = '';
        for(let i = 0; i < speakers.length; i++){
            let speaker = speakers[i];
            newHTML += '<div class="video">'
                     + '<div class="imageWrapper">'
                     + '<a href="video.html"><img'
                     + 'src="' + speaker["image"] + '"'
                     + 'class="" title="" alt="video"></a>'
                     + '</div>'
                     + '<div class="videoSidebar">'
                     + '<div class="title">'
                     + '<a href="video.html" title="" onclick="">'
                     + speaker["name"] + '</a>'
                     + '</div>'
                     + '<div class="descriptionPadding">'
                     + '<div class="description">'
                     + speaker["description"]
                     + '</div></div>' 
                     + '<div class="metadata">'
                     + '<div class="views">Views: 83,190</div>'
                     + '<div class="runtime">04:11</div>'
                     + '</div></div></div>';  
        }
        let videos = document.getElementById('video_box');  
        if(videos){
            videos.innerHTML = video_box;
        }
    })
    .catch(function(error){
        console.log(error);
    });
}
