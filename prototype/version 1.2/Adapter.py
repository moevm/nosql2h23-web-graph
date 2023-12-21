import json


class Adapter:

    @staticmethod
    def get_graph(graph):
        nodes_info = graph.get_nodes()
        edges_info = graph.get_edges()
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
