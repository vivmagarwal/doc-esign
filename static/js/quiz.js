// Quiz JavaScript
let quizId = null;
let questions = [];
let currentQuestionIndex = 0;
let answers = {};
let attempts = 0;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Get quiz ID from URL
    const pathParts = window.location.pathname.split('/');
    quizId = pathParts[pathParts.length - 1];
    
    if (quizId) {
        loadQuiz();
    } else {
        showError('Invalid quiz link');
    }
});

// Load quiz data
async function loadQuiz() {
    try {
        const response = await fetch(`/api/quiz/${quizId}`);
        const result = await response.json();
        
        if (result.success) {
            questions = result.data.questions;
            attempts = result.data.attempts;
            displayQuiz();
        } else {
            showError(result.message || 'Failed to load quiz');
        }
    } catch (error) {
        console.error('Error loading quiz:', error);
        showError('Error loading quiz');
    }
}

// Display quiz
function displayQuiz() {
    // Hide loading, show content
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('quizContent').classList.remove('hidden');
    
    // Show attempt info if not first attempt
    if (attempts > 0) {
        document.getElementById('attemptInfo').innerHTML = `
            <div class="alert alert-warning">
                <strong>Attempt ${attempts + 1}:</strong> Remember, all questions must be answered correctly.
            </div>
        `;
    }
    
    // Display first question
    displayQuestion(0);
}

// Display a specific question
function displayQuestion(index) {
    currentQuestionIndex = index;
    const question = questions[index];
    
    // Update progress bar
    updateProgressBar(index);
    
    // Update question text
    document.getElementById('questionText').textContent = question.question;
    document.getElementById('currentQuestion').textContent = index + 1;
    
    // Display options
    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';
    
    question.options.forEach((option, optionIndex) => {
        const optionElement = document.createElement('div');
        optionElement.className = 'option-card';
        optionElement.innerHTML = `
            <label class="flex items-center cursor-pointer">
                <input type="radio" name="question${index}" value="${option}" 
                       class="mr-3 h-4 w-4 text-blue-600" ${answers[question.id] === option ? 'checked' : ''}>
                <span class="flex-1">${option}</span>
            </label>
        `;
        
        // Add click handler
        optionElement.addEventListener('click', () => {
            selectOption(question.id, option, optionElement);
        });
        
        // Mark as selected if previously answered
        if (answers[question.id] === option) {
            optionElement.classList.add('selected');
        }
        
        optionsContainer.appendChild(optionElement);
    });
    
    // Update navigation buttons
    updateNavigationButtons(index);
}

// Select an option
function selectOption(questionId, option, element) {
    // Save answer
    answers[questionId] = option;
    
    // Update UI
    document.querySelectorAll('#optionsContainer .option-card').forEach(card => {
        card.classList.remove('selected');
    });
    element.classList.add('selected');
    element.querySelector('input[type="radio"]').checked = true;
}

// Update progress bar
function updateProgressBar(index) {
    document.querySelectorAll('.progress-step').forEach((step, i) => {
        step.classList.remove('active', 'completed', 'inactive');
        
        if (i < index) {
            step.classList.add('completed');
        } else if (i === index) {
            step.classList.add('active');
        } else {
            step.classList.add('inactive');
        }
    });
}

// Update navigation buttons
function updateNavigationButtons(index) {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    // Previous button
    prevBtn.disabled = index === 0;
    
    // Next/Submit buttons
    if (index === questions.length - 1) {
        nextBtn.classList.add('hidden');
        submitBtn.classList.remove('hidden');
    } else {
        nextBtn.classList.remove('hidden');
        submitBtn.classList.add('hidden');
    }
}

// Navigate to previous question
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        displayQuestion(currentQuestionIndex - 1);
    }
}

// Navigate to next question
function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        displayQuestion(currentQuestionIndex + 1);
    }
}

// Submit quiz
async function submitQuiz() {
    // Check if all questions are answered
    const allAnswered = questions.every(q => answers[q.id]);
    
    if (!allAnswered) {
        alert('Please answer all questions before submitting.');
        return;
    }
    
    // Prepare submission data
    const submission = {
        answers: answers
    };
    
    try {
        const response = await fetch(`/api/submit-quiz/${quizId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(submission)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showResult(result.data);
        } else {
            alert(`Error: ${result.message || 'Failed to submit quiz'}`);
        }
    } catch (error) {
        console.error('Error submitting quiz:', error);
        alert('Error submitting quiz. Please try again.');
    }
}

// Show result modal
function showResult(data) {
    const resultContent = document.getElementById('resultContent');
    
    if (data.passed) {
        resultContent.innerHTML = `
            <svg class="success-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--success-700); margin-bottom: var(--space-2);">
                Congratulations!
            </h3>
            <p style="color: var(--gray-600); margin-bottom: var(--space-2);">
                You passed the quiz with a score of ${data.score}.
            </p>
            <p style="font-size: var(--text-sm); color: var(--gray-500); margin-bottom: var(--space-6);">
                Your signature has been successfully verified.
            </p>
            <a href="/" class="btn btn-success">Go to Dashboard</a>
        `;
    } else {
        resultContent.innerHTML = `
            <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--danger-700); margin-bottom: var(--space-2);">
                Quiz Not Passed
            </h3>
            <p style="color: var(--gray-600); margin-bottom: var(--space-2);">Your score: ${data.score}</p>
            <p style="font-size: var(--text-sm); color: var(--gray-500); margin-bottom: var(--space-6);">
                All questions must be answered correctly. Please try again.
            </p>
            <button onclick="retakeQuiz()" class="btn btn-danger">Retake Quiz</button>
        `;
    }
    
    showResultModal();
}

// Retake quiz
function retakeQuiz() {
    // Reset state
    answers = {};
    currentQuestionIndex = 0;
    
    // Hide modal
    document.getElementById('resultModal').classList.add('hidden');
    
    // Reload quiz
    loadQuiz();
}

// Show error state
function showError(message) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('errorState').classList.remove('hidden');
    document.getElementById('errorMessage').textContent = message;
}