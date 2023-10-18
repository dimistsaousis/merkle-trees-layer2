import hashlib


class NodeStore:
    def __init__(self, height):
        self.nodes = {}
        self.height = height
        self.zero_hashes = self._compute_zero_hashes()

    @staticmethod
    def hash(left_node, right_node):
        hasher = hashlib.sha256()
        concatenated_nodes = f"{left_node}{right_node}".encode("utf-8")
        hasher.update(concatenated_nodes)
        return hasher.hexdigest()

    def _compute_zero_hashes(self):
        """
        Compute zero hashes for a given height.
        """
        current_zero_hash = 0
        zero_hashes = [current_zero_hash]
        for _ in range(1, self.height + 1):
            current_zero_hash = self.hash(current_zero_hash, current_zero_hash)
            zero_hashes.append(current_zero_hash)
        return zero_hashes

    def set(self, level: int, index: int, value: str):
        """
        Set the value of the node in the data store.

        Args:
        - level (int): Level of the node.
        - index (int): Index of the node.
        - value (str): Value to set.
        """
        self.nodes[(level, index)] = value

    def get(self, level: int, index: int) -> str:
        """
        Get the value of the node from the data store or return the correct zero hash if it doesn't exist.

        Args:
        - level (int): Level of the node.
        - index (int): Index of the node.

        Returns:
        - str: Node value.
        """
        return self.nodes.get((level, index), self.zero_hashes[self.height - level])
