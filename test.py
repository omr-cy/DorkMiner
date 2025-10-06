
from playwright.sync_api import sync_playwright, Browser
import time

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    
    context = browser.new_context(
        user_agent=("Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0"),
        viewport={"width": 1366, "height": 768},
        extra_http_headers={"Accept-Language": "en-US;q=0.8,en;q=0.7",},
        java_script_enabled=True
    )

    page = context.new_page()
    page.goto("https://www.duckduckgo.com?q=site:instagram.com", wait_until="load")
    # time.sleep(100)
    content = page.content()
    # page.close()
    
import re
from bs4 import BeautifulSoup

class DomainParser:
    def __init__(self, domain):
        self.domain = domain

    

parser = DomainParser("instagram.com")
results = parser._parse_src(content)

for r in results:
    print(" -", r)

