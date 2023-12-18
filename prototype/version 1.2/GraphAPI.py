from threading import Thread, Lock


class Graph_API:
    def __init__(self, source_url, graph):
        self.construct_thread = None
        self.lock = Lock()
        self.construction_mode = False
        self.creator = self._Creator(self)

        self.source = source_url
        self.graph = graph

    def start_construction(self):
        self.construction_mode = True
        self.construct_thread = Thread(target=self._thread_func)
        self.construct_thread.start()

    def stop_construction(self):
        self.construct_thread = False

    def _thread_func(self):
        while True:
            if not self.construction_mode:
                return

            self.creator.next_interation()





    class _Creator:

        def __init__(self,owner):
            self.iteration = 0
            self.owner = owner

        def next_interation(self):
            pass


        def _init_graph(self):
            pass

