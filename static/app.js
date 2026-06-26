const form = document.getElementById('chatForm');
const input = document.getElementById('userInput');
const chatHistory = document.getElementById('chatHistory');
const sendBtn = document.getElementById('sendBtn');

// Helper to create a user message element
function appendUserMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message user-message';
    msgDiv.innerHTML = `
        <div class="avatar"><i data-feather="user"></i></div>
        <div class="message-content">${text}</div>
    `;
    chatHistory.appendChild(msgDiv);
    feather.replace();
    scrollToBottom();
}

// Helper to show the typing indicator
function showTypingIndicator() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ai-message typing-msg';
    msgDiv.id = 'typingIndicator';
    msgDiv.innerHTML = `
        <div class="avatar"><i data-feather="cpu"></i></div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    chatHistory.appendChild(msgDiv);
    feather.replace();
    scrollToBottom();
}

// Helper to remove the typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Helper to create the AI response element
function appendAiMessage(answer, route) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ai-message';

    // Create the route badge HTML
    let badgeHtml = '';
    if (route) {
        const badgeClass = route === 'relational' ? 'route-relational' : 'route-semantic';
        badgeHtml = `<div class="route-badge ${badgeClass}">${route} Graph</div>`;
    }

    // Parse markdown (requires marked.js included in HTML)
    const parsedAnswer = typeof marked !== 'undefined' ? marked.parse(answer) : answer;

    msgDiv.innerHTML = `
        <div class="avatar"><i data-feather="cpu"></i></div>
        <div class="message-content">
            ${badgeHtml}
            ${parsedAnswer}
        </div>
    `;
    chatHistory.appendChild(msgDiv);
    feather.replace();
    scrollToBottom();
}

function scrollToBottom() {
    chatHistory.scrollTo({
        top: chatHistory.scrollHeight,
        behavior: 'smooth'
    });
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    // UI Updates
    appendUserMessage(question);
    input.value = '';
    input.disabled = true;
    sendBtn.disabled = true;
    showTypingIndicator();

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        removeTypingIndicator();

        if (response.ok) {
            appendAiMessage(data.answer, data.route_used);
        } else {
            appendAiMessage('**Error**: The system encountered an issue processing your request.');
        }
    } catch (err) {
        removeTypingIndicator();
        appendAiMessage('**Network Error**: Could not reach the FastAPI server.');
        console.error(err);
    } finally {
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    }
});
