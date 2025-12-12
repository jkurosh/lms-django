/**
 * محافظت شبکه - جلوگیری از Wireshark و ابزارهای تحلیل شبکه
 * Network Protection - Prevent Wireshark and Network Analysis Tools
 */

(function() {
    'use strict';

    // بررسی ملایم ابزارهای تحلیل شبکه
    function detectNetworkTools() {
        // فقط بررسی ابزارهای بسیار مشکوک
        if (window.chrome && window.chrome.runtime && window.chrome.runtime.getManifest) {
            try {
                const manifest = window.chrome.runtime.getManifest();
                if (manifest && manifest.name) {
                    const name = manifest.name.toLowerCase();
                    // فقط ابزارهای بسیار مشکوک
                    if (name.includes('wireshark') || name.includes('tcpdump') || name.includes('burp')) {
                        return true;
                    }
                }
            } catch (e) {}
        }

        return false;
    }

    // مسدود کردن دسترسی
    function blockAccess(reason) {
        console.clear();
        console.log('%c🚫 دسترسی مسدود شد', 'color: red; font-size: 20px; font-weight: bold;');
        console.log('%c' + reason, 'color: red; font-size: 14px;');
        
        // جایگزینی کامل صفحه
        document.documentElement.innerHTML = `
            <!DOCTYPE html>
            <html dir="rtl" lang="fa">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>دسترسی مسدود - HeyVoonak</title>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                        color: white;
                        font-family: 'Vazir', Arial, sans-serif;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        text-align: center;
                    }
                    .blocked-container {
                        max-width: 500px;
                        padding: 2rem;
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 15px;
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                    }
                    .blocked-icon {
                        font-size: 4rem;
                        margin-bottom: 1rem;
                        color: #ff4444;
                    }
                    .blocked-title {
                        font-size: 1.5rem;
                        font-weight: bold;
                        margin-bottom: 1rem;
                        color: #ff4444;
                    }
                    .blocked-message {
                        font-size: 1rem;
                        line-height: 1.6;
                        margin-bottom: 1.5rem;
                        color: #cccccc;
                    }
                    .blocked-contact {
                        font-size: 0.9rem;
                        color: #888;
                        border-top: 1px solid rgba(255, 255, 255, 0.2);
                        padding-top: 1rem;
                    }
                </style>
            </head>
            <body>
                <div class="blocked-container">
                    <div class="blocked-icon">🚫</div>
                    <div class="blocked-title">دسترسی مسدود شد</div>
                    <div class="blocked-message">
                        استفاده از ابزارهای تحلیل شبکه مجاز نیست.<br>
                        لطفاً از مرورگر استاندارد استفاده کنید.
                    </div>
                    <div class="blocked-contact">
                        برای اطلاعات بیشتر با پشتیبانی تماس بگیرید
                    </div>
                </div>
            </body>
            </html>
        `;

        // مسدود کردن تمام events
        ['keydown', 'keyup', 'keypress', 'mousedown', 'mouseup', 'click', 'contextmenu', 'touchstart', 'touchend'].forEach(event => {
            document.addEventListener(event, function(e) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }, true);
        });

        // مسدود کردن console
        Object.defineProperty(window, 'console', {
            value: {},
            writable: false,
            configurable: false
        });
    }

    // محافظت از درخواست‌های شبکه
    function protectNetworkRequests() {
        // مسدود کردن XMLHttpRequest
        const originalXHR = window.XMLHttpRequest;
        window.XMLHttpRequest = function() {
            const xhr = new originalXHR();
            const originalOpen = xhr.open;
            
            xhr.open = function(method, url, async, user, password) {
                // بررسی URL های مشکوک
                if (typeof url === 'string' && (
                    url.includes('wireshark') ||
                    url.includes('tcpdump') ||
                    url.includes('fiddler') ||
                    url.includes('burp') ||
                    url.includes('charles') ||
                    url.includes('mitmproxy') ||
                    url.includes('localhost:8080') ||
                    url.includes('127.0.0.1:8080')
                )) {
                    throw new Error('Network request blocked for security');
                }
                
                return originalOpen.apply(this, arguments);
            };
            
            return xhr;
        };

        // مسدود کردن fetch
        const originalFetch = window.fetch;
        window.fetch = function(url, options) {
            if (typeof url === 'string' && (
                url.includes('wireshark') ||
                url.includes('tcpdump') ||
                url.includes('fiddler') ||
                url.includes('burp') ||
                url.includes('charles') ||
                url.includes('mitmproxy') ||
                url.includes('localhost:8080') ||
                url.includes('127.0.0.1:8080')
            )) {
                throw new Error('Fetch request blocked for security');
            }
            
            return originalFetch.apply(this, arguments);
        };

        // مسدود کردن WebSocket
        const originalWebSocket = window.WebSocket;
        window.WebSocket = function(url, protocols) {
            if (typeof url === 'string' && (
                url.includes('wireshark') ||
                url.includes('tcpdump') ||
                url.includes('fiddler') ||
                url.includes('burp') ||
                url.includes('charles') ||
                url.includes('mitmproxy')
            )) {
                throw new Error('WebSocket connection blocked for security');
            }
            
            return new originalWebSocket(url, protocols);
        };
    }

    // محافظت ملایم از Developer Tools
    function protectDevTools() {
        // فقط مسدود کردن راست کلیک و کلیدهای میانبر
        // بررسی مداوم Developer Tools را حذف کردیم
        
        // مسدود کردن کلیدهای میانبر
        document.addEventListener('keydown', function(e) {
            // فقط F12 و Ctrl+Shift+I
            if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
                e.preventDefault();
                return false;
            }
        });
    }

    // محافظت از Network Information API
    function protectNetworkAPI() {
        if ('connection' in navigator) {
            Object.defineProperty(navigator, 'connection', {
                value: undefined,
                writable: false,
                configurable: false
            });
        }

        // مسدود کردن Network Information API
        if ('networkInformation' in navigator) {
            Object.defineProperty(navigator, 'networkInformation', {
                value: undefined,
                writable: false,
                configurable: false
            });
        }
    }

    // محافظت از Performance API
    function protectPerformanceAPI() {
        if ('performance' in window) {
            // مسدود کردن Network Performance
            if ('getEntriesByType' in window.performance) {
                const originalGetEntriesByType = window.performance.getEntriesByType;
                window.performance.getEntriesByType = function(type) {
                    if (type === 'navigation' || type === 'resource') {
                        return [];
                    }
                    return originalGetEntriesByType.apply(this, arguments);
                };
            }
        }
    }

    // محافظت ملایم از فرم‌های ورود
    function protectLoginForms() {
        // فقط بررسی ابزارهای بسیار مشکوک
        const loginForms = document.querySelectorAll('form');
        
        loginForms.forEach(form => {
            // بررسی اینکه آیا فرم ورود است
            const isLoginForm = form.querySelector('input[type="password"]') || 
                               form.action.includes('login') || 
                               form.querySelector('button[type="submit"]')?.textContent.includes('ورود');
            
            if (isLoginForm) {
                form.addEventListener('submit', function(e) {
                    // فقط بررسی ابزارهای شبکه بسیار مشکوک
                    if (detectNetworkTools()) {
                        e.preventDefault();
                        blockAccess('Network analysis tool detected');
                        return false;
                    }
                });
            }
        });
        
        // محافظت ملایم از دکمه‌های ورود
        const loginButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
        loginButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                // فقط بررسی ابزارهای شبکه بسیار مشکوک
                if (detectNetworkTools()) {
                    e.preventDefault();
                    blockAccess('Network analysis tool detected');
                    return false;
                }
            });
        });
    }
    

    // شروع محافظت ملایم
    function initProtection() {
        // فقط بررسی ابزارهای بسیار مشکوک
        if (detectNetworkTools()) {
            return;
        }

        // محافظت ملایم از Developer Tools
        protectDevTools();
        
        // محافظت ملایم از فرم‌های ورود
        protectLoginForms();

        // مسدود کردن راست کلیک
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
        });
    }

    // شروع محافظت پس از بارگذاری صفحه
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initProtection);
    } else {
        initProtection();
    }

})();
