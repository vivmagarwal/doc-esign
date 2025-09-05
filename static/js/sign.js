// Sign Document JavaScript
let trackingId = null;
let signatureData = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Get tracking ID from URL
    const pathParts = window.location.pathname.split('/');
    trackingId = pathParts[pathParts.length - 1];
    
    if (trackingId) {
        loadSignature();
    } else {
        showError('Invalid signature link');
    }
    
    // Setup form submission
    document.getElementById('signForm').addEventListener('submit', handleSignSubmit);
    
    // Set today's date
    document.querySelector('input[name="date"]').valueAsDate = new Date();
});

// Load signature data
async function loadSignature() {
    try {
        const response = await fetch(`/api/signature/${trackingId}`);
        const result = await response.json();
        
        if (result.success) {
            signatureData = result.data;
            displayDocument();
        } else {
            showError(result.message || 'Failed to load document');
        }
    } catch (error) {
        console.error('Error loading signature:', error);
        showError('Error loading document');
    }
}

// Display document
function displayDocument() {
    const { signature, document: doc } = signatureData;
    
    // Hide loading, show content
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('documentContent').classList.remove('hidden');
    
    // Set document info
    document.getElementById('documentTitle').textContent = doc.title;
    document.getElementById('senderInfo').textContent = `${signature.sender_name} (${signature.sender_email})`;
    document.getElementById('purposeText').textContent = signature.purpose;
    
    // Display document content
    document.getElementById('documentDisplay').innerHTML = doc.html;
    
    // Check signature status
    updateSignatureStatus(signature);
}

// Update signature status display
function updateSignatureStatus(signature) {
    const statusBadge = document.getElementById('statusBadge');
    const signatureForm = document.getElementById('signatureForm');
    const alreadySigned = document.getElementById('alreadySigned');
    const quizStatus = document.getElementById('quizStatus');
    
    switch (signature.status) {
        case 'sent':
            statusBadge.className = 'badge badge-info';
            statusBadge.textContent = 'Awaiting Signature';
            break;
            
        case 'acknowledged':
        case 'quiz_pending':
            statusBadge.className = 'badge badge-warning';
            statusBadge.textContent = 'Quiz Pending';
            signatureForm.classList.add('hidden');
            alreadySigned.classList.remove('hidden');
            quizStatus.innerHTML = `
                <p style="color: var(--gray-600); margin-bottom: var(--space-3);">Please complete the verification quiz:</p>
                <a href="/quiz/${signature.quiz_id}" class="btn btn-primary">
                    Take Quiz
                </a>
            `;
            break;
            
        case 'quiz_failed':
            statusBadge.className = 'badge badge-danger';
            statusBadge.textContent = 'Quiz Failed';
            signatureForm.classList.add('hidden');
            alreadySigned.classList.remove('hidden');
            quizStatus.innerHTML = `
                <p style="color: var(--danger-600); margin-bottom: var(--space-3);">Quiz verification failed. Please try again:</p>
                <a href="/quiz/${signature.quiz_id}" class="btn btn-danger">
                    Retake Quiz
                </a>
            `;
            break;
            
        case 'completed':
            statusBadge.className = 'badge badge-success';
            statusBadge.textContent = 'Completed';
            signatureForm.classList.add('hidden');
            alreadySigned.classList.remove('hidden');
            quizStatus.innerHTML = `
                <p style="color: var(--success-600);">✅ Document successfully signed and verified!</p>
            `;
            break;
    }
}

// Handle sign form submission
async function handleSignSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        acknowledged: formData.get('acknowledged') === 'on',
        name: formData.get('name'),
        date: formData.get('date'),
        location: formData.get('location')
    };
    
    try {
        const response = await fetch(`/api/submit-signature/${trackingId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Redirect to dashboard after signing
            window.location.href = '/';
        } else {
            alert(`Error: ${result.message || 'Failed to submit signature'}`);
        }
    } catch (error) {
        console.error('Error submitting signature:', error);
        alert('Error submitting signature. Please try again.');
    }
}

// Show error state
function showError(message) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('errorState').classList.remove('hidden');
    document.getElementById('errorMessage').textContent = message;
}