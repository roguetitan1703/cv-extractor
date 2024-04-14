document.addEventListener('DOMContentLoaded', () => {
    const cvInput = document.getElementById('file');
    const extractButton = document.getElementById('extractButton');
    const message = document.getElementById('message');
  
    extractButton.addEventListener('click', async () => {
    const file = cvInput.files[0];
    try {
        
        if (!file) {
            message.textContent = 'Please select a file.';
            return;
        }
        else if (file.type != 'application/x-zip-compressed') {
            message.textContent = 'Please select a ZIP file.';
            return;
        }
        
        console.log(cvInput.files);
        console.log(file);
        console.log(file.type);
        
        // Create a FormData object to hold file and other data (optional)
        const formData = new FormData();
        formData.append('uploaded_file', file, file.name);

        // Add a class to the extractButton to indicate that it's processing
        extractButton.classList.add('.loading-spinner');

        // Wait for the response
        // Send a POST request (recommended) to the backend endpoint
        
        // Send the POST request with FormData
        const response = await fetch('/extract_data', {
            method: 'POST',
            body: formData,
        });


    
        // Simulate successful processing
        message.textContent = 'CVs processed successfully! Download the Excel sheet.';
    
        // Download functionality (replace with actual Excel generation logic)
        const downloadLink = document.createElement('a');
        downloadLink.href = '#'; // Replace with actual Excel file URL
        downloadLink.download = 'extracted_data.xlsx';
        downloadLink.click();

    } catch (error) {
        console.error(error);
        message.textContent = 'An error occurred while processing the CVs. Please try again.';
    }
    });
});