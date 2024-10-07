import { listRecords } from '../api-interactions.js';
import { showErrorMessage } from '../dashboard.js';


async function loadRecords() {
    try {
        const records = await listRecords();
        const recordsTableBody = document.getElementById('recordsTableBody');
        recordsTableBody.innerHTML = '';
        records.forEach(record => {
            const row = `
                <tr>
                    <td>${record.id}</td>
                    <td>${record.action}</td>
                    <td>${record.user_id}</td>
                    <td>${record.event_id}</td>
                    <td>${record.created_at}</td>
                </tr>
            `;
            recordsTableBody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error loading records:', error);
        showErrorMessage('Failed to load records. Please try again.');
    }
}

// Export the functions to be used in other scripts
export {
    loadRecords,
};