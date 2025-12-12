// HeyVoonak Ultra Strong Protection
(function() {
    'use strict';
    
    // پیام خطا
    const blockedHTML = `
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>دسترسی محدود</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                text-align: center;
                direction: rtl;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
                max-width: 500px;
                width: 90%;
            }
            .icon { font-size: 64px; margin-bottom: 20px; }
            h1 { font-size: 28px; margin-bottom: 15px; }
            p { font-size: 16px; line-height: 1.6; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🚫</div>
            <h1>دسترسی محدود</h1>
            <p>این صفحه برای کاربران عادی قابل مشاهده نیست.</p>
        </div>
    </body>
    </html>
    `;
    
    // مسدود کردن فوری
    function blockImmediately() {
        document.documentElement.innerHTML = blockedHTML;
        document.documentElement.style.overflow = 'hidden';
        
        // مسدود کردن تمام events
        ['keydown', 'keyup', 'keypress', 'mousedown', 'mouseup', 'click', 'contextmenu', 
         'touchstart', 'touchend', 'touchmove', 'resize', 'scroll'].forEach(event => {
            document.addEventListener(event, function(e) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }, true);
        });
        
        // مسدود کردن console
        console.clear();
        Object.defineProperty(console, 'log', { value: function() {}, writable: false });
        Object.defineProperty(console, 'warn', { value: function() {}, writable: false });
        Object.defineProperty(console, 'error', { value: function() {}, writable: false });
        
        // مسدود کردن Developer Tools
        Object.defineProperty(window, 'devtools', { value: {}, writable: false });
        Object.defineProperty(window, 'chrome', { value: undefined, writable: false });
    }
    
    // تشخیص Developer Tools - روش قوی
    let devtoolsOpen = false;
    
    function checkDevTools() {
        const threshold = 30;
        const heightDiff = window.outerHeight - window.innerHeight;
        const widthDiff = window.outerWidth - window.innerWidth;
        
        if (heightDiff > threshold || widthDiff > threshold) {
            if (!devtoolsOpen) {
                devtoolsOpen = true;
                blockImmediately();
            }
        }
    }
    
    // بررسی مداوم
    setInterval(checkDevTools, 10);
    
    // مسدود کردن کلیدها
    document.addEventListener('keydown', function(e) {
        if (e.keyCode === 123 || // F12
            (e.ctrlKey && e.shiftKey && e.keyCode === 73) || // Ctrl+Shift+I
            (e.ctrlKey && e.shiftKey && e.keyCode === 67) || // Ctrl+Shift+C
            (e.ctrlKey && e.shiftKey && e.keyCode === 74) || // Ctrl+Shift+J
            (e.ctrlKey && e.keyCode === 85)) { // Ctrl+U
            e.preventDefault();
            blockImmediately();
            return false;
        }
    }, true);
    
    // مسدود کردن راست کلیک
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        blockImmediately();
        return false;
    }, true);
    
    // مسدود کردن انتخاب متن
    document.addEventListener('selectstart', function(e) {
        e.preventDefault();
        return false;
    }, true);
    
    // بررسی اولیه
    checkDevTools();
    
    // بررسی بعد از load
    window.addEventListener('load', checkDevTools);
    window.addEventListener('resize', checkDevTools);
    
    // مسدود کردن تمام منابع
    const originalOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function() {
        if (devtoolsOpen) {
            throw new Error('Access denied');
        }
        return originalOpen.apply(this, arguments);
    };
    
    // مسدود کردن fetch
    const originalFetch = window.fetch;
    window.fetch = function() {
        if (devtoolsOpen) {
            throw new Error('Access denied');
        }
        return originalFetch.apply(this, arguments);
    };
    
})();
