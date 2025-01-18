const API_URL = 'http://127.0.0.1:5000'; // Backend server URL

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
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();
        if (response.ok) {
             loginMessage.textContent = data.message;
            loginMessage.style.color = "green";
            showUploadForm();
        } else {
              loginMessage.textContent = data.message || 'Login failed.';
              loginMessage.style.color = "red";
        }
    } catch (error) {
      loginMessage.textContent = 'An error occurred: ' + error;
        loginMessage.style.color = 'red';
    }
}

async function uploadFile() {
  const fileInput = document.getElementById('pdf-file');
    const uploadMessage = document.getElementById("upload-message");
    const file = fileInput.files[0];

    if (!file) {
         uploadMessage.textContent = 'Please select a file.';
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
                window.location.href = 'index.html';

          } else {
            uploadMessage.textContent = data.message || "File upload failed"
             uploadMessage.style.color = "red";
          }
    } catch (error) {
         uploadMessage.textContent = 'An error occurred: ' + error;
            uploadMessage.style.color = "red";
    }
}


 function showLoginForm() {
            document.getElementById("login-form").style.display = "block";
            document.getElementById("upload-form").style.display = "none";
            document.getElementById("register-form").style.display = "none";
 }