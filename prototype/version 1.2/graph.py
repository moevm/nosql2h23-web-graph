from Link_loader import Link_loader
import threading
import atexit
import tldextract


class Graph:
    def __init__(self, db):
        self.db = db
        self.proj_name = "temp graph"
        self._graph_init = False
        self.label = self._get_label()
        self.lock = threading.Lock()
        atexit.register(self._exit_func)

    def load_node(self, source_node, dest_node):
        source_domain = tldextract.extract(source_node).domain
        dest_domain = tldextract.extract(dest_node).domain
        query = "MERGE(a:" + self.label + " {url:$url_1 ,active:false, domain:$domain_1} ) MERGE (b:" + self.label + " {url:$url_2, active:false, domain:$domain_2}) MERGE (a)-[:c]->(b)"

        self.lock.acquire()
        self.db.run_query(query, {"url_1": source_node, "url_2": dest_node, "domain_1": source_domain,
                                  "domain_2": dest_domain})
        self.lock.release()

    def load_nodes(self, source_node, children):
        for node in children:
            self.load_node(source_node, node)

    def get_node_id(self, url):
        query = "match(n:" + self.label + ") where n.url = $url return id(n) as id"
        return self.db.run_query(query, {"url": url})[0].get("id")

    def activate_node(self, node_id):
        query = "match(n:" + self.label + ") where id(n)=$id SET n.active = TRUE"
        self.lock.acquire()
        self.db.run_query(query, {"id": node_id})
        self.lock.release()

    def get_info(self, node_id):
        query = "match(n:" + self.label + ") where id(n)=$id return n.url as url, n.domain as domain"
        self.lock.acquire()
        answer = self.db.run_query(query, {"id": node_id})[0]
        self.lock.release()
        res = {"url": answer.get("url"), "domain": answer.get("domain")}
        return res

    def delete_node(self, node_id):
        query = "match(n:" + self.label + ") where id(n)=$id detach delete n"
        self.lock.acquire()
        self.db.run_query(query, {"id": node_id})
        self.lock.release()

    def get_nodes(self):
        query = "match(n:" + self.label + ") return id(n) as id, n.url as url, n.domain as domain"
        answer = self.db.run_query(query)
        return answer

    def get_edges(self):
        query = "match (a:" + self.label + ")-[b]->(c:" + self.label + ")return ID(a) as source, ID(c) as target"
        answer = self.db.run_query(query)
        return answer

    def get_enabled_nodes(self):
        query = "MATCH(n:" + self.label + " {active:True}) RETURN id(n) as id"
        answer = self.db.run_query(query)
        res = set()
        for record in answer:
            res.add(record.get("id"))

        return res

    def delete_second_level_disabled_nodes(self):
        query = "MATCH(n:" + self.label + " {active:FALSE}) WHERE NOT (:" + self.label + " {active:TRUE})-[:c]->(n) detach delete n"
        self.db.run_query(query)

    def delete_disabled_nodes(self):
        query = "MATCH(n:" + self.label + " {active:FALSE}) detach delete n"
        self.db.run_query(query)

    def _create_projection(self):
        query = "CALL gds.graph.project($name, $label, 'c')"
        self.db.run_query(query, {"name": self.proj_name, "label": self.label})
        self._graph_init = True

    def _drop_projection(self):
        if not self._graph_init:
            return
        self.db.run_query("CALL gds.graph.drop($name)", {"name": self.proj_name})
        self._graph_init = False

    def update_projection(self):
        if self._graph_init:
            self._drop_projection()
        self._create_projection()

    def _get_label(self):
        query = "merge(n:INFO) on create SET n.counter= 'c_0' RETURN n.counter as new_label"
        label = self.db.run_query(query)[0].get("new_label")
        return label

    def inc_label(self):
        label_parts = self.label.split("_")
        number_part = int(label_parts[-1]) + 1
        new_label = "c_" + str(number_part)
        query = "MATCH (n:INFO) SET n.counter = $new_label"
        self.db.run_query(query, {"new_label": new_label})
        self.label = new_label

    def _exit_func(self):
        self._drop_projection()
