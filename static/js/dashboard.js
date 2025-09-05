// Dashboard JavaScript
let allSignatures = [];
let filteredSignatures = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    // Auto-refresh every 30 seconds
    setInterval(loadDashboard, 30000);
    
    // Setup form submission
    document.getElementById('sendForm').addEventListener('submit', handleSendDocument);
});

// Load dashboard data
async function loadDashboard() {
    try {
        const response = await fetch('/api/dashboard');
        const result = await response.json();
        
        if (result.success) {
            allSignatures = result.data.signatures;
            updateDashboard(allSignatures);
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Update dashboard display
function updateDashboard(signatures) {
    filteredSignatures = signatures;
    
    // Update stats
    updateStats(signatures);
    
    // Update table
    const tbody = document.getElementById('dashboardTable');
    const noDataMsg = document.getElementById('noDataMessage');
    
    if (signatures.length === 0) {
        tbody.innerHTML = '';
        noDataMsg.classList.remove('hidden');
    } else {
        noDataMsg.classList.add('hidden');
        tbody.innerHTML = signatures.map(sig => createTableRow(sig)).join('');
    }
}

// Update statistics cards
function updateStats(signatures) {
    const stats = {
        total: signatures.length,
        pending: signatures.filter(s => ['sent', 'acknowledged', 'quiz_pending'].includes(s.status)).length,
        completed: signatures.filter(s => s.status === 'completed').length,
        failed: signatures.filter(s => s.status === 'quiz_failed').length
    };
    
    document.getElementById('totalCount').textContent = stats.total;
    document.getElementById('pendingCount').textContent = stats.pending;
    document.getElementById('completedCount').textContent = stats.completed;
    document.getElementById('failedCount').textContent = stats.failed;
}

// Create table row HTML
function createTableRow(signature) {
    const sentDateTime = new Date(signature.created_at);
    
    // Convert to IST timezone
    const sentDateIST = sentDateTime.toLocaleDateString('en-IN', { 
        timeZone: 'Asia/Kolkata',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
    const sentTimeIST = sentDateTime.toLocaleTimeString('en-IN', { 
        timeZone: 'Asia/Kolkata',
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    });
    
    const statusText = signature.status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    // Truncate tracking ID for display (show first 8 chars)
    const shortTrackingId = signature.tracking_id.substring(0, 8) + '...';
    
    // Map status to badge class
    let badgeClass = 'badge-info';
    switch(signature.status) {
        case 'sent':
            badgeClass = 'badge-info';
            break;
        case 'acknowledged':
        case 'quiz_pending':
            badgeClass = 'badge-warning';
            break;
        case 'quiz_failed':
            badgeClass = 'badge-danger';
            break;
        case 'completed':
            badgeClass = 'badge-success';
            break;
    }
    
    return `
        <tr>
            <td>
                <div style="font-weight: var(--font-medium); color: var(--gray-900);">${signature.document_title || 'Unknown'}</div>
                <div style="font-size: var(--text-sm); color: var(--gray-500);">${signature.document_id}</div>
                <div style="font-size: var(--text-xs); color: var(--gray-400); margin-top: 2px;" title="${signature.tracking_id}">ID: ${shortTrackingId}</div>
            </td>
            <td>
                <div style="color: var(--gray-900);">${signature.sender_name}</div>
                <div style="font-size: var(--text-sm); color: var(--gray-500);">${signature.sender_email}</div>
            </td>
            <td>
                <div style="color: var(--gray-900);">${signature.receiver_email}</div>
            </td>
            <td>
                <span class="badge ${badgeClass}">${statusText}</span>
            </td>
            <td>
                <div style="font-size: var(--text-sm); color: var(--gray-700);">${sentDateIST}</div>
                <div style="font-size: var(--text-xs); color: var(--gray-500);">${sentTimeIST} IST</div>
            </td>
            <td>
                <a href="/sign/${signature.tracking_id}" target="_blank" 
                   style="color: var(--primary-600); font-weight: var(--font-medium); text-decoration: none;">View</a>
            </td>
        </tr>
    `;
}

// Apply filters
function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    
    let filtered = allSignatures;
    
    // Apply search filter
    if (searchTerm) {
        filtered = filtered.filter(sig => 
            sig.sender_email.toLowerCase().includes(searchTerm) ||
            sig.receiver_email.toLowerCase().includes(searchTerm) ||
            sig.document_title?.toLowerCase().includes(searchTerm) ||
            sig.document_id.toLowerCase().includes(searchTerm)
        );
    }
    
    // Apply status filter
    if (statusFilter) {
        filtered = filtered.filter(sig => sig.status === statusFilter);
    }
    
    updateDashboard(filtered);
}

// Modal functions are now defined inline in HTML for better integration with new design system

// Handle send document form submission
async function handleSendDocument(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch('/api/send-document', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Document sent successfully!');
            closeSendModal();
            loadDashboard();
        } else {
            alert(`Error: ${result.message || 'Failed to send document'}`);
        }
    } catch (error) {
        console.error('Error sending document:', error);
        alert('Error sending document. Please try again.');
    }
}