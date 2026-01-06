/**
 * RAG Chatbot - Frontend JavaScript with Advanced Features
 * Project: RAG Chatbot
 * Developer: RSK World
 * Website: https://rskworld.in
 * Email: help@rskworld.in
 * Phone: +91 93305 39277
 * Year: 2026
 * Description: Frontend JavaScript for the RAG chatbot interface with advanced features
 */

// Global state
let sessionId = 'default-' + Date.now();
let isStreaming = true;
let useHybrid = false;
let currentStreamingMessage = null;

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const loadingOverlay = document.getElementById('loadingOverlay');
const hybridSearchToggle = document.getElementById('hybridSearchToggle');
const streamingToggle = document.getElementById('streamingToggle');
const clearChatBtn = document.getElementById('clearChatBtn');
const exportChatBtn = document.getElementById('exportChatBtn');
const uploadBtn = document.getElementById('uploadBtn');
const analyticsBtn = document.getElementById('analyticsBtn');
const uploadModal = document.getElementById('uploadModal');
const analyticsModal = document.getElementById('analyticsModal');
const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');
const fileUploadArea = document.getElementById('fileUploadArea');
const closeUploadModal = document.getElementById('closeUploadModal');
const closeAnalyticsModal = document.getElementById('closeAnalyticsModal');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Generate session ID
    sessionId = 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    
    // Focus on input
    userInput.focus();
    
    // Add event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Toggle listeners
    hybridSearchToggle.addEventListener('change', function() {
        useHybrid = this.checked;
    });
    
    streamingToggle.addEventListener('change', function() {
        isStreaming = this.checked;
    });
    
    // Button listeners
    clearChatBtn.addEventListener('click', clearChat);
    exportChatBtn.addEventListener('click', exportChat);
    uploadBtn.addEventListener('click', () => uploadModal.style.display = 'block');
    analyticsBtn.addEventListener('click', showAnalytics);
    
    // Modal close listeners
    closeUploadModal.addEventListener('click', () => uploadModal.style.display = 'none');
    closeAnalyticsModal.addEventListener('click', () => analyticsModal.style.display = 'none');
    
    // Click outside modal to close
    window.addEventListener('click', function(e) {
        if (e.target === uploadModal) uploadModal.style.display = 'none';
        if (e.target === analyticsModal) analyticsModal.style.display = 'none';
    });
    
    // File upload
    fileUploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    uploadForm.addEventListener('submit', handleFileUpload);
    
    // Drag and drop
    fileUploadArea.addEventListener('dragover', handleDragOver);
    fileUploadArea.addEventListener('drop', handleFileDrop);
    
    // Check chatbot health
    checkHealth();
});

/**
 * Check chatbot health status
 */
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (!data.initialized) {
            addBotMessage('⚠️ Chatbot is not fully initialized. Please check the server configuration.');
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

/**
 * Send a message to the chatbot
 */
async function sendMessage() {
    const question = userInput.value.trim();
    
    if (!question) {
        return;
    }
    
    // Disable input and button
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message to chat
    addUserMessage(question);
    
    // Clear input
    userInput.value = '';
    
    // Show loading
    showLoading();
    
    try {
        if (isStreaming) {
            await sendStreamingMessage(question);
        } else {
            await sendRegularMessage(question);
        }
    } catch (error) {
        hideLoading();
        addBotMessage('❌ An error occurred while processing your request. Please try again.');
        console.error('Error:', error);
    } finally {
        // Re-enable input and button
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

/**
 * Send regular (non-streaming) message
 */
async function sendRegularMessage(question) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question: question,
            session_id: sessionId,
            use_hybrid: useHybrid,
            include_history: true
        })
    });
    
    const data = await response.json();
    hideLoading();
    
    if (data.success) {
        addBotMessage(data.answer, data.sources, data.response_time);
    } else {
        addBotMessage('❌ ' + data.answer);
    }
    
    // Update session ID if provided
    if (data.session_id) {
        sessionId = data.session_id;
    }
}

/**
 * Send streaming message
 */
async function sendStreamingMessage(question) {
    const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question: question,
            session_id: sessionId
        })
    });
    
    if (!response.ok) {
        throw new Error('Streaming failed');
    }
    
    hideLoading();
    
    // Create message element for streaming
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-icon">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <p class="streaming-content"></p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    currentStreamingMessage = messageDiv.querySelector('.streaming-content');
    
    // Read stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') {
                    continue;
                }
                
                try {
                    const json = JSON.parse(data);
                    if (json.chunk && currentStreamingMessage) {
                        currentStreamingMessage.textContent += json.chunk;
                        scrollToBottom();
                    }
                } catch (e) {
                    console.error('Error parsing stream data:', e);
                }
            }
        }
    }
    
    currentStreamingMessage = null;
    scrollToBottom();
}

/**
 * Add a user message to the chat
 */
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    messageDiv.innerHTML = `
        <div class="message-icon">
            <i class="fas fa-user"></i>
        </div>
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add a bot message to the chat
 */
function addBotMessage(message, sources = [], responseTime = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `
            <div class="sources">
                <div class="sources-title">📚 Sources:</div>
                ${sources.map((source, index) => `
                    <div class="source-item">
                        ${index + 1}. ${escapeHtml(source.content)}
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    let responseTimeHtml = '';
    if (responseTime) {
        responseTimeHtml = `<div class="response-time">⏱️ ${responseTime}s</div>`;
    }
    
    messageDiv.innerHTML = `
        <div class="message-icon">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
            ${sourcesHtml}
            ${responseTimeHtml}
            <div class="message-actions">
                <button class="btn-feedback" data-positive="true" onclick="submitFeedback(true)">
                    <i class="fas fa-thumbs-up"></i>
                </button>
                <button class="btn-feedback" data-positive="false" onclick="submitFeedback(false)">
                    <i class="fas fa-thumbs-down"></i>
                </button>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Submit feedback
 */
async function submitFeedback(positive) {
    try {
        await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ positive: positive })
        });
        
        // Show feedback confirmation
        const feedbackMsg = positive ? '👍 Thank you for your positive feedback!' : '👎 Thank you for your feedback!';
        showNotification(feedbackMsg);
    } catch (error) {
        console.error('Error submitting feedback:', error);
    }
}

/**
 * Clear chat
 */
async function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        try {
            await fetch(`/api/conversation/${sessionId}`, {
                method: 'DELETE'
            });
            
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <p>Chat cleared! How can I help you today?</p>
                    </div>
                </div>
            `;
            
            // Generate new session ID
            sessionId = 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    }
}

/**
 * Export chat
 */
async function exportChat() {
    try {
        const response = await fetch(`/api/conversation/${sessionId}/export`);
        const data = await response.json();
        
        // Create download
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat-export-${sessionId}-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('✅ Chat exported successfully!');
    } catch (error) {
        console.error('Error exporting chat:', error);
        showNotification('❌ Error exporting chat');
    }
}

/**
 * Handle file select
 */
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        showFilePreview(file);
    }
}

/**
 * Handle drag over
 */
function handleDragOver(e) {
    e.preventDefault();
    fileUploadArea.classList.add('drag-over');
}

/**
 * Handle file drop
 */
function handleFileDrop(e) {
    e.preventDefault();
    fileUploadArea.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files;
        showFilePreview(file);
    }
}

/**
 * Show file preview
 */
function showFilePreview(file) {
    const preview = document.getElementById('filePreview');
    const submitBtn = document.getElementById('uploadSubmitBtn');
    
    if (file.size > 16 * 1024 * 1024) {
        preview.innerHTML = '<p class="error">File size exceeds 16MB limit</p>';
        submitBtn.disabled = true;
        return;
    }
    
    preview.innerHTML = `
        <div class="file-preview-item">
            <i class="fas fa-file"></i>
            <span>${escapeHtml(file.name)}</span>
            <span class="file-size">(${(file.size / 1024).toFixed(2)} KB)</span>
        </div>
    `;
    submitBtn.disabled = false;
}

/**
 * Handle file upload
 */
async function handleFileUpload(e) {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    const submitBtn = document.getElementById('uploadSubmitBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`✅ ${data.message}`);
            uploadModal.style.display = 'none';
            fileInput.value = '';
            document.getElementById('filePreview').innerHTML = '';
        } else {
            showNotification(`❌ ${data.error || 'Upload failed'}`);
        }
    } catch (error) {
        showNotification('❌ Error uploading file');
        console.error('Upload error:', error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-upload"></i> Upload and Process';
    }
}

/**
 * Show analytics
 */
async function showAnalytics() {
    analyticsModal.style.display = 'block';
    
    try {
        const response = await fetch('/api/analytics?days=30');
        const data = await response.json();
        
        // Update stats
        document.getElementById('totalQueries').textContent = data.total_queries || 0;
        document.getElementById('totalSessions').textContent = data.total_sessions || 0;
        document.getElementById('avgResponseTime').textContent = (data.avg_response_time || 0) + 's';
        document.getElementById('feedbackScore').textContent = (data.feedback_score || 0) + '%';
        
        // Top queries
        const topQueriesDiv = document.getElementById('topQueries');
        if (data.top_queries && data.top_queries.length > 0) {
            topQueriesDiv.innerHTML = data.top_queries.map(q => `
                <div class="query-item">
                    <span class="query-text">${escapeHtml(q.query)}</span>
                    <span class="query-count">${q.count}</span>
                </div>
            `).join('');
        } else {
            topQueriesDiv.innerHTML = '<p>No queries yet</p>';
        }
        
        // Top sources
        const topSourcesDiv = document.getElementById('topSources');
        if (data.top_sources && data.top_sources.length > 0) {
            topSourcesDiv.innerHTML = data.top_sources.map(s => `
                <div class="source-item">
                    <span class="source-name">${escapeHtml(s.source)}</span>
                    <span class="source-count">${s.count}</span>
                </div>
            `).join('');
        } else {
            topSourcesDiv.innerHTML = '<p>No sources yet</p>';
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

/**
 * Show notification
 */
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Show loading overlay
 */
function showLoading() {
    loadingOverlay.classList.add('active');
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    loadingOverlay.classList.remove('active');
}
