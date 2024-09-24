import { getCurrentUser, logout, createEvent, listEvents, deleteEvent, updateEvent, listContents, createContent, deleteContent, updateContent, subscribeToEvent, unsubscribeFromEvent, listSubscribers, triggerEvent } from './api-interactions.js';
import { loadRecords } from './components/records.js';
import { loadEvents, handleCreateEvent, handleEventActions, handleUpdateEvent, handleTriggerEvent } from './components/event-management.js';
import { handleViewContent,handleContentActions, handleSaveContent } from './components/content-management.js';
import { handleViewSubscribers, handleSubscribe, handleUnsubscribe, updateSubscriptionButtons } from './components/subscription-management.js';

document.addEventListener('DOMContentLoaded', () => {
    // Handle navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = e.target.getAttribute('href').substring(1);
            showSection(targetId);
        });
    });

    // Load user profile
    loadUserProfile();

    // Load events
    loadEvents();

    // Load records
    // loadRecords();

    // Add event listener for logout button
    document.getElementById('logoutButton').addEventListener('click', handleLogout);

    // Handle event creation
    const createEventForm = document.getElementById('createEventForm');
    createEventForm.addEventListener('submit', handleCreateEvent);

    // Handle event actions (view content / edit and delete events / subscription)
    document.querySelector('#eventsTableBody').addEventListener('click', (e) => {
        const eventId = e.target.getAttribute('data-event-id');
        if (e.target.matches('.edit-event, .delete-event')) {
            handleEventActions(e);
        }else if (e.target.matches('.view-content')) {
            handleViewContent(e)
        }else if (e.target.matches('.subscribe-event')) {
            handleSubscribe(eventId);
        }else if (e.target.matches('.unsubscribe-event')) {
            handleUnsubscribe(eventId)
        }else if (e.target.matches('.view-subscribers')) {
            handleViewSubscribers(eventId)
        }else if (e.target.matches('.trigger-event')) {
            handleTriggerEvent(eventId);
        }
    });

    // Handle event update
    document.getElementById('editEventForm').addEventListener('submit', handleUpdateEvent);

    // Handle content actions
    document.getElementById('eventContentList').addEventListener('click', handleContentActions);
        
    // Add event listener for saving content
    document.getElementById('eventContentForm').addEventListener('submit', handleSaveContent);
    
});

async function handleLogout(e) {
    e.preventDefault();
    try {
        await logout();
    } catch (error) {
        console.error('Error during logout:', error);
        showErrorMessage('Failed to logout. Please try again.');
    }
}

function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.add('d-none');
    });
    document.getElementById(sectionId).classList.remove('d-none');
}

async function loadUserProfile() {
    try {
        const user = await getCurrentUser();
        document.getElementById('profileUserId').textContent = user.User['id'];
        document.getElementById('profileUsername').textContent = user.User['username'] || "Social Login";
        document.getElementById('profileLanguage').textContent = user.User['language'];
        document.getElementById('profileLineUserId').textContent = user.User['line_user_id'] || 'Not connected';
    } catch (error) {
        console.error('Error loading user profile:', error);
    }
}

function getEventById(eventId) {
    const eventRow = document.querySelector(`[data-event-id="${eventId}"]`).closest('tr');
    if (eventRow) {
        return {
            id: eventId,
            name: eventRow.cells[0].textContent,
            route: eventRow.cells[1].textContent
        };
    }
    return null;
}


function showSuccessMessage(message) {
    // Implementation of success message 
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-success alert-dismissible" role="alert">
           ${message}
           <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    alertPlaceholder.append(wrapper);
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        const alert = bootstrap.Alert.getOrCreateInstance(wrapper.firstElementChild);
        alert.close();
    }, 3000);
}

function showErrorMessage(message) {
    // Implementation of error message
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-danger alert-dismissible" role="alert">
           ${message}
           <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    alertPlaceholder.append(wrapper);
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = bootstrap.Alert.getOrCreateInstance(wrapper.firstElementChild);
        alert.close();
    }, 5000);
}


export {
    updateSubscriptionButtons,
    getEventById,
    showErrorMessage,
    showSuccessMessage,
};