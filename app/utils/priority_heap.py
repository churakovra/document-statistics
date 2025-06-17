from app.utils.binary_node import BinaryNode


class PriorityHeap:
    def __init__(self):
        self.data = []

    def add(self, item: BinaryNode, priority: float):
        self.data.append((item, priority))
        self.data.sort(key=lambda x: x[1], reverse=True)

    def pop(self) -> tuple[BinaryNode, float]:
        return self.data.pop()

    def is_empty(self):
        return len(self.data) == 0

    def fill(self, tf: dict[str, float]):
        for letter, statistics in tf.items():
            node = BinaryNode(value=letter)
            self.add(node, priority=statistics)
