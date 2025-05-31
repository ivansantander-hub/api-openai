const { useState, useEffect, useRef } = React;

// API Configuration
// Automatically detect the API base URL based on current location
const API_BASE_URL = window.location.origin;

// DOM Elements (these will be initialized after DOM loads)
let statusText, statusDot, loadingOverlay;

// Temperature sliders (will be initialized after DOM loads)
let chatTempSlider, chatTempValue, completionTempSlider, completionTempValue;

// Theme Hook
const useTheme = () => {
    const [theme, setTheme] = useState(() => {
        return localStorage.getItem('theme') || 'light';
    });

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    };

    return [theme, toggleTheme];
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 OpenAI API Client initialized');
    console.log('🌐 API Base URL:', API_BASE_URL);
    
    // Initialize DOM elements
    statusText = document.getElementById('status-text');
    statusDot = document.getElementById('status-dot');
    loadingOverlay = document.getElementById('loading-overlay');
    
    // Initialize temperature sliders
    chatTempSlider = document.getElementById('chat-temperature');
    chatTempValue = document.getElementById('chat-temp-value');
    completionTempSlider = document.getElementById('completion-temperature');
    completionTempValue = document.getElementById('completion-temp-value');
    
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
const makeRequest = async (endpoint, options = {}) => {
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
};

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

// Utility Components
const LoadingOverlay = ({ show }) => {
    if (!show) return null;
    
    return (
        <div className="loading-overlay show">
            <div className="loading-spinner">
                <i className="fas fa-spinner fa-spin"></i>
                <p>Processing...</p>
            </div>
        </div>
    );
};

const Result = ({ content, type = 'info', className = '' }) => {
    if (!content) return null;
    
    return (
        <div className={`${className} result-${type} fade-in`}>
            <div dangerouslySetInnerHTML={{ __html: content }} />
        </div>
    );
};

// Header Component
const Header = ({ status, theme, toggleTheme }) => {
    return (
        <header className="header">
            <h1>
                <i className="fas fa-robot"></i> 
                OpenAI API Client
            </h1>
            <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                <div className="status-indicator">
                    <span>{status.message}</span>
                    <div className={`status-dot ${status.type}`}></div>
                </div>
                <button className="theme-toggle" onClick={toggleTheme}>
                    <i className={`fas ${theme === 'light' ? 'fa-moon' : 'fa-sun'}`}></i>
                    {theme === 'light' ? 'Dark' : 'Light'}
                </button>
            </div>
        </header>
    );
};

// Health Check Component
const HealthSection = ({ onStatusChange }) => {
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);

    const checkHealth = async () => {
        try {
            setLoading(true);
            const data = await makeRequest('/health');
            
            onStatusChange({ type: 'online', message: 'Service Online' });
            setResult(
                formatSuccess('Service is healthy and operational') + 
                formatJSON(data)
            );
            
        } catch (error) {
            onStatusChange({ type: 'offline', message: 'Service Offline' });
            setResult(formatError(error));
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        checkHealth();
    }, []);

    return (
        <section className="status-section">
            <h2><i className="fas fa-heartbeat"></i> Service Status</h2>
            <div className="status-card">
                <button className="btn btn-primary" onClick={checkHealth} disabled={loading}>
                    <i className="fas fa-sync-alt"></i> Check Health
                </button>
                <Result content={result} type={result.includes('error') ? 'error' : 'success'} className="status-result" />
            </div>
        </section>
    );
};

// Models Section Component
const ModelsSection = () => {
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);

    const getModels = async () => {
        try {
            setLoading(true);
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
                setResult(modelsHtml);
            } else {
                setResult(formatJSON(data));
            }
            
        } catch (error) {
            setResult(formatError(error));
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="models-section">
            <h2><i className="fas fa-list"></i> Available Models</h2>
            <div className="models-card">
                <button className="btn btn-secondary" onClick={getModels} disabled={loading}>
                    <i className="fas fa-download"></i> Load Models
                </button>
                <Result content={result} type={result.includes('error') ? 'error' : 'success'} className="models-result" />
            </div>
        </section>
    );
};

// Chat Component
const ChatSection = () => {
    const [model, setModel] = useState('gpt-3.5-turbo');
    const [message, setMessage] = useState('');
    const [temperature, setTemperature] = useState(0.7);
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);

    const sendChatMessage = async () => {
        if (!message.trim()) {
            setResult(formatError('Please enter a message'));
            return;
        }
        
        try {
            setLoading(true);
            const data = await makeRequest('/chat', {
                method: 'POST',
                body: JSON.stringify({
                    model: model,
                    messages: [{ role: 'user', content: message }],
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
                setResult(responseHtml);
            } else {
                setResult(formatJSON(data));
            }
            
        } catch (error) {
            setResult(formatError(error));
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="chat-section">
            <h2><i className="fas fa-comments"></i> Chat Completion</h2>
            <div className="chat-card">
                <div className="input-group">
                    <label htmlFor="chat-model">Model:</label>
                    <select 
                        id="chat-model" 
                        className="form-select" 
                        value={model} 
                        onChange={(e) => setModel(e.target.value)}
                    >
                        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                        <option value="gpt-4">GPT-4</option>
                        <option value="gpt-4-turbo-preview">GPT-4 Turbo</option>
                    </select>
                </div>
                <div className="input-group">
                    <label htmlFor="chat-message">Message:</label>
                    <textarea 
                        id="chat-message" 
                        className="form-textarea" 
                        rows="4"
                        placeholder="Type your message here..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="chat-temperature">Temperature: {temperature}</label>
                    <input 
                        type="range" 
                        id="chat-temperature" 
                        className="form-range"
                        min="0" 
                        max="2" 
                        step="0.1" 
                        value={temperature}
                        onChange={(e) => setTemperature(parseFloat(e.target.value))}
                    />
                </div>
                <button className="btn btn-primary" onClick={sendChatMessage} disabled={loading}>
                    <i className="fas fa-paper-plane"></i> Send Message
                </button>
                <Result content={result} type={result.includes('error') ? 'error' : 'success'} className="chat-result" />
            </div>
        </section>
    );
};

// Text Completion Component
const CompletionSection = () => {
    const [model, setModel] = useState('gpt-3.5-turbo-instruct');
    const [prompt, setPrompt] = useState('');
    const [temperature, setTemperature] = useState(0.7);
    const [maxTokens, setMaxTokens] = useState(100);
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);

    const generateCompletion = async () => {
        if (!prompt.trim()) {
            setResult(formatError('Please enter a prompt'));
            return;
        }
        
        try {
            setLoading(true);
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
                setResult(responseHtml);
            } else {
                setResult(formatJSON(data));
            }
            
        } catch (error) {
            setResult(formatError(error));
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="completion-section">
            <h2><i className="fas fa-edit"></i> Text Completion</h2>
            <div className="completion-card">
                <div className="input-group">
                    <label htmlFor="completion-model">Model:</label>
                    <select 
                        id="completion-model" 
                        className="form-select"
                        value={model}
                        onChange={(e) => setModel(e.target.value)}
                    >
                        <option value="gpt-3.5-turbo-instruct">GPT-3.5 Turbo Instruct</option>
                    </select>
                </div>
                <div className="input-group">
                    <label htmlFor="completion-prompt">Prompt:</label>
                    <textarea 
                        id="completion-prompt" 
                        className="form-textarea" 
                        rows="4"
                        placeholder="Enter your prompt here..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="completion-temperature">Temperature: {temperature}</label>
                    <input 
                        type="range" 
                        id="completion-temperature" 
                        className="form-range"
                        min="0" 
                        max="2" 
                        step="0.1" 
                        value={temperature}
                        onChange={(e) => setTemperature(parseFloat(e.target.value))}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="completion-max-tokens">Max Tokens:</label>
                    <input 
                        type="number" 
                        id="completion-max-tokens" 
                        className="form-input"
                        value={maxTokens} 
                        min="1" 
                        max="4000"
                        onChange={(e) => setMaxTokens(parseInt(e.target.value))}
                    />
                </div>
                <button className="btn btn-primary" onClick={generateCompletion} disabled={loading}>
                    <i className="fas fa-magic"></i> Generate Completion
                </button>
                <Result content={result} type={result.includes('error') ? 'error' : 'success'} className="completion-result" />
            </div>
        </section>
    );
};

// Image Generation Component
const ImageSection = () => {
    const [prompt, setPrompt] = useState('');
    const [size, setSize] = useState('1024x1024');
    const [quality, setQuality] = useState('standard');
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);

    const generateImage = async () => {
        if (!prompt.trim()) {
            setResult(formatError('Please enter an image prompt'));
            return;
        }
        
        try {
            setLoading(true);
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
                setResult(responseHtml);
            } else {
                setResult(formatJSON(data));
            }
            
        } catch (error) {
            setResult(formatError(error));
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="image-section">
            <h2><i className="fas fa-image"></i> Image Generation</h2>
            <div className="image-card">
                <div className="input-group">
                    <label htmlFor="image-prompt">Prompt:</label>
                    <textarea 
                        id="image-prompt" 
                        className="form-textarea" 
                        rows="3"
                        placeholder="Describe the image you want to generate..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="image-size">Size:</label>
                    <select 
                        id="image-size" 
                        className="form-select"
                        value={size}
                        onChange={(e) => setSize(e.target.value)}
                    >
                        <option value="1024x1024">1024x1024</option>
                        <option value="1792x1024">1792x1024</option>
                        <option value="1024x1792">1024x1792</option>
                    </select>
                </div>
                <div className="input-group">
                    <label htmlFor="image-quality">Quality:</label>
                    <select 
                        id="image-quality" 
                        className="form-select"
                        value={quality}
                        onChange={(e) => setQuality(e.target.value)}
                    >
                        <option value="standard">Standard</option>
                        <option value="hd">HD</option>
                    </select>
                </div>
                <button className="btn btn-primary" onClick={generateImage} disabled={loading}>
                    <i className="fas fa-palette"></i> Generate Image
                </button>
                <Result content={result} type={result.includes('error') ? 'error' : 'success'} className="image-result" />
            </div>
        </section>
    );
};

// Embeddings Component
const EmbeddingsSection = () => {
    const [model, setModel] = useState('text-embedding-ada-002');
    const [text, setText] = useState('');
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);

    const createEmbeddings = async () => {
        if (!text.trim()) {
            setResult(formatError('Please enter text to create embeddings'));
            return;
        }
        
        try {
            setLoading(true);
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
                setResult(responseHtml);
            } else {
                setResult(formatJSON(data));
            }
            
        } catch (error) {
            setResult(formatError(error));
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="embeddings-section">
            <h2><i className="fas fa-project-diagram"></i> Text Embeddings</h2>
            <div className="embeddings-card">
                <div className="input-group">
                    <label htmlFor="embeddings-model">Model:</label>
                    <select 
                        id="embeddings-model" 
                        className="form-select"
                        value={model}
                        onChange={(e) => setModel(e.target.value)}
                    >
                        <option value="text-embedding-ada-002">text-embedding-ada-002</option>
                        <option value="text-embedding-3-small">text-embedding-3-small</option>
                        <option value="text-embedding-3-large">text-embedding-3-large</option>
                    </select>
                </div>
                <div className="input-group">
                    <label htmlFor="embeddings-text">Text:</label>
                    <textarea 
                        id="embeddings-text" 
                        className="form-textarea" 
                        rows="4"
                        placeholder="Enter text to create embeddings..."
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />
                </div>
                <button className="btn btn-primary" onClick={createEmbeddings} disabled={loading}>
                    <i className="fas fa-vector-square"></i> Create Embeddings
                </button>
                <Result content={result} type={result.includes('error') ? 'error' : 'success'} className="embeddings-result" />
            </div>
        </section>
    );
};

// Footer Component
const Footer = () => {
    return (
        <footer className="footer">
            <p>&copy; 2025 OpenAI API Client - Built with ❤️ and React 18</p>
        </footer>
    );
};

// Main App Component
const App = () => {
    const [theme, toggleTheme] = useTheme();
    const [status, setStatus] = useState({ type: '', message: 'Checking...' });
    const [globalLoading, setGlobalLoading] = useState(false);

    useEffect(() => {
        console.log('🚀 OpenAI API Client with React 18 initialized');
        console.log('🌐 API Base URL:', API_BASE_URL);
        console.log('🎨 Current Theme:', theme);
    }, [theme]);

    return (
        <div className="container">
            <Header status={status} theme={theme} toggleTheme={toggleTheme} />
            
            <main className="main-content">
                <HealthSection onStatusChange={setStatus} />
                <ModelsSection />
                <ChatSection />
                <CompletionSection />
                <ImageSection />
                <EmbeddingsSection />
            </main>
            
            <Footer />
            <LoadingOverlay show={globalLoading} />
        </div>
    );
};

// Render the App
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

console.log('✅ OpenAI API Client with React 18 ready!'); 