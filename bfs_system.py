from queue import Queue

class BfsSystem:
    def __init__(self, node):
        self.queue = Queue()
        self.queue.put(node)
        self.hash = {}  # hash will map tuples to a list of solutions

# to be implemented