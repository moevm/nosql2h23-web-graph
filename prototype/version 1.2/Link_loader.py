import concurrent.futures

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import datetime
import tldextract
from concurrent.futures import ThreadPoolExecutor


class Link_loader:
    @staticmethod
    def get_link(root_link, limit=100):
        result = set()  # заменить на set

        try:
            response = requests.get(root_link, timeout=5)
        except:
            return result

        soup = BeautifulSoup(response.content, 'html.parser')
        for a_tag in soup.findAll("a"):
            link_raw_url = a_tag.attrs.get("href")
            if link_raw_url == "" or link_raw_url is None:
                continue

            link_url = urljoin(root_link, link_raw_url)
            parsed_url = urlparse(link_url)
            res_link = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
            if res_link != root_link:
                result.add(res_link)
            if len(result) >= limit:
                return result

        return result
