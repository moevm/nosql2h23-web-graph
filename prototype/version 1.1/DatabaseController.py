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

    def export(self, file_name='test'):
        end_path = file_name + '.graphml'
        temp_string = "CALL apoc.export.graphml.query('MATCH (n)-[m:LEADS_TO {is_active: 1}]->(r) RETURN n, r, m','" + end_path + "', {})"
        self.run_query(temp_string)
        return end_path

    def import_(self, file_name='test.graphml'):
        query_string = "CALL apoc.import.graphml('" + file_name + "', {readLabels:true, storeNodeIds:true})"
        self.run_query(query_string)       

        query_string = """MATCH (a)
                    WITH a.url AS url, COLLECT(a) AS branches
                    WHERE SIZE(branches) > 1
                    FOREACH (n IN TAIL(branches) | DETACH DELETE n)"""
        self.run_query(query_string)



