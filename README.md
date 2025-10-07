
# DorkMiner

**DorkMiner** — a Python tool that extracts hostnames/domains using search-engine “dorks” (DuckDuckGo, Yahoo, Naver, ...).  
This README contains installation & usage instructions for CLI and as an importable module.

**DorkMiner**:
اداة بلغة بايثون، لأستخراج النطاقات (الدومينز - domains) من محركات البحث المختلفة، عن طريق تقنية الـ Dorking

---

## English

### Requirements
- Python 3.12+ (tested with 3.12)  
- `pip`  
- `playwright`, `beautifulsoup4`, `lxml` (see `requirements.txt`)

---

### Quick install (recommended: virtual environment)
```bash
# create & activate venv
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate       # Windows (PowerShell/CMD)

# upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# download Playwright browsers
python -m playwright install
```

---

### CLI usage
Basic call:
```bash
python dorkminer.py -d example.com -s duck,yahoo -m 200
```

Options:
- `-d / --domain` : target domain (required)  

- `-s / --searchers` : comma-separated searchers (`duck`, `yahoo`, `naver`, ...). Example: `duck,yahoo`  

- `-m / --max` : max results per search (default `500`)  

- `-o / --outfile` : output file (default prints to stdout and asks to save)

- `-b / --browser` : Browser type (default 'chromium')

- `-v / --view` : View Browser Proces (default 'False')

Save results directly:
```bash
python dorkminer.py -d example.com -s duck,yahoo -m 500 -o ./results.txt
```

Use all Search Engines:
```bash
python dorkminer.py -d example.com -s all
```
---

### Use as a Python module

```python
import asyncio
from dorkminer import main  # if dorkminer.py is in your PYTHONPATH

async def run():
    hosts = await main(
        domain="example.com",
        searchers=['_duck_', '_yahoo_'],
        max_results=200,
        browser='chromium'  # or 'firefox'
    )
    print(hosts)

asyncio.run(run())
```

Notes:
- `main(...)` returns a sorted list of hosts.
- When calling programmatically use searcher tokens like `"_duck_"`, `"_yahoo_"`, or `"_all_"`. The CLI converts `duck,yahoo` → 

---

### Disclaimer
This tool is provided **for educational and legitimate OSINT purposes only**. Do **not** use it to access systems or data without authorization. The author and contributors are **not responsible** for misuse.

---

### Contributing & License
- Open to PRs and issues. Please open an issue before large changes.  
- License: MIT (read the `LICENSES`).


---
---


## العربية (Arabic)

### المتطلبات
- بايثون 3.12 أو أحدث  (مجرب بـ3.12)
- `pip`  
- الحزم: `playwright`, `beautifulsoup4`, `lxml` (راجع `requirements.txt`)

---

### تثبيت سريع (مستحسن: virtualenv - بيئة معزولة)
```bash
# إنشاء وتفعيل البيئة الافتراضية
python -m venv .venv
source .venv/bin/activate      # على لينكس / ماك
# .venv\Scripts\activate       # على ويندوز

# تحديث pip وتثبيت المتطلبات
python -m pip install --upgrade pip
pip install -r requirements.txt

# تحميل المتصفحات
python -m playwright install
```

---

### التشغيل من سطر الأوامر (CLI)
مثال أساسي:
```bash
python dorkminer.py -d example.com -s duck,yahoo -m 200
```

خيارات العمل:
- `-d / --domain` : النطاق الهدف (مطلوب)  

- `-s / --searchers` : محركات البحث مفصولة بفاصلة (`duck`, `yahoo`, `naver`, ...). مثال: `duck,yahoo`  

- `-m / --max` : الحد الأقصى للنتائج (افتراضي 500)  

- `-o / --outfile` : ملف الإخراج (افتراضي يطبع ثم يسألك حفظ)

- `-b / --browser` : لأختيار المتصفح (إفتراضي 'chromium')

- `-v / --view` : مطالعة عمليات المتصفح (الإفتراضي 'False - موقوف')

```bash
python dorkminer.py -d example.com -s duck,yahoo -m 500 -o ./results.txt
```

استعمال كل المحركات البحثية:
```bash
python dorkminer.py -d example.com -s all
```

---

### استخدام كـمكتبة في بايثون

```python
import asyncio
from dorkminer import main

async def run():
    hosts = await main(
        domain="example.com",
        searchers=['_duck_', '_yahoo_'],
        max_results=200,
        browser='chromium'  # أو 'firefox'
    )
    print(hosts)

asyncio.run(run())
```

ملاحظات:
- الدالة `main(...)` تُرجع قائمة مرتبة من النطاقات.  
- في الاستدعاء البرمجي استخدم رموز `searchers` مثل `"_duck_"` أو `"_all_"`. واجهة CLI تحول المدخلات تلقائيًا.

---

### إخلاء المسؤولية
الأداة مخصصة لأغراض اخلاقية ومشاريع OSINT المشروعة فقط. لا تستخدمها للوصول غير المصرح به أو لأي نشاط مخالف للقانون او غير شرعي. المؤلف غير مسؤول عن أي استخدام ضار.

---

### المساهمة والترخيص
- المساهمات مرحب بها: افتح Issue قبل تغييرات كبيرة.  
- الترخيص: MIT (اقرأ ملف الـ`LICENSE`).

---

