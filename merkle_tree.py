import hashlib


def hash_nodes(left_node, right_node):
    hasher = hashlib.sha256()
    concatenated_nodes = f"{left_node}{right_node}".encode("utf-8")
    hasher.update(concatenated_nodes)
    return hasher.hexdigest()


class MerkleTree:
    def __init__(self, height, leaves):
        self.height = height
        self.leaves = leaves

    def node(self, level, index):
        """
        Compute the value of a node in the Merkle tree given its level and index.

        Parameters:
        - level (int): The level of the node in the tree.
          Level 0 represents the root node, while the maximum level (equal to the height of the tree) represents the leaves.
        - index (int): The index of the node at the given level.
          The index starts from 0 and increases from left to right.

        Returns:
        - str: The value of the node. This could either be a hash value (for non-leaf nodes) or actual data (for leaf nodes).

        Logic:
        - If the node is a leaf (i.e., level equals the height of the tree), return the corresponding data from the leaves list.
        - Otherwise, the value of the node is computed by hashing the values of its two child nodes.
          The left child node is at [level + 1, index * 2] and the right child node is at [level + 1, index * 2 + 1].

        Example:
        Given the tree:
            Level 0:    N(0,0)
            Level 1:  N(1,0)   N(1,1)
            Level 2: N(2,0) N(2,1) N(2,2) N(2,3)

        To compute the value of node N(1,1), the method will hash the values of N(2,2) and N(2,3).

        Refer to the Merkle Tree Diagram Cheat Sheet for a visual representation.
        """
        if level == self.height:
            # if level == height, the node is a leaf,
            # so just return the value from our dataset
            return self.leaves[index]
        else:
            # if the node is not a leaf, use:
            # N(level, index) = Hash(N(level+1, index*2), N(level+1, index*2+1))
            return hash_nodes(
                self.node(level + 1, 2 * index), self.node(level + 1, 2 * index + 1)
            )

    def root(self):
        return self.node(0, 0)
