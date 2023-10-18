import hashlib


class MerkleTree:
    def __init__(self, height, leaves):
        self.height = height
        self.leaves = leaves

    @staticmethod
    def hash(left_node, right_node):
        hasher = hashlib.sha256()
        concatenated_nodes = f"{left_node}{right_node}".encode("utf-8")
        hasher.update(concatenated_nodes)
        return hasher.hexdigest()

    @staticmethod
    def get_merkle_path_of_node(level, index):
        """
        Computes the Merkle path of a node in a Merkle tree.

        When a leaf in a Merkle tree is updated, the change bubbles up the tree
        affecting all ancestor nodes. These nodes form the Merkle path for the leaf.
        The Merkle path of a node represents the nodes affected by a change to the node.

        Given a node N(level, index), its parent is N(level-1, floor(index/2)).
        For every node N(level, index), it has two children: N(level+1, index*2) and N(level+1, index*2+1).
        Thus, to compute the Merkle path of a node, we recursively list out its ancestors.

        Parameters:
        - level (int): The level of the node in the Merkle tree.
        - index (int): The index of the node at the given level.

        Returns:
        list: A list of dictionaries containing the level and index of each node in the Merkle path excluding the root.
        """
        merkle_path = []
        current_level = level
        while current_level > 0:
            merkle_path.append({"level": current_level, "index": index})
            index //= 2
            current_level -= 1
        return merkle_path

    @staticmethod
    def get_sibling_node(level, index):
        if level == 0:
            raise ValueError("The root does not have a sibling")
        elif index % 2 == 0:
            # if node is even, its sibling is at index+1
            return {"level": level, "index": index + 1}
        else:
            # if node is odd, its sibling is at index-1
            return {"level": level, "index": index - 1}

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
            return self.hash(
                self.node(level + 1, 2 * index), self.node(level + 1, 2 * index + 1)
            )

    def root(self):
        return self.node(0, 0)

    def get_merkle_proof(self, level, index):
        """
        Generate a merkle proof for a given leaf node.

        A merkle proof consists of the following components:
        - The root of the Merkle tree
        - The siblings of the leaf's merkle path
        - The index of the leaf in the tree
        - The value of the leaf

        Using these components, it is possible to prove the inclusion of a certain leaf in a Merkle tree with a known root.

        Parameters:
        - level (int): The level of the leaf node in the tree.
        - index (int): The index of the leaf node at the given level.

        Returns:
        dict: A dictionary containing the components of the merkle proof.
        """
        # get the value of the leaf node
        leaf_value = self.node(level, index)

        # get the levels and indexes of the nodes on the leaf's merkle path
        merkle_path = self.get_merkle_path_of_node(level, index)

        # get the levels and indexes of the siblings of the nodes on the merkle path
        merkle_path_siblings = [
            self.get_sibling_node(node["level"], node["index"]) for node in merkle_path
        ]

        # get the values of the sibling nodes
        sibling_values = [
            self.node(node["level"], node["index"]) for node in merkle_path_siblings
        ]

        return {
            "root": self.root(),  # the root we claim to be our tree's root
            "siblings": sibling_values,  # the siblings of our leaf's merkle path
            "index": index,  # the index of our leaf
            "value": leaf_value,  # the value of our leaf
        }
