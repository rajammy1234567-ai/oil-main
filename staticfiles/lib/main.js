// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Language Toggle Functionality
    const langToggle = document.getElementById('langToggle');
    const langTexts = document.querySelectorAll('.lang-text');
    const translatableElements = document.querySelectorAll('[data-translate]');
    
    // Set initial language
    let currentLang = localStorage.getItem('cattlecart_lang') || 'en';
    updateLanguage(currentLang);
    
    // Language toggle event
    if (langToggle) {
        langToggle.addEventListener('click', function() {
            currentLang = currentLang === 'en' ? 'hi' : 'en';
            localStorage.setItem('cattlecart_lang', currentLang);
            updateLanguage(currentLang);
            
            // Update language via AJAX
            updateLanguagePreference(currentLang);
        });
    }
    
    // Mobile Menu Toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileNav = document.getElementById('mobileNav');
    const closeMenu = document.getElementById('closeMenu');
    
    if (mobileMenuToggle && mobileNav) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileNav.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
        
        if (closeMenu) {
            closeMenu.addEventListener('click', function() {
                mobileNav.classList.remove('active');
                document.body.style.overflow = '';
            });
        }
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileNav.contains(event.target) && !mobileMenuToggle.contains(event.target)) {
                mobileNav.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    // Update cart count from localStorage
    updateCartCount();
    
    // Initialize dropdown menus
    initDropdowns();
});

// Language Functions
function updateLanguage(lang) {
    // Update button text
    document.querySelectorAll('.lang-text').forEach(el => {
        el.style.display = el.dataset.lang === lang ? 'inline' : 'none';
    });
    
    // Update all translatable elements
    document.querySelectorAll('[data-translate]').forEach(el => {
        const key = el.dataset.translate;
        if (translations[lang] && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
    
    // Update HTML lang attribute
    document.documentElement.lang = lang;
    
    // Update direction for RTL languages if needed
    document.documentElement.dir = lang === 'hi' ? 'ltr' : 'ltr'; // Hindi is LTR in this context
}

function updateLanguagePreference(lang) {
    // Send AJAX request to update language preference on server
    fetch('/api/set-language/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
        body: JSON.stringify({ language: lang })
    }).then(response => {
        if (response.ok) {
            console.log('Language preference updated');
        }
    }).catch(error => {
        console.error('Error updating language:', error);
    });
}

// Cart Functions
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cattlecart_cart') || '[]');
    const cartCount = cart.reduce((total, item) => total + item.quantity, 0);
    
    const cartCountElement = document.getElementById('cartCount');
    if (cartCountElement) {
        cartCountElement.textContent = cartCount;
        cartCountElement.style.display = cartCount > 0 ? 'flex' : 'none';
    }
}

// Dropdown Functions
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.user-dropdown');
    
    dropdowns.forEach(dropdown => {
        const button = dropdown.querySelector('.user-btn');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (button && menu) {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                const isVisible = menu.style.display === 'block';
                closeAllDropdowns();
                menu.style.display = isVisible ? 'none' : 'block';
            });
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function() {
        closeAllDropdowns();
    });
}

function closeAllDropdowns() {
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.style.display = 'none';
    });
}

// Utility Functions
function showToast(message, type = 'success') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
        <span>${message}</span>
        <button class="toast-close"><i class="fas fa-times"></i></button>
    `;
    
    // Add to page
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
    
    // Close button
    toast.querySelector('.toast-close').addEventListener('click', function() {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    });
}

// AJAX Helper Function
function makeRequest(url, method = 'GET', data = null) {
    const headers = {
        'X-CSRFToken': CSRF_TOKEN
    };
    
    if (data && !(data instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
        data = JSON.stringify(data);
    }
    
    return fetch(url, {
        method: method,
        headers: headers,
        body: data
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    });
}

// Add CSS for toast notifications
const toastCSS = `
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    padding: 15px 20px;
    border-radius: 5px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 10px;
    transform: translateX(150%);
    transition: transform 0.3s ease;
    z-index: 9999;
    min-width: 300px;
    max-width: 400px;
}

.toast.show {
    transform: translateX(0);
}

.toast-success {
    border-left: 4px solid #27ae60;
}

.toast-error {
    border-left: 4px solid #e74c3c;
}

.toast-warning {
    border-left: 4px solid #f39c12;
}

.toast-close {
    background: none;
    border: none;
    color: #95a5a6;
    cursor: pointer;
    margin-left: auto;
}

.toast-close:hover {
    color: #7f8c8d;
}
`;

// Inject toast CSS
const style = document.createElement('style');
style.textContent = toastCSS;
document.head.appendChild(style);