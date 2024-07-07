document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var fileInput = document.getElementById('imageInput');
    var messageDiv = document.getElementById('message');
    var imageContainer = document.getElementById('imageContainer');
    var cancerMessageDiv = document.getElementById('cancerMessage');
    imageContainer.innerHTML = ''; // Clear any previous images
    cancerMessageDiv.textContent = ''; // Clear any previous cancer messages

    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        var fileType = file.type;

        if (fileType === 'image/png' || fileType === 'image/jpeg') {
            messageDiv.textContent = 'Poza a fost încărcată.';

            // Create an image element
            var img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.onload = function() {
                URL.revokeObjectURL(this.src);
                // Simulate cancer detection (replace with actual ML model)
                var isCancerous = detectCancerousMole(file);
                if (isCancerous) {
                    cancerMessageDiv.textContent = 'Atenție: Trebuie să consultați un medic!';
                }
            };

            // Append the image to the imageContainer
            imageContainer.appendChild(img);
        } else {
            messageDiv.textContent = 'Vă rugăm să încărcați o poză de tip PNG sau JPG.';
        }
    } else {
        messageDiv.textContent = 'Vă rugăm să încărcați o poză.';
    }
});

// Simulate cancer detection based on file name (replace with actual ML model)
function detectCancerousMole(file) {
    var fileName = file.name.toLowerCase();
    // Check if the file name contains the word 'cancerous'
    return fileName.includes('c');
}
