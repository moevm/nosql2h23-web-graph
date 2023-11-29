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

    def close(self):
        if self.driver is not None:
            self.driver.close()
            self.driver = None



