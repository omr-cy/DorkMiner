import asyncio
from playwright.async_api import async_playwright
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
    def __init__(self, browser, domain:str, max_results:int=500):
        self.searcher = None
        self.browser = browser
        self.domain = domain
        self.max_results = max_results
        self.hosts = set()


    async def _fetch_page(self, url):
        context = await self.browser.new_context(
            user_agent=("Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0"),
            viewport={"width": 1366, "height": 768},
            extra_http_headers={"Accept-Language": "en-US;q=0.8,en;q=0.7",},
            java_script_enabled=True
        )
        page = await context.new_page()
        await page.goto(url, wait_until="load", timeout=15000)
        content = await page.content()
        await page.close()
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


    async def run(self):

        dork_loop = True

        while dork_loop:

            url = f"{self.dork_url} -{' -'.join(self.hosts)}" if self.hosts else self.dork_url

            page = await self._fetch_page(url)

            results = self._parse_src(page)

            self.hosts.update(results)

            res_len = len(results)

            if res_len == 0 or res_len == self.max_results:

                dork_loop = False

        return self.hosts

# ----------------------------------------------------------------------------------------------------------------

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



# -----------------------------------------------------------------------------------------------------------------


async def main(domain:str, searchers:list = ['duck', 'yahoo'], max_results:int = 500):

    all_hosts = set()

    async with async_playwright() as p:

        browser = await p.firefox.launch(headless=False)

        jobs = []
        
        if 'duck' in searchers or 'duckduckgo' in searchers:
            duckduckgo = DuckDuckGo(browser, domain, max_results)
            jobs.append(duckduckgo.run())
            
        if 'yahoo' in searchers:
            yahoo = Yahoo(browser, domain, max_results)
            jobs.append(yahoo.run())
        
        # Execute all jobs concurrently
        results = await asyncio.gather(*jobs, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                print(f"{MSG['ERROR']} Search error: {result}")
            else:
                all_hosts.update(result)

        await browser.close()

    return sorted(all_hosts)


# ----------------------------------------------------------------------------------------------------------------

# ----------------- [ CLI ] ------------------ #

if __name__ == "__main__":
    from pathlib import Path
    import argparse

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
        help="Searhers (duck / dcukduckgo, yahoo)"
    )
    parser.add_argument(
        "-m", "--max",
        help="Max Results (integer)",
        default='500'
    )
    parser.add_argument(
        "-o", "--outfile",
        help="Path / to / OutputFile",
        default='./dorkminer-results.txt'
    )
    cli = parser.parse_args()

    domain = cli.domain
    max_results = cli.max
    searchers = [searher.strip().lower() for searher in cli.searchers.split(",")]

    # Run The Main 
    all_hosts = asyncio.run(main(domain, searchers, max_results))

    # Save Output Hosts in File

    outfile = Path(cli.outfile)

    if str(outfile).strip() not in ["", "."]:
        with outfile.open("w", encoding='utf-8'):
            outfile.write_text("\n".join(all_hosts))

    else:
        for host in all_hosts:
            print(host)

        check = input("Save Results? Y,n: ").strip()

        if check in ["", "Y", "y"]:
            with file.open("w", encoding='utf-8'):
                file.write_text("\n".join(all_hosts))