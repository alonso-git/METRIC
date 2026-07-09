import { loginToServer } from './authService.js';

const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('loginBtn');
const messageDiv = document.getElementById('message');

const toggleLink = document.getElementById('toggleLink');
const toggleText = document.getElementById('toggleText');


const formTitle = document.querySelector('h1');
const formSubtitle = document.getElementById('formSubtitle');

let isSignUpMode = false;

loginBtn.addEventListener('click', handleAuthAction);

passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleAuthAction();
});


if (toggleLink) {
    toggleLink.addEventListener('click', (e) => {
        e.preventDefault();
        isSignUpMode = !isSignUpMode;

        if (isSignUpMode) {
            formTitle.innerText = "Create Account";
            if (formSubtitle) formSubtitle.innerText = "Join the METRIC platform today.";
            loginBtn.innerText = "Register to Metric";
            toggleText.innerHTML = `Already have an account? <a href="#" id="toggleLink" class="text-blue-400 hover:text-blue-300 font-medium transition-colors">Log in here</a>`;
        } else {
            formTitle.innerText = "Welcome Back";
            if (formSubtitle) formSubtitle.innerText = "Enter your credentials to access the METRIC platform.";
            loginBtn.innerText = "Login to Metric";
            toggleText.innerHTML = `Don't have an account? <a href="#" id="toggleLink" class="text-blue-400 hover:text-blue-300 font-medium transition-colors">Sign up here</a>`;
        }

        setTimeout(() => {
            const newToggleLink = document.getElementById('toggleLink');
            if (newToggleLink) {
                newToggleLink.addEventListener('click', () => toggleLink.click());
            }
        }, 50);
    });
}

async function handleAuthAction() {
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!username || !password) {
        showError("Por favor, rellena todos los campos.");
        return;
    }

    if (isSignUpMode) {

        alert(`¡Enviando datos al Backend para registrar a: ${username}!`);
    } else {
        try {
            messageDiv.classList.add('hidden');
            loginBtn.innerText = "Connecting to METRIC...";
            loginBtn.disabled = true;

            const userData = await loginToServer(username, password);

            localStorage.setItem('iAuthToken', userData.token);
            localStorage.setItem('userRole', userData.role);
            localStorage.setItem('agentName', userData.name);
            localStorage.setItem('userId', userData.user_id);
            localStorage.setItem('userEmail', username);
            localStorage.setItem('userPassword', password);
            if (userData.client_chat) {
                localStorage.setItem('client_chat', JSON.stringify(userData.client_chat));
            }
            if (userData.agent_chat) {
                localStorage.setItem('agent_chat', JSON.stringify(userData.agent_chat));
            }

            if (userData.role === 'agent') {
                window.location.href = 'chat.html';
            } else {
                window.location.href = 'client-chat.html';
            }

            console.log(userData);

        } catch (error) {
            showError(error.message);
            loginBtn.innerText = "Login to Metric";
            loginBtn.disabled = false;
        }
    }
}

function showError(msg) {
    messageDiv.innerText = msg;
    messageDiv.className = "mt-4 text-center text-sm font-semibold text-red-500 block";
}