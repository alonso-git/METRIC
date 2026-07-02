// js/auth/authUI.js
import { loginToServer } from './authService.js';

const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('loginBtn');
const messageDiv = document.getElementById('message');

loginBtn.addEventListener('click', handleLogin);


passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleLogin();
});

async function handleLogin() {
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!username || !password) {
        showError("Por favor, rellena todos los campos.");
        return;
    }

    try {
        messageDiv.classList.add('hidden');
        loginBtn.innerText = "Connecting to METRIC...";
        loginBtn.disabled = true;


        const userData = await loginToServer(username, password);

        localStorage.setItem('iAuthToken', userData.token);
        localStorage.setItem('userRole', userData.role);
        localStorage.setItem('agentName', userData.name);
        localStorage.setItem('userId', userData.user_id);


        if (userData.role === 'agent') {
            window.location.href = 'chat.html';
        } else {
            window.location.href = 'client-chat.html';
        }

    } catch (error) {
        showError(error.message);
        loginBtn.innerText = "Login to Metric";
        loginBtn.disabled = false;
    }
}

function showError(msg) {
    messageDiv.innerText = msg;
    messageDiv.className = "mt-4 text-center text-sm font-semibold text-red-500 block";
}