// DOM Elements
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('loginBtn');
const togglePasswordBtn = document.getElementById('togglePassword');
const alert = document.getElementById('alert');

// Toggle Password Visibility
togglePasswordBtn.addEventListener('click', () => {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    
    // Change icon (optional: you can add different icons for show/hide)
    togglePasswordBtn.classList.toggle('active');
});

// Show Alert Function
function showAlert(message, type) {
    alert.textContent = message;
    alert.className = `alert ${type} show`;
    
    setTimeout(() => {
        alert.classList.remove('show');
    }, 4000);
}

// Login Form Submit
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = usernameInput.value.trim();
    const password = passwordInput.value;
    
    // Validation
    if (!username) {
        showAlert('Please enter your username', 'error');
        usernameInput.focus();
        return;
    }
    
    if (username.length < 3) {
        showAlert('Username must be at least 3 characters', 'error');
        usernameInput.focus();
        return;
    }
    
    if (!password) {
        showAlert('Please enter your password', 'error');
        passwordInput.focus();
        return;
    }
    
    if (password.length < 6) {
        showAlert('Password must be at least 6 characters', 'error');
        passwordInput.focus();
        return;
    }
    
    // Show loading state
    loginBtn.classList.add('loading');
    
    try {
        // AJAX Request - API endpoint'inizi buraya ekleyin
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Success
            showAlert('Login successful! Redirecting...', 'success');
            
            // Store token if provided
            if (data.token) {
                localStorage.setItem('authToken', data.token);
            }
            
            // Redirect after 1.5 seconds
            setTimeout(() => {
                window.location.href = data.redirectUrl || '/dashboard';
            }, 1500);
        } else {
            // Error from server
            showAlert(data.message || 'Login failed. Please check your credentials.', 'error');
        }
    } catch (error) {
        // Network or other errors
        console.error('Login error:', error);
        
        // Demo mode - simulated success (remove this in production)
        showAlert('Demo mode: Login successful! (No API connection)', 'success');
        
        setTimeout(() => {
            console.log('Login attempted with:', { username, password });
            // In production, remove the demo code above and show real error:
            // showAlert('An error occurred. Please try again later.', 'error');
        }, 1500);
    } finally {
        // Remove loading state
        setTimeout(() => {
            loginBtn.classList.remove('loading');
        }, 1500);
    }
});

// Input animations
[usernameInput, passwordInput].forEach(input => {
    input.addEventListener('focus', () => {
        input.parentElement.classList.add('focused');
    });
    
    input.addEventListener('blur', () => {
        input.parentElement.classList.remove('focused');
    });
});

// Prevent multiple form submissions
loginForm.addEventListener('submit', (e) => {
    if (loginBtn.classList.contains('loading')) {
        e.preventDefault();
    }
});

// Hijri Date Calculation - Corrected algorithm
function getHijriDate() {
    const today = new Date();
    const gYear = today.getFullYear();
    const gMonth = today.getMonth() + 1;
    const gDay = today.getDate();
    
    // Calculate Julian Day Number
    let a = Math.floor((14 - gMonth) / 12);
    let y = gYear + 4800 - a;
    let m = gMonth + 12 * a - 3;
    let jdn = gDay + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
    
    // Convert to Hijri
    let l = jdn - 1948440 + 10632;
    let n = Math.floor((l - 1) / 10631);
    let l2 = l - 10631 * n + 354;
    let j = (Math.floor((10985 - l2) / 5316)) * (Math.floor((50 * l2) / 17719)) + (Math.floor(l2 / 5670)) * (Math.floor((43 * l2) / 15238));
    let l3 = l2 - (Math.floor((30 - j) / 15)) * (Math.floor((17719 * j) / 50)) - (Math.floor(j / 16)) * (Math.floor((15238 * j) / 43)) + 29;
    let hMonth = Math.floor((24 * l3) / 709);
    let hDay = l3 - Math.floor((709 * hMonth) / 24);
    let hYear = 30 * n + j - 30;
    
    const hijriMonths = [
        'Muharram', 'Safar', 'Rabi al-Awwal', 'Rabi al-Thani',
        'Jumada al-Awwal', 'Jumada al-Akhira', 'Rajab', "Sha'ban",
        'Ramadan', 'Shawwal', "Dhu al-Qi'dah", 'Dhu al-Hijjah'
    ];
    
    return `${hDay} ${hijriMonths[hMonth - 1]} ${hYear} H`;
}

// Display Hijri Date
function displayHijriDate() {
    const hijriDateElement = document.getElementById('hijriDate');
    if (hijriDateElement) {
        hijriDateElement.textContent = getHijriDate();
    }
}

// Auto-focus username input on page load
window.addEventListener('load', () => {
    usernameInput.focus();
    displayHijriDate();
});

// Handle "Enter" key in inputs
usernameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        passwordInput.focus();
    }
});
