import { createEvent, listEvents, deleteEvent, updateEvent, triggerEvent } from '../api-interactions.js';
import { getEventById, showErrorMessage,showSuccessMessage } from '../dashboard.js'
import { updateSubscriptionButtons } from '../components/subscription-management.js'

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
    try {
        await createEvent(name, route);
        // Close the modal and refresh the events list
        const modal = bootstrap.Modal.getInstance(document.getElementById('createEventModal'));
        modal.hide();
        loadEvents();
        showSuccessMessage('Event created successfully!');
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

function openEditEventModal(eventId) {
    const event = getEventById(eventId);
    if (event) {
        document.getElementById('editEventId').value = event.id;
        document.getElementById('editEventName').value = event.name;
        document.getElementById('editEventRoute').value = event.route;
        const editEventModal = new bootstrap.Modal(document.getElementById('editEventModal'));
        editEventModal.show();
    } else {
        showErrorMessage('Failed to load event details. Please try again.');
    }
}

async function handleUpdateEvent(e) {
    e.preventDefault();
    const eventId = document.getElementById('editEventId').value;
    const name = document.getElementById('editEventName').value;
    const route = document.getElementById('editEventRoute').value;
    try {
        await updateEvent(eventId, name, route);
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

