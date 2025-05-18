document.getElementById('playlist-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var playlistURL = document.getElementById('playlist-url').value;
    document.getElementById('status').textContent = 'Processing...';

    // Add your API call here or processing logic
    setTimeout(() => {
        document.getElementById('status').textContent = 'Download complete!';
    }, 2000); // Mocking a 2-second wait for processing
});
