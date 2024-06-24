var socket = io.connect('http://' + location.hostname + ':' + location.port);

/// store elements to control dynamically
var playButtonIcon = document.getElementById('playButton');
var stopButton = document.getElementById('stop');
var bpmButton = document.getElementById('song_bpm');
var beats = document.getElementsByClassName('beat');
var currTimeElement = document.getElementById('curr_time');
var abletonLinkElement = document.getElementById('ableton_link');
var currentNoteElement = document.getElementById('current_note');
var currentBeatElement = document.getElementById('current_beat');

/// player object to store the player state
const player = {
    is_playing: false,
    is_linked: false,
    bpm: parseInt(bpmButton.textContent),
    current_note: '-',
    current_beat: '-',
}

for (const idx in this.beats) {
    if (this.beats.hasOwnProperty(idx)){
        beats[idx].addEventListener('click', () => {
            player.current_beat = idx;
            player.current_note = beats[idx].textContent;
            currentNoteElement.textContent = player.current_note;
            currentBeatElement.textContent = player.current_beat;
            document.querySelectorAll('.beat.selected').forEach(beat => {
                beat.classList.remove('selected');
            });
            beats[idx].classList.add('selected');
        });  
    }

}

this.abletonLinkElement.addEventListener('click', (event) => {
    socket.emit('ableton_link');
    event.preventDefault();
});

/// update the bpm on drag up or down
let isDragging = false;
let isOverBpmDiv = false;
let currBpm = parseInt(bpmButton.textContent);
let startY;

this.bpmButton.addEventListener('mousedown', (event) => {
    isDragging = true;
    startY = event.clientY;
    event.preventDefault();
});

this.bpmButton.addEventListener('mouseenter', (event) => {
    isOverBpmDiv = true;
    event.preventDefault();
});

window.addEventListener('mousemove', (event) => {
    if (isDragging && isOverBpmDiv) {
        const deltaY = startY - event.clientY;
        let newBpm = player.bpm + parseInt(deltaY * 0.5); // Adjust the multiplier as needed
        console.log('newBpm:', newBpm, 'player.bpm:', player.bpm)
        if(newBpm != player.bpm)
            setBpm(newBpm, true);
        startY = event.clientY;
        event.preventDefault();
    }
});

window.addEventListener('mouseup', (event) => {
    isOverBpmDiv = false;
    isDragging = false;
});


function setBpm(bpm, emit = false){
    player.bpm = bpm;
    console.log('-> player.bpm:', player.bpm);
    bpmButton.textContent = player.bpm;
    if(emit){
        socket.emit('set_bpm', player.bpm);
    }
}




/// control the play/pause status of player
socket.on('status', function(status) {
    if (status === 'playing') {
        playButtonIcon.classList.remove('fa-play');
        playButtonIcon.classList.add('fa-pause');
    } else {
        playButtonIcon.classList.remove('fa-pause');
        playButtonIcon.classList.add('fa-play');
    }
});

/// play/pause the player
document.getElementById('play').addEventListener('click', function() {
    if (playButtonIcon.classList.contains('fa-play')) {
        socket.emit('play');
    } else {
        socket.emit('pause');
    }
});

/// stop the player
document.getElementById('stop').addEventListener('click', function() {
    socket.emit('stop');
});

socket.on('bpm', function(bpm) {
    console.log('bpm:', bpm);
    setBpm(bpm);
});

/// update the current beat
socket.on('curr', function(curr) {
    console.log('curr:', curr);

    // Remove the 'current' class from all beats
    for (var i = 0; i < beats.length; i++) {
        beats[i].classList.remove('current');
    }

    // Add the 'current' class to the current beat
    if (curr.beat < beats.length) {
        beats[curr.beat].classList.add('current');
    }

    // Update the curr_time element
    currTimeElement.textContent = curr.time.toFixed(2);

});