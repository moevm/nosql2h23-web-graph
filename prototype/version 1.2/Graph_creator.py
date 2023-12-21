import concurrent.futures
from Link_loader import Link_loader
import threading


class Graph_creator:
    def __init__(self, graph, algorithms):
        self.graph = graph
        self.algorithms = algorithms
        self.nodes_per_iteration = 10
        self.load_limit = 20
        self.iteration_count = 2
        self.lock = threading.Lock()

    def _init_graph(self, root_node):
        first_level_nodes = Link_loader.get_link(root_node, self.load_limit)
        self.graph.load_nodes(root_node, first_level_nodes)
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for node in first_level_nodes:
                executor.submit(self.init_and_load, root_node=node)

        self.graph.activate_node(self.graph.get_node_id(root_node))
        self.next_vertices_to_activate()
        self.graph.delete_second_level_disabled_nodes()

    def init_and_load(self, root_node):
        dist_nodes = Link_loader.get_link(root_node, self.load_limit)
        self.graph.load_nodes(root_node, dist_nodes)

    def next_vertices_to_activate(self):
        self.graph.update_projection()
        enabled_id = self.graph.get_enabled_nodes()
        sorted_page_rank = self.algorithms.get_page_rank()
        counter = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for id in sorted_page_rank.keys():
                if id in enabled_id:
                    continue

                if executor.submit(self.activate_node, node_id=id):
                    counter += 1
                if counter >= self.nodes_per_iteration:
                    break

    def construct_graph(self, root_node):
        self._init_graph(root_node)
        for i in range(0, self.iteration_count):
            print(i)
            self.next_vertices_to_activate()

        self.graph.update_projection()

    def activate_node(self, node_id):
        url = self.graph.get_info(node_id)["url"]
        children = Link_loader.get_link(url, self.load_limit)
        if len(children) == 0:
            self.graph.delete_node(node_id)
            return False

        self.graph.load_nodes(url, children)
        self.graph.activate_node(node_id)
        return True
