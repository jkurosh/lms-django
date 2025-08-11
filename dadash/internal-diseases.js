// داده‌های نمونه برای بیماری‌های داخلی
const internalDiseasesData = {
    gastrointestinal: {
        title: "بیماری‌های گوارشی",
        cases: [
            {
                id: 1,
                title: "پانکراتیت حاد در سگ",
                patientHistory: `سگ ماده 5 ساله از نژاد لابرادور با وزن 25 کیلوگرم
                
تاریخچه: بیمار از 3 روز پیش دچار بی‌اشتهایی، استفراغ و درد شکم شده است. صاحب حیوان گزارش می‌دهد که حیوان در حالت "praying position" قرار می‌گیرد و تمایل به خوردن غذا ندارد.

علائم بالینی:
- بی‌اشتهایی کامل
- استفراغ مکرر (3-4 بار در روز)
- درد شکم (حیوان هنگام لمس شکم ناله می‌کند)
- افسردگی و بی‌حالی
- کاهش وزن 2 کیلوگرمی در 3 روز گذشته

معاینه فیزیکی:
- دمای بدن: 39.2°C
- ضربان قلب: 120 ضربه در دقیقه
- تنفس: 25 بار در دقیقه
- مخاطات: کمی رنگ‌پریده
- هیدراتاسیون: 5-7% دهیدراته`,
                difficulty: "متوسط",
                estimatedTime: 25,
                tests: [
                    {
                        id: 1,
                        name: "آزمایش خون کامل (CBC)",
                        description: "بررسی تعداد سلول‌های خونی و هموگلوبین",
                        result: `WBC: 18,500/μL (افزایش)
RBC: 5.2 × 10⁶/μL (طبیعی)
Hgb: 12.5 g/dL (کمی کاهش)
Hct: 37% (کمی کاهش)
Platelets: 250,000/μL (طبیعی)

نوتروفیل: 85% (افزایش)
لنفوسیت: 10% (کاهش)
مونوسیت: 3% (طبیعی)
ائوزینوفیل: 2% (طبیعی)`,
                        isRequired: true,
                        sortOrder: 1
                    },
                    {
                        id: 2,
                        name: "پروفایل بیوشیمیایی",
                        description: "بررسی عملکرد کبد، کلیه و پانکراس",
                        result: `Glucose: 180 mg/dL (افزایش)
BUN: 45 mg/dL (افزایش)
Creatinine: 1.8 mg/dL (افزایش)
ALT: 85 U/L (افزایش خفیف)
AST: 120 U/L (افزایش)
ALP: 450 U/L (افزایش)
Total Protein: 6.2 g/dL (طبیعی)
Albumin: 2.8 g/dL (کمی کاهش)
Amylase: 2,500 U/L (افزایش شدید)
Lipase: 1,800 U/L (افزایش شدید)`,
                        isRequired: true,
                        sortOrder: 2
                    },
                    {
                        id: 3,
                        name: "رادیوگرافی شکم",
                        description: "بررسی ساختارهای شکمی و وجود گاز یا مایع",
                        result: `رادیوگرافی شکم در وضعیت راست و چپ:

- افزایش تراکم بافت نرم در ناحیه قدامی شکم
- کاهش جزئی در تراکم گاز روده
- عدم وجود جسم خارجی قابل مشاهده
- اندازه کبد در محدوده طبیعی
- کلیه‌ها در اندازه و موقعیت طبیعی`,
                        imageUrl: "https://via.placeholder.com/400x300/4CAF50/white?text=رادیوگرافی+شکم",
                        imageAltText: "رادیوگرافی شکم سگ با پانکراتیت",
                        isRequired: true,
                        sortOrder: 3
                    },
                    {
                        id: 4,
                        name: "سونوگرافی شکم",
                        description: "بررسی دقیق‌تر ارگان‌های شکمی",
                        result: `سونوگرافی شکم:

پانکراس:
- افزایش اندازه و ضخامت
- کاهش اکوژنیتی (hypoechoic)
- وجود مایع اطراف پانکراس
- عدم وجود آبسه یا نکروز

کبد:
- اندازه طبیعی
- اکوژنیتی یکنواخت
- عدم وجود توده یا ضایعه

کلیه‌ها:
- اندازه و شکل طبیعی
- عدم وجود سنگ یا هیدرونفروز`,
                        imageUrl: "https://via.placeholder.com/400x300/2196F3/white?text=سونوگرافی+شکم",
                        imageAltText: "سونوگرافی شکم سگ",
                        isRequired: false,
                        sortOrder: 4
                    }
                ],
                options: [
                    {
                        id: 1,
                        text: "پانکراتیت حاد",
                        isCorrect: true,
                        explanation: "افزایش شدید آمیلاز و لیپاز، همراه با علائم بالینی و یافته‌های رادیوگرافی و سونوگرافی، تشخیص پانکراتیت حاد را تأیید می‌کند."
                    },
                    {
                        id: 2,
                        text: "انسداد روده",
                        isCorrect: false,
                        explanation: "اگرچه استفراغ و درد شکم وجود دارد، اما رادیوگرافی نشان‌دهنده انسداد نیست و افزایش آنزیم‌های پانکراس این تشخیص را رد می‌کند."
                    },
                    {
                        id: 3,
                        text: "هپاتیت حاد",
                        isCorrect: false,
                        explanation: "اگرچه ALT و AST افزایش یافته‌اند، اما افزایش شدید آمیلاز و لیپاز و یافته‌های سونوگرافی پانکراس، تشخیص هپاتیت را رد می‌کند."
                    },
                    {
                        id: 4,
                        text: "گاستریت حاد",
                        isCorrect: false,
                        explanation: "اگرچه استفراغ وجود دارد، اما افزایش آنزیم‌های پانکراس و یافته‌های تصویربرداری، تشخیص گاستریت ساده را رد می‌کند."
                    }
                ],
                explanation: {
                    text: "این مورد یک پانکراتیت حاد کلاسیک است که با افزایش شدید آنزیم‌های پانکراس (آمیلاز و لیپاز)، علائم بالینی مشخص و یافته‌های تصویربرداری تشخیص داده می‌شود.",
                    keyLearningPoints: [
                        "افزایش آمیلاز و لیپاز > 3 برابر حد طبیعی، نشان‌دهنده پانکراتیت است",
                        "علائم بالینی شامل درد شکم، استفراغ و بی‌اشتهایی است",
                        "سونوگرافی ابزار تشخیصی ارزشمندی برای تأیید تشخیص است",
                        "درمان شامل هیدراتاسیون، کنترل درد و تغذیه مناسب است"
                    ],
                    references: [
                        "Steiner JM. Diagnosis of pancreatitis. Vet Clin North Am Small Anim Pract. 2003;33(6):1181-1195.",
                        "Watson PJ. Pancreatitis in dogs and cats: definitions and pathophysiology. J Small Anim Pract. 2015;56(1):3-12."
                    ]
                }
            },
            {
                id: 2,
                title: "IBD در گربه",
                patientHistory: `گربه نر 3 ساله از نژاد پرشین با وزن 4.5 کیلوگرم

تاریخچه: بیمار از 6 ماه پیش دچار اسهال مزمن و کاهش وزن شده است. صاحب حیوان گزارش می‌دهد که حیوان گاهی استفراغ می‌کند و اشتهای متغیری دارد.

علائم بالینی:
- اسهال مزمن (6 ماه)
- کاهش وزن 1.5 کیلوگرمی
- استفراغ متناوب
- اشتهای متغیر
- بی‌حالی خفیف

معاینه فیزیکی:
- دمای بدن: 38.5°C
- ضربان قلب: 140 ضربه در دقیقه
- تنفس: 30 بار در دقیقه
- مخاطات: طبیعی
- هیدراتاسیون: طبیعی
- وضعیت بدنی: 3/9 (لاغر)`,
                difficulty: "پیشرفته",
                estimatedTime: 30,
                tests: [
                    {
                        id: 1,
                        name: "آزمایش خون کامل (CBC)",
                        description: "بررسی تعداد سلول‌های خونی",
                        result: `WBC: 12,500/μL (افزایش خفیف)
RBC: 6.8 × 10⁶/μL (طبیعی)
Hgb: 14.2 g/dL (طبیعی)
Hct: 42% (طبیعی)
Platelets: 280,000/μL (طبیعی)

نوتروفیل: 75% (افزایش خفیف)
لنفوسیت: 20% (طبیعی)
مونوسیت: 3% (طبیعی)
ائوزینوفیل: 2% (طبیعی)`,
                        isRequired: true,
                        sortOrder: 1
                    },
                    {
                        id: 2,
                        name: "پروفایل بیوشیمیایی",
                        description: "بررسی عملکرد ارگان‌ها",
                        result: `Glucose: 95 mg/dL (طبیعی)
BUN: 25 mg/dL (طبیعی)
Creatinine: 1.2 mg/dL (طبیعی)
ALT: 65 U/L (طبیعی)
AST: 45 U/L (طبیعی)
ALP: 120 U/L (طبیعی)
Total Protein: 5.8 g/dL (کمی کاهش)
Albumin: 2.5 g/dL (کمی کاهش)
Globulin: 3.3 g/dL (افزایش خفیف)
B12: 180 pg/mL (کاهش)`,
                        isRequired: true,
                        sortOrder: 2
                    },
                    {
                        id: 3,
                        name: "آزمایش مدفوع",
                        description: "بررسی انگل‌ها و باکتری‌ها",
                        result: `آزمایش مدفوع:
- عدم وجود تخم انگل
- عدم وجود پروتوزوآ
- کشت باکتری: منفی
- تست Giardia: منفی
- تست Tritrichomonas: منفی

میکروسکوپی:
- افزایش تعداد سلول‌های التهابی
- وجود نوتروفیل‌ها و ماکروفاژها`,
                        isRequired: true,
                        sortOrder: 3
                    },
                    {
                        id: 4,
                        name: "بیوپسی روده",
                        description: "بررسی بافت‌شناسی روده",
                        result: `بیوپسی از دوازدهه و ایلئوم:

دوازدهه:
- افزایش سلول‌های التهابی در لامینا پروپریا
- هیپرپلازی سلول‌های گابلت
- ضخیم شدن لایه عضلانی مخاطی

ایلئوم:
- افزایش لنفوسیت‌ها و پلاسماسل‌ها
- آتروفی خفیف ویلی
- افزایش سلول‌های التهابی

تشخیص بافت‌شناسی: IBD (Inflammatory Bowel Disease)`,
                        isRequired: false,
                        sortOrder: 4
                    }
                ],
                options: [
                    {
                        id: 1,
                        text: "IBD (بیماری التهابی روده)",
                        isCorrect: true,
                        explanation: "علائم مزمن، یافته‌های بیوپسی و رد سایر علل، تشخیص IBD را تأیید می‌کند."
                    },
                    {
                        id: 2,
                        text: "عفونت انگلی",
                        isCorrect: false,
                        explanation: "آزمایش مدفوع منفی است و علائم مزمن با عفونت انگلی سازگار نیست."
                    },
                    {
                        id: 3,
                        text: "لنفوم روده",
                        isCorrect: false,
                        explanation: "اگرچه کاهش وزن وجود دارد، اما یافته‌های بیوپسی نشان‌دهنده لنفوم نیست."
                    },
                    {
                        id: 4,
                        text: "پانکراتیت مزمن",
                        isCorrect: false,
                        explanation: "آنزیم‌های پانکراس طبیعی هستند و علائم با پانکراتیت سازگار نیست."
                    }
                ],
                explanation: {
                    text: "IBD یک بیماری التهابی مزمن روده است که با نفوذ سلول‌های التهابی به دیواره روده مشخص می‌شود.",
                    keyLearningPoints: [
                        "IBD تشخیصی است که پس از رد سایر علل مطرح می‌شود",
                        "بیوپسی روده برای تشخیص قطعی ضروری است",
                        "درمان شامل رژیم غذایی و داروهای سرکوب‌کننده ایمنی است",
                        "پیگیری طولانی‌مدت برای کنترل بیماری ضروری است"
                    ],
                    references: [
                        "Jergens AE. Inflammatory bowel disease. Vet Clin North Am Small Anim Pract. 1999;29(2):501-521.",
                        "Simpson KW, Jergens AE. Pitfalls and progress in the diagnosis and management of canine inflammatory bowel disease. Vet Clin North Am Small Anim Pract. 2011;41(2):381-398."
                    ]
                }
            }
        ]
    },
    cardiovascular: {
        title: "بیماری‌های قلبی و عروقی",
        cases: [
            {
                id: 1,
                title: "نارسایی قلبی در سگ",
                patientHistory: `سگ نر 8 ساله از نژاد گلدن رتریور با وزن 30 کیلوگرم

تاریخچه: بیمار از 2 هفته پیش دچار سرفه شبانه و تنگی نفس شده است. صاحب حیوان گزارش می‌دهد که حیوان خیلی زود خسته می‌شود و تمایل به فعالیت ندارد.

علائم بالینی:
- سرفه شبانه
- تنگی نفس
- عدم تحمل فعالیت
- کاهش اشتها
- افزایش تشنگی و ادرار

معاینه فیزیکی:
- دمای بدن: 38.8°C
- ضربان قلب: 140 ضربه در دقیقه (نامنظم)
- تنفس: 45 بار در دقیقه
- مخاطات: کمی کبود
- هیدراتاسیون: طبیعی
- ادم خفیف در اندام‌های خلفی`,
                difficulty: "متوسط",
                estimatedTime: 25,
                tests: [
                    {
                        id: 1,
                        name: "رادیوگرافی قفسه سینه",
                        description: "بررسی اندازه قلب و ریه‌ها",
                        result: `رادیوگرافی قفسه سینه در وضعیت راست و چپ:

قلب:
- افزایش اندازه کلی قلب
- افزایش نسبت VHS (Vertebral Heart Score): 12.5
- برجستگی قوس آئورت

ریه‌ها:
- افزایش تراکم عروقی
- وجود خطوط Kerley B
- ادم ریوی خفیف در نواحی قاعدی

پلور:
- عدم وجود مایع پلور`,
                        imageUrl: "https://via.placeholder.com/400x300/FF5722/white?text=رادیوگرافی+قفسه+سینه",
                        imageAltText: "رادیوگرافی قفسه سینه سگ با نارسایی قلبی",
                        isRequired: true,
                        sortOrder: 1
                    },
                    {
                        id: 2,
                        name: "الکتروکاردیوگرام (ECG)",
                        description: "بررسی ریتم و فعالیت الکتریکی قلب",
                        result: `ECG 12-lead:

ریتم: فیبریلاسیون دهلیزی
ضربان قلب: 140 ضربه در دقیقه
محور QRS: +60 درجه (طبیعی)
عرض QRS: 0.08 ثانیه (طبیعی)

موج P: نامشخص (فیبریلاسیون دهلیزی)
فاصله PR: قابل اندازه‌گیری نیست
فاصله QT: 0.28 ثانیه (طبیعی)

تشخیص: فیبریلاسیون دهلیزی با پاسخ بطنی سریع`,
                        isRequired: true,
                        sortOrder: 2
                    },
                    {
                        id: 3,
                        name: "اکوکاردیوگرام",
                        description: "بررسی ساختار و عملکرد قلب",
                        result: `اکوکاردیوگرام:

بطن چپ:
- افزایش اندازه (LVIDd: 6.2 cm)
- کاهش کسر تخلیه (EF: 35%)
- هیپرتروفی دیواره

دهلیز چپ:
- افزایش اندازه (LA/Ao: 2.1)
- وجود ترومبوس

دریچه میترال:
- نارسایی خفیف تا متوسط
- عدم وجود تنگی

دریچه آئورت:
- طبیعی

تشخیص: کاردیومیوپاتی اتساعی با نارسایی قلبی`,
                        isRequired: false,
                        sortOrder: 3
                    }
                ],
                options: [
                    {
                        id: 1,
                        text: "کاردیومیوپاتی اتساعی با نارسایی قلبی",
                        isCorrect: true,
                        explanation: "افزایش اندازه قلب، کاهش کسر تخلیه و فیبریلاسیون دهلیزی، تشخیص کاردیومیوپاتی اتساعی را تأیید می‌کند."
                    },
                    {
                        id: 2,
                        text: "بیماری دریچه میترال",
                        isCorrect: false,
                        explanation: "اگرچه نارسایی میترال وجود دارد، اما افزایش اندازه بطن چپ و کاهش کسر تخلیه نشان‌دهنده کاردیومیوپاتی است."
                    },
                    {
                        id: 3,
                        text: "پریکاردیت",
                        isCorrect: false,
                        explanation: "عدم وجود مایع پریکارد و یافته‌های اکوکاردیوگرام، تشخیص پریکاردیت را رد می‌کند."
                    },
                    {
                        id: 4,
                        text: "تومور قلبی",
                        isCorrect: false,
                        explanation: "اکوکاردیوگرام نشان‌دهنده تومور نیست و یافته‌ها با کاردیومیوپاتی سازگار است."
                    }
                ],
                explanation: {
                    text: "کاردیومیوپاتی اتساعی یک بیماری عضله قلب است که منجر به نارسایی قلبی می‌شود.",
                    keyLearningPoints: [
                        "فیبریلاسیون دهلیزی شایع‌ترین آریتمی در کاردیومیوپاتی است",
                        "درمان شامل کنترل آریتمی و نارسایی قلبی است",
                        "پیگیری منظم برای تنظیم دارو ضروری است",
                        "پیش‌آگهی در مراحل پیشرفته ضعیف است"
                    ],
                    references: [
                        "Tidholm A, Jönsson L. A retrospective study of canine dilated cardiomyopathy (189 cases). J Am Anim Hosp Assoc. 1997;33(6):544-550.",
                        "O'Grady MR, O'Sullivan ML. Dilated cardiomyopathy: an update. Vet Clin North Am Small Anim Pract. 2004;34(5):1187-1207."
                    ]
                }
            }
        ]
    }
};

// متغیرهای سراسری
let currentSubcategory = null;
let currentCaseIndex = 0;
let currentCase = null;
let attempts = 0;
const maxAttempts = 3;

// عناصر DOM
const subcategoriesGrid = document.querySelector('.subcategories-grid');
const casesSection = document.getElementById('cases-section');
const casesGrid = document.getElementById('cases-grid');
const caseStudySection = document.getElementById('case-study-section');
const backToSubcategoriesBtn = document.getElementById('back-to-subcategories');
const backToCasesBtn = document.getElementById('back-to-cases');
const subcategoryTitle = document.getElementById('subcategory-title');
const caseTitle = document.getElementById('case-title');
const caseTime = document.getElementById('case-time');
const caseDifficulty = document.getElementById('case-difficulty');
const patientHistory = document.getElementById('patient-history');
const testButtons = document.getElementById('test-buttons');
const labReportsContainer = document.getElementById('lab-reports-container');
const optionsContainer = document.getElementById('options-container');
const attemptsCount = document.getElementById('attempts-count');
const diagnosisText = document.getElementById('diagnosis-text');
const submitDiagnosisBtn = document.getElementById('submit-diagnosis');
const explanationSection = document.getElementById('explanation-section');
const explanationContent = document.getElementById('explanation-content');
const nextCaseBtn = document.getElementById('next-case');

// رویدادهای کلیک روی کارت‌های زیردسته‌بندی
subcategoriesGrid.addEventListener('click', (e) => {
    const subcategoryCard = e.target.closest('.subcategory-card');
    if (subcategoryCard) {
        const subcategoryId = subcategoryCard.dataset.subcategory;
        showCases(subcategoryId);
    }
});

// نمایش مطالعات موردی
function showCases(subcategoryId) {
    currentSubcategory = subcategoryId;
    const subcategoryData = internalDiseasesData[subcategoryId];
    
    if (!subcategoryData) {
        alert('داده‌ای برای این زیردسته‌بندی یافت نشد!');
        return;
    }
    
    // مخفی کردن بخش زیردسته‌بندی‌ها
    document.querySelector('.subcategories-section').style.display = 'none';
    
    // نمایش بخش مطالعات موردی
    casesSection.style.display = 'block';
    subcategoryTitle.textContent = subcategoryData.title;
    
    // ایجاد کارت‌های مطالعات موردی
    casesGrid.innerHTML = '';
    subcategoryData.cases.forEach((caseStudy, index) => {
        const caseCard = createCaseCard(caseStudy, index);
        casesGrid.appendChild(caseCard);
    });
}

// ایجاد کارت مطالعه موردی
function createCaseCard(caseStudy, index) {
    const caseCard = document.createElement('div');
    caseCard.className = 'case-card';
    caseCard.innerHTML = `
        <h4>${caseStudy.title}</h4>
        <div class="case-meta">
            <span><i class="fas fa-clock"></i> ${caseStudy.estimatedTime} دقیقه</span>
            <span><i class="fas fa-signal"></i> ${caseStudy.difficulty}</span>
        </div>
    `;
    
    caseCard.addEventListener('click', () => {
        showCaseStudy(index);
    });
    
    return caseCard;
}

// نمایش مطالعه موردی
function showCaseStudy(caseIndex) {
    currentCaseIndex = caseIndex;
    currentCase = internalDiseasesData[currentSubcategory].cases[caseIndex];
    attempts = 0;
    
    // مخفی کردن بخش مطالعات موردی
    casesSection.style.display = 'none';
    
    // نمایش بخش مطالعه موردی
    caseStudySection.style.display = 'block';
    
    // پر کردن اطلاعات مطالعه موردی
    caseTitle.textContent = currentCase.title;
    caseTime.textContent = currentCase.estimatedTime;
    caseDifficulty.textContent = currentCase.difficulty;
    patientHistory.textContent = currentCase.patientHistory;
    
    // ایجاد دکمه‌های تست
    createTestButtons();
    
    // ایجاد گزینه‌ها
    createOptions();
    
    // نمایش حالت خالی گزارش‌ها
    showEmptyReports();
    
    // ریست کردن فرم‌ها
    resetForms();
}

// ایجاد دکمه‌های تست
function createTestButtons() {
    testButtons.innerHTML = '';
    
    // گروه‌بندی تست‌ها بر اساس نوع
    const testGroups = groupTestsByType(currentCase.tests);
    
    // ایجاد دکمه‌ها برای هر گروه
    Object.keys(testGroups).forEach(groupKey => {
        const group = testGroups[groupKey];
        const button = createTestButton(groupKey, group);
        testButtons.appendChild(button);
    });
}

// گروه‌بندی تست‌ها بر اساس نوع
function groupTestsByType(tests) {
    const groups = {
        'cbc': { name: 'CBC', icon: 'fas fa-tint', tests: [] },
        'chemistry': { name: 'Clinical Chemistry', icon: 'fas fa-flask', tests: [] },
        'imaging': { name: 'تصاویر تشخیصی', icon: 'fas fa-x-ray', tests: [] },
        'other': { name: 'سایر تست‌ها', icon: 'fas fa-microscope', tests: [] }
    };
    
    tests.forEach(test => {
        const testName = test.name.toLowerCase();
        
        if (testName.includes('cbc') || testName.includes('خون') || testName.includes('complete blood')) {
            groups.cbc.tests.push(test);
        } else if (testName.includes('chemistry') || testName.includes('بیوشیمی') || testName.includes('biochemistry')) {
            groups.chemistry.tests.push(test);
        } else if (testName.includes('رادیوگرافی') || testName.includes('سونوگرافی') || testName.includes('اکو') || 
                   testName.includes('x-ray') || testName.includes('ultrasound') || testName.includes('ecg')) {
            groups.imaging.tests.push(test);
        } else {
            groups.other.tests.push(test);
        }
    });
    
    // حذف گروه‌های خالی
    Object.keys(groups).forEach(key => {
        if (groups[key].tests.length === 0) {
            delete groups[key];
        }
    });
    
    return groups;
}

// ایجاد دکمه تست
function createTestButton(groupKey, group) {
    const button = document.createElement('button');
    button.className = 'test-btn';
    button.dataset.group = groupKey;
    
    button.innerHTML = `
        <span>
            <i class="${group.icon}"></i>
            ${group.name}
        </span>
        <span>${group.tests.length} تست</span>
    `;
    
    button.addEventListener('click', () => {
        // حذف کلاس active از همه دکمه‌ها
        document.querySelectorAll('.test-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // اضافه کردن کلاس active به دکمه کلیک شده
        button.classList.add('active');
        
        // نمایش گزارش‌های گروه انتخاب شده
        showLabReports(groupKey, group);
    });
    
    return button;
}

// نمایش گزارش‌های آزمایش
function showLabReports(groupKey, group) {
    labReportsContainer.innerHTML = '';
    
    // اگر گروه CBC است، جدول مخصوص CBC نمایش بده
    if (groupKey === 'cbc') {
        showCBCReport(group);
        return;
    }
    
    // ایجاد جدول گزارش‌ها برای سایر گروه‌ها
    const table = document.createElement('table');
    table.className = 'lab-reports-table';
    
    // ایجاد header جدول
    const tableHeader = `
        <thead>
            <tr>
                <th>نام تست</th>
                <th>توضیحات</th>
                <th>نتیجه</th>
                <th>اسلاید</th>
            </tr>
        </thead>
    `;
    
    // ایجاد body جدول
    let tableBody = '<tbody>';
    
    group.tests.forEach(test => {
        let slidesCell = '';
        if (test.imageUrl) {
            slidesCell = `
                <div class="test-slides">
                    <img src="${test.imageUrl}" alt="${test.imageAltText}" onclick="openImageModal('${test.imageUrl}', '${test.imageAltText}')">
                </div>
            `;
        }
        
        tableBody += `
            <tr>
                <td class="test-name">${test.name}</td>
                <td class="test-description">${test.description}</td>
                <td class="test-result">${test.result}</td>
                <td class="test-slides">${slidesCell}</td>
            </tr>
        `;
    });
    
    tableBody += '</tbody>';
    
    table.innerHTML = tableHeader + tableBody;
    labReportsContainer.appendChild(table);
}

// نمایش گزارش CBC به شکل جدول مخصوص
function showCBCReport(group) {
    const container = document.createElement('div');
    container.className = 'cbc-report-container';
    
    const title = document.createElement('h4');
    title.className = 'cbc-report-title';
    title.innerHTML = '<i class="fas fa-tint"></i> نتایج CBC';
    container.appendChild(title);
    
    const table = document.createElement('table');
    table.className = 'cbc-results-table';
    
    // داده‌های CBC بر اساس تصویر
    const cbcData = [
        { parameter: 'Hematocrit', reference: '(0.37-0.55 L/L)', result: '0.33' },
        { parameter: 'Hemoglobin', reference: '(120-180 g/L)', result: '108' },
        { parameter: 'Erythrocytes', reference: '(5.5-8.5 x 10¹² /L)', result: '4.65' },
        { parameter: 'MCV', reference: '(60-77 fL)', result: '77' },
        { parameter: 'MCHC', reference: '(320-360 g/L)', result: '300' },
        { parameter: 'Reticulocytes (%)', reference: '(<1 %)', result: '3' },
        { parameter: 'Reticulocytes (absolute)', reference: '(<60 000 x 10⁶/L)', result: '139 500' },
        { parameter: 'Platelets', reference: '(200-900 x 10⁹/L)', result: 'adequate' },
        { parameter: 'Plasma protein', reference: '(60-80 g/L)', result: '60' },
        { parameter: 'Leukocytes', reference: '(6.0-17.0 x 10⁹/L)', result: '10.8' },
        { parameter: 'Neutrophils (mature)', reference: '(3.0-11.5 x 10⁹/L)', result: '8.0' },
        { parameter: 'Neutrophils (band)', reference: '(0-0.3 x 10⁹/L)', result: '0' },
        { parameter: 'Lymphocytes', reference: '(1.0-4.8 x 10⁹/L)', result: '0.4' },
        { parameter: 'Monocytes', reference: '(<1.4 x 10⁹/L)', result: '1.2' },
        { parameter: 'Eosinophils', reference: '(0.1-1.3 x 10⁹/L)', result: '1.2' },
        { parameter: 'Basophils', reference: '(0 -scarce x 10⁹/L)', result: '0' }
    ];
    
    let tableHTML = `
        <thead>
            <tr>
                <th>پارامتر</th>
                <th>محدوده مرجع</th>
                <th>نتیجه</th>
            </tr>
        </thead>
        <tbody>
    `;
    
    cbcData.forEach(item => {
        const isAbnormal = isAbnormalResult(item.parameter, item.result, item.reference);
        tableHTML += `
            <tr class="${isAbnormal ? 'abnormal-result' : ''}">
                <td class="parameter-name">${item.parameter}</td>
                <td class="reference-range">${item.reference}</td>
                <td class="result-value ${isAbnormal ? 'abnormal' : ''}">${item.result}</td>
            </tr>
        `;
    });
    
    tableHTML += '</tbody>';
    table.innerHTML = tableHTML;
    
    container.appendChild(table);
    labReportsContainer.appendChild(container);
}

// بررسی نتایج غیرطبیعی
function isAbnormalResult(parameter, result, reference) {
    // این تابع می‌تواند منطق پیچیده‌تری برای تشخیص نتایج غیرطبیعی داشته باشد
    const abnormalResults = ['0.33', '108', '4.65', '300', '3', '139 500', '0.4', '0'];
    return abnormalResults.includes(result);
}

// نمایش حالت خالی گزارش‌ها
function showEmptyReports() {
    labReportsContainer.innerHTML = `
        <div class="lab-reports-empty">
            <i class="fas fa-flask"></i>
            <h4>هیچ آزمایشی انتخاب نشده</h4>
            <p>برای مشاهده گزارش‌های آزمایش، روی یکی از دکمه‌های سمت راست کلیک کنید</p>
        </div>
    `;
}





// ایجاد گزینه‌های پاسخ
function createOptions() {
    optionsContainer.innerHTML = '';
    
    currentCase.options.forEach(option => {
        const optionItem = document.createElement('div');
        optionItem.className = 'option-item';
        optionItem.dataset.optionId = option.id;
        
        optionItem.innerHTML = `
            <div class="option-text">${option.text}</div>
        `;
        
        optionItem.addEventListener('click', () => {
            selectOption(optionItem, option);
        });
        
        optionsContainer.appendChild(optionItem);
    });
}

// انتخاب گزینه
function selectOption(optionElement, option) {
    // حذف انتخاب قبلی
    document.querySelectorAll('.option-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // انتخاب گزینه جدید
    optionElement.classList.add('selected');
    
    // فعال کردن دکمه ارسال
    submitDiagnosisBtn.disabled = false;
}

// ریست کردن فرم‌ها
function resetForms() {
    diagnosisText.value = '';
    submitDiagnosisBtn.disabled = true;
    explanationSection.style.display = 'none';
    
    document.querySelectorAll('.option-item').forEach(item => {
        item.classList.remove('selected', 'correct', 'incorrect');
    });
    
    // ریست کردن بخش دکمه‌های تست
    document.querySelectorAll('.test-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // نمایش حالت خالی گزارش‌ها
    showEmptyReports();
    
    attempts = 0;
    attemptsCount.textContent = attempts;
}

// ارسال تشخیص
submitDiagnosisBtn.addEventListener('click', () => {
    const selectedOption = document.querySelector('.option-item.selected');
    
    if (!selectedOption) {
        alert('لطفاً یک گزینه انتخاب کنید!');
        return;
    }
    
    attempts++;
    attemptsCount.textContent = attempts;
    
    const selectedOptionId = parseInt(selectedOption.dataset.optionId);
    const selectedOptionData = currentCase.options.find(opt => opt.id === selectedOptionId);
    
    // نمایش نتیجه
    document.querySelectorAll('.option-item').forEach(item => {
        const optionId = parseInt(item.dataset.optionId);
        const optionData = currentCase.options.find(opt => opt.id === optionId);
        
        if (optionData.isCorrect) {
            item.classList.add('correct');
        } else if (optionId === selectedOptionId) {
            item.classList.add('incorrect');
        }
    });
    
    // نمایش توضیح
    showExplanation(selectedOptionData);
    
    // غیرفعال کردن دکمه ارسال
    submitDiagnosisBtn.disabled = true;
});

// نمایش توضیح
function showExplanation(selectedOption) {
    explanationSection.style.display = 'block';
    
    const explanation = currentCase.explanation;
    
    explanationContent.innerHTML = `
        <div class="explanation-details">
            <h4>توضیح پاسخ شما:</h4>
            <p>${selectedOption.explanation}</p>
            
            <h4>تشخیص صحیح:</h4>
            <p>${explanation.text}</p>
            
            <h4>نکات کلیدی یادگیری:</h4>
            <ul>
                ${explanation.keyLearningPoints.map(point => `<li>${point}</li>`).join('')}
            </ul>
            
            <h4>منابع:</h4>
            <ul>
                ${explanation.references.map(ref => `<li>${ref}</li>`).join('')}
            </ul>
        </div>
    `;
    
    // اسکرول به توضیح
    explanationSection.scrollIntoView({ behavior: 'smooth' });
}

// دکمه بازگشت به زیردسته‌بندی‌ها
backToSubcategoriesBtn.addEventListener('click', () => {
    casesSection.style.display = 'none';
    document.querySelector('.subcategories-section').style.display = 'block';
    currentSubcategory = null;
});

// دکمه بازگشت به مطالعات موردی
backToCasesBtn.addEventListener('click', () => {
    caseStudySection.style.display = 'none';
    casesSection.style.display = 'block';
    currentCase = null;
});

// دکمه مطالعه موردی بعدی
nextCaseBtn.addEventListener('click', () => {
    const nextIndex = currentCaseIndex + 1;
    const cases = internalDiseasesData[currentSubcategory].cases;
    
    if (nextIndex < cases.length) {
        showCaseStudy(nextIndex);
    } else {
        // بازگشت به لیست مطالعات موردی
        caseStudySection.style.display = 'none';
        casesSection.style.display = 'block';
    }
});

// باز کردن مودال تصویر
function openImageModal(imageUrl, altText) {
    const modal = document.createElement('div');
    modal.className = 'test-image-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <img src="${imageUrl}" alt="${altText}">
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // بستن مودال
    modal.querySelector('.close').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

// اضافه کردن استایل‌های اضافی برای مودال
const additionalStyles = `
.test-image-modal {
    display: flex;
    position: fixed;
    z-index: 2000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    justify-content: center;
    align-items: center;
}

.modal-content {
    position: relative;
    max-width: 90%;
    max-height: 90%;
}

.modal-content img {
    width: 100%;
    height: auto;
    border-radius: 8px;
}

.close {
    position: absolute;
    top: -40px;
    right: 0;
    color: white;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover {
    color: #ccc;
}

.explanation-details h4 {
    color: #667eea;
    margin: 1rem 0 0.5rem 0;
    font-size: 1.1rem;
}

.explanation-details ul {
    margin: 0.5rem 0 1rem 2rem;
}

.explanation-details li {
    margin: 0.25rem 0;
    line-height: 1.5;
}
`;

// اضافه کردن استایل‌ها به صفحه
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// راه‌اندازی اولیه
document.addEventListener('DOMContentLoaded', () => {
    console.log('صفحه بیماری‌های داخلی آماده است!');
}); 