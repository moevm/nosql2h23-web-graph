import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def get_link(root_link):
    result = set()

    try:
        response = requests.get(root_link, timeout=5)
    except:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    for a_tag in soup.findAll("a"):
        link_raw_url = a_tag.attrs.get("href")
        if link_raw_url == "" or link_raw_url is None:
            continue
        link_url = urljoin(root_link, link_raw_url)
        parsed_url = urlparse(link_url)
        result.add(parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path)
    return list(result)
