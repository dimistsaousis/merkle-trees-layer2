import hashlib


class ZeroMerkleTree:
    def __init__(self, height, leaves):
        self.height = height
        self.leaves = leaves
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

    def get_node_value(self, level: int) -> str:
        """
        Get the node value for a given tree height and level on an empty tree

        Args:
        - tree_height (int): Height of the tree.
        - level (int): Level of the node.

        Returns:
        - str: Node value.
        """
        return self.zero_hashes[self.height - level]
