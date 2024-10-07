import { login, register, getLineLoginUrl, handleLineCallback} from './api-interactions.js';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    try {
        const response = await login(username, password);
        window.location.href = 'main.html';
        console.log('Login successful: ', response);
    } catch (error) {
        console.error('Login failed: ', error);
        alert(error.message || 'Login failed. Please check your credentials.');
    }
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const language = document.getElementById('language').value;
    
    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    try {
        await register(username, email, password, language);
        alert('Registration successful. Please sign in.');
        bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
    } catch (error) {
        alert('Registration failed: ' + (error.message || 'Please try again.'));
    }
});

document.getElementById('lineLoginBtn').addEventListener('click', async () => {
    try {
        const response = await getLineLoginUrl()
        const lineLoginUrl = response["LINE login URL"]
        window.location.href = lineLoginUrl;
    } catch (error) {
        console.error('Error initiating LINE login:', error);
        alert('Failed to initiate LINE login. Please try again.');
    }
});

// Handle LINE login callback
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');
const state = urlParams.get('state');

if (code && state) {
    processLineCallback(code, state);
}

async function processLineCallback(code, state) {
    try {
        const response = await handleLineCallback(code, state);
        console.log('LINE login successful:', response);
        window.location.href = 'main.html'; // Redirect to main page after successful LINE login
    } catch (error) {
        alert('Failed to complete LINE login. Please try again.');
    }
}