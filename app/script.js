const API_BASE_URL = window.location.origin.includes(':8000') ? window.location.origin : 'http://127.0.0.1:8000';
const PREDICT_ENDPOINT = `${API_BASE_URL}/predict`;

const FIELD_NAMES = [
    'age', 'sex', 'bmi', 'bp',
    's1', 's2', 's3', 's4', 's5', 's6'
];

// Theme toggle (Light / Dark mode)
const themeToggleBtn = document.getElementById('theme-toggle');

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

// Initial theme resolution: localStorage preference or system preference
const savedTheme = localStorage.getItem('theme');
const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
applyTheme(initialTheme);

if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme);
    });
}

// Tab switching
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanels = document.querySelectorAll('.tab-panel');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');

        tabBtns.forEach(b => {
            b.classList.remove('active');
            b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');

        tabPanels.forEach(panel => {
            if (panel.id === `panel-${targetTab}`) {
                panel.classList.add('active');
                panel.classList.remove('hidden');
            } else {
                panel.classList.remove('active');
                panel.classList.add('hidden');
            }
        });
    });
});

// Form elements
const form = document.getElementById('prediction-form');
const predictBtn = document.querySelector('.btn-predict');
const resultContainer = document.getElementById('result-container');
const errorContainer = document.getElementById('error-container');
const scoreValueEl = document.getElementById('score-value');
const interpretationValueEl = document.getElementById('interpretation-value');
const errorMessageEl = document.getElementById('error-message');
const dismissErrorBtn = document.querySelector('.btn-dismiss');

function getPayload() {
    const payload = {};
    FIELD_NAMES.forEach((name) => {
        const input = document.getElementById(name);
        payload[name] = parseFloat(input.value) || 0;
    });
    return payload;
}

function setLoading(isLoading) {
    if (isLoading) {
        predictBtn.classList.add('loading');
        predictBtn.disabled = true;
    } else {
        predictBtn.classList.remove('loading');
        predictBtn.disabled = false;
    }
}

// ── Scale marker ──────────────────────────────────────────
const SCALE_MIN = 25;
const SCALE_MAX = 346;

function updateScaleMarker(score) {
    const marker      = document.getElementById('score-marker');
    const markerLabel = document.getElementById('score-marker-label');
    if (!marker || !markerLabel) return;

    // Clamp within dataset bounds then convert to a percentage position
    const clamped = Math.min(Math.max(score, SCALE_MIN), SCALE_MAX);
    const pct     = ((clamped - SCALE_MIN) / (SCALE_MAX - SCALE_MIN)) * 100;

    marker.style.left = `${pct}%`;
    markerLabel.textContent = score;
    marker.classList.remove('hidden');
}

function showResult(score, interpretation) {
    scoreValueEl.textContent = score;
    interpretationValueEl.textContent = interpretation;
    resultContainer.classList.remove('hidden');
    errorContainer.classList.add('hidden');
    updateScaleMarker(score);
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    errorMessageEl.textContent = message;
    errorContainer.classList.remove('hidden');
    resultContainer.classList.add('hidden');
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideFeedback() {
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
}

async function handleSubmit(event) {
    event.preventDefault();
    hideFeedback();
    setLoading(true);

    const payload = getPayload();

    try {
        const response = await fetch(PREDICT_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            let errorDetail = `Received status code ${response.status} from server.`;
            try {
                const errBody = await response.json();
                if (errBody.detail) {
                    errorDetail = `Server error: ${errBody.detail}`;
                } else if (errBody.message) {
                    errorDetail = `Server error: ${errBody.message}`;
                }
            } catch (_) {
                // ignore JSON parse errors
            }
            throw new Error(errorDetail);
        }

        const data = await response.json();

        const score = data.predicted_progression_socre;
        const interpretation = data.interpretation;

        if (score === undefined || interpretation === undefined) {
            throw new Error('Unexpected response format from server.');
        }

        showResult(score, interpretation);
    } catch (err) {
        if (err.name === 'TypeError' && err.message.includes('fetch')) {
            showError('Could not connect to the FastAPI server. Is it running on http://127.0.0.1:8000?');
        } else {
            showError(err.message || 'An unexpected error occurred.');
        }
    } finally {
        setLoading(false);
    }
}

dismissErrorBtn.addEventListener('click', () => {
    errorContainer.classList.add('hidden');
});

form.addEventListener('submit', handleSubmit);
