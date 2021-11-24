/* Soren DeHaan and Carl Tankersley
 * 15 November 2021
 * CS 257 - Software Design
 */

window.onload = initialize;

function initialize() {
    let element = document.getElementById('random');
    let element2 = document.getElementById('submit');
    let element3 = document.getElementById('big_video');
    if (element) {
        element.onclick = oneRandomTalk;
    }
    if (element2) {
        element2.onclick = search_speaker;
    }
    if (element3) {
        get_video();
    }
}

String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours < 10) { hours = "0" + hours; }
    if (minutes < 10) { minutes = "0" + minutes; }
    if (seconds < 10) { seconds = "0" + seconds; }
    if (minutes + hours < 1) { return '00:' + seconds; }
    if (hours < 1) { return minutes + ':' + seconds; }
    return hours + ':' + minutes + ':' + seconds;
}

function getAPIBaseURL() {
    let baseURL = window.location.protocol
        + '//' + window.location.hostname
        + ':' + window.location.port
        + '/api';
    return baseURL;
}

// function onRandomSpeakerButton() {
//     let url = getAPIBaseURL() + '/random/';

//     fetch(url, { method: 'get' })
//         .then((response) => response.json())
//         .then(function (speaker) {
//             let str = '';
//             str += '<h2>' + speaker['name']
//                 + ': ' + speaker['title']
//                 + '</h2>';
//             let newHTML = document.getElementById('random_speaker');
//             if (newHTML) {
//                 newHTML.innerHTML = str;
//             }
//         })
//         .catch(function (error) {
//             console.log(error);
//         });
// }

function oneRandomTalk() {
    let url = getAPIBaseURL() + '/search_videos/?sort=random';
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (speakers) {
            window.location.href = 'video.html?id=' + speakers[0]["id"];
        })
        .catch(function (error) {
            console.log(error);
        });
}

function search_speaker() {
    let input = document.getElementById('speaker_search').value;
    let secondaryInput = document.getElementById('sorter').value;
    console.log("secondary=" + secondaryInput)
    let url = getAPIBaseURL() + '/search_videos/?search=' + input;
    if (secondaryInput) {
        url += '&sort="' + secondaryInput + '"'
        console.log(url)
    }
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (speakers) {
            let newHTML = '';
            for (let i = 0; i < speakers.length; i++) {
                let speaker = speakers[i];
                let duration = String(speaker["duration"]);
                console.log(duration);
                duration = duration.toHHMMSS();
                console.log(duration);
                newHTML += '<div class="video">'
                    + '<div class="imageWrapper">'
                    + '<a href="video.html?id=' + speaker["id"] + '"><img '
                    + 'src="' + speaker["image"] + '" '
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
                    + '<div class="runtime">'
                    + duration
                    + '</div></div></div></div>';
            }
            // newHTML = decodeURIComponent(newHTML);
            let videos = document.getElementById('video_box');
            if (videos) {
                videos.innerHTML = newHTML;
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}


function get_video() {
    let pattern = /\?id=([\d]*)/g;
    let input = window.location.href.match(pattern)[0].substring(4);
    // console.log("input = "+input);
    let url = getAPIBaseURL() + '/video/' + input;
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (talk_id) {
            let newHTML = '';
            newHTML += '<div class="bigImageWrapper">'
                + ' <div class="bigImageContainer">'
                + ' <a href="' + encodeURIComponent(talk_id["url"]).replace(/\s+/g, '') + '"><img'
                + ' src="' + encodeURIComponent(talk_id["image"]).replace(/\s+/g, '') + '"'
                + ' class="" title="" alt="video"><div class="middle">Watch it on TED.com!</div></a>'
                + ' </div>'
                + ' </div>'
                + ' <div class="title">'
                + ' <h2><a href="" title="" onclick="">'
                + talk_id["name"]
                + ' </a></h2>'
                + ' </div>'
                + ' <div class="descriptionPadding">'
                + ' <div class="bigDescription">'
                + talk_id["description"]
                + ' </div>'
                + ' </div>';
            console.log(newHTML)
            newHTML = decodeURIComponent(newHTML);
            console.log(newHTML)
            let video_output = document.getElementById('big_video');
            if (video_output) {
                video_output.innerHTML = newHTML;
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}