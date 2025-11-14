// content_script.js - Captures AI responses from various platforms

let isCapturing = false;
const CORTEX_SERVER = 'http://localhost:5000';

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "toggle") {
        isCapturing = request.enabled;
        console.log("Cortex capture:", isCapturing ? "ON" : "OFF");
        sendResponse({status: "ok"});
    }
});

// Detect which AI platform we're on
function detectPlatform() {
    const hostname = window.location.hostname;
    if (hostname.includes('chat.openai.com')) return 'chatgpt';
    if (hostname.includes('claude.ai')) return 'claude';
    if (hostname.includes('perplexity.ai')) return 'perplexity';
    return 'unknown';
}

// Extract conversation context
function extractConversationContext(platform) {
    const context = {
        platform: platform,
        url: window.location.href,
        timestamp: new Date().toISOString(),
        conversation_id: null,
        messages: []
    };

    // Extract conversation ID from URL
    const urlMatch = window.location.pathname.match(/\/c\/([a-zA-Z0-9-]+)/);
    context.conversation_id = urlMatch ? urlMatch[1] : `conv_${Date.now()}`;

    // Platform-specific message extraction
    if (platform === 'chatgpt') {
        const messages = document.querySelectorAll('[data-message-author-role]');
        messages.forEach(msg => {
            const role = msg.getAttribute('data-message-author-role');
            const content = msg.querySelector('.markdown')?.textContent || '';
            if (content) {
                context.messages.push({ role, content });
            }
        });
    } else if (platform === 'claude') {
        const messages = document.querySelectorAll('[data-testid="message"]');
        messages.forEach(msg => {
            const role = msg.querySelector('[data-testid="message-sender"]')?.textContent.toLowerCase() || 'unknown';
            const content = msg.querySelector('[data-testid="message-text"]')?.textContent || '';
            if (content) {
                context.messages.push({
                    role: role.includes('you') ? 'user' : 'assistant',
                    content
                });
            }
        });
    }

    return context;
}

// Send data to Cortex server
async function sendToCortex(data) {
    try {
        const response = await fetch(`${CORTEX_SERVER}/ingest`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const result = await response.json();
        console.log('[Cortex] Server response:', result);
        return result;
    } catch (error) {
        console.error('[Cortex] Failed to send data:', error);
        // Server might not be running - fail silently
        return null;
    }
}

// Observer to watch for new AI responses
const observer = new MutationObserver((mutations) => {
    if (!isCapturing) return;

    const platform = detectPlatform();

    // Platform-specific selectors
    const selectors = {
        chatgpt: '.markdown',
        claude: '[data-testid="message-text"]',
        perplexity: '.prose'
    };

    const selector = selectors[platform];
    if (!selector) return;

    mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType === 1) {
                const responseElement = node.querySelector(selector) ||
                                      (node.matches && node.matches(selector) ? node : null);

                if (responseElement) {
                    const text = responseElement.textContent;
                    console.log(`[Cortex] Captured ${platform} response:`, text.substring(0, 100));

                    // Extract full conversation context
                    const context = extractConversationContext(platform);

                    // Send to server
                    sendToCortex(context);
                }
            }
        });
    });
});

// Start observing
observer.observe(document.body, {
    childList: true,
    subtree: true
});
