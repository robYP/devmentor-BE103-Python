import { createEvent, listEvents, deleteEvent, updateEvent, triggerEvent, createContent, listContents, updateContent, deleteContent } from '../api-interactions.js';
import { getEventById, showErrorMessage,showSuccessMessage } from '../dashboard.js'
import { updateSubscriptionButtons } from './subscription-management.js'

let currentEventContents = "";

async function loadEvents() {
    try {
        const events = await listEvents();
        const eventsTableBody = document.getElementById('eventsTableBody');
        eventsTableBody.innerHTML = '';
        events.forEach(event => {
            const row = `
                <tr>
                    <td>${event.name}</td>
                    <td>${event.route}</td>
                    <td>${new Date(event.create_time).toLocaleString()}</td>
                    <td>
                        <button class="btn btn-sm btn-info view-content" data-event-id="${event.id}">View Content</button>
                        <button class="btn btn-sm btn-primary edit-event" data-event-id="${event.id}">Edit</button>
                        <button class="btn btn-sm btn-danger delete-event" data-event-id="${event.id}">Delete</button>
                        <button class="btn btn-sm btn-secondary view-subscribers" data-event-id="${event.id}">View Subscribers</button>
                        <button class="btn btn-sm btn-success subscribe-event" data-event-id="${event.id}">Subscribe</button>
                        <button class="btn btn-sm btn-warning unsubscribe-event" data-event-id="${event.id}" style="display:none;">Unsubscribe</button>
                        <button class="btn btn-sm btn-info trigger-event" data-event-id="${event.id}">Trigger</button>
                    </td>
                </tr>
            `;
            eventsTableBody.innerHTML += row;
        });
        // Update subscription buttons for all events after loading
        for (const event of events) {
            await updateSubscriptionButtons(event.id);
        }
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

async function handleCreateEvent(e) {
    e.preventDefault();
    const name = document.getElementById('eventName').value;
    const route = document.getElementById('eventRoute').value;
    const contentLanguages = document.getElementsByName('contentLanguage[]');
    const contentTexts = document.getElementsByName('contentText[]');

    try {
        const newEvent = await createEvent(name, route)
        console.log('New event created:', newEvent);

        for (let i = 0; i < contentLanguages.length; i++) {
            await createContent(newEvent.id, { content: contentTexts[i].value }, contentLanguages[i].value);
        }
        
        // Close the modal and refresh the events list
        const modal = bootstrap.Modal.getInstance(document.getElementById('createEventModal'));
        modal.hide();
        await loadEvents();
        showSuccessMessage('Event created successfully with content!');
    } catch (error) {
        console.error('Error creating event:', error);
        showErrorMessage('Failed to create event. Please try again.');
    }
}

async function handleEventActions(e) {
    const target = e.target;
    const eventId = target.getAttribute('data-event-id');
    if (!eventId || isNaN(parseInt(eventId))) {
        console.error('Invalid event ID');
        showErrorMessage('An error occurred. Please try again.');
        return;
    }

    if (target.classList.contains('delete-event')) {

        if (confirm('Are you sure you want to delete this event?')) {
            try {
                await deleteEvent(eventId);
                await loadEvents(); // Refresh the events list
                showSuccessMessage('Event deleted successfully!');
            } catch (error) {
                console.error('Error deleting event:', error);
                showErrorMessage('Failed to delete event. Please try again.');
            }
        }
    } else if (target.classList.contains('edit-event')) {
        openEditEventModal(eventId);
    }
}

async function openEditEventModal(eventId) {
    try {
        const event = getEventById(eventId);
        if (event) {
            document.getElementById('editEventId').value = event.id;
            document.getElementById('editEventName').value = event.name;
            document.getElementById('editEventRoute').value = event.route;

            currentEventContents = await listContents(eventId);
            displayEditEventContents(currentEventContents);

            const editEventModal = new bootstrap.Modal(document.getElementById('editEventModal'));
            editEventModal.show();
        } else {
            showErrorMessage('Failed to load event details. Please try again.');
        }
    } catch (error) {
        console.error('Error opening edit event modal:', error);
        showErrorMessage('Failed to load event details. Please try again.');
    }
}

function displayEditEventContents(contents) {
    const contentList = document.getElementById('editContentList');
    contentList.innerHTML = '';
    contents.forEach((content, index) => {
        const contentEntry = document.createElement('div');
        contentEntry.className = 'content-entry';
        contentEntry.innerHTML = `
            <div class="mb-2">
                <select class="form-select content-language" name="editContentLanguage[]">
                    <option value="EN" ${content.language === 'EN' ? 'selected' : ''}>English</option>
                    <option value="ZH" ${content.language === 'ZH' ? 'selected' : ''}>Chinese</option>
                </select>
            </div>
            <div class="mb-2">
                <textarea class="form-control content-text" name="editContentText[]" rows="3" required>${content.content}</textarea>
            </div>
            <button type="button" class="btn btn-danger btn-sm delete-content" data-index="${index}">Delete Content</button>
        `;
        contentList.appendChild(contentEntry);
    });
    updateAddContentButton();
}

function updateAddContentButton() {
    const addContentButton = document.getElementById('addEditContentField');
    const availableLanguages = getAvailableLanguages();
    
    if (availableLanguages.length === 0) {
        addContentButton.disabled = true;
        addContentButton.textContent = 'No more languages available';
    } else {
        addContentButton.disabled = false;
        addContentButton.textContent = 'Add New Content';
    }
}

function getAvailableLanguages() {
    const allLanguages = ['EN', 'ZH'];
    const usedLanguages = currentEventContents.map(content => content.language);
    return allLanguages.filter(lang => !usedLanguages.includes(lang));
}

document.getElementById('addEditContentField').addEventListener('click', () => {
    const availableLanguages = getAvailableLanguages();
    if (availableLanguages.length > 0) {
        const contentList = document.getElementById('editContentList');
        const newContentEntry = document.createElement('div');
        newContentEntry.className = 'content-entry';
        newContentEntry.innerHTML = `
            <div class="mb-2">
                <select class="form-select content-language" name="editContentLanguage[]">
                    ${availableLanguages.map(lang => `<option value="${lang}">${lang === 'EN' ? 'English' : 'Chinese'}</option>`).join('')}
                </select>
            </div>
            <div class="mb-2">
                <textarea class="form-control content-text" name="editContentText[]" rows="3" required></textarea>
            </div>
            <button type="button" class="btn btn-danger btn-sm delete-content" data-index="${contentList.children.length}">Delete Content</button>
        `;
        contentList.appendChild(newContentEntry);
        currentEventContents.push({ language: availableLanguages[0], content: '' });
        updateAddContentButton();
    }
});

document.getElementById('editContentList').addEventListener('click', async (e) => {
    if (e.target.classList.contains('delete-content')) {
        const index = e.target.getAttribute('data-index');
        const language = currentEventContents[index].language;
        const eventId = document.getElementById('editEventId').value;

        if (confirm('Are you sure you want to delete this content?')) {
            try {
                await deleteContent(eventId, language);
                currentEventContents.splice(index, 1);
                displayEditEventContents(currentEventContents);
                showSuccessMessage('Content deleted successfully!');
            } catch (error) {
                console.error('Error deleting content:', error);
                showErrorMessage('Failed to delete content. Please try again.');
            }
        }
    }
});

async function handleUpdateEvent(e) {
    e.preventDefault();
    const eventId = document.getElementById('editEventId').value;
    const name = document.getElementById('editEventName').value;
    const route = document.getElementById('editEventRoute').value;
    const contentLanguages = document.getElementsByName('editContentLanguage[]');
    const contentTexts = document.getElementsByName('editContentText[]');

    try {
        await updateEvent(eventId, name, route);
        
        currentEventContents = await listContents(eventId)
        // Update or create content for each language
        for (let i = 0; i < contentLanguages.length; i++) {
            const language = contentLanguages[i].value;
            const content = contentTexts[i].value;
            const existingContent = currentEventContents.find(c => c.language === language);
            console.log(existingContent)
            if (existingContent) {
                await updateContent(eventId, { content }, language);
            } else {
                await createContent(eventId, { content }, language);
            }
        }

        const editEventModal = bootstrap.Modal.getInstance(document.getElementById('editEventModal'));
        editEventModal.hide();
        await loadEvents(); // Refresh the events list
        showSuccessMessage('Event updated successfully!');
    } catch (error) {
        console.error('Error updating event:', error);
        showErrorMessage('Failed to update event. Please try again.');
    }
}

async function handleTriggerEvent(eventId) {
    try {
        await triggerEvent(eventId);
        showSuccessMessage('Event triggered successfully!');
    } catch (error) {
        console.error('Error triggering event:', error);
        showErrorMessage('Failed to trigger event. Please try again.');
    }
}

export {
    loadEvents,
    handleCreateEvent,
    handleEventActions,
    handleUpdateEvent,
    handleTriggerEvent
}

