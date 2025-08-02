const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const fileBtn = document.getElementById('fileBtn');
const fileInput = document.getElementById('fileInput');
const clearBtn = document.getElementById('clearBtn');

let isStreaming = false;
let uploadedFile = null;
let serviceReady = false;
let statusCheckInterval = null;

// Generate or retrieve session ID
function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 16) + '_' + Date.now();
}

// Get session ID from localStorage or generate new one
let sessionId = localStorage.getItem('chat_session_id');
if (!sessionId) {
    sessionId = generateSessionId();
    localStorage.setItem('chat_session_id', sessionId);
}

// Service status checker
async function checkServiceStatus() {
    try {
        const response = await fetch('/health', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (response.ok) {
            const health = await response.json();
            const agentReady = health.agent_service?.agent_initialized === true;
            
            if (agentReady && !serviceReady) {
                serviceReady = true;
                showServiceReadyMessage();
                clearInterval(statusCheckInterval);
                statusCheckInterval = null;
                
                // Enable UI controls
                sendBtn.disabled = false;
                fileBtn.disabled = false;
                clearBtn.disabled = false;
                messageInput.disabled = false;
                messageInput.placeholder = 'Type your message or upload a file...';
            } else if (!agentReady && serviceReady) {
                serviceReady = false;
                showServiceNotReadyMessage();
            }
            
            return agentReady;
        }
        return false;
    } catch (error) {
        console.log('Service check failed, retrying...', error.message);
        return false;
    }
}

// Show service ready message
function showServiceReadyMessage() {
    // Remove any existing status messages
    const existingStatus = document.querySelector('.service-status');
    if (existingStatus) {
        existingStatus.remove();
    }
    
    const statusDiv = document.createElement('div');
    statusDiv.className = 'message assistant service-status';
    statusDiv.innerHTML = '✅ <strong>Agent service is ready!</strong> You can now start chatting.';
    statusDiv.style.background = '#d4edda';
    statusDiv.style.color = '#155724';
    statusDiv.style.border = '1px solid #c3e6cb';
    messagesDiv.appendChild(statusDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    // Remove the message after 3 seconds
    setTimeout(() => {
        if (statusDiv.parentNode) {
            statusDiv.parentNode.removeChild(statusDiv);
        }
    }, 3000);
}

// Show service not ready message
function showServiceNotReadyMessage() {
    // Remove any existing status messages
    const existingStatus = document.querySelector('.service-status');
    if (existingStatus) {
        existingStatus.remove();
    }
    
    const statusDiv = document.createElement('div');
    statusDiv.className = 'message assistant service-status';
    statusDiv.innerHTML = '⏳ <strong>Agent service is starting up...</strong> Please wait while the AI agent initializes.';
    statusDiv.style.background = '#fff3cd';
    statusDiv.style.color = '#856404';
    statusDiv.style.border = '1px solid #ffeaa7';
    messagesDiv.appendChild(statusDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    // Disable UI controls while not ready
    sendBtn.disabled = true;
    fileBtn.disabled = true;
    clearBtn.disabled = true;
    messageInput.disabled = true;
    messageInput.placeholder = 'Please wait - agent service is starting up...';
}

// Start service status monitoring
function startServiceMonitoring() {
    // Initial check
    checkServiceStatus().then(ready => {
        if (!ready) {
            showServiceNotReadyMessage();
            // Start polling every 2 seconds
            statusCheckInterval = setInterval(checkServiceStatus, 2000);
        } else {
            serviceReady = true;
            sendBtn.disabled = false;
            fileBtn.disabled = false;
            clearBtn.disabled = false;
            messageInput.disabled = false;
        }
    });
}

// Add message to chat
function addMessage(content, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return messageDiv;
}

// Add typing indicator
function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant typing-indicator';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="typing-animation">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
        <span class="typing-text">AI is thinking...</span>
    `;
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return typingDiv;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Add file info display
function addFileInfo(fileName, fileSize) {
    const fileInfoDiv = document.createElement('div');
    fileInfoDiv.className = 'file-info';
    fileInfoDiv.innerHTML = `
        📄 <span class="file-name">${fileName}</span>
        <span class="file-size">(${formatFileSize(fileSize)})</span>
    `;
    messagesDiv.appendChild(fileInfoDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return fileInfoDiv;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Show centered confirmation dialog
function showCenteredConfirmDialog(title, message) {
    return new Promise((resolve) => {
        // Create modal overlay
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        `;
        
        // Create modal dialog
        const dialog = document.createElement('div');
        dialog.style.cssText = `
            background: white;
            border-radius: 8px;
            padding: 24px;
            max-width: 400px;
            width: 90%;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            text-align: center;
        `;
        
        // Create title
        const titleElement = document.createElement('h3');
        titleElement.textContent = title;
        titleElement.style.cssText = `
            margin: 0 0 16px 0;
            color: #333;
            font-size: 18px;
            font-weight: 600;
        `;
        
        // Create message
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        messageElement.style.cssText = `
            margin: 0 0 24px 0;
            color: #666;
            line-height: 1.5;
        `;
        
        // Create button container
        const buttonContainer = document.createElement('div');
        buttonContainer.style.cssText = `
            display: flex;
            gap: 12px;
            justify-content: center;
        `;
        
        // Create cancel button
        const cancelButton = document.createElement('button');
        cancelButton.textContent = 'Cancel';
        cancelButton.style.cssText = `
            padding: 10px 20px;
            border: 1px solid #ddd;
            background: white;
            color: #333;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            min-width: 80px;
        `;
        
        // Create confirm button
        const confirmButton = document.createElement('button');
        confirmButton.textContent = 'Clear';
        confirmButton.style.cssText = `
            padding: 10px 20px;
            border: none;
            background: #dc3545;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            min-width: 80px;
        `;
        
        // Add hover effects
        cancelButton.addEventListener('mouseenter', () => {
            cancelButton.style.backgroundColor = '#f8f9fa';
        });
        cancelButton.addEventListener('mouseleave', () => {
            cancelButton.style.backgroundColor = 'white';
        });
        
        confirmButton.addEventListener('mouseenter', () => {
            confirmButton.style.backgroundColor = '#c82333';
        });
        confirmButton.addEventListener('mouseleave', () => {
            confirmButton.style.backgroundColor = '#dc3545';
        });
        
        // Add event listeners
        cancelButton.addEventListener('click', () => {
            document.body.removeChild(overlay);
            resolve(false);
        });
        
        confirmButton.addEventListener('click', () => {
            document.body.removeChild(overlay);
            resolve(true);
        });
        
        // Close on overlay click
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                document.body.removeChild(overlay);
                resolve(false);
            }
        });
        
        // Close on Escape key
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                document.removeEventListener('keydown', handleKeyDown);
                document.body.removeChild(overlay);
                resolve(false);
            }
        };
        document.addEventListener('keydown', handleKeyDown);
        
        // Assemble dialog
        buttonContainer.appendChild(cancelButton);
        buttonContainer.appendChild(confirmButton);
        dialog.appendChild(titleElement);
        dialog.appendChild(messageElement);
        dialog.appendChild(buttonContainer);
        overlay.appendChild(dialog);
        
        // Add to page
        document.body.appendChild(overlay);
        
        // Focus the confirm button
        confirmButton.focus();
    });
}

// Handle file selection
function handleFileSelection() {
    const file = fileInput.files[0];
    if (!file) return;
    
    // Check file size (limit to 10MB)
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        fileInput.value = '';
        return;
    }
    
    uploadedFile = file;
    addFileInfo(file.name, file.size);
    messageInput.placeholder = `File selected: ${file.name}. Type a message or press Send to analyze the file.`;
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    
    // Check if service is ready
    if (!serviceReady) {
        addMessage('⚠️ Please wait - the agent service is still starting up. Try again in a moment.', false);
        return;
    }
    
    // Check if we have a message or a file
    if ((!message && !uploadedFile) || isStreaming) return;
    
    // Disable input
    isStreaming = true;
    sendBtn.disabled = true;
    fileBtn.disabled = true;
    clearBtn.disabled = true;
    
    // Update send button to show processing state
    const originalSendText = sendBtn.textContent;
    sendBtn.textContent = 'Sending...';
    
    try {
        let finalMessage = message;
        
        // Handle file upload
        if (uploadedFile) {
            // Add user message showing file upload
            const fileMessage = message ? 
                `${message}\n\n📄 Uploaded file: ${uploadedFile.name}` : 
                `📄 Analyze this file: ${uploadedFile.name}`;
            addMessage(fileMessage, true);
            
            // Upload file first
            const formData = new FormData();
            formData.append('file', uploadedFile);
            if (message) formData.append('message', message);
            
            const uploadResponse = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!uploadResponse.ok) {
                throw new Error('File upload failed');
            }
            
            const uploadResult = await uploadResponse.json();
            finalMessage = uploadResult.content || 'Please analyze this file.';
            
            // Clear file after upload
            uploadedFile = null;
            fileInput.value = '';
            messageInput.placeholder = 'Type your message or upload a file...';
        } else {
            // Regular text message
            addMessage(message, true);
        }
        
        messageInput.value = '';
        
        // Show typing indicator while waiting for response
        sendBtn.textContent = 'Waiting';
        const typingIndicator = addTypingIndicator();
        
        // Use EventSource for Server-Sent Events
        const eventSource = new EventSource('/chat/stream?' + new URLSearchParams({
            message: finalMessage,
            session_id: sessionId
        }));
        
        let assistantMessage = '';
        let renderTimeout = null;
        let lastRenderLength = 0;
        let lastRenderTime = 0;
        let assistantDiv = null;
        
        // Function to render markdown progressively
        function renderProgressiveMarkdown() {
            const now = Date.now();
            
            // Skip if we rendered very recently and content hasn't changed much
            if (now - lastRenderTime < 10 && assistantMessage.length - lastRenderLength < 3) {
                return;
            }
            
            try {
                // Parse the current markdown content
                const renderedContent = marked.parse(assistantMessage);
                assistantDiv.innerHTML = renderedContent + '<span class="cursor">▌</span>';
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                lastRenderLength = assistantMessage.length;
                lastRenderTime = now;
            } catch (e) {
                // If markdown parsing fails (incomplete structure), try partial rendering
                try {
                    // Attempt to render what we can by adding temporary closing tags for incomplete structures
                    let tempContent = assistantMessage;
                    
                    // Count unclosed code blocks and try to close them temporarily
                    const codeBlockMatches = tempContent.match(/```/g);
                    if (codeBlockMatches && codeBlockMatches.length % 2 === 1) {
                        tempContent += '\n```';
                    }
                    
                    // Count unclosed inline code and try to close them
                    const inlineCodeMatches = tempContent.match(/(?<!\\)`/g);
                    if (inlineCodeMatches && inlineCodeMatches.length % 2 === 1) {
                        tempContent += '`';
                    }
                    
                    const renderedContent = marked.parse(tempContent);
                    assistantDiv.innerHTML = renderedContent + '<span class="cursor">▌</span>';
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    lastRenderLength = assistantMessage.length;
                    lastRenderTime = now;
                } catch (e2) {
                    // If all else fails, show raw text with cursor
                    assistantDiv.innerHTML = assistantMessage.replace(/\n/g, '<br>') + '<span class="cursor">▌</span>';
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    lastRenderLength = assistantMessage.length;
                    lastRenderTime = now;
                }
            }
        }
        
        // Optimized render scheduling
        function scheduleRender() {
            if (renderTimeout) {
                clearTimeout(renderTimeout);
            }
            
            // Immediate render for significant content changes, word boundaries, or start of content
            const contentDelta = assistantMessage.length - lastRenderLength;
            const isWordBoundary = assistantMessage.endsWith(' ') || assistantMessage.endsWith('\n');
            
            if (contentDelta > 10 || assistantMessage.length < 20 || isWordBoundary) {
                renderProgressiveMarkdown();
                return;
            }
            
            // Use requestAnimationFrame for smooth rendering
            renderTimeout = setTimeout(() => {
                requestAnimationFrame(renderProgressiveMarkdown);
            }, 8);
        }
        
        eventSource.onmessage = function(event) {
            if (event.data === '[DONE]') {
                // Clear any pending render timeout
                if (renderTimeout) {
                    clearTimeout(renderTimeout);
                    renderTimeout = null;
                }
                // Render final markdown without cursor
                if (assistantDiv) {
                    assistantDiv.innerHTML = marked.parse(assistantMessage);
                }
                eventSource.close();
                // Re-enable input
                isStreaming = false;
                sendBtn.disabled = false;
                fileBtn.disabled = false;
                clearBtn.disabled = false;
                sendBtn.textContent = originalSendText;
                messageInput.focus();
                return;
            }
            
            try {
                const parsed = JSON.parse(event.data);
                if (parsed.content) {
                    // First content received - replace typing indicator with assistant div
                    if (!assistantDiv) {
                        removeTypingIndicator();
                        assistantDiv = document.createElement('div');
                        assistantDiv.className = 'message assistant';
                        messagesDiv.appendChild(assistantDiv);
                        sendBtn.textContent = 'Receiving...';
                    }
                    
                    // Handle regular text content (backward compatibility)
                    assistantMessage += parsed.content;
                    // Schedule progressive markdown rendering
                    scheduleRender();
                } else if (parsed.type === 'text' && parsed.content) {
                    // First content received - replace typing indicator with assistant div
                    if (!assistantDiv) {
                        removeTypingIndicator();
                        assistantDiv = document.createElement('div');
                        assistantDiv.className = 'message assistant';
                        messagesDiv.appendChild(assistantDiv);
                        sendBtn.textContent = 'Receiving...';
                    }
                    
                    // Handle new text format
                    assistantMessage += parsed.content;
                    // Schedule progressive markdown rendering
                    scheduleRender();
                } else if (parsed.file || (parsed.type === 'file' && parsed.file_info)) {
                    // Handle file (image) display
                    const fileInfo = parsed.file || parsed.file_info;
                    console.log('Received file info:', fileInfo); // Debug log
                    if (fileInfo.is_image) {
                        // Add image to the chat
                        const imageDiv = document.createElement('div');
                        imageDiv.className = 'image-container';
                        imageDiv.innerHTML = `
                            <img src="${fileInfo.relative_path}" 
                                 alt="${fileInfo.attachment_name}" 
                                 class="generated-image"
                                 loading="lazy" 
                                 onerror="console.error('Image failed to load:', '${fileInfo.relative_path}')" />
                            <p class="image-caption">${fileInfo.attachment_name}</p>
                        `;
                        messagesDiv.appendChild(imageDiv);
                        messagesDiv.scrollTop = messagesDiv.scrollHeight;
                        console.log('Added image with src:', fileInfo.relative_path); // Debug log
                    } else {
                        // Handle non-image files
                        assistantMessage += `\n\n📎 Generated file: [${fileInfo.file_name}](${fileInfo.relative_path})\n`;
                        assistantDiv.innerHTML = assistantMessage + '<span class="cursor">▌</span>';
                        messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    }
                } else if (parsed.error) {
                    // Clear any pending render timeout
                    if (renderTimeout) {
                        clearTimeout(renderTimeout);
                        renderTimeout = null;
                    }
                    
                    // Remove typing indicator if still present and create error div
                    if (!assistantDiv) {
                        removeTypingIndicator();
                        assistantDiv = document.createElement('div');
                        assistantDiv.className = 'message assistant';
                        messagesDiv.appendChild(assistantDiv);
                    }
                    
                    assistantDiv.textContent = `Error: ${parsed.error}`;
                    assistantDiv.style.color = '#dc3545';
                    eventSource.close();
                    isStreaming = false;
                    sendBtn.disabled = false;
                    fileBtn.disabled = false;
                    clearBtn.disabled = false;
                    sendBtn.textContent = originalSendText;
                    messageInput.focus();
                }
            } catch (e) {
                console.error('JSON parse error:', e);
            }
        };
        
        eventSource.onerror = function(event) {
            console.error('EventSource failed:', event);
            // Clear any pending render timeout
            if (renderTimeout) {
                clearTimeout(renderTimeout);
                renderTimeout = null;
            }
            
            // Remove typing indicator if still present and create error div
            if (!assistantDiv) {
                removeTypingIndicator();
                assistantDiv = document.createElement('div');
                assistantDiv.className = 'message assistant';
                messagesDiv.appendChild(assistantDiv);
            }
            
            assistantDiv.textContent = 'Connection error';
            assistantDiv.style.color = '#dc3545';
            eventSource.close();
            isStreaming = false;
            sendBtn.disabled = false;
            fileBtn.disabled = false;
            clearBtn.disabled = false;
            sendBtn.textContent = originalSendText;
            messageInput.focus();
        };
        
    } catch (error) {
        // Handle upload or streaming errors
        removeTypingIndicator();
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message assistant';
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.style.color = '#dc3545';
        messagesDiv.appendChild(errorDiv);
        
        isStreaming = false;
        sendBtn.disabled = false;
        fileBtn.disabled = false;
        clearBtn.disabled = false;
        sendBtn.textContent = originalSendText;
        messageInput.focus();
    }
}

// Clear chat function
async function clearChat() {
    if (!serviceReady) {
        alert('Please wait - the agent service is still starting up.');
        return;
    }
    
    if (isStreaming) {
        alert('Please wait for the current response to finish before clearing chat.');
        return;
    }
    
    // Show custom centered confirmation dialog
    const shouldClear = await showCenteredConfirmDialog(
        'Clear Chat History',
        'Are you sure you want to clear the chat history? This action cannot be undone.'
    );
    
    if (!shouldClear) {
        return;
    }
    
    try {
        // Disable the clear button
        clearBtn.disabled = true;
        clearBtn.textContent = 'Clearing...';
        
        // Call the clear endpoint with session ID
        const response = await fetch('/chat/clear?' + new URLSearchParams({
            session_id: sessionId
        }), {
            method: 'DELETE',
        });
        
        if (!response.ok) {
            throw new Error(`Failed to clear chat: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Clear the messages display
        messagesDiv.innerHTML = '';
        
        // Generate new session ID for fresh start
        sessionId = generateSessionId();
        localStorage.setItem('chat_session_id', sessionId);
        
        // Clear any uploaded file state
        uploadedFile = null;
        fileInput.value = '';
        messageInput.placeholder = 'Type your message or upload a file...';
        
        // Show success message briefly
        const successDiv = document.createElement('div');
        successDiv.className = 'message assistant';
        successDiv.textContent = '✅ Chat cleared successfully. You can start a new conversation.';
        successDiv.style.background = '#d4edda';
        successDiv.style.color = '#155724';
        successDiv.style.border = '1px solid #c3e6cb';
        messagesDiv.appendChild(successDiv);
        
        // Remove success message after 3 seconds
        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.parentNode.removeChild(successDiv);
            }
        }, 3000);
        
        console.log('Chat cleared:', result);
        
    } catch (error) {
        console.error('Error clearing chat:', error);
        
        // Show error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message assistant';
        errorDiv.textContent = `❌ Failed to clear chat: ${error.message}`;
        errorDiv.style.color = '#dc3545';
        messagesDiv.appendChild(errorDiv);
        
    } finally {
        // Re-enable the clear button
        clearBtn.disabled = false;
        clearBtn.textContent = 'Clear';
        messageInput.focus();
    }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// File upload event listeners
fileBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', handleFileSelection);

// Clear chat event listener
clearBtn.addEventListener('click', clearChat);

// Clear chat on page refresh/unload to clean up agent thread
window.addEventListener('beforeunload', (e) => {
    // Use fetch with keepalive for DELETE request during page unload
    try {
        fetch('/chat/clear', {
            method: 'DELETE',
            keepalive: true
        }).catch(() => {
            // Ignore errors during page unload
        });
    } catch (error) {
        console.log('Failed to clear chat on page unload:', error);
    }
});

// Start service monitoring on page load
startServiceMonitoring();

// Focus input on load
messageInput.focus();
