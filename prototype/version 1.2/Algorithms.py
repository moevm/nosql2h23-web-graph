from enum import Enum
import atexit


class Centrality_type(str, Enum):
    DEGREE = "degree"
    CLOSENESS = "closeness"
    BETWEENNESS = "betweenness"


class Algorithms:

    def __init__(self, db):
        self.db = db
        self.graph_name = "algorithms graph"
        self.graph_init = False
        atexit.register(self.drop_graph)

    def find_path(self, start_id, finish_id):
        if not self.graph_init:
            raise Exception("No graph")

        conf = {"SourceNode": start_id, "targetNode": finish_id}
        query = "CALL gds.shortestPath.dijkstra.stream('{0}' ,$config) YIELD nodeIds as path".format(self.graph_name)
        result = self.db.run_query(query, {"config": conf})
        if len(result) > 0:
            result = result[0].get("path")
        return result

    def get_page_rank(self):
        if not self.graph_init:
            raise Exception("No graph")

        query = "CALL gds.pageRank.stream('{0}') YIELD nodeId as id, score".format(self.graph_name)
        records = self.db.run_query(query)
        return dict(records)

    def get_strongly_connected_components(self):
        if not self.graph_init:
            raise Exception("No graph")

        query = "CALL gds.scc.stream('{0}') YIELD nodeId as id, componentId as component".format(self.graph_name)
        records = self.db.run_query(query)
        return dict(records)

    def get_centrality(self, config):
        if not self.graph_init:
            raise Exception("No graph")

        query = "CALL gds." + config["type"] + ".stream('{0}') YIELD nodeId as id, score".format(self.graph_name)
        records = self.db.run_query(query)
        return dict(records)

        pass

    def update_graph(self):
        if self.graph_init:
            self.drop_graph()

        nodes_query = "MATCH (n)-[]->(m) "
        create_graph_query = "WITH gds.graph.project($name,n,m) as g RETURN g.nodeCount"
        self.db.run_query(nodes_query + create_graph_query, {"name": self.graph_name})
        self.graph_init = True

    def drop_graph(self):
        if not self.graph_init:
            return
        self.db.run_query("CALL gds.graph.drop($name)", {"name": self.graph_name})
        self.graph_init = False
