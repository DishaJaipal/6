// DOM Elements
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const uploadArea = document.getElementById('uploadArea');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const filenameDisplay = document.getElementById('filenameDisplay');
const askBtn = document.getElementById('askBtn');
const questionInput = document.getElementById('question');
const chatHistory = document.getElementById('chatHistory');
const initialMessage = document.getElementById('initialMessage');

let selectedFile = null;

// Event Listeners
browseBtn.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    selectedFile = e.target.files[0];
    filenameDisplay.textContent = `Selected: ${selectedFile.name}`;
    uploadBtn.disabled = false;
    
    // Remove any previous alerts
    uploadStatus.innerHTML = '';
  }
});

// Handle drag and drop
// [Previous DOM elements and event listeners remain exactly the same...]

// Upload PDF - Modified error handling
uploadBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  
  try {
    uploadBtn.innerHTML = '<span class="spinner-text"><div class="loading"></div> Processing...</span>';
    uploadBtn.disabled = true;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });
    
    // Check for HTTP errors
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Upload failed. Please try again.');
    }

    const data = await response.json();
    
    showAlert(data.message || 'PDF uploaded and processed successfully!', 'success');
    askBtn.disabled = false;
    initialMessage.textContent = 'Ask your first question about the PDF';
    
  } catch (error) {
    showAlert(`API Error: ${error.message}`, 'error');
    console.error('Upload error:', error);
  } finally {
    uploadBtn.innerHTML = '<i class="fas fa-upload"></i> Upload & Process';
    uploadBtn.disabled = false;
  }
});

// Ask Question - Enhanced error handling
async function askQuestion() {
  const question = questionInput.value.trim();
  
  if (!question) {
    showAlert('Please enter a question', 'error', chatHistory);
    return;
  }
  
  try {
    // Add user question to chat
    addMessage(question, 'user');
    questionInput.value = '';
    askBtn.disabled = true;
    askBtn.innerHTML = '<span class="spinner-text"><div class="loading"></div> Thinking...</span>';
    
    if (initialMessage) initialMessage.style.display = 'none';
    
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });

    // Check for HTTP errors first
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get answer from server');
    }

    const data = await response.json();
    

    if (data.error) {
      throw new Error(data.error);
    }
    
    addMessage(data.answer || 'No answer was returned', 'ai');
    
  } catch (error) {
    addMessage(`Error: ${error.message}`, 'ai');
    console.error('API Error:', error);
  } finally {
    askBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Ask';
    askBtn.disabled = false;
    questionInput.focus();
  }
}
// Helper functions
function addMessage(text, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message');
  messageDiv.classList.add(sender === 'user' ? 'user-message' : 'ai-message');
  messageDiv.textContent = text;
  chatHistory.appendChild(messageDiv);
  messageDiv.scrollIntoView({ behavior: 'smooth' });
}

function showAlert(message, type, parent = uploadStatus) {
  const alertDiv = document.createElement('div');
  alertDiv.classList.add('alert');
  alertDiv.classList.add(`alert-${type}`);
  
  const icon = document.createElement('i');
  icon.classList.add('fas', type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle');
  
  alertDiv.appendChild(icon);
  alertDiv.appendChild(document.createTextNode(message));
  
  parent.innerHTML = '';
  parent.appendChild(alertDiv);
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    alertDiv.style.opacity = '0';
    setTimeout(() => alertDiv.remove(), 300);
  }, 5000);
}

// Allow pressing Enter to ask question
questionInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    askQuestion();
  }
});