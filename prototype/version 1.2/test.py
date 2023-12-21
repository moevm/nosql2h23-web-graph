from Algorithms import Algorithms
from DatabaseController import DatabaseController
from Graph import Graph
from Graph_creator import Graph_creator

db = DatabaseController("bolt://localhost:7687", "neo4j", "67tyghbn")
graph = Graph(db)
res = graph.get_nodes()
for elem in res:
    print(elem.data())
#algs = Algorithms(db, graph)
#first = Graph_creator(graph, algs)
#first.construct_graph("https://note.nkmk.me/en/python-str-num-conversion/")