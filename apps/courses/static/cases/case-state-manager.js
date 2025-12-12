/**
 * مدیریت state برای حفظ گزینه‌های انتخاب شده در تب‌های مختلف
 * 
 * این فایل مشکل ریست شدن گزینه‌ها هنگام جابجایی بین تب‌ها را حل می‌کند
 */

// ذخیره‌ساز مرکزی برای انتخاب‌های هر تست
window.testSelections = window.testSelections || {};

// Override کردن تابع displayTests برای حفظ state
(function() {
    // ذخیره تابع اصلی
    const originalDisplayTests = window.displayTests;
    
    if (typeof originalDisplayTests !== 'function') {
        console.error('displayTests function not found!');
        return;
    }
    
    // تابع جدید با قابلیت حفظ state
    window.displayTests = function(test) {
        const testType = test.title;
        
        // اگر این تست قبلاً انتخاب شده، state آن را بارگذاری کن
        if (window.testSelections[testType]) {
            console.log(`بارگذاری state ذخیره شده برای ${testType}:`, window.testSelections[testType]);
        }
        
        // فراخوانی تابع اصلی
        originalDisplayTests.call(this, test);
        
        // بازگرداندن انتخاب‌های قبلی
        if (window.testSelections[testType] && window.testSelections[testType].length > 0) {
            const obsDiv = document.getElementById("observations");
            if (obsDiv) {
                // بازگرداندن checkbox های انتخاب شده
                window.testSelections[testType].forEach(obs => {
                    const checkbox = obsDiv.querySelector(`input[value="${obs}"]`);
                    if (checkbox) {
                        checkbox.checked = true;
                        checkbox.parentElement.classList.add('selected');
                    }
                });
                
                // به‌روزرسانی selectedObservations
                if (typeof window.selectedObservations !== 'undefined') {
                    window.selectedObservations = [...window.testSelections[testType]];
                }
                
                // به‌روزرسانی شمارنده
                if (typeof window.updateSelectionCount === 'function') {
                    window.updateSelectionCount();
                }
            }
        }
    };
    
    console.log('✅ State Manager برای case detail فعال شد');
})();

// Override کردن تابع toggleObservation برای ذخیره state
(function() {
    const originalToggleObservation = window.toggleObservation;
    
    if (typeof originalToggleObservation !== 'function') {
        // اگر تابع اصلی وجود ندارد، خودمان بسازیم
        window.toggleObservation = function(checkbox) {
            const observation = checkbox.value;
            const testType = window.currentTestType;
            
            if (!window.testSelections[testType]) {
                window.testSelections[testType] = [];
            }
            
            if (checkbox.checked) {
                // اضافه کردن به لیست
                if (!window.testSelections[testType].includes(observation)) {
                    window.testSelections[testType].push(observation);
                }
                checkbox.parentElement.classList.add('selected');
            } else {
                // حذف از لیست
                const index = window.testSelections[testType].indexOf(observation);
                if (index > -1) {
                    window.testSelections[testType].splice(index, 1);
                }
                checkbox.parentElement.classList.remove('selected');
            }
            
            // به‌روزرسانی selectedObservations
            if (typeof window.selectedObservations !== 'undefined') {
                window.selectedObservations = [...window.testSelections[testType]];
            }
            
            // به‌روزرسانی شمارنده
            if (typeof window.updateSelectionCount === 'function') {
                window.updateSelectionCount();
            }
            
            console.log(`${testType} selections:`, window.testSelections[testType]);
        };
    } else {
        // Override تابع موجود
        window.toggleObservation = function(checkbox) {
            // فراخوانی تابع اصلی
            originalToggleObservation.call(this, checkbox);
            
            // ذخیره state
            const testType = window.currentTestType;
            const observation = checkbox.value;
            
            if (!window.testSelections[testType]) {
                window.testSelections[testType] = [];
            }
            
            if (checkbox.checked) {
                if (!window.testSelections[testType].includes(observation)) {
                    window.testSelections[testType].push(observation);
                }
            } else {
                const index = window.testSelections[testType].indexOf(observation);
                if (index > -1) {
                    window.testSelections[testType].splice(index, 1);
                }
            }
            
            console.log(`${testType} selections updated:`, window.testSelections[testType]);
        };
    }
})();

// تابع helper برای ریست کردن تمام انتخاب‌ها
window.resetAllSelections = function() {
    window.testSelections = {};
    window.selectedObservations = [];
    console.log('✅ تمام انتخاب‌ها ریست شد');
};

// تابع helper برای دریافت تمام انتخاب‌ها
window.getAllSelections = function() {
    return window.testSelections;
};

// نمایش وضعیت در console
console.log('📊 Case Detail State Manager loaded');
console.log('دستورات موجود:');
console.log('  - getAllSelections(): دریافت تمام انتخاب‌ها');
console.log('  - resetAllSelections(): ریست کردن تمام انتخاب‌ها');

