document.querySelectorAll('.slider').forEach(slider => {
    slider.addEventListener('input', function() {
        const channelId = this.getAttribute('data-channel-id');
        const value = this.value;
        socket.emit('slider_change', { channel_id: channelId, value: value });
    });
});

// buttons
var dmxReset = document.getElementById('dmx-reset');
var dmxSaveNote = document.getElementById('dmx-save-note');
var dmxSaveBeat = document.getElementById('dmx-save-beat');
var dmxBlackout = document.getElementById('dmx-blackout');

dmxSaveBeat.addEventListener('click', ()=>{
    if(player.current_beat=='-') return;
    console.log(player.current_beat)
    socket.emit('save_beat', parseInt(player.current_beat));
});

dmxSaveNote.addEventListener('click', ()=>{
    if(player.current_note=='-') return;
    console.log(player.current_note)
    socket.emit('save_note', player.current_note);
});
