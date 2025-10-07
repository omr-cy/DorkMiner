import asyncio
from playwright.async_api import async_playwright
from fake_user_agent import aio_user_agent
import re
from bs4 import BeautifulSoup
from pathlib import Path
import subprocess


DIR = Path(__file__).parent.resolve()

MSG = {
    'INIT'  : f"{'\033[95m'}[INIT]{'\033[0m'}",    # Purple
    'INFO'  : f"{'\033[94m'}[INFO]{'\033[0m'}",    # Blue
    'SUCC'  : f"{'\033[92m'}[SCSS]{'\033[0m'}",    # Green
    'DONE'  : f"{'\033[92m'}[DONE]{'\033[0m'}",    # Green
    'WARN'  : f"{'\033[93m'}[WARN]{'\033[0m'}",    # Yellow
    '!ERR'  : f"{'\033[91m'}[!ERR]{'\033[0m'}",    # Red
}

# ----------------------------------------------------------------------------------------------------------------

class Droker:
    def __init__(self, browser, domain:str, max_results:int=500):
        self.searcher = None
        self.browser = browser
        self.domain = domain
        self.max_results = max_results
        self.hosts = set()


    async def _fetch_page(self, url):
        page = await self.browser.new_page()
        await page.goto(url, wait_until="load", timeout=70000) 
        content = await page.content()
        await page.close()
        return content


    def _parse_src(self, src):

        if not src:
            print(f"{MSG['!ERR']} Error Page is empty, return []")
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

        return matches_set


    async def run(self):

        dork_loop = True

        while dork_loop:

            url = f"{self.dork_url} -{' -'.join(self.hosts)}" if self.hosts else self.dork_url

            page = await self._fetch_page(url)

            results = self._parse_src(page)

            res_len = len(results)

            if res_len == 0 or res_len == self.max_results:
                dork_loop = False
            
            elif results.issubset(self.hosts):
                dork_loop = False

            else:
                self.hosts.update(results)

        return self.hosts

class DuckDuckGo(Droker):
    """duckduckgo search engine implementation"""
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://www.duckduckgo.com/search?q="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Yahoo(Droker):
    """Yahoo search engine implementation"""
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://search.yahoo.com/search?p="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Yendix(Droker): # RS
    """Yendix search engine implementation"""
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://search.yahoo.com/search?p="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class YahooJP(Droker): # JO
    """Yahoo Japan search engine implementation"""
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://search.yahoo.co.jp/search?p="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Dmenu(Droker): # JP
    """Dmenu search engine implementation"""
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://service.smt.docomo.ne.jp/portal/search/web/result.html?q="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Naver(Droker): # CO
    """Naver search engine implementation"""
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://search.naver.com/search.naver?query="
        self.dork_url = f"{self.searcher}site:{self.domain}"

# class Google(Droker): # CO
#     """Naver search engine implementation"""
#     def __init__(self, browser, domain, max_results):
#         super().__init__(browser, domain, max_results)
#         self.searcher = "https://www.google.com/search?q="
#         self.dork_url = f"{self.searcher}site:{self.domain}"


# -----------------------------------------------------------------------------------------------------------------

async def main(domain:str, searchers:list = ['duck', 'yahoo'], max_results:int = 500, browser:str = 'chromium', view:bool = False):

    all_hosts = set()

    if browser == "chromium":
        # browser_path = str(DIR / '.browsers/chromium-1187/chrome-linux/chrome')
        browser_temp = str(DIR / '.tmp/cache/chromium')
        user_agent = await aio_user_agent(browser='chrome')

    elif browser == "firefox":
        # browser_path = str(DIR / '.browsers/firefox-1490/firefox/firefox')
        browser_temp = str(DIR / '.tmp/cache/firefox')
        user_agent = await aio_user_agent(browser='firefox')

    else:
        raise ValueError("browser must be 'chromium' or 'firefox'")


    async with async_playwright() as p:
        browser = await eval(f'p.{browser}').launch_persistent_context(
            headless = not view,
            # user_agent = ("Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0"),
            user_agent = user_agent,
            viewport = {"width": 1366, "height": 768},
            extra_http_headers = {"Accept-Language": "en-US;q=0.8,en;q=0.7",},
            java_script_enabled = True,
            user_data_dir = browser_temp,
            # executable_path= browser_path
        )

        jobs = []
        
        if '_duck_' in searchers or '_duckduckgo_' in searchers or "_all_" in searchers:
            duck_hosts = DuckDuckGo(browser, domain, max_results)
            jobs.append(duck_hosts.run())
            
        if '_yahoo_' in searchers or "_all_" in searchers: # OR ALL
            yahoo_hosts = Yahoo(browser, domain, max_results)
            jobs.append(yahoo_hosts.run())

        if '_yendix_' in searchers or "_all_" in searchers:
            yendix_hosts = Yendix(browser, domain, max_results)
            jobs.append(yendix_hosts.run())

        if '_yahoojp_' in searchers or "_all_" in searchers:
            yahoojp_hosts = YahooJP(browser, domain, max_results)
            jobs.append(yahoojp_hosts.run())

        if '_dmenu_' in searchers or "_all_" in searchers:
            dmenu_hosts = Dmenu(browser, domain, max_results)
            jobs.append(dmenu_hosts.run())

        if '_naver_' in searchers or "_all_" in searchers:
            naver_hosts = Naver(browser, domain, max_results)
            jobs.append(naver_hosts.run())

        # if '_google_' in searchers or "_all_" in searchers:
        #     google_hosts = Google(browser, domain, max_results)
        #     jobs.append(google_hosts.run())

        
        # Execute all jobs concurrently
        results = await asyncio.gather(*jobs, return_exceptions=True, )
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                print(f"{MSG['!ERR']} Search error: {result}")
            else:
                all_hosts.update(result)

        await browser.close()
        subprocess.run(f"rm -rf {browser_temp}", shell=True)

    return sorted(all_hosts)


# ----------------- [ CLI ] ------------------ #

if __name__ == "__main__":
    import argparse

    # INIT CLI Args
    parser = argparse.ArgumentParser(
        description="DrokMiner - Using Dorks For duckduckgo, yahoo"
    )
    parser.add_argument(
        "-d", "--domain",
        required=True,
        help="Target Domain"
    )
    parser.add_argument(
        "-s", "--searchers",
        required=True,
        help="Searhers (duck / dcukduckgo, yahoo...)",
    )
    parser.add_argument(
        "-m", "--max",
        help="Max Results (integer)",
        default='500'
    )
    parser.add_argument(
        "-o", "--outfile",
        help="(Path/to/File) default = './dorkminer-results.txt'",
        default="",
    )
    parser.add_argument(
        "-b", "--browser",
        help="Browser Type",
        default='chromium'
    )
    parser.add_argument(
        "-v", "--view",
        help="View Browser Proces",
        action="store_true"
    )
    cli = parser.parse_args()

    # Run The Main 
    all_hosts = asyncio.run(main(
        domain = cli.domain, 
        searchers = [f"_{searher.strip().lower()}_" for searher in cli.searchers.split(",")],
        max_results = cli.max,
        browser=cli.browser,
        view=cli.view,
    ))

    # Save Output Hosts in File
    outfile = Path(cli.outfile)

    if outfile.exists() and outfile.suffix == "txt":
        with outfile.open("w", encoding='utf-8'):
            outfile.write_text("\n".join(all_hosts))

    else:
        outfile = Path("dorkminer-results.txt")
        outfile.touch(exist_ok=True)

        for host in all_hosts:
            print(host)

        check = input("Save Results? (Y,n): ").strip()

        if check in ["", "Y", "y"]:
            with outfile.open("w", encoding='utf-8') as file:
                file.writelines(all_hosts)



# ----------------- [ TEST ] ------------------ #

# if __name__ == "__main__":
#     all_hosts = asyncio.run(main(
#         domain = "instagram.com",
#         searchers = ['_all_'],
#         max_results = 500
#     ))
#     for h in all_hosts:
#         print(h)