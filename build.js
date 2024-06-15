document.addEventListener("DOMContentLoaded", function() {
    fetch('biography.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Update the HTML content with the JSON data
            document.getElementById('name').textContent = data.name;
            document.getElementById('name-subheader').textContent = data.summary;
            document.getElementById('languages').textContent = data.languages;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});