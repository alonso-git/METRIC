import { loginToServer, registerToServer } from './authService.js';

const authBtn = document.getElementById('loginBtn');
const toggleLink = document.getElementById('toggleLink');
const toggleText = document.getElementById('toggleText');
const titleH1 = document.querySelector('h1');
const messageDiv = document.getElementById('message');

let isLoginMode = true;


toggleLink.addEventListener('click', (e) => {
    e.preventDefault();
    isLoginMode = !isLoginMode;
    messageDiv.classList.add('hidden');

    if (isLoginMode) {
        titleH1.innerText = "Welcome Back";
        authBtn.innerText = "Login to Metric";
        toggleText.innerHTML = `Don't have an account? <a href="#" id="toggleLink" class="text-blue-400 font-medium hover:text-blue-300">Sign up here</a>`;
    } else {
        titleH1.innerText = "Create Account";
        authBtn.innerText = "Register Now";
        toggleText.innerHTML = `Already have an account? <a href="#" id="toggleLink" class="text-blue-400 font-medium hover:text-blue-300">Login here</a>`;
    }

    document.getElementById('toggleLink').addEventListener('click', () => toggleLink.click());
});

authBtn.addEventListener('click', async () => {
    const usernameInput = document.getElementById('username').value.trim();
    const passwordInput = document.getElementById('password').value.trim();

    if (!usernameInput || !passwordInput) {
        messageDiv.className = "mt-4 text-center text-sm font-medium text-red-500 block";
        messageDiv.innerText = "Please fill out all fields.";
        return;
    }

    try {
        messageDiv.className = "mt-4 text-center text-sm font-medium text-blue-400 block";

        if (isLoginMode) {

            messageDiv.innerText = "Verifying identity...";
            const data = await loginToServer(usernameInput, passwordInput);

            if (data.status === "success") {
                messageDiv.className = "mt-4 text-center text-sm font-medium text-green-500 block";
                messageDiv.innerText = `Redirecting as ${data.user.role}...`;


                localStorage.setItem('iAuthToken', data.token);
                localStorage.setItem('agentName', data.user.full_name);


                setTimeout(() => {
                    if (data.user.role === "Support Agent") {
                        window.location.href = 'chat.html';
                    } else if (data.user.role === "Customer") {
                        window.location.href = 'client-chat.html';
                    }
                }, 1000);

            } else {
                messageDiv.className = "mt-4 text-center text-sm font-medium text-red-500 block";
                messageDiv.innerText = data.message;
            }
        } else {

            messageDiv.innerText = "Creating secure customer account...";
            const result = await registerToServer(usernameInput, passwordInput);

            if (result.status === "success") {
                messageDiv.className = "mt-4 text-center text-sm font-medium text-green-500 block";
                messageDiv.innerText = result.message;

                setTimeout(() => toggleLink.click(), 1500);
            }
        }
    } catch (error) {
        messageDiv.className = "mt-4 text-center text-sm font-medium text-red-500 block";
        messageDiv.innerText = "System connection link error.";
    }
});