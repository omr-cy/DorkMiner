import asyncio
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


class Droker:
    def __init__(self, browser, domain, max_results=500):
        self.searcher = None
        self.browser = browser
        self.domain = domain
        self.max_results = max_results

        self.hosts = set()
        self.dork_url = f"{self.searcher}site:{self.domain}"


    def _fetch_page(url):
        with self.browser.new_page() as page:
            page.goto(url)
            return page.content()


    def _parse_page(page) -> list:
        ...


    def run():

        dork_loop = True

        while dork_loop:

            url = f"{self.dork_url} -{','.join(self.hosts)}" if self.hosts else self.dork_url

            page = self._fetch_page(url)

            results = self._parse_page(page)

            self.hosts.update(results)

            res_len = len(results)

            if res_len == 0 or res_len == self.max_results:

                dork_loop = False

        return self.hosts

# ----------------------------------------------------------------------------------------------------------------

class DorkGoogle(Droker):
    def __init__(self, browser, domain, max_results):
        super().__init__(browser, domain, max_results)
        self.searcher = "https://www.google.com/search?q="

    def _parse_page(page) -> list:
        soup = BeautifulSoup(page, "lxml")
        parsed_hosts = set()

        for cite in soup.find_all("cite"):
            sub:str = cite.get_text(strip=True).rstrip("/")

            if sub.endswith(self.domain):
                parsed_hosts.add(sub)

        return parsed_hosts

# ----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    domain = "instagram.com"
    all_hosts = set()

    with sync_playwright() as p:
        main_browser = p.firefox.launch(headless=False)
        google_hosts = DorkGoogle(domain, main_browser, 20)
        all_hosts.update(google_hosts.run())

    print(all_hosts)