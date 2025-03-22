// Wait until the page is fully loaded before running any code
document.addEventListener('DOMContentLoaded', function() {
    
    // Get references to HTML elements we'll need to work with
    const textInput = document.getElementById('textInput');
    const extractButton = document.getElementById('extractButton');
    const resultsSection = document.getElementById('resultsSection');
    const emailCount = document.getElementById('emailCount');
    const emailList = document.getElementById('emailList');
    const copyButton = document.getElementById('copyButton');
    const downloadButton = document.getElementById('downloadButton');
    
    // Variable to store the emails we extract
    let extractedEmails = [];
    
    // Add a click listener to the extract button
    extractButton.addEventListener('click', function() {
        // Get the text from the input and remove extra spaces
        const text = textInput.value.trim();
        
        // Check if the input is empty
        if (!text) {
            alert('Please enter some text first.');
            return;
        }
        
        // Create a FormData object to send to the server
        const formData = new FormData();
        formData.append('text', text);
        
        // Send the text to our server to extract emails
        fetch('/extract', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // Check if the response is OK
            if (!response.ok) {
                throw new Error('Server error');
            }
            return response.json();
        })
        .then(data => {
            // Store the extracted emails
            extractedEmails = data.emails;
            
            // Update the display with the results
            displayResults(extractedEmails);
        })
        .catch(error => {
            // Show an error message if something went wrong
            console.error('Error:', error);
            alert('An error occurred while extracting emails. Please try again.');
        });
    });
    
    // Function to display the extracted emails
    function displayResults(emails) {
        // Update the count text
        emailCount.textContent = emails.length + ' emails found';
        
        // Clear any previous results
        emailList.innerHTML = '';
        
        // If no emails were found, show a message
        if (emails.length === 0) {
            emailList.innerHTML = '<div class="email-item">No email addresses found.</div>';
        } else {
            // Add each email to the list
            emails.forEach(email => {
                const emailItem = document.createElement('div');
                emailItem.className = 'email-item';
                emailItem.textContent = email;
                emailList.appendChild(emailItem);
            });
        }
        
        // Show the results section
        resultsSection.style.display = 'block';
    }
    
    // Add a click listener to the copy button
    copyButton.addEventListener('click', function() {
        // Check if we have any emails to copy
        if (extractedEmails.length === 0) {
            alert('No emails to copy.');
            return;
        }
        
        // Join all emails with line breaks
        const emailText = extractedEmails.join('\n');
        
        // Copy to clipboard
        navigator.clipboard.writeText(emailText)
            .then(() => {
                alert('Emails copied to clipboard!');
            })
            .catch(err => {
                console.error('Failed to copy:', err);
                alert('Failed to copy emails. Your browser may not support this feature.');
            });
    });
    
    // Add a click listener to the download button
    downloadButton.addEventListener('click', function() {
        // Check if we have any emails to download
        if (extractedEmails.length === 0) {
            alert('No emails to download.');
            return;
        }
        
        // Join all emails with line breaks
        const emailText = extractedEmails.join('\n');
        
        // Create a Blob (Binary Large Object) with the email text
        const blob = new Blob([emailText], { type: 'text/plain' });
        
        // Create a URL for the Blob
        const url = URL.createObjectURL(blob);
        
        // Create a temporary link element
        const a = document.createElement('a');
        a.href = url;
        a.download = 'extracted_emails.txt';
        
        // Add the link to the page, click it, and remove it
        document.body.appendChild(a);
        a.click();
        
        // Clean up
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
    });
});
