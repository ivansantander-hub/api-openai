// API Configuration
const API_BASE_URL = process.env.API_BASE_URL;

// DOM Elements
const statusText = document.getElementById('status-text');
const statusDot = document.getElementById('status-dot');
const loadingOverlay = document.getElementById('loading-overlay');

// Temperature sliders
const chatTempSlider = document.getElementById('chat-temperature');
const chatTempValue = document.getElementById('chat-temp-value');
const completionTempSlider = document.getElementById('completion-temperature');
const completionTempValue = document.getElementById('completion-temp-value');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 OpenAI API Client initialized');
    
    // Set up temperature sliders
    if (chatTempSlider && chatTempValue) {
        chatTempSlider.addEventListener('input', function() {
            chatTempValue.textContent = this.value;
        });
    }
    
    if (completionTempSlider && completionTempValue) {
        completionTempSlider.addEventListener('input', function() {
            completionTempValue.textContent = this.value;
        });
    }
    
    // Check initial health status
    checkHealth();
});

// Utility Functions
function showLoading() {
    loadingOverlay.classList.add('show');
}

function hideLoading() {
    loadingOverlay.classList.remove('show');
}

function updateStatus(status, message) {
    statusText.textContent = message;
    statusDot.className = 'status-dot';
    
    if (status === 'online') {
        statusDot.classList.add('online');
    } else if (status === 'offline') {
        statusDot.classList.add('offline');
    }
}

function showResult(elementId, content, type = 'info') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = content;
        element.className = `${elementId} result-${type}`;
        element.classList.add('fade-in');
    }
}

function formatJSON(obj) {
    return `<pre class="code-block">${JSON.stringify(obj, null, 2)}</pre>`;
}

function formatError(error) {
    return `<div class="message error">
        <strong>Error:</strong> ${error.message || error}
    </div>`;
}

function formatSuccess(message) {
    return `<div class="message success">
        <strong>Success:</strong> ${message}
    </div>`;
}

// API Functions
async function makeRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const requestOptions = { ...defaultOptions, ...options };
    
    try {
        console.log(`Making request to: ${url}`, requestOptions);
        const response = await fetch(url, requestOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}

// Health Check
async function checkHealth() {
    try {
        showLoading();
        const data = await makeRequest('/health');
        
        updateStatus('online', 'Service Online');
        showResult('health-result', 
            formatSuccess('Service is healthy and operational') + 
            formatJSON(data), 
            'success'
        );
        
    } catch (error) {
        updateStatus('offline', 'Service Offline');
        showResult('health-result', formatError(error), 'error');
    } finally {
        hideLoading();
    }
}

// Get Models
async function getModels() {
    try {
        showLoading();
        const data = await makeRequest('/models');
        
        if (data.models && Array.isArray(data.models)) {
            const modelsHtml = `
                ${formatSuccess(`Found ${data.models.length} models`)}
                <div class="models-grid">
                    ${data.models.map(model => 
                        `<div class="model-item">${model.id || model}</div>`
                    ).join('')}
                </div>
            `;
            showResult('models-result', modelsHtml, 'success');
        } else {
            showResult('models-result', formatJSON(data), 'info');
        }
        
    } catch (error) {
        showResult('models-result', formatError(error), 'error');
    } finally {
        hideLoading();
    }
}

// Chat Completion
async function sendChatMessage() {
    const model = document.getElementById('chat-model').value;
    const message = document.getElementById('chat-message').value.trim();
    const temperature = parseFloat(document.getElementById('chat-temperature').value);
    
    if (!message) {
        showResult('chat-result', formatError('Please enter a message'), 'error');
        return;
    }
    
    try {
        showLoading();
        const data = await makeRequest('/chat', {
            method: 'POST',
            body: JSON.stringify({
                model: model,
                messages: [
                    {
                        role: 'user',
                        content: message
                    }
                ],
                temperature: temperature,
                max_tokens: 1000
            })
        });
        
        if (data.message) {
            const responseHtml = `
                ${formatSuccess('Message sent successfully')}
                <div class="chat-response">
                    <h4>AI Response:</h4>
                    <div class="response-content">${data.message}</div>
                </div>
                <details>
                    <summary>Full Response Data</summary>
                    ${formatJSON(data)}
                </details>
            `;
            showResult('chat-result', responseHtml, 'success');
        } else {
            showResult('chat-result', formatJSON(data), 'info');
        }
        
    } catch (error) {
        showResult('chat-result', formatError(error), 'error');
    } finally {
        hideLoading();
    }
}

// Text Completion
async function generateCompletion() {
    const model = document.getElementById('completion-model').value;
    const prompt = document.getElementById('completion-prompt').value.trim();
    const temperature = parseFloat(document.getElementById('completion-temperature').value);
    const maxTokens = parseInt(document.getElementById('completion-max-tokens').value);
    
    if (!prompt) {
        showResult('completion-result', formatError('Please enter a prompt'), 'error');
        return;
    }
    
    try {
        showLoading();
        const data = await makeRequest('/completion', {
            method: 'POST',
            body: JSON.stringify({
                model: model,
                prompt: prompt,
                temperature: temperature,
                max_tokens: maxTokens
            })
        });
        
        if (data.text) {
            const responseHtml = `
                ${formatSuccess('Completion generated successfully')}
                <div class="completion-response">
                    <h4>Generated Text:</h4>
                    <div class="response-content">${data.text}</div>
                </div>
                <details>
                    <summary>Full Response Data</summary>
                    ${formatJSON(data)}
                </details>
            `;
            showResult('completion-result', responseHtml, 'success');
        } else {
            showResult('completion-result', formatJSON(data), 'info');
        }
        
    } catch (error) {
        showResult('completion-result', formatError(error), 'error');
    } finally {
        hideLoading();
    }
}

// Image Generation
async function generateImage() {
    const prompt = document.getElementById('image-prompt').value.trim();
    const size = document.getElementById('image-size').value;
    const quality = document.getElementById('image-quality').value;
    
    if (!prompt) {
        showResult('image-result', formatError('Please enter an image prompt'), 'error');
        return;
    }
    
    try {
        showLoading();
        const data = await makeRequest('/images/generate', {
            method: 'POST',
            body: JSON.stringify({
                prompt: prompt,
                size: size,
                quality: quality,
                n: 1
            })
        });
        
        if (data.url) {
            const responseHtml = `
                ${formatSuccess('Image generated successfully')}
                <div class="image-response">
                    <img src="${data.url}" alt="Generated image" class="generated-image">
                    <p><strong>Prompt:</strong> ${prompt}</p>
                    <p><strong>Size:</strong> ${size} | <strong>Quality:</strong> ${quality}</p>
                </div>
                <details>
                    <summary>Full Response Data</summary>
                    ${formatJSON(data)}
                </details>
            `;
            showResult('image-result', responseHtml, 'success');
        } else {
            showResult('image-result', formatJSON(data), 'info');
        }
        
    } catch (error) {
        showResult('image-result', formatError(error), 'error');
    } finally {
        hideLoading();
    }
}

// Create Embeddings
async function createEmbeddings() {
    const model = document.getElementById('embeddings-model').value;
    const text = document.getElementById('embeddings-text').value.trim();
    
    if (!text) {
        showResult('embeddings-result', formatError('Please enter text to create embeddings'), 'error');
        return;
    }
    
    try {
        showLoading();
        const data = await makeRequest('/embeddings', {
            method: 'POST',
            body: JSON.stringify({
                model: model,
                input: text
            })
        });
        
        if (data.embeddings && Array.isArray(data.embeddings)) {
            const embedding = data.embeddings[0];
            const embeddingPreview = Array.isArray(embedding) ? 
                embedding.slice(0, 10).map(n => n.toFixed(6)).join(', ') + '...' : 
                JSON.stringify(embedding).substring(0, 100) + '...';
            
            const responseHtml = `
                ${formatSuccess('Embeddings created successfully')}
                <div class="embeddings-response">
                    <p><strong>Model:</strong> ${model}</p>
                    <p><strong>Input Text:</strong> "${text}"</p>
                    <p><strong>Embedding Dimensions:</strong> ${Array.isArray(embedding) ? embedding.length : 'N/A'}</p>
                    <div class="embeddings-preview">
                        <strong>First 10 values:</strong><br>
                        ${embeddingPreview}
                    </div>
                </div>
                <details>
                    <summary>Full Response Data</summary>
                    ${formatJSON(data)}
                </details>
            `;
            showResult('embeddings-result', responseHtml, 'success');
        } else {
            showResult('embeddings-result', formatJSON(data), 'info');
        }
        
    } catch (error) {
        showResult('embeddings-result', formatError(error), 'error');
    } finally {
        hideLoading();
    }
}

// Example prompts and texts
const examples = {
    chat: [
        "Explain quantum computing in simple terms",
        "Write a short story about a robot learning to paint",
        "What are the benefits of renewable energy?"
    ],
    completion: [
        "The future of artificial intelligence is",
        "Once upon a time in a digital world",
        "The most important skill for the 21st century is"
    ],
    image: [
        "A futuristic city with flying cars at sunset",
        "A cute robot sitting in a garden with flowers",
        "Abstract art representing the concept of time"
    ],
    embeddings: [
        "Machine learning is a subset of artificial intelligence",
        "The quick brown fox jumps over the lazy dog",
        "Sustainability and environmental conservation are crucial for our future"
    ]
};

// Add example buttons functionality
function loadExample(type) {
    const exampleTexts = examples[type];
    if (!exampleTexts) return;
    
    const randomExample = exampleTexts[Math.floor(Math.random() * exampleTexts.length)];
    
    switch(type) {
        case 'chat':
            document.getElementById('chat-message').value = randomExample;
            break;
        case 'completion':
            document.getElementById('completion-prompt').value = randomExample;
            break;
        case 'image':
            document.getElementById('image-prompt').value = randomExample;
            break;
        case 'embeddings':
            document.getElementById('embeddings-text').value = randomExample;
            break;
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to send chat message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeElement = document.activeElement;
        
        if (activeElement.id === 'chat-message') {
            sendChatMessage();
        } else if (activeElement.id === 'completion-prompt') {
            generateCompletion();
        } else if (activeElement.id === 'image-prompt') {
            generateImage();
        } else if (activeElement.id === 'embeddings-text') {
            createEmbeddings();
        }
    }
});

// Add tooltips and help text
const tooltips = {
    'chat-temperature': 'Controls randomness: 0 = focused, 2 = creative',
    'completion-temperature': 'Controls randomness: 0 = focused, 2 = creative',
    'completion-max-tokens': 'Maximum number of tokens in the response',
    'image-quality': 'HD quality costs more but provides better results',
    'embeddings-model': 'Different models have different dimensions and capabilities'
};

// Add tooltip functionality
Object.keys(tooltips).forEach(id => {
    const element = document.getElementById(id);
    if (element) {
        element.title = tooltips[id];
    }
});

// Export functions for global access
window.checkHealth = checkHealth;
window.getModels = getModels;
window.sendChatMessage = sendChatMessage;
window.generateCompletion = generateCompletion;
window.generateImage = generateImage;
window.createEmbeddings = createEmbeddings;
window.loadExample = loadExample;

console.log('✅ OpenAI API Client ready!'); 