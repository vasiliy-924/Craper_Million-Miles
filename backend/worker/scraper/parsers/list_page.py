from urllib.parse import urljoin

from bs4 import BeautifulSoup


def extract_detail_urls(html: str, base_url: str) -> list[str]:
    """
    Extract car detail URLs from a brand listing page.
    Ignores lease pages (/usedcar/lease/...).
    """
    soup = BeautifulSoup(html, "html.parser")
    seen = set()
    urls = []

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if "/usedcar/detail/" in href and "/index.html" in href:
            if "/lease/" in href:
                continue
            full_url = urljoin(base_url, href)
            if full_url not in seen:
                seen.add(full_url)
                urls.append(full_url)

    return urls
