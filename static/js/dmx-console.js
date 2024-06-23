document.querySelectorAll('.slider').forEach(slider => {
    slider.addEventListener('input', function() {
        const channelId = this.getAttribute('data-channel-id');
        const value = this.value;
        socket.emit('slider_change', { channel_id: channelId, value: value });
    });
});