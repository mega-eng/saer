# مراجعة هوية سعّر — ملفًا بملف

مرجع البداية: `775de1f2d9c7d380c6321d5ead5d0359fdda4d06`.
كل ملف نصي أدناه جُلب كاملًا أو استُخدمت نسخة سبق جلبها مطابقة لبصمة Git، ثم أُعيد البحث في محتواه. المراجعة تخص هوية المشروع، ولا تدّعي تدقيقًا علميًا كاملًا لكل منطق التدريب. الصور والأوزان وSQLite والخط فُحصت مساراتها وأحجامها فقط؛ لم تُفتح بصريًا ولم تتغير.

## الأسماء المعتمدة

- الاسم الظاهر: سعّر. يستخدم Saer/saer في الأسماء التقنية والإنجليزية الحالية.
- الدفتر الحالي: `notebooks/saer_identity_reference.ipynb`؛ عنوانه الداخلي سعّر ومفتاح metadata هو saer.
- المشغّل: `run_saer.bat`. عامل الصورة: `scripts/saer_price_worker.py` ونسخته في hf_backend؛ حُدث المستدعيان.
- الجلسات الجديدة saer_session؛ قراءة الكوكي السابق محصورة في طبقة التوافق واختباراتها. قاعدة بيانات جديدة saer.sqlite، مع إعادة استخدام القاعدة السابقة إن كانت موجودة دون تغييرها.

## الاستثناءات الدقيقة الباقية

| المجموعة | السبب |
|---|---|
| CSV وJSON بيانات الإعلانات، ثوابت source_dataset وlisting_uid ومسارات raw والاستعادة والاختبارات المتعلقة بها | معرّفات مصدر مترابطة مع بيانات ونماذج محفوظة؛ تغييرها يتطلب migration خارج هذه المهمة. ليست اسم العلامة الظاهر |
| backend/app/branding_compat.py وtests/test_branding_compat.py | اسما كوكي وقاعدة سابقان فقط للحفاظ على بيانات وجلسات المستخدمين؛ الثلاثة اختبارات نجحت |
| tools/export_demo_data.py | أسماء إدخال قديمة للتحويل إلى الاسم الحالي؛ حذفها يعطل تنظيف المدخلات السابقة |
| scripts/image_price_final.py وscripts/ml_common.py ونسخته وscripts/day20_inventory.py | مسارات موارد تدريب خارجية قديمة؛ لم تُنقل الموارد الخارجية |
| scripts/day20_report.py | إسناد إلى حزمة مصدر قديمة غير مرفقة؛ لا يعاد اختراع اسم الحزمة |
| docs/PHASE5_VERIFICATION.json وdocs/FILE_MANIFEST.json وREPO_AUDIT_REPORT.md | سجلات لقطة سابقة وأسماء أصلية وبصمات؛ لا تُحرّف أدلة الفحص التاريخية بعد إعادة التسمية |
| docs/PHASE3_RUNTIME.md وdocs/SAMPLE_IMAGES.md وDATA_CONTRACT.md وREQ.md | تعريف مصدر البيانات ومعرّف العينة أو مسارها الأصلي، وليس عنوان المنتج |

لا توجد أسماء قديمة متبقية في عناوين/وصف الخادم والدفاتر ونوافذ أدوات الاختبار أو قالب عنوان تقدير الصورة بعد التعديل. لا توجد مسارات ملفات حالية بأسماء العلامتين السابقتين؛ الاستثناء فقط داخل السجلات التاريخية والمعرّفات المذكورة.

## التحقق

- 3 اختبارات توافق مستقلة: ناجحة؛ اختبرت بقاء محتوى قاعدة قديمة كما هو، تفضيل القاعدة الحالية، واستمرار قراءة جلسة سابقة.
- 7 اختبارات سلوك واجهة: ناجحة. TypeScript والبناء العادي التشخيصي ناجحان؛ الأصول الثنائية غير موجودة في نسخة الاختبار النصية لذا بقيت تحذيرات أصولها، ولم يُدّع اختبار حزمة النشر المكتملة.
- التحليل النحوي لملفات Python وخلايا code في الدفتر المعاد تسميته: ناجح. الدفتر لم يُنفذ، لأنه يعتمد نتائج وكاشًا وملفات خارج المستودع.
- الجولة الشاملة الحالية: 82 تشغيل اختبار، 11 خطأ و4 تخطيات كما في العوائق البيئية السابقة، ولا فشل assertions؛ لا ادعاء بنجاح كامل أو اختبار الاستدلال الفعلي.
- لم تُثبّت أو تُرقّ حزم في هذه الجولة، ولم تتغير الأوزان أو البيانات أو قيم المقاييس أو النشر أو main أو تاريخ commits.

## جدول الملفات

الأرقام في عمود المطابقات تعني عدد الأسطر المطابقة بعد التعديل، لا عدد العلامات الظاهرة في المنتج. سجلات التدقيق قد تذكر الأسماء الأصلية عمدًا. الملفات المضافة للتقرير نفسه خارج مرجع البداية.

| المسار الحالي | القراءة | الإجراء | أسطر مطابقة باقية |
|---|---|---|---:|
| .env.example | نصي كامل | محفوظ | 0 |
| .gitignore | نصي كامل | محفوظ | 0 |
| AGENTS.md | نصي كامل | محفوظ | 0 |
| DATA_CONTRACT.md | نصي كامل | محفوظ | 3 |
| DELIVERY.md | نصي كامل | محفوظ | 0 |
| ML_SPEC.md | نصي كامل | محفوظ | 0 |
| PROGRESS.md | نصي كامل | محفوظ | 0 |
| README.md | نصي كامل | محفوظ | 0 |
| REPO_AUDIT_REPORT.md | نصي كامل | محفوظ | 83 |
| REQ.md | نصي كامل | محفوظ | 1 |
| ROADMAP.md | نصي كامل | محفوظ | 0 |
| TEST_PLAN.md | نصي كامل | محفوظ | 0 |
| backend/__init__.py | نصي كامل | تعديل | 0 |
| backend/app/__init__.py | نصي كامل | تعديل | 0 |
| backend/app/branding_compat.py | نصي كامل | تعديل | 2 |
| backend/app/config.py | نصي كامل | تعديل | 0 |
| backend/app/db.py | نصي كامل | محفوظ | 0 |
| backend/app/main.py | نصي كامل | تعديل | 0 |
| backend/app/runtime_bridge.py | نصي كامل | محفوظ | 0 |
| backend/app/schemas.py | نصي كامل | محفوظ | 0 |
| backend/app/services.py | نصي كامل | تعديل | 0 |
| data/processed/images.csv | نصي كامل | محفوظ | 13416 |
| data/processed/listings.csv | نصي كامل | محفوظ | 2742 |
| data/seed/saer.sqlite | اسم/حجم/نوع فقط | محفوظ | 0 |
| docs/BRANCH_NAMING_UPDATE.md | نصي كامل | محفوظ | 0 |
| docs/FILE_MANIFEST.json | نصي كامل | محفوظ | 4 |
| docs/FRONTEND_FIX_VALIDATION.md | نصي كامل | محفوظ | 0 |
| docs/GRADIO_VERIFICATION.json | نصي كامل | محفوظ | 0 |
| docs/PHASE2_HANDOFF.md | نصي كامل | محفوظ | 0 |
| docs/PHASE3_RUNTIME.md | نصي كامل | محفوظ | 1 |
| docs/PHASE4_REPRODUCIBILITY.md | نصي كامل | محفوظ | 0 |
| docs/PHASE4_VERIFICATION.json | نصي كامل | محفوظ | 0 |
| docs/PHASE5_VERIFICATION.json | نصي كامل | محفوظ | 2 |
| docs/PUBLIC_ENCODERS.json | نصي كامل | محفوظ | 0 |
| docs/PUBLIC_ENCODERS.md | نصي كامل | محفوظ | 0 |
| docs/PUBLISHED_STATE.json | نصي كامل | محفوظ | 0 |
| docs/RUNTIME_VERIFICATION.json | نصي كامل | محفوظ | 0 |
| docs/SAMPLE_IMAGES.md | نصي كامل | محفوظ | 1 |
| docs/SETUP.md | نصي كامل | محفوظ | 0 |
| docs/UNIFICATION_VERIFICATION.json | نصي كامل | محفوظ | 0 |
| docs/assets/README.md | نصي كامل | محفوظ | 0 |
| docs/assets/home-screen.jpg | اسم/حجم/نوع فقط | محفوظ | 0 |
| docs/assets/listings-screen.jpg | اسم/حجم/نوع فقط | محفوظ | 0 |
| docs/assets/market-screen.jpg | اسم/حجم/نوع فقط | محفوظ | 0 |
| docs/runtime-assets.json | نصي كامل | محفوظ | 0 |
| frontend/.env.example | نصي كامل | محفوظ | 0 |
| frontend/_headers | نصي كامل | محفوظ | 0 |
| frontend/_redirects | نصي كامل | محفوظ | 0 |
| frontend/index.html | نصي كامل | محفوظ | 0 |
| frontend/package.json | نصي كامل | محفوظ | 0 |
| frontend/pnpm-lock.yaml | نصي كامل | محفوظ | 0 |
| frontend/public/assets/road-cars/car1.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/assets/road-cars/car2.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/assets/road-cars/car3.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/assets/road-cars/car4.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/assets/road-cars/car5.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/brands/README.md | نصي كامل | محفوظ | 0 |
| frontend/public/brands/audi.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/bmw.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/brands.json | نصي كامل | محفوظ | 0 |
| frontend/public/brands/cadillac.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/chevrolet.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/chrysler.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/ford.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/honda.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/hyundai.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/jeep.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/kia.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/mazda.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/mg.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/mini.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/mitsubishi.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/nissan.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/porsche.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/suzuki.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/toyota.svg | نصي كامل | محفوظ | 0 |
| frontend/public/brands/volkswagen.svg | نصي كامل | محفوظ | 0 |
| frontend/public/demo/img/sample-1186/04.webp | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/demo/listings.json | نصي كامل | محفوظ | 0 |
| frontend/public/demo/market.json | نصي كامل | محفوظ | 0 |
| frontend/public/demo/meta.json | نصي كامل | محفوظ | 0 |
| frontend/public/demo/placeholder.svg | نصي كامل | محفوظ | 0 |
| frontend/public/demo/pricing-options.json | نصي كامل | محفوظ | 0 |
| frontend/public/demo/recommendations.json | نصي كامل | محفوظ | 0 |
| frontend/public/fonts/Cairo.ttf | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/fonts/OFL.txt | نصي كامل | محفوظ | 0 |
| frontend/public/ui/budget/background.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/car0-default.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/car1-default.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/car2-default.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/car3-default.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/car4-default.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/filters.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/heading.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/notice.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/refresh.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/budget/results-heading.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/compare/background.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/compare/first-reference.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/compare/heading.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/compare/information.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/compare/second-reference.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/compare/submit.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/compare/table.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/details/background.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/details/breadcrumb.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/details/form-no-confirm.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/details/heading.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/details/identity-manual.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/details/identity-reference.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/details/information.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/home/browse-feature-user.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/home/budget-cars-cutout.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/home/compare-feature-user.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/home/estimate-feature-user.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/home/home-final.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/home/sell-car-cutout.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/login/login-final-market.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/login/login-reference.jpg | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/saer-header.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/saer-logo.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/sell/background.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/sell/breadcrumb.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/sell/heading.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/sell/information.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/sell/manual-reference.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/sell/photo-reference.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/public/ui/skyline.png | اسم/حجم/نوع فقط | محفوظ | 0 |
| frontend/robots.txt | نصي كامل | محفوظ | 0 |
| frontend/src/App.tsx | نصي كامل | محفوظ | 0 |
| frontend/src/DemoBanner.tsx | نصي كامل | محفوظ | 0 |
| frontend/src/LoginPage.tsx | نصي كامل | محفوظ | 0 |
| frontend/src/ReferenceApp.tsx | نصي كامل | تعديل | 0 |
| frontend/src/config.ts | نصي كامل | محفوظ | 0 |
| frontend/src/data/reference-layout.json | نصي كامل | محفوظ | 0 |
| frontend/src/hamoud-live-controls.css | نصي كامل | محفوظ | 0 |
| frontend/src/hamoud-live-original.css | نصي كامل | محفوظ | 0 |
| frontend/src/hamoud-live-original.ts | نصي كامل | تعديل | 0 |
| frontend/src/hamoud-live-scoped.css | نصي كامل | محفوظ | 0 |
| frontend/src/main.tsx | نصي كامل | محفوظ | 0 |
| frontend/src/reference.css | نصي كامل | محفوظ | 0 |
| frontend/src/services/demoService.ts | نصي كامل | محفوظ | 0 |
| frontend/src/services/imageUpload.ts | نصي كامل | محفوظ | 0 |
| frontend/src/services/uiService.ts | نصي كامل | محفوظ | 0 |
| frontend/src/style.css | نصي كامل | محفوظ | 0 |
| frontend/src/vite-env.d.ts | نصي كامل | محفوظ | 0 |
| frontend/tsconfig.json | نصي كامل | محفوظ | 0 |
| frontend/vite.config.ts | نصي كامل | محفوظ | 0 |
| hf_backend/.gitignore | نصي كامل | محفوظ | 0 |
| hf_backend/README.md | نصي كامل | محفوظ | 0 |
| hf_backend/app.py | نصي كامل | محفوظ | 0 |
| hf_backend/backend/__init__.py | نصي كامل | محفوظ | 0 |
| hf_backend/backend/app/__init__.py | نصي كامل | محفوظ | 0 |
| hf_backend/backend/app/config.py | نصي كامل | محفوظ | 0 |
| hf_backend/backend/app/hf_runtime.py | نصي كامل | محفوظ | 0 |
| hf_backend/backend/app/services.py | نصي كامل | تعديل | 0 |
| hf_backend/model_store.py | نصي كامل | محفوظ | 0 |
| hf_backend/models/image_price_hamoud_20261028/image_to_price_v2.py | نصي كامل | تعديل | 0 |
| hf_backend/models/image_price_hamoud_20261028/predict_image_price.py | نصي كامل | محفوظ | 0 |
| hf_backend/requirements.txt | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/car_model_runtime.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/clip_identity_round_20261027.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/clip_identity_runtime_20261028.py | نصي كامل | تعديل | 0 |
| hf_backend/scripts/day20_common.py | نصي كامل | محفوظ | 3 |
| hf_backend/scripts/day20_data_policy.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/day21_dataset_contract.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/foreground_visual_round_20261026.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/generalization_identity_runtime_20261028.py | نصي كامل | تعديل | 0 |
| hf_backend/scripts/geometry_visual_round_20261026.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/image_input_policy_20261026.py | نصي كامل | تعديل | 0 |
| hf_backend/scripts/improve_common.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/improve_visual.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/ml_common.py | نصي كامل | محفوظ | 2 |
| hf_backend/scripts/ml_price.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/ml_visual.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/model_image_tester.py | نصي كامل | تعديل | 0 |
| hf_backend/scripts/model_image_tester_20261026.py | نصي كامل | تعديل | 0 |
| hf_backend/scripts/rescue_six_20261025.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/robust_visual_round_20261026.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/saer_price_worker.py | نصي كامل | تعديل | 0 |
| hf_backend/scripts/visual_fusion_predict.py | نصي كامل | محفوظ | 0 |
| hf_backend/scripts/visual_fusion_round.py | نصي كامل | محفوظ | 0 |
| models/identity_current.json | نصي كامل | محفوظ | 0 |
| models/image_price_current.json | نصي كامل | محفوظ | 0 |
| models/image_price_hamoud_20261028/bundle.joblib | اسم/حجم/نوع فقط | محفوظ | 0 |
| models/image_price_hamoud_20261028/image_to_price_v2.py | نصي كامل | تعديل | 0 |
| models/image_price_hamoud_20261028/predict_image_price.py | نصي كامل | محفوظ | 0 |
| models/improvement_20261021T093545513846/price/best_model.joblib | اسم/حجم/نوع فقط | محفوظ | 0 |
| models/improvement_20261021T093545513846/price/selected.json | نصي كامل | محفوظ | 0 |
| models/improvement_current.json | نصي كامل | محفوظ | 0 |
| notebooks/README.md | نصي كامل | تعديل | 0 |
| notebooks/kaggle_server.ipynb | نصي كامل | محفوظ | 0 |
| notebooks/saer_identity_reference.ipynb | نصي كامل | تعديل | 0 |
| outputs/generalization_rescue_20261028_v1/model/candidate.joblib | اسم/حجم/نوع فقط | محفوظ | 0 |
| requirements-data.txt | نصي كامل | محفوظ | 0 |
| requirements-image-lock.txt | نصي كامل | محفوظ | 0 |
| requirements-image.txt | نصي كامل | محفوظ | 0 |
| requirements-models.txt | نصي كامل | محفوظ | 0 |
| requirements-runtime-lock.txt | نصي كامل | محفوظ | 0 |
| requirements-runtime.txt | نصي كامل | محفوظ | 0 |
| requirements-test.txt | نصي كامل | محفوظ | 0 |
| requirements-web.txt | نصي كامل | محفوظ | 0 |
| run_saer.bat | نصي كامل | تعديل | 0 |
| scripts/brand_final_finish.py | نصي كامل | محفوظ | 2 |
| scripts/brand_final_round.py | نصي كامل | محفوظ | 1 |
| scripts/build_essential_bundle.py | نصي كامل | محفوظ | 0 |
| scripts/cache_identity_adapter_20261028.py | نصي كامل | محفوظ | 0 |
| scripts/car_model_runtime.py | نصي كامل | محفوظ | 0 |
| scripts/clip_identity_round_20261027.py | نصي كامل | محفوظ | 0 |
| scripts/clip_identity_runtime_20261028.py | نصي كامل | تعديل | 0 |
| scripts/day20_clean.py | نصي كامل | محفوظ | 0 |
| scripts/day20_common.py | نصي كامل | محفوظ | 3 |
| scripts/day20_content_policy.py | نصي كامل | محفوظ | 0 |
| scripts/day20_content_report.py | نصي كامل | محفوظ | 0 |
| scripts/day20_content_validate.py | نصي كامل | محفوظ | 0 |
| scripts/day20_data_policy.py | نصي كامل | محفوظ | 0 |
| scripts/day20_enrich.py | نصي كامل | محفوظ | 0 |
| scripts/day20_enrichment_audit.py | نصي كامل | محفوظ | 1 |
| scripts/day20_enrichment_policy.py | نصي كامل | محفوظ | 0 |
| scripts/day20_external_review.py | نصي كامل | محفوظ | 1 |
| scripts/day20_finalize_data.py | نصي كامل | محفوظ | 0 |
| scripts/day20_inventory.py | نصي كامل | محفوظ | 1 |
| scripts/day20_publish_enriched.py | نصي كامل | محفوظ | 0 |
| scripts/day20_quality.py | نصي كامل | محفوظ | 0 |
| scripts/day20_recover.py | نصي كامل | تعديل | 0 |
| scripts/day20_report.py | نصي كامل | محفوظ | 2 |
| scripts/day20_supplemental_validate.py | نصي كامل | محفوظ | 0 |
| scripts/day20_validate.py | نصي كامل | محفوظ | 0 |
| scripts/day21_dataset_contract.py | نصي كامل | محفوظ | 0 |
| scripts/day21_issue_validate.py | نصي كامل | محفوظ | 1 |
| scripts/foreground_visual_round_20261026.py | نصي كامل | محفوظ | 0 |
| scripts/fusion_identity_round_20261026.py | نصي كامل | محفوظ | 0 |
| scripts/generalization_identity_runtime_20261028.py | نصي كامل | تعديل | 0 |
| scripts/geometry_visual_round_20261026.py | نصي كامل | محفوظ | 0 |
| scripts/identity_context_runtime_20261027.py | نصي كامل | تعديل | 0 |
| scripts/identity_to_price_handoff_20261028.py | نصي كامل | محفوظ | 0 |
| scripts/image_input_policy_20261026.py | نصي كامل | تعديل | 0 |
| scripts/image_price_final.py | نصي كامل | محفوظ | 1 |
| scripts/image_price_multiview.py | نصي كامل | محفوظ | 0 |
| scripts/image_price_multiview_finish.py | نصي كامل | محفوظ | 0 |
| scripts/image_price_multiview_runtime.py | نصي كامل | محفوظ | 0 |
| scripts/image_price_runtime.py | نصي كامل | محفوظ | 0 |
| scripts/image_price_train.py | نصي كامل | محفوظ | 1 |
| scripts/improve_common.py | نصي كامل | محفوظ | 0 |
| scripts/improve_external.py | نصي كامل | محفوظ | 0 |
| scripts/improve_finalize.py | نصي كامل | محفوظ | 0 |
| scripts/improve_make_head.py | نصي كامل | محفوظ | 0 |
| scripts/improve_package.py | نصي كامل | محفوظ | 0 |
| scripts/improve_predict.py | نصي كامل | محفوظ | 0 |
| scripts/improve_price.py | نصي كامل | محفوظ | 0 |
| scripts/improve_report.py | نصي كامل | تعديل | 0 |
| scripts/improve_search.py | نصي كامل | محفوظ | 0 |
| scripts/improve_val_finalize.py | نصي كامل | محفوظ | 0 |
| scripts/improve_visual.py | نصي كامل | محفوظ | 0 |
| scripts/ml_common.py | نصي كامل | محفوظ | 2 |
| scripts/ml_delivery_runtime.py | نصي كامل | محفوظ | 0 |
| scripts/ml_price.py | نصي كامل | محفوظ | 0 |
| scripts/ml_visual.py | نصي كامل | محفوظ | 0 |
| scripts/model_image_tester.py | نصي كامل | تعديل | 0 |
| scripts/model_image_tester_20261026.py | نصي كامل | تعديل | 0 |
| scripts/rescue_six_20261025.py | نصي كامل | محفوظ | 0 |
| scripts/rescue_six_predict.py | نصي كامل | محفوظ | 0 |
| scripts/retrain_dual_encoder_six.py | نصي كامل | محفوظ | 0 |
| scripts/robust_visual_round_20261026.py | نصي كامل | محفوظ | 0 |
| scripts/run_checks.py | نصي كامل | محفوظ | 1 |
| scripts/saer_price_worker.py | نصي كامل | تعديل | 0 |
| scripts/train_clip_identity_heads_20261027.py | نصي كامل | محفوظ | 0 |
| scripts/verify_essential_bundle.py | نصي كامل | محفوظ | 0 |
| scripts/visual_fusion_predict.py | نصي كامل | محفوظ | 0 |
| scripts/visual_fusion_round.py | نصي كامل | محفوظ | 0 |
| tests/frontend-behavior.mjs | نصي كامل | محفوظ | 0 |
| tests/frontend-harness.html | نصي كامل | محفوظ | 0 |
| tests/test_brand_final_round.py | نصي كامل | محفوظ | 0 |
| tests/test_branding_compat.py | نصي كامل | تعديل | 4 |
| tests/test_cache_identity_adapter_20261028.py | نصي كامل | محفوظ | 0 |
| tests/test_car_model_runtime.py | نصي كامل | محفوظ | 0 |
| tests/test_day20_content_policy.py | نصي كامل | محفوظ | 0 |
| tests/test_day20_data_policy.py | نصي كامل | محفوظ | 0 |
| tests/test_day20_enrichment.py | نصي كامل | محفوظ | 0 |
| tests/test_day20_publication.py | نصي كامل | محفوظ | 0 |
| tests/test_day20_quality.py | نصي كامل | محفوظ | 0 |
| tests/test_day20_recovery.py | نصي كامل | محفوظ | 3 |
| tests/test_day20_supplemental.py | نصي كامل | محفوظ | 0 |
| tests/test_day20_windows_save.py | نصي كامل | محفوظ | 0 |
| tests/test_day21_issue_fixes.py | نصي كامل | محفوظ | 0 |
| tests/test_identity_context_policy_20261027.py | نصي كامل | محفوظ | 0 |
| tests/test_identity_to_price_handoff_20261028.py | نصي كامل | محفوظ | 0 |
| tests/test_image_input_policy_20261026.py | نصي كامل | محفوظ | 0 |
| tests/test_image_price.py | نصي كامل | محفوظ | 0 |
| tests/test_image_price_multiview.py | نصي كامل | محفوظ | 0 |
| tests/test_improvement_protocol.py | نصي كامل | محفوظ | 0 |
| tests/test_ml_price.py | نصي كامل | محفوظ | 0 |
| tests/test_ml_runtime.py | نصي كامل | محفوظ | 0 |
| tests/test_ml_visual.py | نصي كامل | محفوظ | 0 |
| tools/check_runtime_env.py | نصي كامل | محفوظ | 0 |
| tools/clean_cars.py | نصي كامل | محفوظ | 0 |
| tools/export_demo_data.py | نصي كامل | محفوظ | 1 |
| tools/export_demo_images.py | نصي كامل | محفوظ | 0 |
| tools/package_delivery.py | نصي كامل | محفوظ | 0 |
| tools/package_kaggle.py | نصي كامل | محفوظ | 0 |
| tools/restore_public_encoders.py | نصي كامل | محفوظ | 0 |
| tools/start_runtime.ps1 | نصي كامل | محفوظ | 0 |
| tools/verify_delivery_runtime.py | نصي كامل | محفوظ | 0 |
