from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

# HTML template with embedded CSS and JavaScript
HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Extractor</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        
        .container {
            max-width: 800px;
            margin: auto;
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #333;
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        textarea {
            width: 100%;
            height: 200px;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 5px;
            font-size: 16px;
        }
        
        button:hover {
            background-color: #45a049;
        }
        
        #result {
            margin-top: 20px;
            border-top: 1px solid #ddd;
            padding-top: 20px;
        }
        
        .email-list {
            white-space: pre-line;
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        
        .actions {
            margin-top: 10px;
        }
        
        /* Add some modern touches */
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .button-group {
            display: flex;
            justify-content: space-between;
            width: 100%;
            margin-top: 10px;
        }
        
        .button-group button {
            width: 45%;
        }
        
        @media (max-width: 600px) {
            .button-group {
                flex-direction: column;
            }
            .button-group button {
                width: 100%;
                margin-bottom: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Email Extractor</h1>
        <textarea id="inputText" placeholder="Paste your text here..."></textarea>
        <div class="button-group">
            <button onclick="extractEmails()">Extract Emails</button>
            <button onclick="clearInput()">Clear</button>
        </div>
        <div id="result"></div>
    </div>

    <script>
        function extractEmails() {
            var text = document.getElementById('inputText').value;
            fetch('/extract', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text: text})
            })
            .then(response => response.json())
            .then(data => {
                var resultDiv = document.getElementById('result');
                if (data.emails.length > 0) {
                    var emailText = data.emails.join('\\n');
                    resultDiv.innerHTML = '<h3>Extracted Emails:</h3>' +
                        '<div class="email-list">' + emailText + '</div>' +
                        '<div class="actions">' +
                        '<button onclick="copyEmails()">Copy All</button>' +
                        '<button onclick="downloadEmails()">Download</button>' +
                        '</div>';
                } else {
                    resultDiv.innerHTML = '<p>No emails found.</p>';
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('result').innerHTML = '<p>An error occurred. Please try again.</p>';
            });
        }
        
        function copyEmails() {
            var emailList = document.querySelector('.email-list');
            if (emailList) {
                navigator.clipboard.writeText(emailList.textContent)
                    .then(() => alert('Emails copied to clipboard!'))
                    .catch(err => alert('Failed to copy emails: ' + err));
            }
        }
        
        function downloadEmails() {
            var emailList = document.querySelector('.email-list');
            if (emailList) {
                var blob = new Blob([emailList.textContent], {type: 'text/plain'});
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = 'extracted_emails.txt';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        }
        
        function clearInput() {
            document.getElementById('inputText').value = '';
            document.getElementById('result').innerHTML = '';
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    text = data.get('text', '')
    
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Find all emails
    emails = re.findall(email_pattern, text)
    
    # Remove duplicates while preserving order
    unique_emails = list(dict.fromkeys(emails))
    
    return jsonify({'emails': unique_emails})

if __name__ == '__main__':
    app.run(debug=True)
