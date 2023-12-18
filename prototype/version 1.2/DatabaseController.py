from neo4j import GraphDatabase


class DatabaseController:
    def __init__(self, database_url, username, password):
        self.driver = GraphDatabase.driver(database_url, auth=(username, password))

    def run_query(self, query, params=None):
        try:
            result = self.driver.execute_query(query, params)
        except Exception as e:
            print(e)
            return -1
        return result[0]

    def create_graph(self, name, node_projection, relationship_projection, config=None):
        if config is None:
            config = {}
        params = {
            "name": name,
            "nodes": node_projection,
            "edges": relationship_projection,
            "config": config

        }
        query = "CALL gds.graph.project($name,$nodes,$edges)"
        self.run_query(query, params)

    def close(self):
        if self.driver is not None:
            self.driver.close()
            self.driver = None
