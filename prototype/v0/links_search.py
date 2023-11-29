import tldextract
from get_link import get_link
import datetime


def links_search(conn, link, limit, nodes_counter):

    temp = get_link(link)
    if link:
        domain = tldextract.extract(link).domain
        domain = ''.join(letter for letter in domain if letter.isalnum())
        if domain:
            if domain[0]:
                if domain[0].isdigit():
                    domain = 'D' + domain
            if not conn.query('MATCH (n:' + str(domain) + ' {url:"' + str(link) +  '"}) RETURN n', db="test"):
                conn.query('CREATE (n:' + str(domain) + ' {url:"' + str(link) +  '", datatime:"' + str(datetime.datetime.now()) + '"})', db="test")
                nodes_counter += 1
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
                if not conn.query('MATCH (n:' + str(temp_domain) + ' {url:"' + str(i) +  '"}) RETURN n', db="test"):
                    conn.query('CREATE (n:' + str(temp_domain) + ' {url:"' + str(i) +  '", datatime:"' + str(datetime.datetime.now()) + '"})', db="test")
                    nodes_counter += 1
                    print(nodes_counter)
                    if nodes_counter >= limit:
                        return temp, nodes_counter

                #MATCH (n:< Website >{url: "< url1 >"}) MATCH (s:< Website >{url: "< url2 >"}) CREATE (n)-[m:LEADS_TO]->(s) SET m.id = < id >, m.datatime = "< datatime >"
                    conn.query('MATCH (n:' + str(domain) +' {url: "' + str(link) + '"}) MATCH (s:' + str(temp_domain) + '{url: "' + str(i) +'"}) CREATE (n)-[m:LEADS_TO]->(s) SET m.datatime = "' + str(datetime.datetime.now()) +'"', db="test")

                elif not conn.query('MATCH (n:' + str(domain) +' {url:"' + str(link) + '"})-[m:LEADS_TO]->(s:' + str(temp_domain) +' {url:"' + str(i) + '"}) RETURN m', db="test") and link != i:
                    conn.query('MATCH (n:' + str(domain) +' {url: "' + str(link) + '"}) MATCH (s:' + str(temp_domain) + '{url: "' + str(i) +'"}) CREATE (n)-[m:LEADS_TO]->(s) SET m.datatime = "' + str(datetime.datetime.now()) +'"', db="test")

    return temp, nodes_counter
    '''for i in temp:
        if i:
            if nodes_counter >= limit:
                return
            links_search(conn, i)'''