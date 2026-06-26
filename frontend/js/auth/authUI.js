import { loginToServer } from './authService.js';

document.getElementById('loginBtn').addEventListener('click', async () => {
    const usernameInput = document.getElementById('username').value.trim();
    const passwordInput = document.getElementById('password').value.trim();
    const messageDiv = document.getElementById('message');


    if (!usernameInput || !passwordInput) {
        messageDiv.className = "mt-4 text-center text-sm font-medium text-red-500";
        messageDiv.innerText = "Please fill out all fields.";
        return;
    }

    try {

        messageDiv.className = "mt-4 text-center text-sm font-medium text-blue-400";
        messageDiv.innerText = "Verifying identity...";

        const data = await loginToServer(usernameInput, passwordInput);

        if (data.status === "success") {

            messageDiv.className = "mt-4 text-center text-sm font-medium text-green-500";
            messageDiv.innerText = `Success! Verified role: ${data.role}`;
            localStorage.setItem('iAuthToken', data.token);
            setTimeout(() => { window.location.href = 'chat.html'; }, 1000);
        } else {

            messageDiv.className = "mt-4 text-center text-sm font-medium text-red-500";

            messageDiv.innerText = data.message;
        }
    } catch (error) {

        messageDiv.className = "mt-4 text-center text-sm font-medium text-red-500";
        messageDiv.innerText = "System connection link error.";
    }
});