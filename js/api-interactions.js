// api-interactions.js

const API_BASE_URL = 'http://127.0.0.1:8000/v1'; // Replace with your actual API base URL

// Function to handle API requests
async function apiRequest(endpoint, method, data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const options = {
        method: method,
        headers: {
            "ngrok-skip-browser-warning": "69420",
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: data ? JSON.stringify(data) : null
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// User authentication
async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/users/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
    });

    if (!response.ok) {
        const errorData = await response.json();
        console.error('Login error:', errorData);
        throw new Error(errorData.detail || 'Login failed');
    }

    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data;
}

function logout() {
    localStorage.removeItem('access_token');
    window.location.href = 'signin.html'; // Redirect to login page
}

async function register(username, password, language) {
    return await apiRequest('/users/', 'POST', { username, password, language });
}

async function getCurrentUser() {
    return await apiRequest('/users/currentUser');
}

async function getLineLoginUrl() {
    const response = await apiRequest('/users/line-login')
    return response
}

async function handleLineCallback(code, state) {
    const response = await fetch(`${API_BASE_URL}/users/callback?code=${code}&state=${state}`);
    const data = await response.json()
    localStorage.setItem('access_token', data.access_token);
    return response
}


// Event management
async function createEvent(name, route) {
    return await apiRequest('/events/', 'POST', { name, route });
}

async function listEvents(skip = 0, limit = 100) {
    return await apiRequest(`/events/?skip=${skip}&limit=${limit}`);
}

async function deleteEvent(eventId) {
    return await apiRequest(`/events/${eventId}`, 'DELETE');
}

async function updateEvent(eventId, name, route) {
    return await apiRequest(`/events/${eventId}`, 'PUT', { name, route });
}

// Event subscription
async function subscribeToEvent(eventId) {
    return await apiRequest(`/events/${eventId}/subscribe`, 'POST');
}

async function unsubscribeFromEvent(eventId) {
    return await apiRequest(`/events/${eventId}/unsubscribe`, 'DELETE');
}

async function listSubscribers(eventId) {
    return await apiRequest(`/events/${eventId}/subscribers`, 'GET')
}

// Content management
async function createContent(eventId, content, language) {
    return await apiRequest(`/contents/${eventId}/${language}`, 'POST', content );
}

async function listContents(eventId) {
    return await apiRequest(`/contents/${eventId}`, 'GET')
}

async function updateContent(eventId, content, language) {
    return await apiRequest(`/contents/${eventId}/${language}`, 'PUT', content );
}

async function deleteContent(eventId, language) {
    return await apiRequest(`/contents/${eventId}/${language}`, 'DELETE');
}

// Trigger functionality
async function triggerEvent(eventId) {
    return await apiRequest(`/trigger/${eventId}/send_notification`, 'GET');
}

// Load Records
async function listRecords() {
    return await apiRequest('/records/', 'GET');
}

// Export the functions to be used in other scripts
export {
    login,
    register,
    logout,
    getLineLoginUrl,
    handleLineCallback,
    getCurrentUser,
    createEvent,
    listEvents,
    deleteEvent,
    updateEvent,
    subscribeToEvent,
    unsubscribeFromEvent,
    listSubscribers,
    createContent,
    listContents,
    updateContent,
    deleteContent,
    listRecords,
    triggerEvent
};