import asyncio
from playwright.async_api import async_playwright
from fake_user_agent import aio_user_agent
import re
from bs4 import BeautifulSoup
from pathlib import Path
import subprocess

BANNER = (rf"""
    {'\033[95m'}
    ___  ____ ____ _  _      _  _ _ _  _ ____ ____ 
    |  \ |  | |__/ |_/   __  |\/| | |\ | |___ |__/ 
    |__/ |__| |  \ | \_      |  | | | \| |___ |  \ 
    {'\033[0m'}
    """ + rf"""
    Copyright © 2025 Omar Ashraf, known as {'\033[94m'}omr{'\033[0m'}
    Version {'\033[92m'}0.9{'\033[0m'}
""")

MSG = {
    'INIT'  : f"{'\033[95m'}[INIT]{'\033[0m'}",    # Purple
    'INFO'  : f"{'\033[94m'}[INFO]{'\033[0m'}",    # Blue
    'SUCC'  : f"{'\033[92m'}[SCSS]{'\033[0m'}",    # Green
    'DONE'  : f"{'\033[92m'}[DONE]{'\033[0m'}",    # Green
    'WARN'  : f"{'\033[93m'}[WARN]{'\033[0m'}",    # Yellow
    '!ERR'  : f"{'\033[91m'}[!ERR]{'\033[0m'}",    # Red
    'TAP4'  : "    "
}

DIR = Path(__file__).parent.resolve()

# ----------------------------------------------------------------------------------------------------------------

class Droker:
    name = 'Dorker'

    def __init__(self, browser, domain:str, max_results:int, silent:bool):
        self.searcher = None
        self.browser = browser
        self.domain = domain
        self.max_results = max_results
        self.silent = silent
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

        if not self.silent:
            print(MSG['TAP4'] + f"{MSG['INFO']} - Dorking: {self.name}")

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
    name = "DuckDuckGo"
    def __init__(self, browser, domain, max_results, silent):
        super().__init__(browser, domain, max_results, silent)
        self.searcher = "https://www.duckduckgo.com/search?q="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Yahoo(Droker):
    """Yahoo search engine implementation"""
    name = "Yahoo"
    def __init__(self, browser, domain, max_results, silent):
        super().__init__(browser, domain, max_results, silent)
        self.searcher = "https://search.yahoo.com/search?p="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Yendix(Droker): # RS
    """Yendix search engine implementation"""
    name = "Yendix"
    def __init__(self, browser, domain, max_results, silent):
        super().__init__(browser, domain, max_results, silent)
        self.searcher = "https://search.yahoo.com/search?p="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class YahooJP(Droker): # JO
    """Yahoo Japan search engine implementation"""
    name = "Yahoo Japan"
    def __init__(self, browser, domain, max_results, silent):
        super().__init__(browser, domain, max_results, silent)
        self.searcher = "https://search.yahoo.co.jp/search?p="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Dmenu(Droker): # JP
    """Dmenu search engine implementation"""
    name = "Dmenu-GOO"
    def __init__(self, browser, domain, max_results, silent):
        super().__init__(browser, domain, max_results, silent)
        self.searcher = "https://service.smt.docomo.ne.jp/portal/search/web/result.html?q="
        self.dork_url = f"{self.searcher}site:{self.domain}"

class Naver(Droker): # CO
    """Naver search engine implementation"""
    name = "Naver"
    def __init__(self, browser, domain, max_results, silent):
        super().__init__(browser, domain, max_results, silent)
        self.searcher = "https://search.naver.com/search.naver?query="
        self.dork_url = f"{self.searcher}site:{self.domain}"


# -----------------------------------------------------------------------------------------------------------------

async def main(
    domain:str, searchers:list = ["duck","yahoo"], outfile:str = "", max_results:int = 500, browser:str = "chromium", view:bool = False, silent:bool = False
    ):

    print(BANNER) if not silent else ...

    if type(searchers) == str:
        searchers = [f"_{searher.strip().lower()}_" for searher in searchers.split(",")]
    else:
        ...

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
            duck_hosts = DuckDuckGo(browser, domain, max_results, silent)
            jobs.append(duck_hosts.run())
            
        if '_yahoo_' in searchers or "_all_" in searchers: # OR ALL
            yahoo_hosts = Yahoo(browser, domain, max_results, silent)
            jobs.append(yahoo_hosts.run())

        if '_yendix_' in searchers or "_all_" in searchers:
            yendix_hosts = Yendix(browser, domain, max_results, silent)
            jobs.append(yendix_hosts.run())

        if '_yahoojp_' in searchers or "_all_" in searchers:
            yahoojp_hosts = YahooJP(browser, domain, max_results, silent)
            jobs.append(yahoojp_hosts.run())

        if '_dmenu_' in searchers or "_all_" in searchers:
            dmenu_hosts = Dmenu(browser, domain, max_results, silent)
            jobs.append(dmenu_hosts.run())

        if '_naver_' in searchers or "_all_" in searchers:
            naver_hosts = Naver(browser, domain, max_results, silent)
            jobs.append(naver_hosts.run())


        # Execute all jobs concurrently
        results = await asyncio.gather(*jobs, return_exceptions=True, )

        # Just For More Readability
        print(MSG["TAP4"] + "\n"+" |--------------------------------------------|"+"\n")

        # Process results
        for result in results:
            if isinstance(result, Exception):
                print(MSG["TAP4"] + f"{MSG['!ERR']} Search error: {result}")
            else:
                # Print Only New Hosts in Stduot
                for host in result:
                    if not silent and host not in all_hosts:
                        print(MSG['TAP4'] + f"{'\033[92m'}[+]{'\033[0m'}" + " - " + host)
                        # Save New Results
                        all_hosts.add(host)


        await browser.close()

    subprocess.run(f"rm -rf {browser_temp}", shell=True)

    all_hosts = sorted(all_hosts)

    # Save Output Hosts in File
    if outfile:
        outfile = Path(outfile)
        if outfile.suffix == "txt":
            with outfile.open("w", encoding='utf-8'):
                outfile.write_text("\n".join(all_hosts))

    else:
        check = input("\n" + "Save Results? (Y,n): ").strip()
        if check in ["", "Y", "y"]:
            outfile = Path(f"./{domain}-dorkminer-results.txt")
            with outfile.open("w", encoding='utf-8'):
                outfile.write_text("\n".join(all_hosts))

    return all_hosts


# ----------------- [ CLI ] ------------------

def parse_cli_args():
    import argparse
    parser = argparse.ArgumentParser(description="DorkMiner - Using Dorks in (duckduckgo, yahoo, ...)")
    parser.add_argument("-d", "--domain",    required=True,  help="Target domain")
    parser.add_argument("-s", "--searchers", required=False, default="duck,yahoo", help="Searchers (duck,yahoo,naver) or  all")
    parser.add_argument("-m", "--max",       required=False, default=500,          help="Max results (int)")
    parser.add_argument("-o", "--outfile",   required=False, default=None,         help="Output file path (optional)")
    parser.add_argument("-b", "--browser",   required=False, default="chromium",   help="Browser to use (chromium|firefox)")
    parser.add_argument("-v", "--view",      required=False, default=False,        help="View Browser Proces",   action="store_true")
    parser.add_argument("-sl","--silent",    required=False, default=False,        help="No Banner or Messages", action="store_true",)
    return parser.parse_args()

def cli():
    args = parse_cli_args()
    asyncio.run(main(
        domain=args.domain,
        searchers=args.searchers,
        max_results=args.max,
        browser=args.browser,
        view=args.view,
        silent=args.silent,
    ))

# if __name__ == "__main__":
#     cli()


# ----------------- [ TEST ] -----------------

if __name__ == "__main__":
    asyncio.run(main(
        domain = "instagram.com",
        searchers = ['_all_'],
        max_results = 500,
        # view=True,
        # browser="firefox",
    ))

