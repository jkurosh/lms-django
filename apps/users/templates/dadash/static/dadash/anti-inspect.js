// HeyVoonak Anti-Inspect Protection
(function() {
    'use strict';
    
    // پیام خطا برای کاربران غیرمجاز
    const accessDeniedMessage = `
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>دسترسی محدود - HeyVoonak</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Vazir', Arial, sans-serif;
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
            .icon {
                font-size: 64px;
                margin-bottom: 20px;
                opacity: 0.8;
            }
            h1 {
                font-size: 28px;
                margin-bottom: 15px;
                font-weight: 600;
            }
            p {
                font-size: 16px;
                line-height: 1.6;
                opacity: 0.9;
                margin-bottom: 20px;
            }
            .btn {
                background: linear-gradient(45deg, #ff6b6b, #ee5a24);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                margin-top: 10px;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🚫</div>
            <h1>شما دسترسی ندارید</h1>
            <p>این صفحه برای کاربران عادی قابل مشاهده نیست. لطفاً از طریق راه‌های مجاز وارد شوید.</p>
            <a href="/" class="btn">بازگشت به صفحه اصلی</a>
        </div>
    </body>
    </html>
    `;
    
    // تشخیص Developer Tools - فوق‌العاده قوی
    let devtools = { open: false, orientation: null };
    const threshold = 50; // کاهش بیشتر threshold
    
    // تابع نمایش پیام دسترسی محدود
    function showAccessDenied() {
        document.body.innerHTML = accessDeniedMessage;
        document.body.style.overflow = 'hidden';
        document.documentElement.style.overflow = 'hidden';
        document.documentElement.style.margin = '0';
        document.documentElement.style.padding = '0';
        
        // جلوگیری از بازگشت
        window.history.pushState(null, null, window.location.href);
        window.onpopstate = function() {
            window.history.pushState(null, null, window.location.href);
        };
        
        // مسدود کردن تمام کلیدها
        document.addEventListener('keydown', function(e) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }, true);
        
        // مسدود کردن تمام mouse events
        document.addEventListener('mousedown', function(e) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }, true);
        
        // مسدود کردن تمام touch events
        document.addEventListener('touchstart', function(e) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }, true);
    }
    
    // بررسی مداوم Developer Tools
    setInterval(function() {
        // بررسی اندازه پنجره
        const heightDiff = window.outerHeight - window.innerHeight;
        const widthDiff = window.outerWidth - window.innerWidth;
        
        // بررسی کنسول با debugger
        let devtoolsOpen = false;
        const before = Date.now();
        debugger;
        const after = Date.now();
        if (after - before > 50) {
            devtoolsOpen = true;
        }
        
        // بررسی اندازه صفحه
        if (heightDiff > threshold || widthDiff > threshold || devtoolsOpen) {
            if (!devtools.open) {
                devtools.open = true;
                showAccessDenied();
            }
        } else {
            devtools.open = false;
        }
    }, 50); // افزایش فرکانس بررسی
    
    // روش تشخیص اضافی - بررسی کنسول
    let consoleCheck = function() {
        const start = performance.now();
        console.clear();
        console.log('%c', 'font-size: 1px;');
        const end = performance.now();
        if (end - start > 1) {
            devtools.open = true;
            showAccessDenied();
        }
    };
    
    // بررسی مداوم کنسول
    setInterval(consoleCheck, 100);
    
    // تشخیص فوری Developer Tools
    let immediateCheck = function() {
        if (window.outerHeight - window.innerHeight > 50 || 
            window.outerWidth - window.innerWidth > 50) {
            devtools.open = true;
            showAccessDenied();
        }
    };
    
    // بررسی فوری
    immediateCheck();
    
    // بررسی فوری بعد از load
    window.addEventListener('load', immediateCheck);
    window.addEventListener('resize', immediateCheck);
    
    // تشخیص تغییرات DOM برای Developer Tools
    let devtoolsObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes') {
                // اگر attribute های مشکوک اضافه شد
                if (mutation.attributeName === 'style' || 
                    mutation.attributeName === 'class') {
                    devtools.open = true;
                    document.body.innerHTML = accessDeniedMessage;
                    document.body.style.overflow = 'hidden';
                }
            }
        });
    });
    
    // شروع نظارت بر تغییرات
    devtoolsObserver.observe(document.body, {
        attributes: true,
        childList: true,
        subtree: true
    });
    
    // تشخیص تغییرات در window
    let lastInnerHeight = window.innerHeight;
    let lastInnerWidth = window.innerWidth;
    
    setInterval(function() {
        if (window.innerHeight !== lastInnerHeight || 
            window.innerWidth !== lastInnerWidth) {
            lastInnerHeight = window.innerHeight;
            lastInnerWidth = window.innerWidth;
            
            // اگر تغییر قابل توجه باشد
            if (Math.abs(window.outerHeight - window.innerHeight) > 50 ||
                Math.abs(window.outerWidth - window.innerWidth) > 50) {
                devtools.open = true;
                document.body.innerHTML = accessDeniedMessage;
                document.body.style.overflow = 'hidden';
            }
        }
    }, 50);
    
    // مسدود کردن کلیدهای Developer Tools
    document.addEventListener('keydown', function(e) {
        // F12
        if (e.keyCode === 123) {
            e.preventDefault();
            e.stopPropagation();
            document.body.innerHTML = accessDeniedMessage;
            document.body.style.overflow = 'hidden';
            return false;
        }
        
        // Ctrl+Shift+I
        if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
            e.preventDefault();
            document.body.innerHTML = accessDeniedMessage;
            return false;
        }
        
        // Ctrl+Shift+C
        if (e.ctrlKey && e.shiftKey && e.keyCode === 67) {
            e.preventDefault();
            document.body.innerHTML = accessDeniedMessage;
            return false;
        }
        
        // Ctrl+Shift+J
        if (e.ctrlKey && e.shiftKey && e.keyCode === 74) {
            e.preventDefault();
            document.body.innerHTML = accessDeniedMessage;
            return false;
        }
        
        // Ctrl+U (View Source)
        if (e.ctrlKey && e.keyCode === 85) {
            e.preventDefault();
            document.body.innerHTML = accessDeniedMessage;
            return false;
        }
    });
    
    // مسدود کردن راست کلیک
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        document.body.innerHTML = accessDeniedMessage;
        return false;
    });
    
    // پنهان کردن console
    console.clear();
    console.log = function() {};
    console.warn = function() {};
    console.error = function() {};
    console.info = function() {};
    console.debug = function() {};
    console.trace = function() {};
    console.table = function() {};
    console.group = function() {};
    console.groupEnd = function() {};
    console.time = function() {};
    console.timeEnd = function() {};
    
    // مسدود کردن انتخاب متن
    document.addEventListener('selectstart', function(e) {
        // فقط در input fields اجازه انتخاب
        if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            return false;
        }
    });
    
    // مسدود کردن drag & drop
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
        return false;
    });
    
    // مخفی کردن Network Tab
    const originalFetch = window.fetch;
    window.fetch = function() {
        // در صورت تشخیص Developer Tools، پیام خطا نمایش دهید
        if (devtools.open) {
            document.body.innerHTML = accessDeniedMessage;
            return Promise.reject(new Error('Access denied'));
        }
        return originalFetch.apply(this, arguments);
    };
    
    // مخفی کردن XMLHttpRequest
    const originalXHR = window.XMLHttpRequest;
    window.XMLHttpRequest = function() {
        const xhr = new originalXHR();
        const originalOpen = xhr.open;
        xhr.open = function() {
            if (devtools.open) {
                document.body.innerHTML = accessDeniedMessage;
                throw new Error('Access denied');
            }
            return originalOpen.apply(this, arguments);
        };
        return xhr;
    };
    
    // پاک کردن محتوا در صورت تشخیص inspect
    setInterval(function() {
        if (devtools.open) {
            document.body.innerHTML = accessDeniedMessage;
            document.body.style.overflow = 'hidden';
        }
    }, 1000);
    
    // مخفی کردن اطلاعات حساس از Network Tab
    const originalXMLHttpRequest = window.XMLHttpRequest;
    window.XMLHttpRequest = function() {
        const xhr = new originalXMLHttpRequest();
        const originalSend = xhr.send;
        xhr.send = function(data) {
            // مخفی کردن درخواست‌ها در Developer Tools
            if (devtools.open) {
                document.body.innerHTML = accessDeniedMessage;
                return;
            }
            return originalSend.call(this, data);
        };
        return xhr;
    };
    
    // مخفی کردن fetch requests
    const originalFetch = window.fetch;
    window.fetch = function() {
        if (devtools.open) {
            document.body.innerHTML = accessDeniedMessage;
            return Promise.reject(new Error('Access denied'));
        }
        return originalFetch.apply(this, arguments);
    };
    
    // مخفی کردن WebSocket connections
    const originalWebSocket = window.WebSocket;
    window.WebSocket = function() {
        if (devtools.open) {
            document.body.innerHTML = accessDeniedMessage;
            throw new Error('Access denied');
        }
        return new originalWebSocket.apply(this, arguments);
    };
    
    // جلوگیری از مشاهده منابع صفحه
    document.addEventListener('DOMContentLoaded', function() {
        // مخفی کردن تمام منابع
        const links = document.querySelectorAll('link[rel="stylesheet"]');
        const scripts = document.querySelectorAll('script');
        
        // اگر Developer Tools باز باشد، منابع را مخفی کنید
        if (devtools.open) {
            links.forEach(link => link.style.display = 'none');
            scripts.forEach(script => script.style.display = 'none');
        }
    });
    
    // مسدود کردن کلیدهای اضافی
    document.addEventListener('keydown', function(e) {
        // Ctrl+Shift+Delete
        if (e.ctrlKey && e.shiftKey && e.keyCode === 46) {
            e.preventDefault();
            document.body.innerHTML = accessDeniedMessage;
            return false;
        }
        
        // Ctrl+Shift+K (Firefox Console)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 75) {
            e.preventDefault();
            document.body.innerHTML = accessDeniedMessage;
            return false;
        }
    });
    
})();
