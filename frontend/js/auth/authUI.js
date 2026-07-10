import { loginToServer, registerClient, registerAgent } from './authService.js';

const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('loginBtn');
const messageDiv = document.getElementById('message');

const signupName = document.getElementById('signupName');
const signupEmail = document.getElementById('signupEmail');
const signupPassword = document.getElementById('signupPassword');
const signupRole = document.getElementById('signupRole');
const signupBtn = document.getElementById('signupBtn');

const toggleLink = document.getElementById('toggleLink');
const toggleText = document.getElementById('toggleText');
const formTitle = document.querySelector('h1');
const formSubtitle = document.getElementById('formSubtitle');

const loginFields = document.getElementById('loginFields');
const signupFields = document.getElementById('signupFields');

let isSignUpMode = false;

if (toggleLink) {
    toggleLink.addEventListener('click', (e) => {
        e.preventDefault();
        isSignUpMode = !isSignUpMode;

        if (isSignUpMode) {
            loginFields.style.display = 'none';
            signupFields.style.display = 'block';
            loginBtn.style.display = 'none';
            signupBtn.style.display = 'block';

            formTitle.innerText = "Create Account";
            formSubtitle.innerText = "Join the METRIC platform today.";
            toggleText.innerHTML = `Already have an account? <a href="#" id="toggleLink" class="text-blue-400 hover:text-blue-300 font-medium transition-colors">Log in here</a>`;
        } else {
            loginFields.style.display = 'block';
            signupFields.style.display = 'none';
            loginBtn.style.display = 'block';
            signupBtn.style.display = 'none';

            formTitle.innerText = "Welcome Back";
            formSubtitle.innerText = "Enter your credentials to access the METRIC platform.";
            toggleText.innerHTML = `Don't have an account? <a href="#" id="toggleLink" class="text-blue-400 hover:text-blue-300 font-medium transition-colors">Sign up here</a>`;
        }

        setTimeout(() => {
            const newToggleLink = document.getElementById('toggleLink');
            if (newToggleLink) {
                newToggleLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    toggleLink.click();
                });
            }
        }, 50);
    });
}

loginBtn.addEventListener('click', handleLogin);
passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleLogin();
});

async function handleLogin() {
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!username || !password) {
        showError("Please fill in all fields.");
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

    } catch (error) {
        showError(error.message);
        loginBtn.innerText = "Login to Metric";
        loginBtn.disabled = false;
    }
}

signupBtn.addEventListener('click', handleSignUp);
signupPassword.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSignUp();
});

async function handleSignUp() {
    const name = signupName.value.trim();
    const email = signupEmail.value.trim();
    const password = signupPassword.value.trim();
    const role = signupRole.value;

    if (!name || !email || !password) {
        showError("Please fill in all fields.");
        return;
    }

    try {
        messageDiv.classList.add('hidden');
        signupBtn.innerText = "Creating account...";
        signupBtn.disabled = true;

        let response;
        if (role === 'client') {
            response = await registerClient(name, email, password);
        } else {
            response = await registerAgent(name, email, password);
        }

        alert(`Account created! You can now log in as ${role}.`);

        signupName.value = '';
        signupEmail.value = '';
        signupPassword.value = '';

        toggleLink.click();
        signupBtn.innerText = "Create Account";
        signupBtn.disabled = false;

    } catch (error) {
        showError(error.message);
        signupBtn.innerText = "Create Account";
        signupBtn.disabled = false;
    }
}

function showError(msg) {
    messageDiv.innerText = msg;
    messageDiv.className = "mt-4 text-center text-sm font-semibold text-red-500 block";
}