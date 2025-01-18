const API_URL = 'http://127.0.0.1:5000';

async function register(){
const username = document.getElementById("register-username").value;
const password = document.getElementById("register-password").value;
const registerMessage = document.getElementById("register-message");
try {
const response = await fetch(`${API_URL}/register`, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({ username, password }),
});
const data = await response.json();
if (response.ok) {
registerMessage.textContent = data.message;
registerMessage.style.color = "green";
showLoginForm();
} else {
registerMessage.textContent = data.message || 'Register failed.';
registerMessage.style.color = 'red';
}
} catch (error) {
    registerMessage.textContent = 'An error occurred: ' + error;
    registerMessage.style.color = 'red';
}
}
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const loginMessage = document.getElementById("login-message");

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username, password}),
        });

        const data = await response.json();

        if (response.ok) {
            loginMessage.textContent = data.message;
            loginMessage.style.color = "green";
             document.getElementById('admin-panel').style.display = 'block';
            document.getElementById('admin-login-form').style.display = 'none';
           document.getElementById('admin-register-form').style.display = 'none';
        } else {
            loginMessage.textContent = data.message || "Login failed";
            loginMessage.style.color = "red";
        }
    } catch (error) {
        loginMessage.textContent = 'An error occurred: ' + error;
        loginMessage.style.color = "red";
    }
}

async function uploadFile() {
    const fileInput = document.getElementById('pdf-file');
        const uploadMessage = document.getElementById("upload-message");
    const file = fileInput.files[0];

    if (!file) {
       uploadMessage.textContent = "Please select a file";
            uploadMessage.style.color = "red";
            return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
    const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
              body: formData,
            });
           const data = await response.json();
           if(response.ok){
                uploadMessage.textContent = data.message;
               uploadMessage.style.color = "green";
               localStorage.setItem('processedText', data.text);
           alert('File uploaded and processed successfully');
            } else {
                uploadMessage.textContent = data.message || "File upload failed";
                uploadMessage.style.color = "red";
            }
    } catch (error) {
     uploadMessage.textContent = 'An error occurred: ' + error;
        uploadMessage.style.color = 'red';
    }
}

function search() {
        const searchTerm = document.getElementById("search-box").value.toLowerCase();
        const resultsDiv = document.getElementById("results");
        const allText = localStorage.getItem('processedText');

        if (!allText) {
            resultsDiv.textContent = "No text available for search.";
            return;
        }
        if (!searchTerm) {
             resultsDiv.innerHTML = allText.replace(/\\n/g, '<br>');
             return;
        }
        const searchRegex = new RegExp(searchTerm, 'g');
        let highlightedText = allText;
        let match;
        while ((match = searchRegex.exec(allText.toLowerCase())) !== null) {
            let actualStartIndex = match.index;
            let actualEndIndex = searchRegex.lastIndex;
            highlightedText = highlightedText.substring(0, actualStartIndex) +
                '<mark>' + highlightedText.substring(actualStartIndex, actualEndIndex) +
                '</mark>' + highlightedText.substring(actualEndIndex);
            searchRegex.lastIndex = actualEndIndex;
        }
        resultsDiv.innerHTML = highlightedText.replace(/\\n/g, '<br>');
    }