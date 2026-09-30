const API = '/api';

function token() {
    return localStorage.getItem('pocketsmart_token');
}

function headers() {
    return token()
        ? {
            'Authorization': 'Bearer ' + token(),
            'Content-Type': 'application/json'
        }
        : {
            'Content-Type': 'application/json'
        };
}

function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, function (c) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[c];
    });
}

async function postJson(url, body) {
    const response = await fetch(API + url, {
        method: 'POST',
        headers: headers(),
        body: JSON.stringify(body)
    });

    let data;

    try {
        data = await response.json();
    } catch (error) {
        throw new Error('Server returned an invalid response.');
    }

    if (!response.ok) {
        let message = 'Request failed';

        if (Array.isArray(data.detail)) {
            message = data.detail
                .map(function (error) {
                    return error.msg || 'Validation error';
                })
                .join(', ');
        } else if (typeof data.detail === 'string') {
            message = data.detail;
        } else if (data.detail) {
            message = JSON.stringify(data.detail);
        }

        throw new Error(message);
    }

    return data;
}

function showResult(data) {
    const resultElement = document.getElementById('result');

    if (!resultElement) {
        return;
    }

    let html = `
        <div class="result-card">
            <h2>${escapeHtml(data.summary || 'Recommendations')}</h2>
            <p class="mini">
                ${data.ai_used ? 'Gemini AI' : 'Local fallback'}
                •
                ${escapeHtml(data.note || '')}
            </p>
        </div>
    `;

    const recommendations = data.recommendations || [];

    recommendations.forEach(function (item) {
        html += `
            <div class="result-card">
                <h3>${escapeHtml(item.item || 'Recommendation')}</h3>

                <p>
                    <b>${escapeHtml(item.category || '')}</b>
                    •
                    ${escapeHtml(item.platform || '')}
                    •
                    ₹${Number(item.estimated_price || 0).toLocaleString('en-IN')}
                </p>

                <p>
                    ${escapeHtml(item.reason || '')}
                </p>

                <a
                    href="${escapeHtml(item.link || '#')}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Open platform ↗
                </a>
            </div>
        `;
    });

    resultElement.innerHTML = html;
}

function setup() {

    // ============================
    // LOGIN
    // ============================

    const loginForm = document.getElementById('loginForm');

    if (loginForm) {

        loginForm.onsubmit = async function (event) {

            event.preventDefault();

            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');
            const messageElement = document.getElementById('msg');

            try {

                const data = await postJson('/login', {
                    email: emailInput.value.trim(),
                    password: passwordInput.value
                });

                localStorage.setItem(
                    'pocketsmart_token',
                    data.access_token
                );

                window.location.href = '/dashboard';

            } catch (error) {

                if (messageElement) {
                    messageElement.textContent = error.message;
                    messageElement.className = 'error';
                }
            }
        };
    }


    // ============================
    // REGISTER
    // ============================

    const registerForm = document.getElementById('registerForm');

    if (registerForm) {

        registerForm.onsubmit = async function (event) {

            event.preventDefault();

            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');
            const messageElement = document.getElementById('msg');

            try {

                const nameValue = nameInput.value.trim();
                const emailValue = emailInput.value.trim();
                const passwordValue = passwordInput.value;

                if (!nameValue) {
                    throw new Error('Please enter your name.');
                }

                if (!emailValue) {
                    throw new Error('Please enter your email.');
                }

                if (!passwordValue) {
                    throw new Error('Please enter your password.');
                }

                if (passwordValue.length < 6) {
                    throw new Error(
                        'Password must contain at least 6 characters.'
                    );
                }

                const data = await postJson('/register', {
                    name: nameValue,
                    email: emailValue,
                    password: passwordValue
                });

                localStorage.setItem(
                    'pocketsmart_token',
                    data.access_token
                );

                window.location.href = '/dashboard';

            } catch (error) {

                if (messageElement) {
                    messageElement.textContent = error.message;
                    messageElement.className = 'error';
                }
            }
        };
    }


    // ============================
    // HOME PLANNER
    // ============================

    const homeForm = document.getElementById('homeForm');

    if (homeForm) {

        homeForm.onsubmit = async function (event) {

            event.preventDefault();

            const resultElement = document.getElementById('result');

            try {

                const formData = new FormData(homeForm);

                const roomsValue = formData.get('rooms') || '';
                const prioritiesValue = formData.get('priorities') || '';

                const data = await postJson('/generate-home', {

                    budget: Number(
                        formData.get('budget') || 0
                    ),

                    rooms: roomsValue
                        .split(',')
                        .map(function (item) {
                            return item.trim();
                        })
                        .filter(Boolean),

                    style: formData.get('style') || '',

                    priorities: prioritiesValue
                        .split(',')
                        .map(function (item) {
                            return item.trim();
                        })
                        .filter(Boolean),

                    quantities: {}
                });

                showResult(data);

            } catch (error) {

                if (resultElement) {
                    resultElement.innerHTML =
                        '<p class="error">' +
                        escapeHtml(error.message) +
                        '</p>';
                }
            }
        };
    }


    // ============================
    // PARTY PLANNER
    // ============================

    const partyForm = document.getElementById('partyForm');

    if (partyForm) {

        partyForm.onsubmit = async function (event) {

            event.preventDefault();

            const resultElement = document.getElementById('result');

            try {

                const formData = new FormData(partyForm);

                const preferencesValue =
                    formData.get('preferences') || '';

                const data = await postJson('/generate-party', {

                    budget: Number(
                        formData.get('budget') || 0
                    ),

                    guests: Number(
                        formData.get('guests') || 0
                    ),

                    event_type:
                        formData.get('event_type') || '',

                    venue:
                        formData.get('venue') || '',

                    city:
                        formData.get('city') || '',

                    preferences: preferencesValue
                        .split(',')
                        .map(function (item) {
                            return item.trim();
                        })
                        .filter(Boolean)
                });

                showResult(data);

            } catch (error) {

                if (resultElement) {
                    resultElement.innerHTML =
                        '<p class="error">' +
                        escapeHtml(error.message) +
                        '</p>';
                }
            }
        };
    }


    // ============================
    // JEWELRY PLANNER
    // ============================

    const jewelryForm = document.getElementById('jewelryForm');

    if (jewelryForm) {

        jewelryForm.onsubmit = async function (event) {

            event.preventDefault();

            const resultElement = document.getElementById('result');

            try {

                const formData = new FormData(jewelryForm);

                const response = await fetch(
                    API + '/generate-jewelry',
                    {
                        method: 'POST',

                        headers: {
                            'Authorization':
                                'Bearer ' + token()
                        },

                        body: formData
                    }
                );

                let data;

                try {
                    data = await response.json();
                } catch (error) {
                    throw new Error(
                        'Server returned an invalid response.'
                    );
                }

                if (!response.ok) {

                    let message = 'Request failed';

                    if (Array.isArray(data.detail)) {

                        message = data.detail
                            .map(function (error) {
                                return error.msg ||
                                    'Validation error';
                            })
                            .join(', ');

                    } else if (
                        typeof data.detail === 'string'
                    ) {

                        message = data.detail;

                    } else if (data.detail) {

                        message =
                            JSON.stringify(data.detail);
                    }

                    throw new Error(message);
                }

                showResult(data);

            } catch (error) {

                if (resultElement) {
                    resultElement.innerHTML =
                        '<p class="error">' +
                        escapeHtml(error.message) +
                        '</p>';
                }
            }
        };
    }


    // ============================
    // DASHBOARD / HISTORY
    // ============================

    const historyElement =
        document.getElementById('history');

    if (historyElement) {
        loadDashboard(historyElement);
    }
}


// ============================
// LOAD DASHBOARD
// ============================

async function loadDashboard(element) {

    try {

        const sessionResponse = await fetch(
            API + '/session-info',
            {
                headers: headers()
            }
        );

        if (!sessionResponse.ok) {

            element.innerHTML =
                '<p>Please ' +
                '<a href="/login">login</a>' +
                ' to view your dashboard.</p>';

            return;
        }

        const sessionData =
            await sessionResponse.json();

        const welcomeElement =
            document.getElementById('welcome');

        if (welcomeElement) {

            welcomeElement.textContent =
                'Welcome, ' +
                sessionData.user.name +
                '!';
        }


        const historyResponse = await fetch(
            API + '/history',
            {
                headers: headers()
            }
        );

        if (!historyResponse.ok) {

            throw new Error(
                'Could not load recommendation history.'
            );
        }

        const historyData =
            await historyResponse.json();


        if (
            !historyData.items ||
            historyData.items.length === 0
        ) {

            element.innerHTML =
                '<p>No recommendations yet.</p>';

            return;
        }


        let html = '';

        historyData.items.forEach(function (item) {

            let summary = 'Recommendation';

            try {

                const responseData =
                    JSON.parse(item.response_json);

                summary =
                    responseData.summary ||
                    'Recommendation';

            } catch (error) {
                summary = 'Recommendation';
            }


            html += `
                <div class="result-card">
                    <b>
                        ${escapeHtml(
                            String(item.planner || '')
                                .toUpperCase()
                        )}
                    </b>

                    <span class="mini">
                        •
                        ${escapeHtml(
                            item.created_at || ''
                        )}
                    </span>

                    <p>
                        ${escapeHtml(summary)}
                    </p>
                </div>
            `;
        });

        element.innerHTML = html;

    } catch (error) {

        element.innerHTML =
            '<p class="error">' +
            'Could not load dashboard.' +
            '</p>';
    }
}


// ============================
// LOGOUT
// ============================

function logout() {

    localStorage.removeItem(
        'pocketsmart_token'
    );

    window.location.href = '/login';
}


// ============================
// START APPLICATION
// ============================

document.addEventListener(
    'DOMContentLoaded',
    setup
);