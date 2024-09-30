import { getCurrentUser, subscribeToEvent, unsubscribeFromEvent, listSubscribers, triggerEvent } from '../api-interactions.js';
import { getEventById, showErrorMessage,showSuccessMessage } from '../dashboard.js'


async function handleViewSubscribers(eventId) {
    try {
        const subscribers = await listSubscribers(eventId);
        const subscribersList = document.getElementById('subscribersList');
        subscribersList.innerHTML = '';
        
        if (subscribers.length === 0) {
            subscribersList.innerHTML = '<li>No subscribers for this event.</li>';
        } else {
            subscribers.forEach(subscriber => {
                const listItem = document.createElement('li');
                listItem.textContent = `User ID: ${subscriber.user_id}`;
                subscribersList.appendChild(listItem);
            });
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