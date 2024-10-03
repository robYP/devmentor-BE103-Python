import { getCurrentUser, subscribeToEvent, unsubscribeFromEvent, listSubscribers, getUserDetails } from '../api-interactions.js';
import { getEventById, showErrorMessage,showSuccessMessage } from '../dashboard.js'


async function handleViewSubscribers(eventId) {
    try {
        const subscribers = await listSubscribers(eventId);
        const subscribersTableBody = document.getElementById('subscribersTableBody');
        subscribersTableBody.innerHTML = '';
        
        if (subscribers.length === 0) {
            subscribersTableBody.innerHTML = '<tr><td colspan="4" class="text-center">No subscribers for this event.</td></tr>';
        } else {
            for (const subscriber of subscribers) {
                const userDetails = await getUserDetails(subscriber.user_id);
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${userDetails.id}</td>
                    <td>${userDetails.username || 'N/A'}</td>
                    <td>${userDetails.email || 'N/A'}</td>
                    <td>${userDetails.line_user_id || 'N/A'}</td>
                `;
                subscribersTableBody.appendChild(row);
            }
        }
        
        const subscribersModal = new bootstrap.Modal(document.getElementById('subscribersModal'));
        subscribersModal.show();
    } catch (error) {
        console.error('Error fetching subscribers:', error);
        showErrorMessage('Failed to fetch subscribers. Please try again.');
    }
}

async function handleSubscribe(eventId) {
    try {
        await subscribeToEvent(eventId)
        showSuccessMessage('Successfully subscribed to the event.');
        await updateSubscriptionButtons(eventId)
    } catch (error) {
        console.error('Error unsubscribing from event:', error);
        showErrorMessage('Failed to unsubscribe from the event. Please try again.');
    }
}

async function handleUnsubscribe(eventId) {
    try {
        await unsubscribeFromEvent(eventId);
        showSuccessMessage('Successfully unsubscribed from the event.');
        await updateSubscriptionButtons(eventId);
    } catch (error) {
        console.error('Error unsubscribing from event:', error);
        showErrorMessage('Failed to unsubscribe from the event. Please try again.');
    }
}

async function updateSubscriptionButtons(eventId) {
    const currentUser = await getCurrentUser();
    const subscribers = await listSubscribers(eventId);
    
    const isSubscribed = subscribers.some(subscriber => subscriber.user_id === currentUser.User.id);

    const subscribeButton = document.querySelector(`.subscribe-event[data-event-id="${eventId}"]`);
    const unsubscribeButton = document.querySelector(`.unsubscribe-event[data-event-id="${eventId}"]`);

    if (subscribeButton && unsubscribeButton) {
        subscribeButton.style.display = isSubscribed ? 'none' : 'inline-block';
        unsubscribeButton.style.display = isSubscribed ? 'inline-block' : 'none';
    }
}


export {
    handleViewSubscribers,
    handleSubscribe,
    handleUnsubscribe,
    updateSubscriptionButtons,
}