// Developer Tools Protection Script
(function() {
    'use strict';
    
    // بررسی اینکه آیا کاربر ادمین است یا نه
    function isAdmin() {
        // بررسی از طریق Django template context
        if (typeof window.isAdmin !== 'undefined') {
            return window.isAdmin;
        }
        
        // بررسی از طریق URL یا کلاس‌های CSS
        if (document.body.classList.contains('admin-user')) {
            return true;
        }
        
        // بررسی از طریق localStorage (اختیاری)
        if (localStorage.getItem('isAdmin') === 'true') {
            return true;
        }
        
        return false;
    }
    
    // اگر کاربر ادمین است، محافظت را غیرفعال کن
    if (isAdmin()) {
        console.log('%c🔓 Developer Tools Protection Disabled for Admin', 'color: #00ff00; font-size: 16px; font-weight: bold;');
        return;
    }
    
    // آیکون ممنوع برای نمایش به جای محتوا
    const forbiddenIcon = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            font-family: 'Vazir', 'Tahoma', sans-serif;
            color: #ff4444;
            text-align: center;
            direction: rtl;
        ">
            <div style="
                font-size: 8rem;
                margin-bottom: 2rem;
                animation: pulse 2s infinite;
            ">🚫</div>
            <h1 style="
                font-size: 2.5rem;
                margin-bottom: 1rem;
                color: #ff4444;
                text-shadow: 0 0 20px rgba(255, 68, 68, 0.5);
            ">دسترسی غیرمجاز</h1>
            <p style="
                font-size: 1.2rem;
                color: #cccccc;
                max-width: 500px;
                line-height: 1.6;
            ">استفاده از Developer Tools در این سایت مجاز نیست</p>
            <div style="
                margin-top: 2rem;
                padding: 1rem 2rem;
                background: rgba(255, 68, 68, 0.1);
                border: 2px solid #ff4444;
                border-radius: 10px;
                color: #ff6666;
            ">
                لطفاً Developer Tools را ببندید و صفحه را رفرش کنید
            </div>
        </div>
    `;
    
    // CSS برای انیمیشن
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .devtools-warning {
            animation: shake 0.5s ease-in-out;
        }
    `;
    document.head.appendChild(style);
    
    let devtoolsOpen = false;
    let warningShown = false;
    
    // تابع تشخیص باز بودن Developer Tools
    function detectDevTools() {
        const threshold = 160;
        
        // روش 1: بررسی اندازه صفحه
        if (window.outerHeight - window.innerHeight > threshold || 
            window.outerWidth - window.innerWidth > threshold) {
            return true;
        }
        
        // روش 2: بررسی console
        let devtools = false;
        const element = new Image();
        Object.defineProperty(element, 'id', {
            get: function() {
                devtools = true;
                throw new Error('DevTools detected');
            }
        });
        
        try {
            console.log(element);
            console.clear();
        } catch (e) {
            devtools = true;
        }
        
        return devtools;
    }
    
    // تابع نمایش هشدار
    function showWarning() {
        if (warningShown) return;
        
        warningShown = true;
        
        // مخفی کردن محتوای اصلی
        document.body.style.display = 'none';
        
        // اضافه کردن آیکون ممنوع
        document.body.innerHTML = forbiddenIcon;
        document.body.style.display = 'block';
        
        // اضافه کردن کلاس انیمیشن
        document.body.classList.add('devtools-warning');
        
        // پخش صدای هشدار (اختیاری)
        try {
            const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT');
            audio.volume = 0.3;
            audio.play().catch(() => {});
        } catch (e) {}
        
        // لاگ کردن تلاش دسترسی
        console.clear();
        console.log('%c🚫 دسترسی غیرمجاز به Developer Tools', 'color: #ff4444; font-size: 20px; font-weight: bold;');
        console.log('%cاین سایت از Developer Tools محافظت می‌شود', 'color: #ff6666; font-size: 14px;');
    }
    
    // تابع مخفی کردن هشدار
    function hideWarning() {
        if (!warningShown) return;
        
        warningShown = false;
        devtoolsOpen = false;
        
        // بازگردانی محتوای اصلی
        location.reload();
    }
    
    // بررسی مداوم Developer Tools
    function checkDevTools() {
        const isOpen = detectDevTools();
        
        if (isOpen && !devtoolsOpen) {
            devtoolsOpen = true;
            showWarning();
        } else if (!isOpen && devtoolsOpen) {
            hideWarning();
        }
    }
    
    // رویدادهای مختلف برای تشخیص Developer Tools
    const events = [
        'resize',
        'mousemove',
        'keydown',
        'keyup',
        'click',
        'scroll'
    ];
    
    // اضافه کردن event listeners
    events.forEach(event => {
        document.addEventListener(event, checkDevTools, true);
    });
    
    // بررسی اولیه
    setTimeout(checkDevTools, 1000);
    
    // بررسی مداوم هر 500 میلی‌ثانیه
    setInterval(checkDevTools, 500);
    
    // محافظت از راست کلیک
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });
    
    // محافظت از کلیدهای میانبر
    document.addEventListener('keydown', function(e) {
        // F12
        if (e.keyCode === 123) {
            e.preventDefault();
            showWarning();
            return false;
        }
        
        // Ctrl+Shift+I
        if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
            e.preventDefault();
            showWarning();
            return false;
        }
        
        // Ctrl+Shift+J
        if (e.ctrlKey && e.shiftKey && e.keyCode === 74) {
            e.preventDefault();
            showWarning();
            return false;
        }
        
        // Ctrl+U
        if (e.ctrlKey && e.keyCode === 85) {
            e.preventDefault();
            showWarning();
            return false;
        }
        
        // Ctrl+S
        if (e.ctrlKey && e.keyCode === 83) {
            e.preventDefault();
            showWarning();
            return false;
        }
    });
    
    // محافظت از انتخاب متن
    document.addEventListener('selectstart', function(e) {
        e.preventDefault();
        return false;
    });
    
    // محافظت از drag
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
        return false;
    });
    
    // مخفی کردن source در view-source
    if (window.location.protocol === 'view-source:') {
        window.location.href = window.location.href.replace('view-source:', '');
    }
    
    console.log('%c🛡️ Developer Tools Protection Active', 'color: #00ff00; font-size: 16px; font-weight: bold;');
    
})();
