var socket = io.connect('http://' + location.hostname + ':' + location.port);

/// store elements to control dynamically
var playButtonIcon = document.getElementById('playButton');
var stopButton = document.getElementById('stop');
var beats = document.getElementsByClassName('beat');
var currTimeElement = document.getElementById('curr_time');

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