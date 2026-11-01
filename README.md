# saer
مشروع سعّر — منصة عربية لتقدير أسعار السيارات والتعرّف عليها من الصور وعرض الإعلانات.

## نسخة تسليم اللجنة — المرحلة الثانية

هذا الفرع مبني على main البعيد ويحفظ README الأصلي أعلاه. نُقلت إليه ملفات مختارة من C:/car_final على demo-mode عند 0f43ac1، بما فيها التعديلات غير المحفوظة وقت التجهيز؛ بقي المصدر المحلي كما هو. لا يعني اكتمال الرفع نجاح الاستدلال الحي: **Kaggle والهوية والسعر من صورة جديدة لم تُختبر حياً بعد**.

### محتويات الفرع

- frontend: مصدر الواجهة RTL وأصولها وخط Cairo وترخيصه، وبيانات العرض لـ2,742 إعلاناً.
- backend: خادم FastAPI المحلي السابق، وscripts/tools: كود التدريب والمعالجة والميزات والتنبؤ. هذه أكواد قائمة ولم يُنفذ تدريب.
- hf_backend: خدمة Gradio للوظائف الثلاث المعدلة للتشغيل على Linux/Kaggle؛ هي مسار التسليم الصغير المعتمد للنماذج.
- models/outputs: الأوزان الثلاثة المعتمدة فقط، 5,916,575 بايت، ومعها المؤشرات وكود preprocessing. التفاصيل والبصمات في docs/runtime-assets.json. يحتوي bundle الصورة preprocessing داخل components، والسعر الجدولي features/encoder/estimator، والهوية scaler وخريطة 59 فئة داخل candidate.joblib. مشفّرات DINOv2/CLIP/ResNet/SSDLite العامة تُنزّل عند التشغيل؛ ليست محفوظة في Git ويلزم الإنترنت أول مرة.
- data/processed: CSV بحقوق وحقول تشغيل محددة؛ حُذفت من نسخ التسليم روابط المصدر والحقول الحرة/provenance، ولم تتغير البيانات الأصلية.
- data/seed/saer.sqlite: قاعدة تشغيل مولدة من CSV المختارة؛ 2,742 إعلاناً و13,416 سجل صورة، صفر صور فعلية مرفقة، وجداول المستخدمين والجلسات فارغة.
- notebooks/kaggle_server.ipynb: دفتر Kaggle، ومخرجات الدفاتر مُفرغة من نسخة التسليم فقط.

### الصور والحقوق

أُجّلت كل صور الإعلانات الكاملة ومشتقاتها البالغ عددها 13,416، وأُجّلت نماذج التجارب القديمة وبيانات التدريب الخام. بقيت محفوظة محلياً. تعرض نسخة المستودع رسماً نائباً مكان صور الإعلانات؛ الفلترة والمقارنة والأسعار والإحصاءات متاحة من البيانات التاريخية، لكن معرض الصور الفعلي غير متاح. أصول واجهة المستخدم وصور السيارات الخمس مضمنة؛ منشأ وترخيص بعض هذه الأصول غير موثق، ومنها car5 بعلامة Sleeping Dogs. المستودع خاص، ولا يوجد إذن مكتوب لإعادة نشر بيانات سيارة؛ الاستخدام الأكاديمي لا يمنح حق النشر العام.

### تشغيل الواجهة

إصدارات مرجع المشروع: Node 24.22.1 وpnpm 11.25.0. من PowerShell:

```powershell
cd frontend
pnpm install --frozen-lockfile
Copy-Item .env.example .env.local
pnpm run dev
```

افتح http://127.0.0.1:5173. لبناء واجهة Pages:

```powershell
$env:VITE_DEMO_MODE='true'
pnpm run build
```

الناتج frontend/dist-demo؛ لا ترفعه إلى Git. البناء المعتاد دون VITE_DEMO_MODE ينتج dist ويستعمل /api المحلي. ضبط Cloudflare Git لاحقاً: root=frontend وbuild=pnpm run build وoutput=dist-demo وVITE_DEMO_MODE=true. لا يوجد نشر تلقائي مفعّل في هذا الفرع بهذه المرحلة. مشروع Pages الحالي Direct Upload لا يُحوّل مباشرة إلى Git integration.

### تشغيل النماذج محلياً أو على Kaggle

مرجع Python هو 3.12. لإنتاج الحزمة التي يتوقعها الدفتر، من جذر المستودع:

```powershell
python tools/package_kaggle.py
```

يُنتج build/kaggle/saer-backend-bundle.zip بملف app.py في الجذر، والشفرة والأصول الستة وmanifest. ارفعه إلى Kaggle Dataset **خاص** باسم saer-backend-bundle، وأضفه إلى الدفتر، وفعّل Internet وGPU ثم شغّل الخلايا. ضع NGROK_AUTHTOKEN وNGROK_STATIC_DOMAIN في Kaggle Secrets عند استعمال ngrok؛ القيم لا تدخل الخلايا أو Git. الرابط الافتراضي للواجهة في الدفتر https://saer-rmsavg637.pages.dev. ضع origin الفعلي في FRONTEND_ORIGINS إذا تغير المشروع. افتح رابط Pages مع ?api= أو ?apiConfig= الذي يطبعه الدفتر. يتوقف الخادم بانتهاء جلسة Kaggle حتى إذا بقي اسم النطاق ثابتاً.

بديل Gradio محلياً (قد يبدأ تنزيل مشفّرات كبيرة عند التشغيل):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r hf_backend/requirements.txt gradio==6.31.0
$env:LOCAL_ASSETS_DIR=(Get-Location).Path
.\.venv\Scripts\python.exe hf_backend/app.py
```

ابدأ تنزيل الأوزان العامة واختبار الاستدلال ضمن المرحلة الثالثة، وليس كاختبار ناجح مفترض. لوحظ عند قراءة الأوزان أن جزءاً منها محفوظ بـscikit-learn 1.6.1 بينما المتطلبات الحالية 1.9.1؛ ظهر تحذير توافق ويجب حسمه باختبار النتائج أو بيئة متوافقة، دون إعادة تدريب.

### FastAPI المحلي السابق

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-web.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

تحقق من http://127.0.0.1:8000/api/health. تُنشأ SQLite محلياً من CSV. **قيود هذا المسار:** بيانات الفلاتر متاحة، لكن عرض الصور لن يعمل مع تأجيل الأصول؛ ومسارا الهوية والسعر الجدولي في backend القديم يتحققان من ملفات تجارب تاريخية غير مرفقة. المسار الموصى به للوظائف الثلاث هو hf_backend؛ توحيد FastAPI مع runtime الصغير وفحص كل endpoint من مهام المرحلة الثالثة. لا تعتبر خادم FastAPI كاملاً بمجرد استجابة health.

### الإعدادات والأسرار

.env.example يحتوي أمثلة غير حقيقية، وfrontend/.env.example قالب Vite. إنشاء .env لا يضبط متغيرات Python تلقائياً؛ صدّر المتغيرات في الطرفية أو Kaggle Secrets. لا تضع الأسرار في أي متغير يبدأ VITE_ لأنه يصل للمتصفح. لا ترفع .env الحقيقي أو الاعتمادات أو الكاش. بيانات raw والنماذج القديمة ليست متجاهلة تلقائياً؛ أضف الملفات المعتمدة بمسارات صريحة فقط.

### حالة التحقق

فُحصت أحجام الأوزان وبصماتها، وقُرئت preprocessing وخرائط الفئات دون تدريب أو استدلال. أُنشئت قاعدة seed من الملفات المختارة بجداول حسابات فارغة. بقي بناء الواجهة وفحص القائمة المجهزة والأسرار ضمن إجراءات هذه المرحلة، وتُسجّل نتيجتها النهائية في PROGRESS.md وdocs/PHASE2_HANDOFF.md. التشغيل الحي وKaggle لم يُختبرا بعد.
