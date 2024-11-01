import { getCurrentUser, listContents, createContent, deleteContent, updateContent } from '../api-interactions.js';
import { getEventById, showErrorMessage,showSuccessMessage } from '../dashboard.js'


let currentContents = "";

async function handleViewContent(e) {
    const eventId = e.target.getAttribute('data-event-id');
    try {
        currentContents = await listContents(eventId)
        const event = getEventById(eventId)
        document.getElementById('eventContentName').textContent = event.name
        document.getElementById('eventContentId').value = eventId;
        displayEventContents(currentContents)
        const eventContentModal = new bootstrap.Modal(document.getElementById('eventContentModal'))
        eventContentModal.show();
    } catch(error) {
        console.error('Error loading event contents:', error);
        showErrorMessage('Failed to load event contents. Please try again.');
    }
}

function handleContentActions(e) {
    if (e.target.classList.contains('edit-content')) {
        const language = e.target.getAttribute('data-language');
        const content = currentContents.find(c => c.language === language);
        document.getElementById('eventContentLanguage').value = language;
        document.getElementById('eventContentText').value = content.content;
    } else if (e.target.classList.contains('delete-content')) {
        const language = e.target.getAttribute('data-language');
        handleDeleteContent(language);
    }
}

async function handleDeleteContent(language) {
    const eventId = document.getElementById('eventContentId').value;
    if (confirm('Are you sure you want to delete this content?')) {
        try {
            await deleteContent(eventId, language);
            const updatedContents = await listContents(eventId);
            displayEventContents(updatedContents);
            showSuccessMessage('Content deleted successfully!');
        } catch (error) {
            console.error('Error deleting content:', error);
            showErrorMessage('Failed to delete content. Please try again.');
        }
    }
}

async function handleSaveContent(e) {
    e.preventDefault();
    const eventId = document.getElementById('eventContentId').value;
    const language = document.getElementById('eventContentLanguage').value;
    const content = document.getElementById('eventContentText').value;
    try {
        const existingContent = await listContents(eventId);
        const contentExists = existingContent.some(c => c.language === language);
        if (contentExists) {
            await updateContent(eventId, { content }, language);
        } else {
            await createContent(eventId, { content }, language);
        }
        const updatedContents = await listContents(eventId);
        displayEventContents(updatedContents);
        showSuccessMessage('Content saved successfully!');
    } catch (error) {
        console.error('Error saving content:', error);
        showErrorMessage('Failed to save content. Please try again.');
    }
}

function displayEventContents(contents) {
    const contentList = document.getElementById('eventContentList');
    contentList.innerHTML = '';
    contents.forEach(content => {
        const contentItem = document.createElement('div');
        contentItem.className = 'mb-3 p-2 border rounded';
        contentItem.innerHTML = `
            <h6>Language: ${content.language}</h6>
            <p>${content.content}</p>
            <button class="btn btn-sm btn-primary edit-content" data-language="${content.language}">Edit</button>
            <button class="btn btn-sm btn-danger delete-content" data-language="${content.language}">Delete</button>
        `;
        contentList.appendChild(contentItem);
    });
}


export {
    handleViewContent,
    handleContentActions,
    handleDeleteContent,
    handleSaveContent
}