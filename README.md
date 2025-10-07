
**DorkMiner** is an automated subdomain discovery tool that uses *search engine dorking* across multiple engines (DuckDuckGo, Yahoo, Naver, etc.) to enumerate subdomains related to a given domain.

---

## 🚀 Features
- Supports multiple search engines:
  - DuckDuckGo 
  - Yahoo
  - Yahoo Japan 🇯🇵
  - Yandex (Yendix) 🇷🇺
  - Dmenu-GOO 
  - Naver 🇰🇷
- Extracts and deduplicates subdomains from search results.
- Async & fast (uses Playwright + asyncio).
- CLI and Python module usage.
- Works with Chromium or Firefox.

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/omarashraf0/DorkMiner.git
cd DorkMiner

# Install in editable mode (recommended for development)
pip install -e .

# Install Playwright browsers (required)
playwright install chromium
playwright install firefox
```

Or

virtual environment

```bash
# Clone the repository
git clone https://github.com/omarashraf0/DorkMiner.git
cd DorkMiner

# create & activate venv
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate       # Windows (PowerShell/CMD)

# upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# download Playwright browsers
python3.12 -m playwright install
```



> **Note:** Make sure you have:

- Python 3.12+ and pip available. 
 
- Installing Playwright browsers is required for the tool to run headless or visible browsers.

---

## Usage (CLI)

### Basic Usage

```bash
dorkminer -d example.com

python3.12 -m dorkminer -d example.com

python3.12 dorkminer.py -d example.com
```

### Options
| Flag              | Description                                                 | Default                           |
| ----------------- | ----------------------------------------------------------- | --------------------------------- |
| `-d, --domain`    | Target domain                                               | *Required*                        |
| `-s, --searchers` | Comma-separated search engines (e.g. `duck,yahoo`) or `all` | `duck,yahoo`                      |
| `-m, --max`       | Max number of results per engine                            | `500`                             |
| `-o, --outfile`   | Output file path                                            | Prints to stdout and asks to save |
| `-b, --browser`   | Browser type (`chromium` or `firefox`)                      | `chromium`                        |
| `-v, --view`      | Show browser UI                                             | `False`                           |
| `-sl, --silent`   | Disable banner/messages                                     | `False`                           |

### Advanced Usage

```bash
dorkminer -d example.com -s all -m 100 -o results.txt
```

---

## Usage as a Python Module


```python
import asyncio
from dorkminer import main

async def run_dorkminer():
    results = await main(
        domain="example.com",
        searchers=["duck", "yahoo"],
        max_results=300,
        browser="chromium",
        view=False,
        silent=True
    )
    print(results)

asyncio.run(run_dorkminer())
```

---

## 🧾 License
Copyright © 2025 **Omar Ashraf (omr)**  
Released under the MIT License.

---
---

# النسخة العربية 


**DorkMiner** أداة آلية لاكتشاف النطاقات الفرعية (subdomains) تعتمد على استخدام *dorks* في محركات البحث المتنوعة (DuckDuckGo، Yahoo، Naver، وغيرها) لجمع النطاقات الفرعية المتعلقة بنطاق مستهدف.

---

## 🚀 الميزات
- تدعم عدة محركات بحث:
  - DuckDuckGo
  - Yahoo
  - Yahoo Japan 🇯🇵
  - Yandex (Yendix) 🇷🇺
  - Dmenu-GOO
  - Naver 🇰🇷
- استخراج وإزالة التكرار من النطاقات الفرعية المستخرجة.
- غير متزامنة وسريعة (باستخدام Playwright + asyncio).
- استخدام كأداة سطر أوامر (CLI) أو كموديول بايثون.
- تعمل مع Chromium و Firefox.

---

## ⚙️ التثبيت

```bash
# استنساخ المستودع
git clone https://github.com/omarashraf0/DorkMiner.git
cd DorkMiner

# التثبيت في وضع التطوير (مستحسن أثناء التطوير)
pip install -e .

# تثبيت متصفحات Playwright المطلوبة
playwright install chromium
playwright install firefox
```

أو باستخدام بيئة افتراضية:

```bash
# استنساخ المستودع
git clone https://github.com/omarashraf0/DorkMiner.git
cd DorkMiner

# إنشاء وتفعيل venv
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scriptsctivate       # Windows (PowerShell/CMD)

# تحديث pip وتثبيت المتطلبات
python -m pip install --upgrade pip
pip install -r requirements.txt

# تنزيل متصفحات Playwright
python3.12 -m playwright install
```

> **ملاحظة:** تأكد من:
> - وجود Python 3.12 أو أعلى و pip.
> - تثبيت متصفحات Playwright ضروري لتشغيل الأداة في وضع headless أو ظاهر.

---

## الاستخدام (CLI)

### الاستخدام الأساسي

```bash
dorkminer -d example.com

python3.12 -m dorkminer -d example.com

python3.12 dorkminer.py -d example.com
```

### الخيارات
| الوسيط | الوصف | الافتراضي |
| ------ | ----- | --------- |
| `-d, --domain` | النطاق الهدف | *مطلوب* |
| `-s, --searchers` | محركات البحث مفصولة بفواصل (مثال: `duck,yahoo`) أو `all` | `duck,yahoo` |
| `-m, --max` | الحد الأقصى لنتائج كل محرك | `500` |
| `-o, --outfile` | مسار ملف الإخراج | يطبع على stdout ويسألك للحفظ |
| `-b, --browser` | نوع المتصفح (`chromium` أو `firefox`) | `chromium` |
| `-v, --view` | عرض واجهة المتصفح | `False` |
| `-sl, --silent` | إخفاء البنر والرسائل | `False` |

### الاستخدام المتقدم

```bash
dorkminer -d example.com -s all -m 100 -o results.txt
```

---

## الاستخدام كمكتبة بايثون


```python
import asyncio
from dorkminer import main

async def run_dorkminer():
    results = await main(
        domain="example.com",
        searchers=["duck", "yahoo"],
        max_results=300,
        browser="chromium",
        view=False,
        silent=True
    )
    print(results)

asyncio.run(run_dorkminer())
```

---

## 🧾 الترخيص

حقوق النسخ © 2025 **Omar Ashraf (omr)**  
مرخّصة بموجب رخصة MIT.

---
