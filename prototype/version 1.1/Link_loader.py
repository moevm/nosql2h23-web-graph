import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import datetime
import tldextract
from concurrent.futures import ThreadPoolExecutor


class Link_loader:

    @staticmethod
    def reset_active_nodes(db):
        db.run_query('MATCH (n) SET n.is_active = 0')
        db.run_query('MATCH ()-[m:LEADS_TO]->() SET m.is_active = 0')

    @staticmethod
    def get_link(root_link):
        result = []  # заменить на set

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
            result.append(parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path)
        return result

    @staticmethod
    def links_search(db, link, limit, nodes_counter):
        temp = Link_loader.get_link(link)
        if link:
            domain = tldextract.extract(link).domain
            domain = ''.join(letter for letter in domain if letter.isalnum())
            if domain:
                if domain[0]:
                    if domain[0].isdigit():
                        domain = 'D' + domain
                if not db.run_query('MATCH (n:' + str(domain) + ' {url:"' + str(link) + '"}) RETURN n'):
                    db.run_query('CREATE (n:' + str(domain) + ' {url:"' + str(link) + '", datatime:"' + str(
                        datetime.datetime.now()) + '"})')
                db.run_query('MATCH (n:' + str(domain) + ' {url:"' + str(link) + '"}) SET n.is_active = 1')
                nodes_counter = db.run_query('MATCH (n {is_active: 1}) RETURN count(*)')[0][0]
                print(nodes_counter)
                if nodes_counter >= limit:
                    return temp, nodes_counter

        for i in temp:
            if i:
                temp_domain = tldextract.extract(i).domain
                temp_domain = ''.join(letter for letter in temp_domain if letter.isalnum())
                if temp_domain:
                    if temp_domain[0]:
                        if temp_domain[0].isdigit():
                            temp_domain = 'D' + temp_domain
                    if not db.run_query('MATCH (n:' + str(temp_domain) + ' {url:"' + str(i) + '"}) RETURN n'):
                        db.run_query('CREATE (n:' + str(temp_domain) + ' {url:"' + str(i) + '", datatime:"' + str(
                            datetime.datetime.now()) + '"})')

                        db.run_query('MATCH (n:' + str(domain) + ' {url: "' + str(link) + '"}) MATCH (s:' + str(temp_domain) 
                                     + '{url: "' + str(i) + '"}) CREATE (n)-[m:LEADS_TO]->(s) SET m = {datatime: "' + str(
                                         datetime.datetime.now()) + '"}')

                    elif not db.run_query('MATCH (n:' + str(domain) + ' {url:"' + str(link) + '"})-[m:LEADS_TO]->(s:' 
                                          + str(temp_domain) + ' {url:"' + str(i) + '"}) RETURN m') and link != i:
                         db.run_query('MATCH (n:' + str(domain) + ' {url: "' + str(link) + '"}) MATCH (s:' + str(temp_domain) 
                                      + '{url: "' + str(i) + '"}) CREATE (n)-[m:LEADS_TO]->(s) SET m = {datatime: "' 
                                      + str(datetime.datetime.now()) + '"}')
                        
                    db.run_query('MATCH (n:' + str(temp_domain) + ' {url:"' + str(i) + '"}) SET n.is_active = 1')
                    db.run_query('MATCH (n:' + str(domain) + ' {url: "' + str(link) + '"})-[m:LEADS_TO]->(s:' + str(
                        temp_domain) + '{url: "' + str(i) + '"}) SET m.is_active = 1')

                    nodes_counter = db.run_query('MATCH (n {is_active: 1}) RETURN count(*)')[0][0]
                    print(nodes_counter)
                    if nodes_counter >= limit:
                        return temp, nodes_counter

        return temp, nodes_counter
