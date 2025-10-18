// XSS Protection Script
(function() {
    'use strict';
    
    // Sanitize HTML content
    function sanitizeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
    
    // Escape HTML characters
    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#x27;')
            .replace(/\//g, '&#x2F;');
    }
    
    // Prevent script injection
    function preventScriptInjection() {
        // Remove any script tags
        const scripts = document.querySelectorAll('script');
        scripts.forEach(script => {
            if (script.src && !script.src.startsWith(window.location.origin)) {
                script.remove();
            }
        });
        
        // Monitor for new script tags
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.tagName === 'SCRIPT' && node.src && !node.src.startsWith(window.location.origin)) {
                        node.remove();
                    }
                });
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // Prevent eval and Function constructor
    function preventEval() {
        const originalEval = window.eval;
        window.eval = function(code) {
            console.warn('eval() is disabled for security reasons');
            return null;
        };
        
        const originalFunction = window.Function;
        window.Function = function() {
            console.warn('Function constructor is disabled for security reasons');
            return function() {};
        };
    }
    
    // Sanitize form inputs
    function sanitizeInputs() {
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', function(e) {
                const value = e.target.value;
                // Remove potentially dangerous characters
                const sanitized = value.replace(/[<>'"&]/g, '');
                if (value !== sanitized) {
                    e.target.value = sanitized;
                }
            });
        });
    }
    
    // Initialize XSS protection
    function initXSSProtection() {
        preventScriptInjection();
        preventEval();
        sanitizeInputs();
        
        console.log('%c🛡️ XSS Protection Active', 'color: #00ff00; font-size: 16px; font-weight: bold;');
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initXSSProtection);
    } else {
        initXSSProtection();
    }
    
    // Export functions for use
    window.XSSProtection = {
        sanitizeHTML: sanitizeHTML,
        escapeHTML: escapeHTML
    };
})();
