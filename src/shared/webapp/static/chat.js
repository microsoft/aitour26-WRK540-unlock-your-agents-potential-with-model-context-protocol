const messagesDiv = document.getElementById("messages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const fileBtn = document.getElementById("fileBtn");
const fileInput = document.getElementById("fileInput");
const clearBtn = document.getElementById("clearBtn");
const settingsBtn = document.getElementById("settingsBtn");
const settingsModal = document.getElementById("settingsModal");
const closeModal = document.querySelector(".close");
const rlsUserSelect = document.getElementById("rlsUserSelect");
const saveRlsUserBtn = document.getElementById("saveRlsUser");
const rlsUserStatus = document.getElementById("rlsUserStatus");
const currentUserDiv = document.getElementById("currentUser");

const chatState = {
  isStreaming: false,
  uploadedFile: null,
  serviceReady: false,
  sessionId: null,
  currentRlsUserId: null,
};

// Generate or retrieve session ID
function generateSessionId() {
  return (
    "session_" + Math.random().toString(36).substr(2, 16) + "_" + Date.now()
  );
}

// Get session ID from localStorage or generate new one
chatState.sessionId = localStorage.getItem("chat_session_id");
if (!chatState.sessionId) {
  chatState.sessionId = generateSessionId();
  localStorage.setItem("chat_session_id", chatState.sessionId);
}

// Service status checker
async function checkServiceStatus() {
  try {
    const response = await fetch("/health", {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (response.ok) {
      chatState.serviceReady = true;
      showServiceReadyMessage();
      // Enable UI controls
      sendBtn.disabled = false;
      fileBtn.disabled = false;
      clearBtn.disabled = false;
      messageInput.disabled = false;
      messageInput.placeholder =
        "Type your message or type help for some suggestions....";
      // Update current user display
      await updateCurrentUserDisplay();
    } else {
      if (chatState.serviceReady) {
        chatState.serviceReady = false;
        showServiceNotReadyMessage();
      }
      setTimeout(checkServiceStatus, 2000);
    }
  } catch (error) {
    showServiceNotReadyMessage();
    setTimeout(checkServiceStatus, 2000);
  }
}

// Show service status message
function showServiceStatusMessage(message, type) {
  // Remove any existing status messages
  const existingStatus = document.querySelector(".service-status");
  if (existingStatus) {
    existingStatus.remove();
  }

  const statusDiv = document.createElement("div");
  statusDiv.className = "message assistant service-status";
  statusDiv.innerHTML = message;

  if (type === "ready") {
    statusDiv.style.background = "#d4edda";
    statusDiv.style.color = "#155724";
    statusDiv.style.border = "1px solid #c3e6cb";
  } else if (type === "not-ready") {
    statusDiv.style.background = "#fff3cd";
    statusDiv.style.color = "#856404";
    statusDiv.style.border = "1px solid #ffeaa7";
  }

  messagesDiv.appendChild(statusDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  if (type === "ready") {
    // Remove the message after 3 seconds
    setTimeout(() => {
      if (statusDiv.parentNode) {
        statusDiv.parentNode.removeChild(statusDiv);
      }
    }, 3000);
  }
}

// Show service ready message
function showServiceReadyMessage() {
  showServiceStatusMessage(
    "✅ <strong>Agent service is ready!</strong> You can now start chatting.",
    "ready"
  );
}

// Show service not ready message
function showServiceNotReadyMessage() {
  showServiceStatusMessage(
    "⏳ <strong>Agent service is starting up...</strong> Please wait while the AI agent initializes.",
    "not-ready"
  );

  // Disable UI controls while not ready
  sendBtn.disabled = true;
  fileBtn.disabled = true;
  clearBtn.disabled = true;
  messageInput.disabled = true;
  messageInput.placeholder = "Please wait - agent service is starting up...";
}
async function getCurrentRlsUserId() {
  // Check if we have it cached first
  if (chatState.currentRlsUserId) {
    return chatState.currentRlsUserId;
  }

  // Try to load from localStorage
  const savedRlsUserId = localStorage.getItem("current_rls_user_id");
  if (savedRlsUserId) {
    chatState.currentRlsUserId = savedRlsUserId;
    return savedRlsUserId;
  }

  // Try to get from select dropdown if settings are open
  if (rlsUserSelect && rlsUserSelect.value) {
    chatState.currentRlsUserId = rlsUserSelect.value;
    // Save to localStorage
    localStorage.setItem("current_rls_user_id", rlsUserSelect.value);
    return rlsUserSelect.value;
  }

  // Final fallback to default Head Office user
  const defaultUserId = "00000000-0000-0000-0000-000000000000";
  chatState.currentRlsUserId = defaultUserId;
  // Save default to localStorage
  localStorage.setItem("current_rls_user_id", defaultUserId);
  return defaultUserId;
}

// Start service status monitoring
async function startServiceMonitoring() {
  showServiceNotReadyMessage();
  await checkServiceStatus();
  await getCurrentRlsUserId();

  if (chatState.serviceReady) {
    await updateCurrentUserDisplay();
  }
}

// Add message to chat
function addMessage(content, isUser) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user" : "assistant"}`;

  // Use innerHTML to properly render newlines and other HTML content
  messageDiv.innerHTML = content.replace(/\n/g, "<br>");

  messagesDiv.appendChild(messageDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
  return messageDiv;
}

// Add typing indicator
function addTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.className = "message assistant typing-indicator";
  typingDiv.id = "typing-indicator";
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
  const typingIndicator = document.getElementById("typing-indicator");
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Add file info display
function addFileInfo(fileName, fileSize) {
  const fileInfoDiv = document.createElement("div");
  fileInfoDiv.className = "file-info";
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
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

// Show centered confirmation dialog
function showCenteredConfirmDialog(title, message) {
  return new Promise((resolve) => {
    // Create modal overlay
    const overlay = document.createElement("div");
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
    const dialog = document.createElement("div");
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
    const titleElement = document.createElement("h3");
    titleElement.textContent = title;
    titleElement.style.cssText = `
            margin: 0 0 16px 0;
            color: #333;
            font-size: 18px;
            font-weight: 600;
        `;

    // Create message
    const messageElement = document.createElement("p");
    messageElement.textContent = message;
    messageElement.style.cssText = `
            margin: 0 0 24px 0;
            color: #666;
            line-height: 1.5;
        `;

    // Create button container
    const buttonContainer = document.createElement("div");
    buttonContainer.style.cssText = `
            display: flex;
            gap: 12px;
            justify-content: center;
        `;

    // Create cancel button
    const cancelButton = document.createElement("button");
    cancelButton.textContent = "Cancel";
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
    const confirmButton = document.createElement("button");
    confirmButton.textContent = "Clear";
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
    cancelButton.addEventListener("mouseenter", () => {
      cancelButton.style.backgroundColor = "#f8f9fa";
    });
    cancelButton.addEventListener("mouseleave", () => {
      cancelButton.style.backgroundColor = "white";
    });

    confirmButton.addEventListener("mouseenter", () => {
      confirmButton.style.backgroundColor = "#c82333";
    });
    confirmButton.addEventListener("mouseleave", () => {
      confirmButton.style.backgroundColor = "#dc3545";
    });

    // Add event listeners
    cancelButton.addEventListener("click", () => {
      document.body.removeChild(overlay);
      resolve(false);
    });

    confirmButton.addEventListener("click", () => {
      document.body.removeChild(overlay);
      resolve(true);
    });

    // Close on overlay click
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        document.body.removeChild(overlay);
        resolve(false);
      }
    });

    // Close on Escape key
    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        document.removeEventListener("keydown", handleKeyDown);
        document.body.removeChild(overlay);
        resolve(false);
      }
    };
    document.addEventListener("keydown", handleKeyDown);

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
    alert("File size must be less than 10MB");
    fileInput.value = "";
    return;
  }

  chatState.uploadedFile = file;
  addFileInfo(file.name, file.size);
  messageInput.placeholder = `File selected: ${file.name}. Type a message or press Send to analyze the file.`;
}

// Send message with retry logic
async function sendMessage() {
  const message = messageInput.value.trim();
  const maxRetries = 15; // 30 seconds / 2 seconds per retry
  const retryDelay = 2000; // 2 seconds
  let attempt = 0;

  // Check if we have a message or a file
  if ((!message && !chatState.uploadedFile) || chatState.isStreaming) return;

  // Get current RLS user ID
  const rlsUserId = await getCurrentRlsUserId();
  if (!rlsUserId) {
    addMessage(
      "❌ Error: No RLS user selected. Please select a user in settings.",
      false
    );
    return;
  }

  // Disable input
  chatState.isStreaming = true;
  sendBtn.disabled = true;
  fileBtn.disabled = true;
  clearBtn.disabled = true;

  // Update send button to show processing state
  const originalSendText = sendBtn.textContent;
  sendBtn.textContent = "Sent";

  // Add user message to chat
  let userMessageDiv;
  if (chatState.uploadedFile) {
    const fileMessage = message
      ? `${message}\n\n📄 Uploaded file: ${chatState.uploadedFile.name}`
      : `📄 Analyze this file: ${chatState.uploadedFile.name}`;
    userMessageDiv = addMessage(fileMessage, true);
  } else {
    userMessageDiv = addMessage(message, true);
  }

  // Show typing indicator
  const typingIndicator = addTypingIndicator();

  while (attempt < maxRetries) {
    try {
      // Check service status before each attempt
      if (!chatState.serviceReady) {
        if (attempt === 0) {
          // Update UI to show connecting status on first attempt
          sendBtn.textContent = "Connecting...";
        }
        await checkServiceStatus();
        attempt++;
        continue;
      }

      // Service is ready, proceed with sending
      sendBtn.textContent = "Sent";

      let finalMessage = message;

      // Handle file upload
      if (chatState.uploadedFile) {
        const formData = new FormData();
        formData.append("file", chatState.uploadedFile);
        if (message) formData.append("message", message);

        const uploadResponse = await fetch("/upload", {
          method: "POST",
          body: formData,
        });

        if (!uploadResponse.ok) {
          const errorData = await uploadResponse.json().catch(() => ({
            detail: "File upload failed with status " + uploadResponse.status,
          }));
          throw new Error(errorData.detail || "File upload failed");
        }

        const uploadResult = await uploadResponse.json();
        finalMessage = uploadResult.content || "Please analyze this file.";

        // Clear file after upload
        chatState.uploadedFile = null;
        fileInput.value = "";
        messageInput.placeholder =
          "Type your message or type help for some suggestions....";
      }

      messageInput.value = "";

      // Use EventSource for Server-Sent Events
      await handleStreamingResponse(
        finalMessage,
        originalSendText,
        typingIndicator,
        rlsUserId
      );

      // Success, exit loop
      return;
    } catch (error) {
      console.log(`Attempt ${attempt + 1} failed:`, error.message);

      // Check for specific, non-retriable errors
      if (error.message.includes("File upload failed")) {
        handleSendError(
          error,
          originalSendText,
          typingIndicator,
          userMessageDiv
        );
        return;
      }

      attempt++;
      if (attempt >= maxRetries) {
        // All retries failed, show final error
        const finalError = new Error(
          "Connection error: The agent service is not responding after multiple attempts."
        );
        handleSendError(
          finalError,
          originalSendText,
          typingIndicator,
          userMessageDiv
        );
        return;
      }

      // Wait before retrying
      await new Promise((resolve) => setTimeout(resolve, retryDelay));
    }
  }
}

// Handle streaming response with optimized rendering
function handleStreamingResponse(
  message,
  originalSendText,
  typingIndicator,
  rlsUserId
) {
  return new Promise((resolve, reject) => {
    const eventSource = new EventSource(
      "/chat/stream?" +
        new URLSearchParams({
          message: message,
          session_id: chatState.sessionId,
          rls_user_id: rlsUserId,
        })
    );

    let assistantMessage = "";
    let renderTimeout = null;
    let assistantDiv = null;

    // Helper to create the assistant message div once
    const createAssistantDiv = () => {
      if (!assistantDiv) {
        removeTypingIndicator();
        assistantDiv = document.createElement("div");
        assistantDiv.className = "message assistant";
        messagesDiv.appendChild(assistantDiv);
        sendBtn.textContent = "Receiving...";
      }
    };

    // Renders markdown content, with fallbacks for incomplete streams
    const renderMarkdown = (final = false) => {
      if (!assistantDiv) return;

      try {
        // A simple heuristic to close unclosed code blocks for progressive rendering
        const contentToRender = final
          ? assistantMessage
          : assistantMessage + "\n```\n";
        // Clean up any empty code blocks that might have been added
        const cleanedContent = contentToRender.replace(/```\n```/g, "```");
        const renderedContent = marked.parse(cleanedContent);
        assistantDiv.innerHTML =
          renderedContent + (final ? "" : '<span class="cursor">▌</span>');
      } catch (e) {
        // Fallback to safer rendering if markdown parsing fails
        assistantDiv.textContent = assistantMessage;
        if (!final) {
          assistantDiv.innerHTML += '<span class="cursor">▌</span>';
        }
      }
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    // Schedules a throttled render to avoid excessive updates
    const scheduleRender = () => {
      if (renderTimeout) return; // A render is already scheduled
      renderTimeout = setTimeout(() => {
        requestAnimationFrame(() => {
          renderMarkdown();
          renderTimeout = null;
        });
      }, 50); // Throttle rendering to a reasonable rate
    };

    eventSource.onmessage = function (event) {
      if (event.data === "[DONE]") {
        if (renderTimeout) {
          clearTimeout(renderTimeout);
          renderTimeout = null;
        }
        renderMarkdown(true); // Final render without cursor
        eventSource.close();
        chatState.isStreaming = false;
        sendBtn.disabled = false;
        fileBtn.disabled = false;
        clearBtn.disabled = false;
        sendBtn.textContent = originalSendText;
        messageInput.focus();
        resolve();
        return;
      }

      try {
        const parsed = JSON.parse(event.data);

        // Unified text handling for both old and new formats
        const textContent = parsed.content;
        if (typeof textContent === "string") {
          createAssistantDiv();
          assistantMessage += textContent;
          scheduleRender();
        }

        // File handling
        const fileInfo =
          parsed.file || (parsed.type === "file" && parsed.file_info);
        if (fileInfo) {
          if (fileInfo.is_image) {
            const imageDiv = document.createElement("div");
            imageDiv.className = "image-container";
            imageDiv.innerHTML = `
                            <img src="${fileInfo.relative_path}" 
                                 alt="${fileInfo.attachment_name}" 
                                 class="generated-image"
                                 loading="lazy" 
                                 onerror="console.error('Image failed to load:', '${fileInfo.relative_path}')" />
                            <p class="image-caption">${fileInfo.attachment_name}</p>
                        `;
            // Insert image right above the assistant message div if it exists
            messagesDiv.appendChild(imageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
          } else {
            createAssistantDiv();
            assistantMessage += `\n\n📎 Generated file: [${fileInfo.file_name}](${fileInfo.relative_path})\n`;
            scheduleRender();
          }
        }

        // Error handling
        if (parsed.error) {
          if (renderTimeout) clearTimeout(renderTimeout);
          createAssistantDiv();
          assistantDiv.textContent = `Error: ${parsed.error}`;
          assistantDiv.style.color = "#dc3545";
          eventSource.close();
          chatState.isStreaming = false;
          sendBtn.disabled = false;
          fileBtn.disabled = false;
          clearBtn.disabled = false;
          sendBtn.textContent = originalSendText;
          messageInput.focus();
          reject(new Error(parsed.error));
        }
      } catch (e) {
        console.error("Stream processing error:", e);
        // Don't reject promise here for a single bad message.
        // The onerror handler will catch a total connection failure.
      }
    };

    eventSource.onerror = function (event) {
      console.error("EventSource failed:", event);
      eventSource.close();
      reject(new Error("Connection to the server was lost."));
    };
  });
}

// Handle send error
function handleSendError(
  error,
  originalSendText,
  typingIndicator,
  userMessageDiv
) {
  // Remove typing indicator
  if (typingIndicator) removeTypingIndicator();

  // Remove the optimistic user message
  if (userMessageDiv) userMessageDiv.remove();

  // Add a single error message
  const errorDiv = document.createElement("div");
  errorDiv.className = "message assistant";
  errorDiv.textContent = `Error: ${error.message}`;
  errorDiv.style.color = "#dc3545";
  messagesDiv.appendChild(errorDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  // Re-enable UI
  chatState.isStreaming = false;
  sendBtn.disabled = false;
  fileBtn.disabled = false;
  clearBtn.disabled = false;
  sendBtn.textContent = originalSendText;
  messageInput.focus();
}

// Clear chat function
async function clearChat() {
  if (!chatState.serviceReady) {
    alert("Please wait - the agent service is still starting up.");
    return;
  }

  if (chatState.isStreaming) {
    alert(
      "Please wait for the current response to finish before clearing chat."
    );
    return;
  }

  // Show custom centered confirmation dialog
  const shouldClear = await showCenteredConfirmDialog(
    "Clear Chat History",
    "Are you sure you want to clear the chat history? This action cannot be undone."
  );

  if (!shouldClear) {
    return;
  }

  try {
    // Disable the clear button
    clearBtn.disabled = true;
    clearBtn.textContent = "Clearing...";

    // Get current RLS user ID
    const rlsUserId = await getCurrentRlsUserId();

    // Call the clear endpoint with session ID and RLS user ID
    const response = await fetch("/chat/clear", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: "", // Required field in ChatRequest but not used for clear
        session_id: chatState.sessionId,
        rls_user_id: rlsUserId,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to clear chat: ${response.status}`);
    }

    const result = await response.json();

    // Clear the messages display
    messagesDiv.innerHTML = "";

    // Generate new session ID for fresh start
    chatState.sessionId = generateSessionId();
    localStorage.setItem("chat_session_id", chatState.sessionId);

    // Clear any uploaded file state
    chatState.uploadedFile = null;
    fileInput.value = "";
    messageInput.placeholder =
      "Type your message or type help for some suggestions....";

    // Show success message briefly
    const successDiv = document.createElement("div");
    successDiv.className = "message assistant";
    successDiv.textContent =
      "✅ Chat cleared successfully. You can start a new conversation.";
    successDiv.style.background = "#d4edda";
    successDiv.style.color = "#155724";
    successDiv.style.border = "1px solid #c3e6cb";
    messagesDiv.appendChild(successDiv);

    // Remove success message after 3 seconds
    setTimeout(() => {
      if (successDiv.parentNode) {
        successDiv.parentNode.removeChild(successDiv);
      }
    }, 3000);

    console.log("Chat cleared:", result);
  } catch (error) {
    console.error("Error clearing chat:", error);

    // Show error message
    const errorDiv = document.createElement("div");
    errorDiv.className = "message assistant";
    errorDiv.textContent = `❌ Failed to clear chat: ${error.message}`;
    errorDiv.style.color = "#dc3545";
    messagesDiv.appendChild(errorDiv);
  } finally {
    // Re-enable the clear button
    clearBtn.disabled = false;
    clearBtn.textContent = "Clear";
    messageInput.focus();
  }
}

// Event listeners
sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// File upload event listeners
fileBtn.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", handleFileSelection);

// Clear chat event listener
clearBtn.addEventListener("click", clearChat);

// Settings modal event listeners
settingsBtn.addEventListener("click", openSettings);
closeModal.addEventListener("click", closeSettings);
saveRlsUserBtn.addEventListener("click", saveRlsUser);

// Close modal when clicking outside of it
window.addEventListener("click", (event) => {
  if (event.target === settingsModal) {
    closeSettings();
  }
});

// Keyboard shortcuts
document.addEventListener("keydown", (event) => {
  // Escape key to close modal
  if (event.key === "Escape" && settingsModal.style.display === "block") {
    closeSettings();
    event.preventDefault();
  }

  // Ctrl/Cmd + , to open settings
  if ((event.ctrlKey || event.metaKey) && event.key === ",") {
    openSettings();
    event.preventDefault();
  }
});

// Settings functionality
async function openSettings() {
  if (!chatState.serviceReady) {
    alert("Please wait - the agent service is still starting up.");
    return;
  }

  if (chatState.isStreaming) {
    alert(
      "Please wait for the current response to finish before accessing settings."
    );
    return;
  }

  settingsModal.style.display = "block";
  await loadRlsUsers();
  await loadCurrentRlsUser();
}

function closeSettings() {
  settingsModal.style.display = "none";
  hideStatusMessage();
}

async function loadRlsUsers() {
  try {
    const response = await fetch("/agent/rls-users");
    const data = await response.json();

    rlsUserSelect.innerHTML = "";

    data.users.forEach((user) => {
      const option = document.createElement("option");
      option.value = user.id;
      option.textContent = `${user.name} (${user.id})`;
      rlsUserSelect.appendChild(option);
    });
  } catch (error) {
    console.error("Error loading RLS users:", error);
    rlsUserSelect.innerHTML = '<option value="">Error loading users</option>';
  }
}

async function loadCurrentRlsUser() {
  try {
    // Use local cached RLS user ID instead of asking server
    const currentRlsUserId = await getCurrentRlsUserId();

    if (currentRlsUserId) {
      rlsUserSelect.value = currentRlsUserId;
    }
  } catch (error) {
    console.error("Error loading current RLS user:", error);
  }
}

async function saveRlsUser() {
  const selectedUserId = rlsUserSelect.value;

  if (!selectedUserId) {
    showStatusMessage("Please select a user", "error");
    return;
  }

  saveRlsUserBtn.disabled = true;
  saveRlsUserBtn.textContent = "Saving...";
  hideStatusMessage();

  try {
    // Validate that the selected user ID exists in our list
    const usersResponse = await fetch("/agent/rls-users");
    const usersData = await usersResponse.json();

    const validUser = usersData.users?.find(
      (user) => user.id === selectedUserId
    );
    if (!validUser) {
      throw new Error("Invalid RLS user ID selected");
    }

    showStatusMessage(
      `RLS user updated successfully to ${validUser.name}`,
      "success"
    );

    // Update cached RLS user ID
    chatState.currentRlsUserId = selectedUserId;
    // Save to localStorage for persistence
    localStorage.setItem("current_rls_user_id", selectedUserId);

    // Clear current chat session since we're switching agents
    // Pass the new selectedUserId to ensure it's used for the clear operation
    await clearChatSession(selectedUserId);

    // Update current user display immediately
    await updateCurrentUserDisplay();

    setTimeout(() => {
      closeSettings();
      // Optionally show a message to the user about the agent switch
      addSystemMessage(`Switched to agent for user: ${validUser.name}`);
    }, 1500);
  } catch (error) {
    console.error("Error saving RLS user:", error);
    showStatusMessage("Error saving RLS user: " + error.message, "error");
  } finally {
    saveRlsUserBtn.disabled = false;
    saveRlsUserBtn.textContent = "Save Changes";
  }
}

function getSelectedUserName() {
  const selectedOption = rlsUserSelect.options[rlsUserSelect.selectedIndex];
  return selectedOption ? selectedOption.textContent : "Unknown User";
}

function showStatusMessage(message, type) {
  rlsUserStatus.textContent = message;
  rlsUserStatus.className = `status-message ${type}`;
}

function hideStatusMessage() {
  rlsUserStatus.className = "status-message";
  rlsUserStatus.textContent = "";
}

async function clearChatSession(rls_user_id = null) {
  try {
    // Use provided RLS user ID or get current one
    const rlsUserId = rls_user_id || await getCurrentRlsUserId();

    // Call the backend clear endpoint to properly clean up server-side state
    const response = await fetch("/chat/clear", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: "", // Required field in ChatRequest but not used for clear
        session_id: chatState.sessionId,
        rls_user_id: rlsUserId,
      }),
    });

    if (!response.ok) {
      console.warn("Backend clear failed, continuing with frontend clear");
    } else {
      const result = await response.json();
      console.log("Clear response:", result);
    }

    // Generate new session ID for fresh start
    chatState.sessionId = generateSessionId();
    localStorage.setItem("chat_session_id", chatState.sessionId);

    // Clear the messages display
    messagesDiv.innerHTML = "";

    // Clear any uploaded file state
    chatState.uploadedFile = null;
    fileInput.value = "";
    messageInput.placeholder =
      "Type your message or type help for some suggestions....";
  } catch (error) {
    console.error("Error clearing chat session:", error);
  }
}

function addSystemMessage(message) {
  const systemDiv = document.createElement("div");
  systemDiv.className = "message assistant";
  systemDiv.textContent = message;
  systemDiv.style.background = "#e3f2fd";
  systemDiv.style.color = "#1565c0";
  systemDiv.style.border = "1px solid #bbdefb";
  systemDiv.style.fontStyle = "italic";
  messagesDiv.appendChild(systemDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  // Remove system message after 5 seconds
  setTimeout(() => {
    if (systemDiv.parentNode) {
      systemDiv.parentNode.removeChild(systemDiv);
    }
  }, 5000);
}

// Update current user display
async function updateCurrentUserDisplay() {
  try {
    // Use local cached RLS user ID instead of asking server
    const currentRlsUserId = await getCurrentRlsUserId();

    // Get user name from the users list
    const usersResponse = await fetch("/agent/rls-users");
    const usersData = await usersResponse.json();

    if (usersData.status === "success" && usersData.users) {
      const currentUser = usersData.users.find(
        (user) => user.id === currentRlsUserId
      );
      const displayName = currentUser ? currentUser.name : "Unknown User";
      currentUserDiv.textContent = `Current User: ${displayName}`;
    } else {
      currentUserDiv.textContent = `Current User: ${currentRlsUserId}`;
    }
  } catch (error) {
    console.error("Error loading current user:", error);
    currentUserDiv.textContent = "Current User: Error";
  }
}

// Clear chat on page refresh/unload to clean up agent thread
window.addEventListener("beforeunload", (e) => {
  // Use fetch with keepalive for DELETE request during page unload
  try {
    // Get the current RLS user ID from localStorage (sync operation for beforeunload)
    const currentRlsUserId = localStorage.getItem("current_rls_user_id") || "00000000-0000-0000-0000-000000000000";
    
    fetch("/chat/clear", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: "", // Required field in ChatRequest but not used for clear
        session_id: chatState.sessionId,
        rls_user_id: currentRlsUserId,
      }),
      keepalive: true,
    }).catch(() => {
      // Ignore errors during page unload
    });
  } catch (error) {
    console.log("Failed to clear chat on page unload:", error);
  }
});

// Start service monitoring on page load
startServiceMonitoring();

// Focus input on load
messageInput.focus();
