// داده‌های نمونه برای اپلیکیشن
const appData = {
    categories: {
        internal: {
            name: "بیماری‌های داخلی",
            subcategories: {
                gastrointestinal: {
                    name: "گوارشی",
                    cases: [
                        {
                            id: 1,
                            title: "استفراغ حاد در سگ 3 ساله Golden Retriever",
                            patientHistory: "Max یک سگ نر Golden Retriever 3 ساله است که با شروع حاد استفراغ در 12 ساعت گذشته مراجعه کرده است. صاحب گزارش می‌دهد که Max بی‌حال بوده و از دیروز صبح غذا نخورده است. سابقه‌ای از بی‌مبالاتی غذایی یا قرار گرفتن در معرض سموم وجود ندارد. معاینه فیزیکی نشان‌دهنده کم‌آبی خفیف و ناراحتی شکمی است.",
                            difficultyLevel: "متوسط",
                            estimatedTime: 20,
                            tests: [
                                {
                                    name: "شمارش کامل خون (CBC)",
                                    description: "آزمایش خون روتین برای ارزیابی عفونت، التهاب یا کم‌خونی. این تست اطلاعات مهمی درباره وضعیت سیستم ایمنی و سلامت کلی ارائه می‌دهد.",
                                    result: "WBC: 18,500/μL (طبیعی: 4,000-15,500)\nNeutrophils: 85% (طبیعی: 60-77%)\nLymphocytes: 10% (طبیعی: 12-30%)\nMonocytes: 3% (طبیعی: 3-10%)\nEosinophils: 1% (طبیعی: 2-10%)\nBasophils: 1% (طبیعی: 0-3%)\nRBC: 6.2 M/μL (طبیعی: 5.5-8.5)\nHemoglobin: 14.2 g/dL (طبیعی: 12-18)\nHematocrit: 42% (طبیعی: 37-55%)\nPlatelets: 250,000/μL (طبیعی: 200,000-500,000)",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "پنل شیمی سرم",
                                    description: "ارزیابی عملکرد اندام‌ها و تعادل الکترولیت‌ها. این تست برای تشخیص مشکلات کبدی، کلیوی و متابولیک ضروری است.",
                                    result: "Glucose: 95 mg/dL (طبیعی: 70-140)\nBUN: 45 mg/dL (طبیعی: 7-27) ⚠️\nCreatinine: 2.1 mg/dL (طبیعی: 0.5-1.8) ⚠️\nALT: 180 U/L (طبیعی: 10-100) ⚠️\nAST: 85 U/L (طبیعی: 15-66) ⚠️\nAlkaline Phosphatase: 120 U/L (طبیعی: 20-150)\nTotal Protein: 6.8 g/dL (طبیعی: 5.4-7.4)\nAlbumin: 3.2 g/dL (طبیعی: 2.7-4.4)\nSodium: 142 mEq/L (طبیعی: 140-150)\nPotassium: 4.1 mEq/L (طبیعی: 3.5-5.5)\nChloride: 105 mEq/L (طبیعی: 105-115)",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "رادیوگرافی شکم",
                                    description: "رادیوگرافی بررسی برای تشخیص جسم خارجی، انسداد یا تغییرات ساختاری در اندام‌های شکمی.",
                                    result: "هیچ جسم خارجی واضحی دیده نمی‌شود.\nاتساع خفیف گاز در روده کوچک.\nکبد در اندازه طبیعی.\nطحال کمی بزرگ شده.\nکلیه‌ها در موقعیت طبیعی.\nمثانه خالی است.",
                                    image: "https://via.placeholder.com/400x300/4CAF50/white?text=Abdominal+X-ray+Image",
                                    required: true
                                },
                                {
                                    name: "آزمایش ادرار",
                                    description: "بررسی وضعیت کلیه‌ها و سیستم ادراری. این تست اطلاعات مهمی درباره هیدراسیون و عملکرد کلیوی ارائه می‌دهد.",
                                    result: "رنگ: زرد تیره\nشفافیت: کدر\npH: 6.5 (طبیعی: 5.5-7.5)\nوزن مخصوص: 1.035 (طبیعی: 1.015-1.045)\nپروتئین: +1 (طبیعی: منفی)\nگلوکز: منفی\nکتون: منفی\nخون: منفی\nلکوسیت: 5-10/HPF (طبیعی: 0-5)\nاریتروسیت: 0-2/HPF (طبیعی: 0-3)",
                                    image: null,
                                    required: false
                                }
                            ],
                            options: [
                                { text: "انسداد جسم خارجی معده", isCorrect: false },
                                { text: "پانکراتیت حاد", isCorrect: true },
                                { text: "عفونت پاروویروس", isCorrect: false },
                                { text: "بیماری آدیسون", isCorrect: false }
                            ],
                            explanation: "این مورد نمایانگر پانکراتیت حاد در سگ است. افزایش تعداد WBC با نوتروفیلی نشان‌دهنده التهاب است، در حالی که افزایش BUN و کراتینین نشان‌دهنده کم‌آبی و درگیری احتمالی کلیه است. افزایش ALT نشان‌دهنده نشت آنزیم‌های کبدی است که در پانکراتیت شایع است. ناراحتی شکمی و استفراغ علائم کلاسیک پانکراتیت هستند.\n\nدرمان شامل مایع‌درمانی، ضد استفراغ، مدیریت درد و عدم تغذیه به مدت 24-48 ساعت و سپس رژیم کم‌چرب خواهد بود."
                        },
                        {
                            id: 2,
                            title: "اسهال مزمن در گربه 5 ساله",
                            patientHistory: "Luna یک گربه ماده 5 ساله Persian است که با اسهال مزمن به مدت 3 هفته مراجعه کرده است. صاحب گزارش می‌دهد که Luna بی‌اشتها بوده و وزن از دست داده است. هیچ تغییر اخیری در رژیم غذایی وجود نداشته است.",
                            difficultyLevel: "پیشرفته",
                            estimatedTime: 25,
                            tests: [
                                {
                                    name: "آزمایش مدفوع",
                                    description: "بررسی وجود انگل‌ها، باکتری‌های بیماری‌زا و خون مخفی. این تست برای تشخیص مشکلات گوارشی ضروری است.",
                                    result: "رنگ: قهوه‌ای تیره\nقوام: نرم تا آبکی\nخون مخفی: منفی\nلکوسیت: 0-2/HPF\nاریتروسیت: منفی\nکشت باکتری: منفی\nتست انگل: منفی\nGiardia: منفی\nCoccidia: منفی",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "شمارش کامل خون (CBC)",
                                    description: "ارزیابی وضعیت کلی سلامت، کم‌خونی و التهاب. این تست اطلاعات مهمی درباره وضعیت سیستم ایمنی ارائه می‌دهد.",
                                    result: "WBC: 12,500/μL (طبیعی: 4,000-15,500)\nNeutrophils: 65% (طبیعی: 60-77%)\nLymphocytes: 25% (طبیعی: 12-30%)\nMonocytes: 8% (طبیعی: 3-10%)\nEosinophils: 2% (طبیعی: 2-10%)\nRBC: 5.8 M/μL (طبیعی: 5.5-8.5) ⚠️\nHemoglobin: 11.5 g/dL (طبیعی: 12-18) ⚠️\nHematocrit: 35% (طبیعی: 37-55%) ⚠️\nMCV: 60 fL (طبیعی: 60-77)\nMCH: 20 pg (طبیعی: 19-23)\nPlatelets: 280,000/μL (طبیعی: 200,000-500,000)",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "پنل شیمی سرم",
                                    description: "ارزیابی عملکرد اندام‌ها و تشخیص مشکلات متابولیک. این تست برای تشخیص بیماری‌های سیستمیک ضروری است.",
                                    result: "Glucose: 88 mg/dL (طبیعی: 70-140)\nBUN: 15 mg/dL (طبیعی: 7-27)\nCreatinine: 0.9 mg/dL (طبیعی: 0.5-1.8)\nALT: 45 U/L (طبیعی: 10-100)\nAST: 38 U/L (طبیعی: 15-66)\nAlkaline Phosphatase: 95 U/L (طبیعی: 20-150)\nTotal Protein: 5.8 g/dL (طبیعی: 5.4-7.4)\nAlbumin: 2.1 g/dL (طبیعی: 2.5-4.0) ⚠️\nGlobulin: 3.7 g/dL (طبیعی: 2.8-4.5)\nSodium: 140 mEq/L (طبیعی: 140-150)\nPotassium: 4.3 mEq/L (طبیعی: 3.5-5.5)",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "سونوگرافی شکم",
                                    description: "بررسی دقیق اندام‌های شکمی و تشخیص تغییرات ساختاری. این تست برای تشخیص بیماری‌های گوارشی و التهابی مفید است.",
                                    result: "کبد: اندازه طبیعی، اکوژنیک یکنواخت\nطحال: اندازه طبیعی\nکلیه‌ها: اندازه طبیعی، اکوژنیک طبیعی\nروده کوچک: دیواره ضخیم شده (4-5mm)\nروده بزرگ: طبیعی\nگره‌های لنفاوی: چندین گره بزرگ شده در ناحیه مزانتر\nمایع آزاد: منفی",
                                    image: "https://via.placeholder.com/400x300/2196F3/white?text=Abdominal+Ultrasound",
                                    required: false
                                }
                            ],
                            options: [
                                { text: "بیماری التهابی روده", isCorrect: true },
                                { text: "عفونت انگلی", isCorrect: false },
                                { text: "سرطان روده", isCorrect: false },
                                { text: "مسمومیت غذایی", isCorrect: false }
                            ],
                            explanation: "این مورد نمایانگر بیماری التهابی روده (IBD) است. اسهال مزمن، کاهش وزن و کم‌آلبومینمی علائم کلاسیک IBD هستند. تشخیص قطعی با بیوپسی روده انجام می‌شود."
                        }
                    ]
                },
                cardiovascular: {
                    name: "قلب و عروق",
                    cases: [
                        {
                            id: 3,
                            title: "سرفه در سگ 8 ساله",
                            patientHistory: "Buddy یک سگ نر 8 ساله است که با سرفه مزمن به مدت 2 ماه مراجعه کرده است. سرفه در شب و هنگام فعالیت بدنی بدتر می‌شود.",
                            difficultyLevel: "متوسط",
                            estimatedTime: 18,
                            tests: [
                                {
                                    name: "رادیوگرافی قفسه سینه",
                                    description: "بررسی قلب، ریه‌ها و عروق خونی قفسه سینه. این تست برای تشخیص بیماری‌های قلبی و ریوی ضروری است.",
                                    result: "قلب: بزرگ شده (VHS: 12.5، طبیعی: 8.5-10.5)\nریه‌ها: احتقان ریوی خفیف\nعروق ریوی: متسع\nریه چپ: طبیعی\nریه راست: طبیعی\nدیافراگم: طبیعی\nفضای پلور: طبیعی\nاستخوان‌ها: طبیعی",
                                    image: "https://via.placeholder.com/400x300/2196F3/white?text=Chest+X-ray+Image",
                                    required: true
                                },
                                {
                                    name: "الکتروکاردیوگرام (ECG)",
                                    description: "بررسی فعالیت الکتریکی قلب و تشخیص آریتمی‌ها. این تست برای تشخیص بیماری‌های قلبی ضروری است.",
                                    result: "ریتم: سینوسی\nضربان قلب: 140 ضربه در دقیقه\nمحور QRS: +60 درجه\nPR interval: 0.12 ثانیه\nQRS duration: 0.06 ثانیه\nQT interval: 0.28 ثانیه\nموج P: طبیعی\nموج Q: طبیعی\nموج R: طبیعی\nموج S: طبیعی\nموج T: معکوس در لیدهای II, III, aVF",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "شمارش کامل خون (CBC)",
                                    description: "ارزیابی وضعیت کلی سلامت و تشخیص کم‌خونی. این تست اطلاعات مهمی درباره وضعیت سیستم ایمنی ارائه می‌دهد.",
                                    result: "WBC: 15,200/μL (طبیعی: 4,000-15,500)\nNeutrophils: 78% (طبیعی: 60-77%)\nLymphocytes: 15% (طبیعی: 12-30%)\nMonocytes: 5% (طبیعی: 3-10%)\nEosinophils: 2% (طبیعی: 2-10%)\nRBC: 6.5 M/μL (طبیعی: 5.5-8.5)\nHemoglobin: 15.8 g/dL (طبیعی: 12-18)\nHematocrit: 48% (طبیعی: 37-55%)\nPlatelets: 320,000/μL (طبیعی: 200,000-500,000)",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "پنل شیمی سرم",
                                    description: "ارزیابی عملکرد اندام‌ها و تشخیص مشکلات متابولیک. این تست برای تشخیص بیماری‌های سیستمیک ضروری است.",
                                    result: "Glucose: 102 mg/dL (طبیعی: 70-140)\nBUN: 28 mg/dL (طبیعی: 7-27) ⚠️\nCreatinine: 1.8 mg/dL (طبیعی: 0.5-1.8)\nALT: 55 U/L (طبیعی: 10-100)\nAST: 65 U/L (طبیعی: 15-66)\nAlkaline Phosphatase: 110 U/L (طبیعی: 20-150)\nTotal Protein: 7.2 g/dL (طبیعی: 5.4-7.4)\nAlbumin: 4.1 g/dL (طبیعی: 2.7-4.4)\nSodium: 138 mEq/L (طبیعی: 140-150) ⚠️\nPotassium: 4.8 mEq/L (طبیعی: 3.5-5.5)\nChloride: 102 mEq/L (طبیعی: 105-115) ⚠️",
                                    image: null,
                                    required: true
                                }
                            ],
                            options: [
                                { text: "نارسایی احتقانی قلب", isCorrect: true },
                                { text: "برونشیت", isCorrect: false },
                                { text: "ذات‌الریه", isCorrect: false },
                                { text: "آسم", isCorrect: false }
                            ],
                            explanation: "این مورد نمایانگر نارسایی احتقانی قلب است. سرفه شبانه و بزرگ شدن قلب در رادیوگرافی علائم کلاسیک هستند."
                        }
                    ]
                }
            }
        },
        surgery: {
            name: "جراحی",
            subcategories: {
                softTissue: {
                    name: "جراحی بافت نرم",
                    cases: [
                        {
                            id: 4,
                            title: "توده شکمی در سگ 6 ساله",
                            patientHistory: "Rex یک سگ نر 6 ساله است که با توده قابل لمس در شکم مراجعه کرده است. توده در 2 هفته گذشته بزرگ‌تر شده است.",
                            difficultyLevel: "پیشرفته",
                            estimatedTime: 30,
                            tests: [
                                {
                                    name: "سونوگرافی شکم",
                                    description: "بررسی دقیق توده، اندازه‌گیری و ارزیابی اندام‌های اطراف. این تست برای تشخیص ماهیت توده و برنامه‌ریزی جراحی ضروری است.",
                                    result: "توده جامد 5x3 سانتی‌متر در ناحیه طحال\nاکوژنیک: مخلوط (هیپو و هیپراکو)\nمرز: نامنظم\nکپسول: شکسته\nاندازه دقیق: 5.2 x 3.1 x 2.8 سانتی‌متر\nحجم: تقریباً 23 میلی‌لیتر\nمتاستاز: منفی\nگره‌های لنفاوی: طبیعی\nمایع آزاد: منفی\nسایر اندام‌ها: طبیعی",
                                    image: "https://via.placeholder.com/400x300/FF9800/white?text=Abdominal+Ultrasound",
                                    required: true
                                },
                                {
                                    name: "رادیوگرافی شکم",
                                    description: "بررسی کلی شکم و تشخیص متاستاز ریوی احتمالی. این تست برای ارزیابی گسترش بیماری ضروری است.",
                                    result: "توده نرم در ناحیه طحال\nهیچ جسم خارجی دیده نمی‌شود\nکبد: اندازه طبیعی\nکلیه‌ها: طبیعی\nروده‌ها: طبیعی\nمثانه: طبیعی\nاستخوان‌ها: طبیعی\nهیچ متاستاز استخوانی دیده نمی‌شود",
                                    image: "https://via.placeholder.com/400x300/FF9800/white?text=Abdominal+X-ray",
                                    required: true
                                },
                                {
                                    name: "شمارش کامل خون (CBC)",
                                    description: "ارزیابی وضعیت کلی سلامت و تشخیص کم‌خونی. این تست برای آماده‌سازی جراحی ضروری است.",
                                    result: "WBC: 18,500/μL (طبیعی: 4,000-15,500) ⚠️\nNeutrophils: 82% (طبیعی: 60-77%) ⚠️\nLymphocytes: 12% (طبیعی: 12-30%)\nMonocytes: 4% (طبیعی: 3-10%)\nEosinophils: 2% (طبیعی: 2-10%)\nRBC: 5.9 M/μL (طبیعی: 5.5-8.5)\nHemoglobin: 13.5 g/dL (طبیعی: 12-18)\nHematocrit: 41% (طبیعی: 37-55%)\nPlatelets: 180,000/μL (طبیعی: 200,000-500,000) ⚠️",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "پنل شیمی سرم",
                                    description: "ارزیابی عملکرد اندام‌ها و آماده‌سازی برای جراحی. این تست برای تشخیص مشکلات متابولیک ضروری است.",
                                    result: "Glucose: 98 mg/dL (طبیعی: 70-140)\nBUN: 22 mg/dL (طبیعی: 7-27)\nCreatinine: 1.2 mg/dL (طبیعی: 0.5-1.8)\nALT: 75 U/L (طبیعی: 10-100)\nAST: 68 U/L (طبیعی: 15-66)\nAlkaline Phosphatase: 145 U/L (طبیعی: 20-150)\nTotal Protein: 6.8 g/dL (طبیعی: 5.4-7.4)\nAlbumin: 3.8 g/dL (طبیعی: 2.7-4.4)\nSodium: 142 mEq/L (طبیعی: 140-150)\nPotassium: 4.2 mEq/L (طبیعی: 3.5-5.5)\nChloride: 108 mEq/L (طبیعی: 105-115)",
                                    image: null,
                                    required: true
                                },
                                {
                                    name: "آزمایش انعقاد خون",
                                    description: "بررسی وضعیت انعقاد خون قبل از جراحی. این تست برای پیشگیری از خونریزی حین جراحی ضروری است.",
                                    result: "PT: 12.5 ثانیه (طبیعی: 10-14)\nPTT: 35 ثانیه (طبیعی: 25-40)\nINR: 1.1 (طبیعی: 0.8-1.2)\nفیبرینوژن: 280 mg/dL (طبیعی: 200-400)\nزمان خونریزی: 3 دقیقه (طبیعی: 2-5)",
                                    image: null,
                                    required: true
                                }
                            ],
                            options: [
                                { text: "تومور طحال", isCorrect: true },
                                { text: "آبسه", isCorrect: false },
                                { text: "فتق", isCorrect: false },
                                { text: "کیست", isCorrect: false }
                            ],
                            explanation: "این مورد نمایانگر تومور طحال است. جراحی برداشت طحال (اسپلنکتومی) درمان انتخابی است."
                        }
                    ]
                }
            }
        }
    }
};

// متغیرهای سراسری
let currentCategory = null;
let currentSubcategory = null;
let currentCase = null;
let selectedOption = null;
let attempts = 0;
const maxAttempts = 3;

// عناصر DOM
const sections = {
    categories: document.getElementById('categories-section'),
    subcategories: document.getElementById('subcategories-section'),
    cases: document.getElementById('cases-section'),
    caseStudy: document.getElementById('case-study-section')
};

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, setting up event listeners...');
    
    // Category cards
    const categoryCards = document.querySelectorAll('.category-card');
    console.log('Found category cards:', categoryCards.length);
    
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            console.log('Category card clicked:', this.dataset.category);
            const category = this.dataset.category;
            showSubcategories(category);
        });
    });

    // Back buttons
    const backToCategoriesBtn = document.getElementById('back-to-categories');
    if (backToCategoriesBtn) {
        backToCategoriesBtn.addEventListener('click', function() {
            console.log('Back to categories clicked');
            showCategories();
        });
    }

    const backToSubcategoriesBtn = document.getElementById('back-to-subcategories');
    if (backToSubcategoriesBtn) {
        backToSubcategoriesBtn.addEventListener('click', function() {
            console.log('Back to subcategories clicked');
            if (currentCategory) {
                showSubcategories(currentCategory);
            }
        });
    }

    const backToCasesBtn = document.getElementById('back-to-cases');
    if (backToCasesBtn) {
        backToCasesBtn.addEventListener('click', function() {
            console.log('Back to cases clicked');
            if (currentSubcategory) {
                showCases(currentSubcategory);
            }
        });
    }

    // Submit diagnosis
    const submitDiagnosisBtn = document.getElementById('submit-diagnosis');
    if (submitDiagnosisBtn) {
        submitDiagnosisBtn.addEventListener('click', function() {
            console.log('Submit diagnosis clicked');
            submitDiagnosis();
        });
    }

    // Next case
    const nextCaseBtn = document.getElementById('next-case');
    if (nextCaseBtn) {
        nextCaseBtn.addEventListener('click', function() {
            console.log('Next case clicked');
            nextCase();
        });
    }
    
    console.log('Event listeners set up successfully');
});

// نمایش دسته‌بندی‌ها
function showCategories() {
    sections.categories.style.display = 'block';
    sections.subcategories.style.display = 'none';
    sections.cases.style.display = 'none';
    sections.caseStudy.style.display = 'none';
}

// نمایش زیردسته‌بندی‌ها
function showSubcategories(categoryKey) {
    console.log('Showing subcategories for category:', categoryKey);
    
    currentCategory = categoryKey;
    const category = appData.categories[categoryKey];
    
    if (!category) {
        console.error('Category not found:', categoryKey);
        return;
    }

    console.log('Category data:', category);

    const categoryTitleElement = document.getElementById('category-title');
    if (categoryTitleElement) {
        categoryTitleElement.textContent = category.name;
    }
    
    const subcategoriesGrid = document.getElementById('subcategories-grid');
    if (!subcategoriesGrid) {
        console.error('Subcategories grid not found');
        return;
    }
    
    subcategoriesGrid.innerHTML = '';

    Object.entries(category.subcategories).forEach(([key, subcategory]) => {
        console.log('Creating subcategory card for:', key, subcategory);
        
        const subcategoryCard = document.createElement('div');
        subcategoryCard.className = 'subcategory-card';
        subcategoryCard.innerHTML = `
            <h4>${subcategory.name}</h4>
            <p>${subcategory.cases.length} مطالعه موردی</p>
        `;
        subcategoryCard.addEventListener('click', function() {
            console.log('Subcategory clicked:', key);
            showCases(key);
        });
        subcategoriesGrid.appendChild(subcategoryCard);
    });

    // نمایش/مخفی کردن بخش‌ها
    if (sections.categories) sections.categories.style.display = 'none';
    if (sections.subcategories) sections.subcategories.style.display = 'block';
    if (sections.cases) sections.cases.style.display = 'none';
    if (sections.caseStudy) sections.caseStudy.style.display = 'none';
    
    console.log('Subcategories displayed successfully');
}

// نمایش مطالعات موردی
function showCases(subcategoryKey) {
    currentSubcategory = subcategoryKey;
    const subcategory = appData.categories[currentCategory].subcategories[subcategoryKey];
    
    if (!subcategory) return;

    document.getElementById('subcategory-title').textContent = subcategory.name;
    
    const casesGrid = document.getElementById('cases-grid');
    casesGrid.innerHTML = '';

    subcategory.cases.forEach(caseItem => {
        const caseCard = document.createElement('div');
        caseCard.className = 'case-card';
        caseCard.innerHTML = `
            <h4>${caseItem.title}</h4>
            <p>${caseItem.patientHistory.substring(0, 150)}...</p>
            <div class="case-meta">
                <span><i class="fas fa-clock"></i> ${caseItem.estimatedTime} دقیقه</span>
                <span><i class="fas fa-signal"></i> ${caseItem.difficultyLevel}</span>
            </div>
        `;
        caseCard.addEventListener('click', () => {
            loadCase(caseItem);
        });
        casesGrid.appendChild(caseCard);
    });

    sections.categories.style.display = 'none';
    sections.subcategories.style.display = 'none';
    sections.cases.style.display = 'block';
    sections.caseStudy.style.display = 'none';
}

// بارگذاری مطالعه موردی
function loadCase(caseItem) {
    currentCase = caseItem;
    selectedOption = null;
    attempts = 0;

    // تنظیم اطلاعات مطالعه موردی
    document.getElementById('case-title').textContent = caseItem.title;
    document.getElementById('case-time').textContent = caseItem.estimatedTime;
    document.getElementById('case-difficulty').textContent = caseItem.difficultyLevel;
    document.getElementById('patient-history').textContent = caseItem.patientHistory;

    // بارگذاری تست‌ها
    const testsContainer = document.getElementById('tests-container');
    testsContainer.innerHTML = '';

    caseItem.tests.forEach((test, index) => {
        const testItem = document.createElement('div');
        testItem.className = 'test-item';
        
        // تبدیل خطوط جدید به <br> برای نمایش بهتر
        const formattedResult = test.result.replace(/\n/g, '<br>');
        
        testItem.innerHTML = `
            <h4>${test.name}</h4>
            <div class="test-description">${test.description}</div>
            <div class="test-result">${formattedResult}</div>
            ${test.image ? `
                <img src="${test.image}" alt="${test.name}" class="test-image" onclick="openImageModal('${test.image}', '${test.name}')">
            ` : ''}
            <div class="test-meta">
                <span>تست شماره ${index + 1}</span>
                <span class="${test.required ? 'test-required' : 'test-optional'}">${test.required ? 'ضروری' : 'اختیاری'}</span>
            </div>
        `;
        testsContainer.appendChild(testItem);
    });

    // بارگذاری گزینه‌ها
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';

    caseItem.options.forEach((option, index) => {
        const optionItem = document.createElement('div');
        optionItem.className = 'option-item';
        optionItem.innerHTML = `
            <div class="option-text">${index + 1}. ${option.text}</div>
        `;
        optionItem.addEventListener('click', () => {
            selectOption(optionItem, option);
        });
        optionsContainer.appendChild(optionItem);
    });

    // بازنشانی بخش‌های دیگر
    document.getElementById('diagnosis-text').value = '';
    document.getElementById('explanation-section').style.display = 'none';
    document.getElementById('attempts-count').textContent = attempts;

    sections.categories.style.display = 'none';
    sections.subcategories.style.display = 'none';
    sections.cases.style.display = 'none';
    sections.caseStudy.style.display = 'block';
}

// انتخاب گزینه
function selectOption(optionElement, option) {
    // حذف انتخاب قبلی
    document.querySelectorAll('.option-item').forEach(item => {
        item.classList.remove('selected');
    });

    // انتخاب گزینه جدید
    optionElement.classList.add('selected');
    selectedOption = option;
}

// ارسال تشخیص
function submitDiagnosis() {
    const diagnosisText = document.getElementById('diagnosis-text').value.trim();
    
    if (!diagnosisText) {
        showMessage('لطفاً تشخیص خود را بنویسید', 'error');
        return;
    }

    if (!selectedOption) {
        showMessage('لطفاً یک گزینه انتخاب کنید', 'error');
        return;
    }

    attempts++;
    document.getElementById('attempts-count').textContent = attempts;

    // بررسی صحت پاسخ
    if (selectedOption.isCorrect) {
        showMessage('تبریک! پاسخ شما صحیح است', 'success');
        showExplanation();
    } else {
        if (attempts < maxAttempts) {
            showMessage(`پاسخ نادرست. ${maxAttempts - attempts} تلاش باقی مانده`, 'error');
            // نشان دادن گزینه نادرست
            document.querySelectorAll('.option-item').forEach(item => {
                if (item.querySelector('.option-text').textContent.includes(selectedOption.text)) {
                    item.classList.add('incorrect');
                }
            });
        } else {
            showMessage('تلاش‌های شما تمام شد. پاسخ صحیح نشان داده می‌شود', 'info');
            showCorrectAnswer();
            showExplanation();
        }
    }
}

// نمایش پاسخ صحیح
function showCorrectAnswer() {
    document.querySelectorAll('.option-item').forEach(item => {
        const optionText = item.querySelector('.option-text').textContent;
        currentCase.options.forEach(option => {
            if (optionText.includes(option.text)) {
                if (option.isCorrect) {
                    item.classList.add('correct');
                } else {
                    item.classList.add('incorrect');
                }
            }
        });
    });
}

// نمایش توضیح
function showExplanation() {
    document.getElementById('explanation-content').textContent = currentCase.explanation;
    document.getElementById('explanation-section').style.display = 'block';
    
    // غیرفعال کردن دکمه ارسال
    document.getElementById('submit-diagnosis').disabled = true;
}

// مطالعه موردی بعدی
function nextCase() {
    const currentSubcategory = appData.categories[currentCategory].subcategories[currentSubcategory];
    const currentIndex = currentSubcategory.cases.findIndex(c => c.id === currentCase.id);
    const nextIndex = (currentIndex + 1) % currentSubcategory.cases.length;
    
    loadCase(currentSubcategory.cases[nextIndex]);
}

// نمایش پیام
function showMessage(message, type) {
    // حذف پیام‌های قبلی
    const existingMessage = document.querySelector('.message');
    if (existingMessage) {
        existingMessage.remove();
    }

    const messageElement = document.createElement('div');
    messageElement.className = `message ${type}`;
    messageElement.textContent = message;

    // اضافه کردن پیام به بالای صفحه
    const main = document.querySelector('.main');
    main.insertBefore(messageElement, main.firstChild);

    // حذف خودکار پیام بعد از 3 ثانیه
    setTimeout(() => {
        if (messageElement.parentNode) {
            messageElement.remove();
        }
    }, 3000);
}

// تابع کمکی برای نمایش زیردسته‌بندی‌ها (برای دکمه بازگشت)
function showSubcategories() {
    if (currentCategory) {
        showSubcategories(currentCategory);
    }
}

// تابع کمکی برای نمایش مطالعات موردی (برای دکمه بازگشت)
function showCases() {
    if (currentSubcategory) {
        showCases(currentSubcategory);
    }
}

// تابع باز کردن مودال تصویر
function openImageModal(imageSrc, imageTitle) {
    // حذف مودال قبلی اگر وجود دارد
    const existingModal = document.querySelector('.test-image-modal');
    if (existingModal) {
        existingModal.remove();
    }

    const modal = document.createElement('div');
    modal.className = 'test-image-modal';
    modal.innerHTML = `
        <span class="close" onclick="closeImageModal()">&times;</span>
        <img src="${imageSrc}" alt="${imageTitle}" title="${imageTitle}">
    `;

    document.body.appendChild(modal);
    modal.style.display = 'block';

    // بستن مودال با کلیک روی پس‌زمینه
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeImageModal();
        }
    });

    // بستن مودال با کلید Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeImageModal();
        }
    });
}

// تابع بستن مودال تصویر
function closeImageModal() {
    const modal = document.querySelector('.test-image-modal');
    if (modal) {
        modal.remove();
    }
}

// تابع بهبود نمایش تست‌ها
function enhanceTestDisplay() {
    // اضافه کردن انیمیشن به تست‌ها
    const testItems = document.querySelectorAll('.test-item');
    testItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

// فراخوانی تابع بهبود نمایش در بارگذاری تست‌ها
document.addEventListener('DOMContentLoaded', function() {
    // کدهای قبلی...
    
    // اضافه کردن event listener برای بهبود نمایش تست‌ها
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.target.id === 'tests-container') {
                enhanceTestDisplay();
            }
        });
    });

    const testsContainer = document.getElementById('tests-container');
    if (testsContainer) {
        observer.observe(testsContainer, { childList: true });
    }
}); 