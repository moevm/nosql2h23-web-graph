from enum import Enum
import atexit
from collections import OrderedDict


class Centrality_type(str, Enum):
    DEGREE = "degree"
    CLOSENESS = "closeness"
    BETWEENNESS = "betweenness"


class Algorithms:

    def __init__(self, db, graph):
        self.db = db
        self.graph = graph

    def find_path(self, start_id, finish_id):
        conf = {"SourceNode": start_id, "targetNode": finish_id}
        query = "CALL gds.shortestPath.dijkstra.stream('{0}' ,$config) YIELD nodeIds as path".format(
            self.graph.proj_name)
        result = self.db.run_query(query, {"config": conf})
        if len(result) > 0:
            result = result[0].get("path")
        return result

    def get_page_rank(self):
        query = "CALL gds.pageRank.stream('{0}') YIELD nodeId as id, score RETURN id, score ORDER BY score DESC".format(
            self.graph.proj_name)
        records = self.db.run_query(query)
        return OrderedDict(records)

    def get_strongly_connected_components(self):
        query = "CALL gds.scc.stream('{0}') YIELD nodeId as id, componentId as component".format(self.graph.proj_name)
        records = self.db.run_query(query)
        return dict(records)

    def get_centrality(self, config):
        query = "CALL gds." + config["type"] + ".stream('{0}') YIELD nodeId as id, score".format(self.graph.proj_name)
        records = self.db.run_query(query)
        return dict(records)

        pass
