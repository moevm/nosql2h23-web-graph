from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def export(self, db, path='test'):
        temp_string = "CALL apoc.export.graphml.all('" + path + ".graphml', {})"
        self.query(temp_string, db=db)

    def import_(self, db, path='test'):
        query_string = '''
        MATCH (n) DETACH DELETE n
        '''
        self.query(query_string, db=db)
        query_string = "CALL apoc.import.graphml('" + path + ".graphml', {readLabels:true, storeNodeIds:true})"
        self.query(query_string, db=db)

    # Метод, который передает запрос в БД
    def query(self, query, db=None):
        assert self.driver is not None, "Driver not initialized!"  # если подключения к DBMS не было
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response
