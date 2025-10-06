import asyncio
from playwright.sync_api import sync_playwright, Browser
import re
from bs4 import BeautifulSoup

MSG = {
    'INIT'    : f"{'\033[95m'}[INIT]{'\033[0m'}",    # Purple
    'INFO'    : f"{'\033[94m'}[INFO]{'\033[0m'}",      # Blue
    'SUCCESS' : f"{'\033[92m'}[SCSS]{'\033[0m'}",      # Green
    'DONE'    : f"{'\033[92m'}[DONE]{'\033[0m'}",      # Green
    'WARNING' : f"{'\033[93m'}[WARN]{'\033[0m'}",      # Yellow
    'ERROR'   : f"{'\033[91m'}[!ERR]{'\033[0m'}",      # Red
}

class Droker:
    def __init__(self, browser:Browser, domain:str, max_results:int=500):
        self.searcher = None
        self.browser = browser
        self.domain = domain
        self.max_results = max_results
        self.hosts = set()


    def _fetch_page(self, url):
        context = self.browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0"
            ),
            viewport={"width": 1366, "height": 768},
            extra_http_headers={
                "Accept-Language": "en-US;q=0.8,en;q=0.7",
            },
            java_script_enabled=True
            )
        page = context.new_page()
        page.goto(url, wait_until="load", timeout=15000)
        content = page.content()
        page.close()
        return content


    def _parse_src(self, src):

        if not src:
            print(f"{MSG['ERROR']} Error Page is empty, return []")
            return []

        soup = BeautifulSoup(src, "lxml")
        text = soup.get_text(" ", strip=True)

        hrefs = [a.get("href") for a in soup.find_all("a", href=True)]
        for h in hrefs:
            text += " " + h

        matches_set = set()

        re_pattern = rf"(https?://)(?:[\w\-]+\.)+{re.escape(self.domain)}(?::\d+)?(?:/[^\s\"'<]*)?"

        for match in re.finditer(re_pattern, text):
            url = match.group().strip()
            url = url.strip(r" ,.;:!()[]{}<>")
            url = url.split("://")[1] if "://" in url else url
            url = url.split("/")[0]

            if len(url) > len(self.domain) and self.domain in url:
                matches_set.add(url)

        return sorted(matches_set)


    def run(self):

        dork_loop = True

        while dork_loop:

            url = f"{self.dork_url} -{' -'.join(self.hosts)}" if self.hosts else self.dork_url

            page = self._fetch_page(url)

            results = self._parse_src(page)

            self.hosts.update(results)

            res_len = len(results)

            if res_len == 0 or res_len == self.max_results:

                dork_loop = False

        return self.hosts

# ----------------------------------------------------------------------------------------------------------------

class DuckDuckGo(Droker):
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://www.duckduckgo.com/search?q="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Yahoo(Droker):
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://search.yahoo.com/search?p="
        self.dork_url = f"{self.searcher}site:{self.domain}"



# ----------------------------------------------------------------------------------------------------------------


# if __name__ == "__main__":
#     from concurrent.futures import ThreadPoolExecutor as TreadX
#     from concurrent.futures import as_completed
#     from pathlib import Path
#     import argparse

#     # ----------------- [ CLI ] ------------------ #

#     parser = argparse.ArgumentParser(
#         description="DrokMiner - Using Dorks For duckduckgo, yahoo"
#     )

#     parser.add_argument(
#         "-d", "--domain",
#         required=True,
#         help="Target Domain"
#     )
#     parser.add_argument(
#         "-s", "--searhers",
#         required=True,
#         help="Searhers ( duck / dcukduckgo,  yahoo )"
#     )
#     parser.add_argument(
#         "-m", "--max",
#         help="Max Results (integer)",
#         default='500'
#     )
#     parser.add_argument(
#         "-o", "--output",
#         help="Output file"
#     )
#     args = parser.parse_args()
#     # -------

#     all_hosts = set()

#     with sync_playwright() as p:
#         domain:str = args.domain
#         max_results:int = args.max
#         searhers:list = [searher.strip().lower() for searher in args.searhers.split(",")]

#         browser = p.firefox.launch(headless=False)
#         threads = []

#         with ThreadX(max_workers=2) as TX:  
#             if 'duck' in searhers or 'duckduckgo' in searhers:
#                 threads.append(TX.submit(DuckDuckGo, browser, domain, max_results))

#             if 'yahoo' in searhers:
#                 threads.append(TX.submit(Yahoo, browser, domain, max_results)) 
            
#             for thread in as_completed(threads):
#                 try:
#                     hosts = thread.result() or set()
#                     all_hosts.update(hosts)
#                 except Exception as e:
#                     print("Worker raised:", e)

#         browser.close()

#     if args.output:
#         ...


# ------- TEST -------

if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor as ThreadX
    from concurrent.futures import as_completed

    all_hosts = set()

    with sync_playwright() as p:
        domain:str = 'instagram.com'
        max_results:int = 500
        searhers:list = ['duck', 'yahoo']

        browser = p.firefox.launch(headless=False)
        threads = []

        with ThreadX(max_workers=2) as TX:  
            if 'duck' in searhers or 'duckduckgo' in searhers:
                threads.append(TX.submit(lambda: DuckDuckGo(browser, domain, max_results).run()))

            if 'yahoo' in searhers:
                threads.append(TX.submit(lambda: DuckDuckGo(browser, domain, max_results).run())) 
            
            for thread in as_completed(threads):
                try:
                    hosts = thread.result() or set()
                    all_hosts.update(hosts)
                except Exception as e:
                    print("Worker raised:", e)

        browser.close()

    print(sorted(all_hosts))