import hashlib
from merkle_tree import MerkleTree


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


class ZeroMerkleTree(MerkleTree):
    def __init__(self, height: int):
        """
        Args:
        - height (int): The height of the tree.
        """
        self.height = height
        self.node_store = NodeStore(height)

    def set_leaf(self, index: int, value: str) -> None:
        """
        Set a leaf in the Merkle tree and update corresponding nodes on the path of the leaf.


        Args:
        - index (int): The index of the leaf to set.
        - value (str): The value to set for the leaf.

        Returns:
        - Delta merkle proof
        """
        old_root = self.root()
        old_value = self.node(self.height, index)
        siblings = []

        # Start traversing the leaf's Merkle path at the leaf node.
        current_index = index
        current_value = value

        # Don't set the root (level = 0) in the loop, as it has no sibling.
        for level in range(self.height, 0, -1):
            # Set the current node in the tree.
            self.node_store.set(level, current_index, current_value)

            if current_index % 2 == 0:
                # If the current index is even, then it has a sibling on the right (same level, index = current_index+1).
                right_sibling = self.node_store.get(level, current_index + 1)
                current_value = self.hash(current_value, right_sibling)
                siblings.append(right_sibling)
            else:
                # If the current index is odd, then it has a sibling on the left (same level, index = current_index-1).
                left_sibling = self.node_store.get(level, current_index - 1)
                current_value = self.hash(left_sibling, current_value)
                siblings.append(left_sibling)

            # Set current index to the index of the parent node.
            current_index = current_index // 2

        # Set the root node (level = 0, index = 0) to current value.
        self.node_store.set(0, 0, current_value)
        return {
            "index": index,
            "siblings": siblings,
            "oldRoot": old_root,
            "oldValue": old_value,
            "newValue": value,
            "newRoot": current_value,
        }

    def node(self, level, index):
        return self.node_store.get(level, index)

    def get_leaf(self, index):
        return self.get_merkle_proof(self.height, index)
