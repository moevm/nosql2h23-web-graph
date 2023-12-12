import json


class Adapter:

    @staticmethod
    def get_graph(db):
        node_query = "match (n {is_active: 1}) return labels(n)[0] as domain, ID(n) as id, n.url as url"
        nodes_info = db.run_query(node_query)
        edge_query = "match (a)-[b {is_active: 1}]->(c) return ID(a) as source, ID(c) as target"
        edges_info = db.run_query(edge_query)
        records = {'nodes': nodes_info, 'edges': edges_info}
        return Adapter._transform(records)

    @staticmethod
    def _transform(records):
        counter = 0
        domains = {}
        node_records = records['nodes']
        edge_records = records['edges']

        nodes = []
        for record in node_records:
            domain = record.get("domain")
            if domain not in domains:
                domains[domain] = counter
                counter += 1
            nodes.append(record.data() | {"group": domains[domain]})

        edges = []

        for record in edge_records:
            edges.append(record.data())

        return json.dumps({"nodes": nodes, "links": edges})
