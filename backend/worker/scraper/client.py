import time

import requests

DEFAULT_TIMEOUT = 20
DEFAULT_RETRIES = 3
DEFAULT_DELAY = 1.5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en;q=0.9",
}


class ScraperClient:
    def __init__(
        self,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        delay: float = DEFAULT_DELAY,
    ):
        self.timeout = timeout
        self.retries = retries
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_html(self, url: str) -> str:
        """Fetch HTML with retries and polite delay."""
        for attempt in range(self.retries):
            try:
                resp = self.session.get(url, timeout=self.timeout)
                resp.raise_for_status()
                resp.encoding = resp.apparent_encoding or "utf-8"
                time.sleep(self.delay)
                return resp.text
            except requests.RequestException:
                if attempt == self.retries - 1:
                    raise
                time.sleep(self.delay * (attempt + 1))
        return ""
