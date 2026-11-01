# saer
مشروع سعّر — منصة عربية لتقدير أسعار السيارات والتعرّف عليها من الصور وعرض الإعلانات.

<div dir="rtl">

## نسخة التسليم الحالية

المرجع الحالي `release/committee-delivery` أثناء التوحيد إلى main. أُدمجت إصلاحات الواجهة الثمانية من `fix/frontend-layout` و[PR #2](https://github.com/rayan18q-bot/saer/pull/2) في التسليم، وحُفظت إصلاحات النماذج وFileData. الموقع المنشور [سعّر](https://saer-rmsavg637.pages.dev) نسخة أقدم مستقلة؛ لم يُعد نشره ولم تصله هذه الإصلاحات. اقرأ `DELIVERY.md` لسيناريو العرض، و`docs/PHASE4_REPRODUCIBILITY.md` للأدلة والحدود.

أُنشئ فرع التسليم من main البعيد، ثم نُقلت ملفات مختارة من المصدر المحلي `C:/car_final` على `demo-mode` عند `0f43ac1` مع تعديلاته وقت التجهيز. بقي المصدر الأصلي محفوظاً. تاريخ المرحلتين في `docs/PHASE2_HANDOFF.md` و`docs/PHASE3_RUNTIME.md` و`PROGRESS.md`؛ تقاريرهما تسجل حالتهما في وقتهما ولا تستبدل هذا الدليل الحالي.

## المرفق والمؤجل

- مصدر React/TypeScript/Vite عربي RTL، والخلفية REST/Gradio، وثلاثة أوزان معتمدة بمجموع 5,916,575 بايت (5.64 MiB)، مع preprocessing وخرائط الفئات داخل الحزم والكود اللازم. البصمات في `docs/runtime-assets.json`.
- 2742 إعلاناً تاريخياً و13416 سجل صورة. توجد **صورة سيارة أصلية واحدة فقط** مرتبطة بـ`demo-1186`؛ بقية صور الإعلانات الفعلية مؤجلة وتظهر صورة نائبة في العرض التجريبي. لا تعني سجلات الصور إرفاق ملفاتها. راجع `docs/SAMPLE_IMAGES.md`.
- المشفرات العامة الكبيرة غير مرفقة، نحو 2.72 GiB. بيان استعادتها `docs/PUBLIC_ENCODERS.json` وسكربتها أدناه. الأوزان الثلاثة الصغيرة وحدها لا تكفي لمساري الهوية والسعر من الصورة.
- لا تُرفق بيئات Python أو node_modules أو الكاش أو أسرار أو بيانات raw أو نماذج التجارب القديمة. الترخيص الخاص بخط Cairo محفوظ في `frontend/public/fonts/OFL.txt`. مصدر وحقوق بعض صور وأصول التصميم غير محسومة؛ حافظ على خصوصية المستودع ولا تعِد نشرها دون تحقق. لم تُرفع الصور الكاملة.

## المتطلبات

البيئة المختبرة: Windows x64، Python 3.12.10، Node 24.22.1، pnpm 11.25.0، CPU وRAM 16GB. خصص مساحة نحو 10–15 GiB للبيئتين والمشفرات والكاش، واتصال إنترنت لتثبيت الحزم واستعادة المشفرات أول مرة. لم يُختبر Linux/macOS أو Kaggle/GPU بهذه الأقفال. يوجد عامل صورة مستقل؛ لا تخلط إصدارات scikit-learn ولا تستخدم `PYTHONPATH` أو `--system-site-packages`.

## تثبيت نظيف للخلفية والنماذج

من جذر نسخة التسليم، في PowerShell:

```powershell
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:SAER_IMAGE_PYTHONPATH -ErrorAction SilentlyContinue
$env:PYTHONNOUSERSITE='1'
py -3.12 -m venv .runtime/clean-main
py -3.12 -m venv .runtime/clean-image
.runtime/clean-main/Scripts/python.exe -m pip install -r requirements-runtime-lock.txt
.runtime/clean-image/Scripts/python.exe -m pip install -r requirements-image-lock.txt
.runtime/clean-main/Scripts/python.exe -m pip check
.runtime/clean-image/Scripts/python.exe -m pip check
.runtime/clean-main/Scripts/python.exe tools/check_runtime_env.py
.runtime/clean-image/Scripts/python.exe tools/check_runtime_env.py --image
```

أقفال `*-lock.txt` تحفظ الاعتماديات المباشرة والانتقالية المثبتة في البيئتين المختبرتين. ملفات `requirements-runtime.txt` و`requirements-image.txt` هي قائمة الاعتماديات المباشرة التي ثُبتت فعلياً لإنشاء الأقفال. مصدر الحزم PyPI ومستودع عجلات PyTorch CPU الرسمي. استخدم بيئتين جديدتين؛ لا تعِد استخدام بيئة تحمل إصدارات متعارضة.

البيئة الأساسية: Torch 2.14.1+cpu وtorchvision 0.29.1+cpu وscikit-learn 1.9.1، للنموذج الجدولي والهوية وREST/Gradio. عامل الصورة: Torch 2.5.1+cpu وtorchvision 0.20.1+cpu وscikit-learn 1.6.1. يشترك الاثنان في Transformers 4.45.2 وNumPy 2.5.3 وPandas 2.3.3 وPillow 11.3.0. هذا الفصل لازم لتشغيل وزن الصورة المجمد، دون إعادة تدريب أو تحويل الوزن.

## استعادة المشفرات العامة

```powershell
.runtime/clean-main/Scripts/python.exe tools/restore_public_encoders.py --download
.runtime/clean-main/Scripts/python.exe tools/restore_public_encoders.py
```

الأمر الأول ينزّل المفقود فقط من المصادر العامة، بلا توكن، ويتحقق من SHA-256 قبل اعتماده؛ يتوقف عند اختلاف ملف موجود ولا يستبدله. الثاني يتحقق محلياً دون تنزيل. الأسماء والمصادر والإصدارات والتخزين مفصلة في `docs/PUBLIC_ENCODERS.md` وJSON المرافق. توجد ملفات CLIP في منزل المستخدم تحت `.cache/huggingface/hub`، وDINOv2/ResNet18/SSDLite تحت `.cache/torch/hub`. الكود الحالي للهوية يقرأ هذه المسارات الافتراضية؛ لا تفترض دعم نقل الكاش بتغيير HF_HOME أو TORCH_HOME. خيار `--home` مخصص لاختبار الاستعادة ولا يغيّر مسار قراءة النموذج.

بعد اكتمال الاستعادة يعمل التشغيل مع `HF_HUB_OFFLINE=1` و`TRANSFORMERS_OFFLINE=1`. السكربت اختُبر للتحقق من 15 ملفاً في الكاش وتنزيل شفرة DINOv2 إلى مجلد فارغ؛ تنزيل كل الأوزان الكبيرة من الصفر لم يُعد اختباره. لا تعتبر الإنترنت غير مطلوب على جهاز جديد.

## تشغيل الخلفية

```powershell
# نافذة مستقلة لخادم Gradio المحلي
./tools/start_runtime.ps1 -Mode gradio
# أو نافذة مستقلة لـREST؛ ليس مطلوباً لتصفح بيانات demo
./tools/start_runtime.ps1 -Mode rest
```

Gradio على http://127.0.0.1:7863 وREST على http://127.0.0.1:8000. السكربت يثبت مجلد الأصول وعامل الصورة، يعطل PYTHONPATH وحزم المستخدم، يتحقق من المشفرات، ويشغّل محلياً فقط دون نفق عام أو نشر. لا تشغل عمليتي استدلال ثقيلتين بالتوازي على RAM 16GB.

لإعادة تحقق REST مع كاش جديد، أوقفه أولاً واختر `SAER_RUNTIME_CACHE` جديداً عند تشغيله يدوياً، ثم:

```powershell
.runtime/clean-main/Scripts/python.exe tools/verify_delivery_runtime.py --output .runtime/api-verification.json
```

الأداة تتطلب نتيجة غير مخزنة للصورة والهوية وتتحقق من بصمات الأوزان. تقارير النتائج أدلة اختبار فقط وليست مصدر نتائج للواجهة.

## تشغيل الواجهة

```powershell
cd frontend
pnpm install --frozen-lockfile
Copy-Item .env.example .env.local
pnpm dev
```

افتح http://127.0.0.1:5173 ثم ادخل كزائر. للتقدير الحي محلياً افتح `http://127.0.0.1:5173/?api=http%3A%2F%2F127.0.0.1%3A7863` في الجلسة نفسها. يُحفظ رابط API في sessionStorage لهذه الجلسة. عدم ضبط الرابط أو توقف الخدمة يجب أن يعرض رسالة عربية؛ لا توجد نتائج بديلة مختلقة.

لبناء نسخة demo محلية، داخل `frontend`:

```powershell
pnpm exec tsc --noEmit
$env:VITE_DEMO_MODE='true'
pnpm build
pnpm preview --port 5194
```

الناتج `frontend/dist-demo`، ولا ينشر تلقائياً ولا يُرفع إلى Git. لا تبنِ داخل مجلد النشر المعتمد. وضع demo يستخدم بيانات الإعلانات التاريخية محلياً ويتصل بـGradio للتقدير فقط. الوضع الآخر يعتمد `/api` ووكيل Vite المحلي؛ اختبره منفصلاً قبل اعتماده. نجاح البناء لا يثبت كل الوظائف.

## متغيرات التشغيل

| المتغير | الغرض |
|---|---|
| SAER_APP_ROOT وLOCAL_ASSETS_DIR | جذر الشفرة والأوزان الصغيرة المرفقة؛ يضبطهما سكربت التشغيل |
| SAER_IMAGE_PYTHON | Python الخاص بعامل الصورة المستقل |
| SAER_RUNTIME_CACHE | كاش قابل للكتابة، وSQLite لـREST؛ استخدم مساراً جديداً للاختبار غير المخزن |
| FRONTEND_ORIGINS | أصول CORS المسموحة مفصولة بفواصل؛ الافتراضي في السكربت localhost:5173 والموقع الحالي |
| HF_HUB_OFFLINE وTRANSFORMERS_OFFLINE | 1 بعد استعادة كل المشفرات |
| OMP_NUM_THREADS وMKL_NUM_THREADS | 4 لتقييد CPU |
| VITE_DEMO_MODE | true لبيانات demo والبناء الثابت |
| VITE_GRADIO_SPACE_URL أو ?api= | رابط Gradio؛ رابط localhost للاختبار المحلي فقط |
| VITE_API_CONFIG_URL أو ?apiConfig= | إعداد عام اختياري يحدد رابط الخدمة؛ غير مضبوط في التسليم |

`.env.example` أمثلة فقط، ولا يحمّله Python تلقائياً. لا تضع أسراراً في متغيرات VITE_ لأنها تصل إلى المتصفح. تشغيل الأصول المحلية والعامة المذكورة لا يحتاج توكنات. تبقى خيارات استعادة الأصول الخاصة في model_store لحالات أخرى؛ لا حاجة لها مع أوزان التسليم المرفقة.

## النسخة الاحتياطية وحدود العرض

استخدم `tools/package_delivery.py --output <مسار-ZIP-خارج-المستودع>` بعد commit نظيف. يحفظ ملفات commit فقط مع VERSION.txt عربي يحوي SHA، ويتحقق من CRC وبصمات الملفات والأسماء المحظورة في الحزمة. لا يضم المشفرات العامة؛ تبقى أوامر استعادتها داخل ZIP. استخرج الحزمة في مجلد جديد، ثم اتبع التثبيت والاستعادة والتشغيل أعلاه.

لا خادم نماذج عام مضبوط ومتحقق حالياً. نجاح النماذج محلياً لا يعني تشغيلها على Cloudflare؛ لا يمكن تقديم localhost بوصفه API عاماً. دفتر Kaggle موجود كخيار سابق غير مختبر في هذه المرحلة؛ لم يبدأ إعداد Kaggle أو GPU أو نفق جديد. المرحلة الخامسة تحتاج خدمة HTTPS مصرحاً بها واختبار CORS من الموقع ومراجعة حقوق الصور واختبارات الوظائف والعروض المتجاوبة غير المعادة بعد الدمج.

</div>
