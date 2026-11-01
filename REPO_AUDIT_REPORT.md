# متابعة تصحيح الهوية — 2026-11-02

هذه المتابعة تصحح قصور الجولة الأولى أدناه: تغير وصف الخادم والواجهة وعناوين أدوات Python، وأُعيدت تسمية الدفتر وعامل الصورة والمشغّل وتحديث مراجعها، وصُحح metadata للدفتر. أضيف توافق يحافظ على الجلسات وقاعدة البيانات السابقة، مع 3 اختبارات ناجحة. أسماء البيانات الداخلية والسجلات التاريخية ليست علامات عرض ولا تُغير دون migration.

**الجرد الجديد وقرار كل ملف والاستثناءات ونتائج الاختبارات:** [مراجعة الهوية ملفًا بملف](docs/BRANDING_FILE_REVIEW.md).

الأقسام التالية سجل الجولة الأولى؛ عباراتها عن تأجيل إعادة التسمية والتعديلات المحدودة بالتوثيق تصف حالتها السابقة، وقد حلت المتابعة أعلاه محلها. لا تعني بقاء المثال الأصلي داخل سجل التدقيق أنه بقي في الملف التشغيلي الحالي.

---

# تقرير مراجعة مستودع سعّر

التاريخ: 2026-11-02. فرع المراجعة: `cleanup/final-review`. المرجع المفحوص: `023998c8895b4aa2909bd54de67be131c4183d81`.

## الملخص وحدود الفحص

- شجرة GitHub غير مبتورة: **300 ملف متتبع**. جُلب محتوى **242 ملفًا نصيًا** وفُحص آليًا للأسماء والأنماط والبنية، مع مراجعة تفصيلية لملفات التشغيل والتوثيق المشار إليها أدناه. هذا لا يعني مراجعة دلالية سطرًا بسطر لكل كود.
- **58 ملفًا** أخرى فُحصت أسماؤها وأحجامها من شجرة GitHub فقط: جدولا CSV و56 أصلًا ثنائيًا. لم تُنزّل الأوزان أو قاعدة البيانات أو الصور، ولم تُفتح الصور بصريًا في هذه الجولة. لا يُدعى فحص محتواها أو سلامة حقوقها.
- **84 سطرًا في 49 ملفًا نصيًا** طابقت البحث الموسع عن الأسماء القديمة قبل التعديل؛ العدد هو أسطر مطابقة، لا عدد مرات ظهور مفردات داخل JSON طويل. لم يشمل محتوى CSV أو SQLite أو الأوزان أو تاريخ Git.
- صُحح اسمان قديمان في عنوان المتطلبات وتعليمات العمل، مع إزالة وصف الاسم بأنه مؤقت. بقيت المطابقات الأخرى موثقة أدناه؛ لا ادعاء بوصول البحث إلى صفر.
- التعديلات محدودة بالتوثيق و.gitignore؛ لا تعديل للكود أو البيانات أو أوزان النماذج، ولا نشر أو دمج إلى main أو إعادة كتابة تاريخ.
- تم الاحتفاظ بإسناد الأدوات والمكتبات والنماذج والتراخيص الصحيحة. أسماء الفريق في README من المستخدم مباشرة وبالعربية دون اختراع تهجئة إنجليزية.

## ما تم تصحيحه

| الملف | التغيير |
|---|---|
| README.md | إزالة إيموجي العناوين ورابط التجربة، وإضافة أسماء الفريق؛ الحفاظ على الإنجليزية والشعار والصور ورابط الموقع وحدود الاستدلال |
| REQ.md | عنوان المشروع سعّر، وحالة الاسم النهائي بدل المؤقت |
| TEST_PLAN.md | تصحيح شرط README العربي إلى README إنجليزي ودليل Windows موثق، وفق طلب المستخدم الحالي |
| AGENTS.md | تصحيح هوية المشروع فقط؛ لم يُحذف الملف أو قواعده أو عنوانه الذي يوضح وظيفته |
| .gitignore | حماية الإضافات الجديدة من raw/recovery وCSV المعالجة وقواعد البيانات والأوزان والأرشيفات وصور بيانات demo؛ لا إزالة لأي ملف متتبع |

## التحقق الفعلي

| الفحص | النتيجة وحدودها |
|---|---|
| Python AST / compileall | نجح تحليل **137 ملف Python**؛ لا يثبت سلامة الاستيراد أو التشغيل |
| node --test tests/frontend-behavior.mjs | **7 ناجحة، 0 فاشلة**، وأُعيدت بعد تغييرات التوثيق |
| TypeScript --noEmit | نجح، وأُعيد بعد التغييرات |
| Vite build | نجح بناء عادي محلي، وأُعيد بعد التغييرات؛ ظهرت تحذيرات عدم توافر Cairo/skyline/login-reference في النسخة النصية المحلية، وهي موجودة بأسمائها في شجرة GitHub. لا ادعاء باختبار حزمة demo المكتملة أو عرض بصري |
| Python unittest discover | قبل التعديل وبعده: **79 تشغيل اختبار، 11 سجل خطأ، 4 تخطيات، 0 فشل assertions**. تشمل الأخطاء فشل تحميل وحدات وsetUpClass، لذلك لا نطرحها لحساب عدد ناجح مضلل. الجولة غير ناجحة بالكامل |
| JSON / notebook JSON | ملفات JSON ودفاتر Jupyter النصية المجلوبة اجتازت JSON.parse |
| روابط README وSETUP | **49 مرجعًا نسبيًا** طوبقت أهدافها مع شجرة GitHub، صفر هدف مفقود. لا يشمل اختبار HTTP لكل رابط خارجي أو صحة كل anchor |
| أسرار | فحص أنماط مفاتيح GitHub/AWS وprivate keys في النصوص المجلوبة: صفر مطابقة. ليس فحصًا كاملًا لكل أنواع الأسرار أو البيانات الشخصية أو التاريخ أو الثنائيات. لا قيم سرية منسوخة |
| تثبيت Windows نظيف / health / النماذج | لم يُنفذ هنا؛ البيئة Linux ولا تتوافر Torch أو المشفرات أو ثنائيات التسليم محليًا. تقارير الجولات السابقة محفوظة ولا تعد اختبارًا جديدًا |

### قيود البيئة المحلية

فشل git clone الخاص لعدم توافر اعتماد CLI؛ استُخدم موصل GitHub المصرح به لجلب الملفات. النسخة المحلية هنا إعادة تكوين نصية وليست checkout كاملًا؛ لا يمكن استخدام git ls-files فيها لاستنتاج ملفات جهاز الفريق غير المتتبعة. لم يُفحص C:/car_final أو أي نسخة على جهاز المستخدم. لا توجد دعوى أن الملفات المحلية غير المتتبعة أو .vscode أو نسخ احتياطية غير مرفوعة قد فُحصت.

تشغيل pnpm المتاح في البيئة مرّ عبر غلاف بيئة قام بتحضير اعتماديات الواجهة محليًا؛ لم تُرفع حزم أو تغييرات lockfile ولم تُرقّ إصدارات المشروع. لذلك نجاح البناء هنا ليس برهان تثبيت frozen-lockfile نظيف. لم تثبت حزم Python أو تُنزّل أوزانًا.

## مشاكل التشغيل والاتساق والتبعيات

1. اختبارات recovery تطلب data/recovery/pages لمجموعتي المصدر وصفحات 291104 و317755؛ هذه الملفات غير موجودة في شجرة GitHub. تحتاج fixtures صغيرة منزوعة البيانات الشخصية أو اختبارات تكامل مشروطة ببيانات خارجية، لا اختلاق ملفات لإسكات الاختبار.
2. test_identity_to_price_handoff يطلب models/delivery_current.json؛ الملف غير موجود في الشجرة. يلزم قرار تحديث الاختبار وفق مؤشرات التشغيل الحالية أو توفير مؤشر صحيح بعد اختبار وظيفي.
3. سبعة أخطاء تحميل وحدات بسبب غياب Torch في بيئة المراجعة؛ لا تُسجل كعيب مثبت في النموذج. توجد أربعة اختبارات متخطاة؛ يلزم مراجعة أسبابها في بيئة الفريق.
4. requirements-runtime.txt يضم requirements-web.txt الذي يضم requirements-models.txt؛ الأخير يثبت numpy 2.5.3 وPillow 11.3.0، بينما runtime.txt يثبت numpy 2.3.5 وPillow 12.3.0 أيضًا. يوجد **تعارض تثبيت مباشر** في ملفات المتطلبات المباشرة. README يستخدم lockfiles؛ لم تُعدّل الإصدارات أو الأقفال. يجب توحيد المصادر وفق البيئة المعتمدة ثم إعادة تثبيت نظيف قبل تغييرها.
5. run_siarad.bat ما زال يعتمد .venv وrequirements-web.txt ويختلف عن مسار البيئتين في SETUP. يُعامل كمشغل قديم يحتاج تحديثًا واختبار Windows وإعادة تسمية، لا كمسار التسليم الموثق.
6. TEST_PLAN يشير إلى /health بينما التشغيل الحالي يوثق /api/health؛ يجب التحقق الفعلي من مسار الخدمة المختار قبل توحيد عقد الاختبار.
7. backend/app/config.py يشير إلى models/price_current.json غير الموجود، لكن مسار التسليم يستخدم runtime_bridge ومؤشرات مختلفة؛ لا نستنتج تعطّل المسار النشط دون اختبار. يلزم تصنيف المسارات القديمة من الحالية.
8. بعض الاستيرادات تخص خيارات تدريب وتجارب وواجهات Tkinter أو ملفات مصدر خارجية. لم تُنتج قائمة مؤكدة شاملة بالحزم الزائدة؛ حذف حزمة اعتمادًا على بحث نصي وحده غير آمن.
9. script run_checks.py يتوقع أن تُتجاهل كل بيانات processed والأوزان، بينما التسليم يتتبع بعضها عمدًا. .gitignore الجديد يحمي الإضافات، لكنه لا يخرج الملفات الحالية من Git. يجب تحديث سياسة الاختبار بموافقة الفريق، لا حذف الأوزان لإرضاء فحص قديم.
10. لا خادم استدلال عام موثق ومتحقق. الموقع الثابت مختلف عن main، ولم يتغير ضمن المراجعة.
11. لا توجد حزمة تثبيت Windows بلا كاش متحقق منها في هذه الجولة، ولا إعادة تقييم دقة خارجية. لا تُضاف أرقام أداء جديدة.

## البيانات والملفات الكبيرة والترخيص

تعليمات الطلب قالت إن الأوزان والبيانات خارج المستودع، لكن الشجرة الحالية تثبت وجود CSV المعالجة وSQLite وثلاثة joblib. احتُفظ بها كما هي. قاعدة البيانات 5,455,872 بايت ووزن الصورة 5,114,410 بايت: يتجاوزان 5 MB عشريًا، ويقلان عن 5 MiB. الحد المقصود يحتاج تحديدًا؛ لا حذف تلقائي.

صورة العينة الأصلية ولقطات README موجودة ضمن المستودع. لم تُفتح في الجولة الحالية ولم تُحسم حقوقها. لا يترتب على خصوصية المستودع إذن إعادة توزيع. ترخيص Cairo موجود، ولا يوجد ترخيص برمجي عام مثبت للمشروع؛ لم يُخترع ترخيص. يجب حفظ إسناد نموذج الصورة ومصادر المشفرات، ومنها معرفات المستودعات الأصلية المطلوبة للتنزيل، حتى لو تضمنت اسم جهة تقنية.

## الأسماء القديمة وقرار التعامل

المتبقي ينقسم إلى: معرّفات بيانات ومسارات ملفات خارجية؛ كوكيز وقاعدة بيانات وعامل مستقل؛ إصلاحات توافق وتحويل نصوص قديمة؛ provenance وسجلات تحقق تاريخية وبيانات بصمات؛ عناوين ونصوص أدوات وتجارب قديمة. لم يُنفذ استبدال شامل لأن الاختبارات الشاملة غير خضراء، ولأن تغيير المعرّفات أو بصمات الأدلة يُفقد الربط والمصداقية. يُقترح mapping عند حدود العرض فقط لمصادر Japan/KG/USA، مع إبقاء المعرف الداخلي دون تغيير إلى أن يتوافر اختبار migration.

| الملف | سطر المرجع | النص الأصلي المختصر | الإجراء |
|---|---:|---|---|
| AGENTS.md | 4 | نفّذ مشروع سيارات أكاديمي باسم مؤقت CarInsight AI. **كل ردودك التوضيحية للمستخدم بالعربية، وجميع عناصر الواجهة والتقارير بالعربية RTL.** أسماء الكود التقنية لا يلزم تعريبها. | صُحح إلى سعّر |
| DATA_CONTRACT.md | 4 | - 'data/raw/CarInsight_USA/': من الملفات الملحوظة 'cars_ready.csv', 'member2_american.csv', 'final_exports/price_dataset.csv', 'final_exports/recognition_images.csv'. | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| DATA_CONTRACT.md | 5 | - 'data/raw/CarInsight_KG/': من الملفات الملحوظة 'member3_korean_german.csv', 'prepared/listings.csv', 'prepared/images.csv' وسكربتات '01_prepare_data.py', '02_price_model.py', '03_train_recognizer.py', '04_visual_search.py'. | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| DATA_CONTRACT.md | 6 | - 'data/raw/CarInsight_Japan/': من الملفات الملحوظة 'member1_japanese.csv', 'car_images_verified.csv', 'CarInsight_member1.xlsx'. | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| REQ.md | 1 | # وثيقة متطلبات المشروع — CarInsight AI | صُحح إلى سعّر |
| REQ.md | 11 | - المصادر: 'CarInsight_USA', 'CarInsight_KG', 'CarInsight_Japan' تحت 'data/raw/'. | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/__init__.py | 1 | """سياراد: الخادم المحلي.""" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/__init__.py | 1 | """خدمات واجهة سياراد المحلية.""" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/config.py | 7 | DB_PATH = DB_DIR / "siarad.sqlite" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/config.py | 10 | UPLOAD_DIR = ROOT / "tmp" / "siarad_uploads" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/main.py | 100 |     fd, temp_name = tempfile.mkstemp(prefix="siarad_", suffix=suffix, dir=UPLOAD_DIR) | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/main.py | 170 |     response.set_cookie("siarad_session", token, max_age=_SESSION_DAYS * 86400, | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/main.py | 178 |     token = request.cookies.get("siarad_session") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/main.py | 221 |     token = request.cookies.get("siarad_session") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/main.py | 227 |     response.delete_cookie("siarad_session", path="/") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| backend/app/services.py | 113 |     worker = ROOT / "scripts" / "siarad_price_worker.py" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| docs/FILE_MANIFEST.json | 887 |       "path": "hf_backend/scripts/siarad_price_worker.py", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| docs/FILE_MANIFEST.json | 942 |       "path": "notebooks/CarInsight_Identity_Model_Make_Reference.ipynb", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| docs/FILE_MANIFEST.json | 1002 |       "path": "run_siarad.bat", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| docs/FILE_MANIFEST.json | 1317 |       "path": "scripts/siarad_price_worker.py", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| docs/PHASE3_RUNTIME.md | 19 | 2742 إعلاناً تاريخياً دون بيانات اتصال شخصية في حقول العرض. أضيفت صورة أصلية واحدة 9280 بايت مرتبطة بـdemo-1186 وCarInsight_Japan:0001JP، مع تحديث مسارها في JSON وCSV وSQLite؛ لم تتغير قيم الإعلان. فحص بصري: لا شخص أو لوحة مقروءة، وليس تدقيق OCR شاملاً. بقية الصور الكاملة مؤجلة؛ الجداول لا تعني إرفا | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| docs/PHASE5_VERIFICATION.json | 273 |       "hf_backend/scripts/siarad_price_worker.py", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| docs/PHASE5_VERIFICATION.json | 274 |       "scripts/siarad_price_worker.py", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| docs/SAMPLE_IMAGES.md | 5 | أُرفقت صورة أصلية واحدة دون تعديل: frontend/public/demo/img/sample-1186/04.webp. مرتبطة بالإعلان التاريخي demo-1186 وفي جدول الصور بالإعلان CarInsight_Japan:0001JP، وتطابق الماركة والموديل والسنة والسعر والممشى بين الجدولين. أصلها صورة جانبية للسيارة؛ فُحصت بصريًا ولا يظهر فيها أشخاص أو لوحة مقروءة. | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/ReferenceApp.tsx | 495 |           animation: 'siyarad-flower-rain ${2.5 + ((index * 7) % 15) / 10}s ease-in ${((index * 11) % 8) / 10}s both', | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/ReferenceApp.tsx | 538 |   const estimateHeroHtml = estimateHeroWithRoadCars().replace("CarInsight AI", APP_NAME); | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-controls.css | 39 |   animation: siyarad-loading-enter 0.24s ease-out both; | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-controls.css | 43 |   animation: siyarad-loading-exit 0.5s ease-in both; | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-controls.css | 104 |   animation: siyarad-loading-progress 1s ease-in-out infinite alternate; | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-controls.css | 107 | @keyframes siyarad-loading-enter { | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-controls.css | 112 | @keyframes siyarad-loading-exit { | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-controls.css | 116 | @keyframes siyarad-loading-progress { | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-controls.css | 120 | @keyframes siyarad-flower-rain { | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-original.ts | 1 | // Copied from the live CarInsight demo Gradio configuration; source URL recorded in PROGRESS.md. | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| frontend/src/hamoud-live-original.ts | 2 | export const hamoudHeroHtml = "\n<div class=\"hero\">\n  <div class=\"stars\"></div><div class=\"sun\"></div>\n  <div class=\"cloud c1\"></div><div class=\"cloud c2\"></div>\n  <div class=\"hero-text\">\n    <h1>🚗 CarInsight AI</h1>\n    <p>ارفع صور سيارتك، ونقدّر لك سعرها بالريال مع نطاق محتمل — ف | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/backend/app/services.py | 103 |         worker = ROOT / "scripts" / "siarad_price_worker.py" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/models/image_price_hamoud_20261028/image_to_price_v2.py | 2 | CarInsight AI - Image-only price estimation  (image -> price) | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/clip_identity_runtime_20261028.py | 75 |     root=tk.Tk();root.title('CarInsight — تجربة CLIP + DINO') | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/day20_common.py | 21 |     "CarInsight_Japan": "member1_japanese.csv", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/day20_common.py | 22 |     "CarInsight_USA": "member2_american.csv", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/day20_common.py | 23 |     "CarInsight_KG": "member3_korean_german.csv", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/generalization_identity_runtime_20261028.py | 114 |     root.title("CarInsight — تجربة نماذج الهوية المعتمدة") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/image_input_policy_20261026.py | 23 |     with TemporaryDirectory(prefix='carinsight_rgb_') as temp: | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/ml_common.py | 44 |                     ROOT/'CarInsight_KG/02_price_model.py', ROOT/'CarInsight_KG/03_train_recognizer.py', | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/ml_common.py | 45 |                     ROOT/'CarInsight_KG/04_visual_search.py']}} | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/model_image_tester.py | 1 | """واجهة محلية لاختبار مرشحي الصور التطويريين في CarInsight.""" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/model_image_tester.py | 154 |         root.title("CarInsight — تجربة نماذج الصور") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| hf_backend/scripts/model_image_tester_20261026.py | 91 |     root.title('CarInsight — تجربة مرشح 26 أكتوبر');root.mainloop() | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| models/image_price_hamoud_20261028/image_to_price_v2.py | 2 | CarInsight AI - Image-only price estimation  (image -> price) | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| notebooks/CarInsight_Identity_Model_Make_Reference.ipynb | 7 |         "# CarInsight — مرجع نموذج الموديل والماركة\n", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| notebooks/CarInsight_Identity_Model_Make_Reference.ipynb | 252 |     "carinsight": { | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| notebooks/README.md | 3 | الملف 'CarInsight_Identity_Model_Make_Reference.ipynb' يغطي رأس الموديل المركب والرأس المنفصل للماركة لأغراض المقارنة فقط. لا يحتوي تدريبًا ولا يستدعي مودل حمود أو نموذج السعر الجدولي أو نماذج اللون والهيكل والبحث. | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| notebooks/README.md | 7 | 1. افتح 'C:\CAR\notebooks\CarInsight_Identity_Model_Make_Reference.ipynb' في Jupyter أو VS Code. | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| notebooks/README.md | 12 | .venv\Scripts\python.exe -m ipykernel install --user --name carinsight-venv --display-name "Python (CarInsight .venv)" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/brand_final_finish.py | 77 |     clean=np.asarray([r['listing_uid']!='CarInsight_USA:0035US' for r in va]) | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/brand_final_finish.py | 162 |       'الصورة CarInsight_USA:0035US:04 في val والصورة CarInsight_USA:0036US:05 في test تعرضان المشهد نفسه، مع تعديل موضع لوحة السيارة بشعار الموقع. اختلاف SHA لا يمنع هذا النوع من التسرب. عُزل إعلان 0035US كاملًا من المقارنة المدققة فقط؛ ظل التقرير يعرض val الكامل أيضًا، ولم تتغير البيانات أو التقسي | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/brand_final_round.py | 257 |     clean = np.asarray([r['listing_uid'] != 'CarInsight_USA:0035US' for r in va]) | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/clip_identity_runtime_20261028.py | 73 |     root=tk.Tk();root.title('CarInsight — تجربة CLIP + DINO') | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_common.py | 21 |     "CarInsight_Japan": "member1_japanese.csv", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_common.py | 22 |     "CarInsight_USA": "member2_american.csv", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_common.py | 23 |     "CarInsight_KG": "member3_korean_german.csv", | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_enrichment_audit.py | 140 |     kg_quarantine = sum(row["source_dataset"] == "CarInsight_KG" for row in quarantine) | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_external_review.py | 118 |     kg = [{"listing_uid": r["listing_uid"], "reasons": r["quarantine_reasons"]} for r in quarantine if r["source_dataset"] == "CarInsight_KG"] | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_inventory.py | 89 |         xlsx = next(base.glob("CarInsight_member*.xlsx")) | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_recover.py | 23 | UA = "CarInsightAcademic/1.0" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_report.py | 10 | AR_SOURCE = {"CarInsight_Japan": "الياباني", "CarInsight_USA": "الأمريكي والصيني", "CarInsight_KG": "الكوري والألماني"} | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day20_report.py | 200 | \| make_data_guide.py في USA \| يحيل إلى carinsight_engine.runner، والحزمة غير مرفقة في الملفات الحالية. لا يعد نقطة تشغيل جاهزة رغم README القديم. \| | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/day21_issue_validate.py | 70 |     q = [r for r in read_csv(processed / "quarantine_listings.csv") if r["source_dataset"] == "CarInsight_KG"] | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/generalization_identity_runtime_20261028.py | 114 |     root.title("CarInsight — تجربة نماذج الهوية المعتمدة") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/identity_context_runtime_20261027.py | 83 |     root.title('CarInsight — تجربة ترجيح هوية السيارة') | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/image_input_policy_20261026.py | 23 |     with TemporaryDirectory(prefix='carinsight_rgb_') as temp: | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/image_price_final.py | 27 | SOURCE = ROOT / 'tmp/independent_review_20261023/gemini/carinsight_v2_20261022' | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/image_price_train.py | 118 |     known_ids = {'CarInsight_USA:0035US', 'CarInsight_USA:0036US'} | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/improve_report.py | 86 | # تحسين نماذج CarInsight — 21 أكتوبر 2026 | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/ml_common.py | 44 |                     ROOT/'CarInsight_KG/02_price_model.py', ROOT/'CarInsight_KG/03_train_recognizer.py', | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/ml_common.py | 45 |                     ROOT/'CarInsight_KG/04_visual_search.py']}} | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/model_image_tester.py | 1 | """واجهة محلية لاختبار مرشحي الصور التطويريين في CarInsight.""" | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/model_image_tester.py | 154 |         root.title("CarInsight — تجربة نماذج الصور") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/model_image_tester_20261026.py | 91 |     root.title('CarInsight — تجربة مرشح 26 أكتوبر');root.mainloop() | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| scripts/run_checks.py | 20 |     blocked = ["CarInsight_Japan/member1_japanese.csv", "CarInsight_USA/images/a.webp", "CarInsight_KG/prepared/listings.csv", "CarInsight_AI_Docs.zip", "data/raw/x.csv", "data/processed/listings.csv", "data/recovery/images/a.webp", "models/price.joblib", ".env", ".env.local", "credentials.json", "p | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| tests/test_day20_recovery.py | 20 |         sample = saved_page("291104", "CarInsight_USA") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| tests/test_day20_recovery.py | 28 |         sample = saved_page("317755", "CarInsight_Japan") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| tests/test_day20_recovery.py | 35 |         sample = saved_page("291104", "CarInsight_USA") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |
| tools/export_demo_data.py | 42 |         value = value.replace("سياراد", "سعّر").replace("Siyarad", "Saer").replace("siarad", "saer") | باقٍ؛ موثق للمراجعة قبل تغيير التشغيل أو السجلات |

أسماء المسارات القديمة في الشجرة: run_siarad.bat، scripts/siarad_price_worker.py، hf_backend/scripts/siarad_price_worker.py، notebooks/CarInsight_Identity_Model_Make_Reference.ipynb. لم تُعد تسميتها؛ يلزم تحديث المراجع واختبار التشغيل قبل اعتمادها. قد تبقى الأسماء في بيانات CSV/SQLite/الأوزان غير المفتوحة وتاريخ commits؛ لم يُفحص التاريخ كاملًا ولم يُغيّر.

## ملفات تعليمات الأدوات وبقايا البرومبتات

AGENTS.md موجود ومقروء، ويحتوي تعليمات فعلية لوكيل العمل، لا توثيقًا للمستخدم النهائي. لم يُحذف لأن المستخدم طلب عرضه للقرار أولًا. لم تظهر في الشجرة المتتبعة CLAUDE.md أو .claude أو .cursor أو .cursorrules أو .github/copilot-instructions.md. هذا لا ينفي وجودها محليًا خارج Git. لم يُفحص تاريخ commits أو كل أوصاف PR/issues بحثًا عن co-authorship، ولم تُحذف معلومات إسناد. لا توجد طريقة موثوقة لإثبات أن الأسلوب كتبه إنسان؛ التعديل يحسن الوضوح ولا يصنع ادعاءً عن التأليف.

## محتاج قرار

- إبقاء AGENTS.md كتعليمات للمطورين أو حذفه من نسخة التسليم؟ لم يُحذف الآن.
- هل نحافظ على نمط README الإنجليزي الحالي؟ اعتمدناه مع إزالة إيموجي العناوين حسب أحدث طلب، وأبقينا أسماء الفريق بالعربية.
- معرّفات المصدر القديمة: موافقة على تصميم mapping لعرض أسماء عامة، دون تعديل CSV/SQLite/الأوزان أو تغيير تاريخ النتائج.
- نطاق توحيد ملفات التشغيل القديمة: تحديث run_siarad.bat والعامل والكوكيز واسم قاعدة البيانات يتطلب اختبارات Windows وخطة توافق للجلسات وقواعد البيانات السابقة.
- قرار إعادة توزيع صورة العينة ولقطات README وأصول الواجهة، قبل إزالة شيء أو إتاحته للعامة.
- إصلاح تعارض requirements المباشر وفق الأقفال، ثم إعادة اختبار تثبيت نظيف. لا ترقية تلقائية.
- فصل اختبارات التجارب التي تحتاج بيانات خارجية عن اختبارات التسليم، وتوفير fixtures قانونية صغيرة.
- إبقاء الأدلة التاريخية دون تحريف؛ إذا أراد الفريق تقليلها في واجهة المستودع يمكن نقلها تنظيميًا مع تحديث الروابط، لا تغيير محتواها لإخفاء التاريخ.

## أسئلة لازم الفريق يجاوب عليها

1. الاسم الإنجليزي المستخدم في README هو Saer؛ config.ts يثبت العربية فقط. هل تعتمدون Saer رسميًا؟ لم يُخترع بديل.
2. هل يوجد تقرير أكاديمي نهائي معين للمقارنة؟ لم يُقدّم محتواه لهذه الجولة، فلا ادعاء بمطابقة أرقامه.
3. ما الإذن الموثق لمشاركة صورة العينة واللقطات وصور التصميم؟
4. هل يسمح بتوفير fixtures recovery من المصدر، أم تعتمدون اختبارات مستقلة ببيانات اصطناعية معلنة لا نتائج علمية وهمية؟
5. هل يوجد رابط HTTPS لخادم النماذج لم يُوثق بعد؟

## الجرد الكامل للملفات المتتبعة

كل مسار أدناه من شجرة GitHub عند المرجع أعلاه، بما فيها الملفات المخفية المتتبعة. الجرد ليس جرد جهاز الفريق. «فحص نصي» يعني تحميل المحتوى وفحوص البحث والبنية، لا شهادة سلامة كل منطق الملف.

| المسار | النوع / بايت | الغرض | الحالة / نطاق الفحص |
|---|---|---|---|
| .env.example | example / 711 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| .gitignore | gitignore / 1242 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| AGENTS.md | md / 4889 | إعدادات أو وثائق جذرية | فيه ملاحظة: اسم قديم؛ فحص نصي |
| DATA_CONTRACT.md | md / 7870 | إعدادات أو وثائق جذرية | فيه ملاحظة: اسم قديم؛ فحص نصي |
| DELIVERY.md | md / 20978 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| ML_SPEC.md | md / 7570 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| PROGRESS.md | md / 34663 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| README.md | md / 11648 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| REQ.md | md / 14758 | إعدادات أو وثائق جذرية | فيه ملاحظة: اسم قديم؛ فحص نصي |
| ROADMAP.md | md / 8355 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| TEST_PLAN.md | md / 3735 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| backend/__init__.py | py / 47 | خدمة REST | فيه ملاحظة: اسم قديم؛ فحص نصي |
| backend/app/__init__.py | py / 57 | خدمة REST | فيه ملاحظة: اسم قديم؛ فحص نصي |
| backend/app/config.py | py / 809 | خدمة REST | فيه ملاحظة: اسم قديم؛ فحص نصي |
| backend/app/db.py | py / 8107 | خدمة REST | فحص نصي؛ لا حكم شامل على المنطق |
| backend/app/main.py | py / 28603 | خدمة REST | فيه ملاحظة: اسم قديم؛ فحص نصي |
| backend/app/runtime_bridge.py | py / 794 | خدمة REST | فحص نصي؛ لا حكم شامل على المنطق |
| backend/app/schemas.py | py / 615 | خدمة REST | فحص نصي؛ لا حكم شامل على المنطق |
| backend/app/services.py | py / 5413 | خدمة REST | فيه ملاحظة: اسم قديم؛ فحص نصي |
| data/processed/images.csv | csv / 3672613 | بيانات معالجة/قاعدة بيانات | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| data/processed/listings.csv | csv / 820078 | بيانات معالجة/قاعدة بيانات | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| data/seed/saer.sqlite | sqlite / 5455872 | بيانات معالجة/قاعدة بيانات | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| docs/BRANCH_NAMING_UPDATE.md | md / 2418 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/FILE_MANIFEST.json | json / 51923 | توثيق وأدلة | فيه ملاحظة: اسم قديم؛ فحص نصي |
| docs/FRONTEND_FIX_VALIDATION.md | md / 6923 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/GRADIO_VERIFICATION.json | json / 804 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/PHASE2_HANDOFF.md | md / 5465 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/PHASE3_RUNTIME.md | md / 9513 | توثيق وأدلة | فيه ملاحظة: اسم قديم؛ فحص نصي |
| docs/PHASE4_REPRODUCIBILITY.md | md / 10138 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/PHASE4_VERIFICATION.json | json / 9080 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/PHASE5_VERIFICATION.json | json / 10214 | توثيق وأدلة | فيه ملاحظة: اسم قديم؛ فحص نصي |
| docs/PUBLIC_ENCODERS.json | json / 25711 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/PUBLIC_ENCODERS.md | md / 3905 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/PUBLISHED_STATE.json | json / 819 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/RUNTIME_VERIFICATION.json | json / 3998 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/SAMPLE_IMAGES.md | md / 1517 | توثيق وأدلة | فيه ملاحظة: اسم قديم؛ فحص نصي |
| docs/SETUP.md | md / 17414 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/UNIFICATION_VERIFICATION.json | json / 9589 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/assets/README.md | md / 1265 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| docs/assets/home-screen.jpg | jpg / 166534 | توثيق وأدلة | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| docs/assets/listings-screen.jpg | jpg / 122412 | توثيق وأدلة | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| docs/assets/market-screen.jpg | jpg / 254059 | توثيق وأدلة | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| docs/runtime-assets.json | json / 1580 | توثيق وأدلة | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/.env.example | example / 221 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/_headers | frontend/_headers / 209 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/_redirects | frontend/_redirects / 19 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/index.html | html / 588 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/package.json | json / 625 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/pnpm-lock.yaml | yaml / 37285 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/assets/road-cars/car1.png | png / 272594 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/assets/road-cars/car2.png | png / 220668 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/assets/road-cars/car3.png | png / 2009370 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/assets/road-cars/car4.png | png / 1881340 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/assets/road-cars/car5.png | png / 97616 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/brands/README.md | md / 435 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/audi.svg | svg / 2128 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/bmw.svg | svg / 1613 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/brands.json | json / 4141 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/cadillac.svg | svg / 1565 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/chevrolet.svg | svg / 511 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/chrysler.svg | svg / 6148 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/ford.svg | svg / 4177 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/honda.svg | svg / 1773 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/hyundai.svg | svg / 1656 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/jeep.svg | svg / 1811 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/kia.svg | svg / 1016 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/mazda.svg | svg / 1566 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/mg.svg | svg / 4859 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/mini.svg | svg / 1676 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/mitsubishi.svg | svg / 198 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/nissan.svg | svg / 1831 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/porsche.svg | svg / 24198 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/suzuki.svg | svg / 364 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/toyota.svg | svg / 989 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/brands/volkswagen.svg | svg / 1103 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/demo/img/sample-1186/04.webp | webp / 9280 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/demo/listings.json | json / 1021637 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/demo/market.json | json / 4680 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/demo/meta.json | json / 7172 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/demo/placeholder.svg | svg / 465 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/demo/pricing-options.json | json / 2672 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/demo/recommendations.json | json / 2282 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/fonts/Cairo.ttf | ttf / 599548 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/fonts/OFL.txt | txt / 4473 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/public/ui/budget/background.png | png / 647693 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/car0-default.png | png / 112507 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/car1-default.png | png / 113171 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/car2-default.png | png / 109836 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/car3-default.png | png / 107905 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/car4-default.png | png / 110042 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/filters.png | png / 288527 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/heading.png | png / 136810 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/notice.png | png / 24701 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/refresh.png | png / 18938 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/budget/results-heading.png | png / 26538 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/compare/background.png | png / 661345 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/compare/first-reference.png | png / 152080 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/compare/heading.png | png / 103183 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/compare/information.png | png / 106330 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/compare/second-reference.png | png / 142563 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/compare/submit.png | png / 19467 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/compare/table.png | png / 320225 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/details/background.png | png / 751557 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/details/breadcrumb.png | png / 16489 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/details/form-no-confirm.png | png / 226984 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/details/heading.png | png / 104028 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/details/identity-manual.png | png / 314789 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/details/identity-reference.png | png / 324465 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/details/information.png | png / 78041 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/home/browse-feature-user.png | png / 569676 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/home/budget-cars-cutout.png | png / 910563 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/home/compare-feature-user.png | png / 632520 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/home/estimate-feature-user.png | png / 515216 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/home/home-final.png | png / 1429534 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/home/sell-car-cutout.png | png / 1161378 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/login/login-final-market.png | png / 1836193 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/login/login-reference.jpg | jpg / 95925 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/saer-header.png | png / 22435 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/saer-logo.png | png / 231596 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/sell/background.png | png / 767968 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/sell/breadcrumb.png | png / 16209 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/sell/heading.png | png / 102302 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/sell/information.png | png / 88462 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/sell/manual-reference.png | png / 306819 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/sell/photo-reference.png | png / 322403 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/public/ui/skyline.png | png / 245427 | واجهة وأصول/بيانات عرض | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| frontend/robots.txt | txt / 26 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/App.tsx | tsx / 330 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/DemoBanner.tsx | tsx / 722 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/LoginPage.tsx | tsx / 2017 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/ReferenceApp.tsx | tsx / 79213 | واجهة وأصول/بيانات عرض | فيه ملاحظة: اسم قديم؛ فحص نصي |
| frontend/src/config.ts | ts / 5889 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/data/reference-layout.json | json / 7173 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/hamoud-live-controls.css | css / 8799 | واجهة وأصول/بيانات عرض | فيه ملاحظة: اسم قديم؛ فحص نصي |
| frontend/src/hamoud-live-original.css | css / 9880 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/hamoud-live-original.ts | ts / 35548 | واجهة وأصول/بيانات عرض | فيه ملاحظة: اسم قديم؛ فحص نصي |
| frontend/src/hamoud-live-scoped.css | css / 11236 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/main.tsx | tsx / 237 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/reference.css | css / 46069 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/services/demoService.ts | ts / 15758 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/services/imageUpload.ts | ts / 820 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/services/uiService.ts | ts / 15923 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/style.css | css / 104 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/src/vite-env.d.ts | ts / 38 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/tsconfig.json | json / 470 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| frontend/vite.config.ts | ts / 4822 | واجهة وأصول/بيانات عرض | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/.gitignore | gitignore / 253 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/README.md | md / 5839 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/app.py | py / 8741 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/backend/__init__.py | py / 1 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/backend/app/__init__.py | py / 1 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/backend/app/config.py | py / 914 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/backend/app/hf_runtime.py | py / 7301 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/backend/app/services.py | py / 4709 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/model_store.py | py / 4385 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/models/image_price_hamoud_20261028/image_to_price_v2.py | py / 18241 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/models/image_price_hamoud_20261028/predict_image_price.py | py / 2740 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/requirements.txt | txt / 655 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/car_model_runtime.py | py / 13284 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/clip_identity_round_20261027.py | py / 6733 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/clip_identity_runtime_20261028.py | py / 4856 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/scripts/day20_common.py | py / 10446 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/scripts/day20_data_policy.py | py / 7100 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/day21_dataset_contract.py | py / 2284 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/foreground_visual_round_20261026.py | py / 16930 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/generalization_identity_runtime_20261028.py | py / 6184 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/scripts/geometry_visual_round_20261026.py | py / 9919 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/image_input_policy_20261026.py | py / 927 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/scripts/improve_common.py | py / 12464 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/improve_visual.py | py / 17029 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/ml_common.py | py / 3965 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/scripts/ml_price.py | py / 10824 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/ml_visual.py | py / 21960 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/model_image_tester.py | py / 20112 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/scripts/model_image_tester_20261026.py | py / 6206 | خادم النماذج ونسخ اعتماده | فيه ملاحظة: اسم قديم؛ فحص نصي |
| hf_backend/scripts/rescue_six_20261025.py | py / 23684 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/robust_visual_round_20261026.py | py / 13617 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/siarad_price_worker.py | py / 1062 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/visual_fusion_predict.py | py / 7058 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| hf_backend/scripts/visual_fusion_round.py | py / 21756 | خادم النماذج ونسخ اعتماده | فحص نصي؛ لا حكم شامل على المنطق |
| models/identity_current.json | json / 2277 | مؤشرات وأكواد/أوزان نماذج | فحص نصي؛ لا حكم شامل على المنطق |
| models/image_price_current.json | json / 1434 | مؤشرات وأكواد/أوزان نماذج | فحص نصي؛ لا حكم شامل على المنطق |
| models/image_price_hamoud_20261028/bundle.joblib | joblib / 5114410 | مؤشرات وأكواد/أوزان نماذج | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| models/image_price_hamoud_20261028/image_to_price_v2.py | py / 17512 | مؤشرات وأكواد/أوزان نماذج | فيه ملاحظة: اسم قديم؛ فحص نصي |
| models/image_price_hamoud_20261028/predict_image_price.py | py / 2740 | مؤشرات وأكواد/أوزان نماذج | فحص نصي؛ لا حكم شامل على المنطق |
| models/improvement_20261021T093545513846/price/best_model.joblib | joblib / 363504 | مؤشرات وأكواد/أوزان نماذج | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| models/improvement_20261021T093545513846/price/selected.json | json / 81 | مؤشرات وأكواد/أوزان نماذج | فحص نصي؛ لا حكم شامل على المنطق |
| models/improvement_current.json | json / 57 | مؤشرات وأكواد/أوزان نماذج | فحص نصي؛ لا حكم شامل على المنطق |
| notebooks/CarInsight_Identity_Model_Make_Reference.ipynb | ipynb / 14065 | دفاتر تجارب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| notebooks/README.md | md / 1548 | دفاتر تجارب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| notebooks/kaggle_server.ipynb | ipynb / 14535 | دفاتر تجارب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| outputs/generalization_rescue_20261028_v1/model/candidate.joblib | joblib / 438661 | ناتج نموذج معتمد | محتاج قرار/تحقق محتوى؛ بيانات الحجم والنوع فقط |
| requirements-data.txt | txt / 44 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| requirements-image-lock.txt | txt / 802 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| requirements-image.txt | txt / 336 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| requirements-models.txt | txt / 173 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| requirements-runtime-lock.txt | txt / 1520 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| requirements-runtime.txt | txt / 196 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| requirements-test.txt | txt / 32 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| requirements-web.txt | txt / 346 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| run_siarad.bat | bat / 577 | إعدادات أو وثائق جذرية | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/brand_final_finish.py | py / 20085 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/brand_final_round.py | py / 14453 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/build_essential_bundle.py | py / 6236 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/cache_identity_adapter_20261028.py | py / 11467 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/car_model_runtime.py | py / 13284 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/clip_identity_round_20261027.py | py / 6697 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/clip_identity_runtime_20261028.py | py / 4717 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/day20_clean.py | py / 39813 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_common.py | py / 10446 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/day20_content_policy.py | py / 5047 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_content_report.py | py / 28882 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_content_validate.py | py / 11443 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_data_policy.py | py / 7100 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_enrich.py | py / 5641 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_enrichment_audit.py | py / 16152 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/day20_enrichment_policy.py | py / 3833 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_external_review.py | py / 12232 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/day20_finalize_data.py | py / 16523 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_inventory.py | py / 10039 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/day20_publish_enriched.py | py / 12867 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_quality.py | py / 5246 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_recover.py | py / 15881 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/day20_report.py | py / 34048 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/day20_supplemental_validate.py | py / 5827 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day20_validate.py | py / 22631 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day21_dataset_contract.py | py / 2284 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/day21_issue_validate.py | py / 7149 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/foreground_visual_round_20261026.py | py / 16930 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/fusion_identity_round_20261026.py | py / 5549 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/generalization_identity_runtime_20261028.py | py / 6184 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/geometry_visual_round_20261026.py | py / 9919 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/identity_context_runtime_20261027.py | py / 4870 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/identity_to_price_handoff_20261028.py | py / 3502 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/image_input_policy_20261026.py | py / 927 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/image_price_final.py | py / 26116 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/image_price_multiview.py | py / 24202 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/image_price_multiview_finish.py | py / 24074 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/image_price_multiview_runtime.py | py / 3841 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/image_price_runtime.py | py / 5656 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/image_price_train.py | py / 32322 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/improve_common.py | py / 12464 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_external.py | py / 6867 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_finalize.py | py / 7569 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_make_head.py | py / 4176 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_package.py | py / 6812 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_predict.py | py / 4272 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_price.py | py / 6274 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_report.py | py / 18505 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/improve_search.py | py / 7681 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_val_finalize.py | py / 2161 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/improve_visual.py | py / 17029 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/ml_common.py | py / 3965 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/ml_delivery_runtime.py | py / 7878 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/ml_price.py | py / 10824 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/ml_visual.py | py / 21960 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/model_image_tester.py | py / 20112 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/model_image_tester_20261026.py | py / 6206 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/rescue_six_20261025.py | py / 23684 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/rescue_six_predict.py | py / 6096 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/retrain_dual_encoder_six.py | py / 14233 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/robust_visual_round_20261026.py | py / 13617 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/run_checks.py | py / 2832 | معالجة وتدريب وتشغيل | فيه ملاحظة: اسم قديم؛ فحص نصي |
| scripts/siarad_price_worker.py | py / 1062 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/train_clip_identity_heads_20261027.py | py / 8884 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/verify_essential_bundle.py | py / 3595 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/visual_fusion_predict.py | py / 6518 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| scripts/visual_fusion_round.py | py / 21662 | معالجة وتدريب وتشغيل | فحص نصي؛ لا حكم شامل على المنطق |
| tests/frontend-behavior.mjs | mjs / 5260 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/frontend-harness.html | html / 1489 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_brand_final_round.py | py / 1386 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_cache_identity_adapter_20261028.py | py / 1629 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_car_model_runtime.py | py / 4470 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_day20_content_policy.py | py / 3744 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_day20_data_policy.py | py / 4071 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_day20_enrichment.py | py / 5373 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_day20_publication.py | py / 1985 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_day20_quality.py | py / 2457 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_day20_recovery.py | py / 3831 | اختبارات | فيه ملاحظة: اسم قديم؛ فحص نصي |
| tests/test_day20_supplemental.py | py / 2126 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_day20_windows_save.py | py / 1903 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_day21_issue_fixes.py | py / 3119 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_identity_context_policy_20261027.py | py / 1914 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_identity_to_price_handoff_20261028.py | py / 1908 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_image_input_policy_20261026.py | py / 3611 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_image_price.py | py / 3762 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_image_price_multiview.py | py / 6076 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_improvement_protocol.py | py / 3143 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_ml_price.py | py / 2303 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_ml_runtime.py | py / 1689 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tests/test_ml_visual.py | py / 1874 | اختبارات | فحص نصي؛ لا حكم شامل على المنطق |
| tools/check_runtime_env.py | py / 1406 | أدوات تشغيل وتحقق | فحص نصي؛ لا حكم شامل على المنطق |
| tools/clean_cars.py | py / 3795 | أدوات تشغيل وتحقق | فحص نصي؛ لا حكم شامل على المنطق |
| tools/export_demo_data.py | py / 12842 | أدوات تشغيل وتحقق | فيه ملاحظة: اسم قديم؛ فحص نصي |
| tools/export_demo_images.py | py / 8849 | أدوات تشغيل وتحقق | فحص نصي؛ لا حكم شامل على المنطق |
| tools/package_delivery.py | py / 3856 | أدوات تشغيل وتحقق | فحص نصي؛ لا حكم شامل على المنطق |
| tools/package_kaggle.py | py / 1521 | أدوات تشغيل وتحقق | فحص نصي؛ لا حكم شامل على المنطق |
| tools/restore_public_encoders.py | py / 4272 | أدوات تشغيل وتحقق | فحص نصي؛ لا حكم شامل على المنطق |
| tools/start_runtime.ps1 | ps1 / 1780 | أدوات تشغيل وتحقق | فحص نصي؛ لا حكم شامل على المنطق |
| tools/verify_delivery_runtime.py | py / 3004 | أدوات تشغيل وتحقق | فحص نصي؛ لا حكم شامل على المنطق |

## نتيجة الإغلاق

التعديلات الآمنة موثقة ومحصورة على فرع المراجعة. بحث الأسماء ليس صفرًا، واختبارات Python ليست ناجحة بالكامل، والتشغيل الكامل والجرد المحلي وحقوق الصور غير متحقق منها. لذلك هذه **مراجعة جزئية موثقة مع عوائق** وليست شهادة تنظيف كامل أو جاهزية تشغيل عامة. لا دمج إلى main قبل مراجعة القرارات أعلاه.

### إعادة الفحص قبل التسليم

بعد التعديلات بقي **82 سطرًا مطابقًا** في نطاق الملفات النصية الأصلية، مقابل 84 قبلها؛ لا تُحسب أسماء التقرير نفسه بوصفها عيبًا جديدًا لأنها سجل النتائج المطلوب. اختبار .gitignore مستقل: **10 مسارات، ناجح** (سبعة محمية وثلاثة مسموحة). أُعيدت اختبارات الواجهة السبعة وTypeScript والبناء والتحليل النحوي؛ نتائج Python بقيت 79 تشغيلًا و11 خطأ و4 تخطيات. طوبقت شجرة الفرع البعيد: 301 ملفًا بعد إضافة التقرير، صفر ملف أصلي مفقود، ولا اختلاف في الكود أو البيانات أو الأوزان أو الصور؛ الاختلافات في ستة ملفات توثيق/إعداد فقط إضافة إلى التقرير الجديد.
