# إصلاح رفع صورة واحدة — Kaggle

المرجع: الدفتر المرفق ai-saer fim.ipynb. لا تعدل الأصل. الدفتر الجديد notebooks/kaggle_single_image.ipynb جاهز للرفع إلى Kaggle كدفتر مستقل، مع نفس Dataset والأسرار المسماة الموجودة سابقًا. إذا أوقفت الدفتر القديم فلا تعِد تشغيله. لا تشغل دفترين على نطاق ngrok نفسه.

## الترتيب

1. في الدفتر الجديد شغل خلايا النسخ والمتطلبات وفحص الأصول بالترتيب. أزيل أمر تثبيت Gradio 5.49.1 المنفرد لأنه يتعارض مع خلية المتطلبات الأصلية التي تختار 6.31.0. لا تغيير للأوزان.
2. خلية إصلاح العقد الجديدة تأتي مباشرة بعد خلية «فحص الأصول وإعداد البيئة» وقبل خلية «تشغيل الخادم والنفق». إذا كنت تعدل الدفتر القديم، أضف الخلية التالية في ذلك الموضع في جلسة لم تستورد app بعد؛ لا يكفي تعديل الملف في خادم قائم. تحفظ الخلية نسخة app السابقة وتتحقق من بنيتها قبل الكتابة.
3. شغل خلية تشغيل الخادم والنفق الأصلية كما هي. لا ترسل محتويات الأسرار في المحادثة.
4. شغل خلية فحص العقد أدناه بعد ظهور الرابط العام. يجب أن يكون مدخلا predict_image وidentify_vehicle كلاهما FileData واحدًا، لا ListFiles.
5. افتح رابط Pages الذي يطبعه الدفتر، ارفع صورة واحدة، واضغط «قدّر السعر». النجاح يتطلب ظهور سعر فعلي. جرّب صورة أخرى أيضًا؛ لا تعتبر فحص المخطط وحده نجاحًا.

## خلية إصلاح العقد كاملة

```python
# إصلاح العقد قبل تشغيل الخادم؛ لا يستدعي النماذج ولا ينزل الأوزان.
import sys
if 'app' in sys.modules:
    raise RuntimeError('app محمل بالفعل؛ شغل هذا الدفتر في جلسة جديدة قبل تشغيل الخادم.')
"""إصلاح عقد الصورة في حزمة Kaggle دون تغيير الأوزان أو تنزيل ملفات."""

import ast
from datetime import datetime, timezone
from pathlib import Path


def repair(root: Path) -> Path:
    path = root / "app.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    for name in ("_valid_image_path", "estimate_image_price", "identify_vehicle"):
        if name not in functions:
            raise RuntimeError(f"توقف: لم أجد الدالة المتوقعة {name}؛ لم أعدل الملف")
    replacements = {
        "_valid_image_path": '''def _valid_image_path(value):
    if isinstance(value, (list, tuple)):
        raise ValueError("ارفع صورة واحدة فقط للسيارة")
    if not isinstance(value, (str, Path)) or not value:
        raise ValueError("اختر صورة السيارة أولًا")
    if _startup_error:
        raise RuntimeError(_startup_error)
    path = Path(value)
    if not path.is_file() or not 0 < path.stat().st_size <= 12 * 1024 * 1024:
        raise ValueError("الصورة مفقودة أو فارغة أو حجمها يتجاوز 12 ميجابايت")
    from PIL import Image, UnidentifiedImageError
    try:
        with Image.open(path) as image:
            if image.format not in {"JPEG", "PNG", "WEBP"}:
                raise ValueError("الصيغ المدعومة: JPG وPNG وWebP")
            if image.width * image.height > 40_000_000:
                raise ValueError("أبعاد الصورة كبيرة جداً")
            image.verify()
    except (OSError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        raise ValueError("ملف الصورة غير صالح") from exc
    return path
''',
        "estimate_image_price": '''def estimate_image_price(upload):
    paths = upload if isinstance(upload, list) else [upload]
    if len(paths) != 1:
        raise ValueError("ارفع صورة واحدة فقط للسيارة")
    checked = [_valid_image_path(path) for path in paths]
    digest = hashlib.sha256("|".join(services.file_sha256(path) for path in checked).encode()).hexdigest()
    result = services.predict_image_price(checked, digest)
    notice = "تقدير تجريبي من صورة واحدة؛ لا يرى الممشى أو الحالة وليس سعر بيع مضموناً."
    return {**result, "image_count": 1, "notice_ar": notice, "notice": notice}
''',
    }
    lines = source.splitlines(keepends=True)
    edits = [(functions[name].lineno - 1, functions[name].end_lineno, code + "\n") for name, code in replacements.items()]
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
            continue
        names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        for name in ("identity_file", "price_files"):
            if name not in names:
                continue
            if ast.unparse(node.value.func) != "gr.File":
                raise RuntimeError(f"توقف: {name} ليس gr.File")
            found.add(name)
            node.value.keywords = [kw for kw in node.value.keywords if kw.arg not in {"file_count", "label"}]
            node.value.keywords.extend([ast.keyword(arg="file_count", value=ast.Constant("single")), ast.keyword(arg="label", value=ast.Constant("صورة السيارة"))])
            indent = " " * node.col_offset
            edits.append((node.lineno - 1, node.end_lineno, indent + ast.unparse(node) + "\n"))
    if found != {"identity_file", "price_files"}:
        raise RuntimeError("توقف: لم أجد مدخلي Gradio المتوقعين؛ لم أعدل الملف")
    for start, end, code in sorted(edits, reverse=True):
        lines[start:end] = [code]
    updated = "".join(lines)
    compile(updated, str(path), "exec")
    backup = path.with_name("app.before-single-image-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + ".py")
    backup.write_bytes(path.read_bytes())
    path.write_text(updated, encoding="utf-8")
    print("تم إصلاح مدخلي الصورة، وحفظ النسخة السابقة:", backup)
    return backup


repair(bundle_root)

```

## خلية فحص الخادم بعد التشغيل

```python
# فحص العقد المحلي والعام بعد تشغيل الخادم والنفق.
import requests
headers = {'ngrok-skip-browser-warning': 'true'}
for base in ('http://127.0.0.1:7860', api_url):
    response = requests.get(base.rstrip('/') + '/config', headers=headers, timeout=45)
    response.raise_for_status()
    cfg = response.json()
    components = {item['id']: item for item in cfg['components']}
    for endpoint in ('predict_image', 'identify_vehicle'):
        dep = next(item for item in cfg['dependencies'] if item.get('api_name') == endpoint)
        assert len(dep['inputs']) == 1, (endpoint, 'عدد معاملات غير متوقع')
        comp = components[dep['inputs'][0]]
        assert comp['type'] == 'file' and comp['props']['file_count'] == 'single', endpoint
        assert comp['api_info']['type'] == 'object', endpoint
        print(base, endpoint, 'FileData واحد — صحيح')
# فحص الرفض في الدالة نفسها قبل تحميل/استدعاء النموذج.
try:
    saer_server.estimate_image_price(['first.jpg', 'second.jpg'])
except ValueError as exc:
    assert 'صورة واحدة' in str(exc)
    print('رفض أكثر من صورة:', exc)
else:
    raise AssertionError('الخادم لم يرفض الصور المتعددة')
print('نجح فحص العقد. هذا ليس إثباتًا لنجاح التنبؤ؛ شغل اختبار الصورة ثم الموقع.')

```

## خلية اختبار النموذجين الاختيارية

حدد TEST_IMAGE بصورة سيارة تملك صلاحية استخدامها، ثم شغل هذه الخلية. لا تحتوي نتائج محفوظة؛ الحقل «من_ذاكرة_مؤقتة» يبين أي استعمال للكاش. فشلها يعني أن الاستدلال لم ينجح، حتى لو كان المخطط صحيحًا.

```python
TEST_IMAGE = ""  # مثال: /kaggle/input/your-dataset/car.jpg
if not TEST_IMAGE:
    print('لم يُختبر التنبؤ بعد: ضع مسار صورة فعلية ثم شغل هذه الخلية.')
else:
    from pathlib import Path
    from gradio_client import Client, handle_file
    import math
    image = Path(TEST_IMAGE)
    assert image.is_file(), 'لم أجد الصورة'
    client = Client(api_url, headers={'ngrok-skip-browser-warning': 'true'})
    price = client.predict(handle_file(str(image)), api_name='/predict_image')
    assert isinstance(price, dict) and isinstance(price.get('price_sar'), (int, float)) and math.isfinite(price['price_sar']), price
    assert price.get('image_count') == 1, price
    print('نتيجة السعر الفعلية:', price)
    identity = client.predict(handle_file(str(image)), api_name='/identify_vehicle')
    assert isinstance(identity, dict) and identity.get('الاقتراح_الرئيسي'), identity
    print('نتيجة التعرف الفعلية:', identity)

```

## حدود التحقق

حُللت خلايا الدفتر نحويًا واختُبر سكربت الإصلاح على نسخة مؤقتة محلية من app.py. لم يُشغّل الدفتر على Kaggle من هذه الجلسة. خادم المستخدم توقف أثناء الفحص وأعاد ERR_NGROK_3200؛ يلزم تشغيل الدفتر ثم إعادة اختبار الموقع. لا ينقل دفع GitHub ولا نشر Pages التعديلات تلقائيًا إلى Dataset على Kaggle، لذلك خلية الإصلاح مضمنة كاملة ولا تعتمد على تنزيل مستودع GitHub الخاص.
