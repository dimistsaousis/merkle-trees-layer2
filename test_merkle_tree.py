import unittest
from merkle_tree import MerkleTree


class TestMerkleTree(unittest.TestCase):
    def test_merkle_tree(self):
        leaves = [1, 3, 3, 7, 4, 2, 0, 6]
        height = 3

        tree = MerkleTree(height, leaves)
        root = tree.root()

        self.assertIsNotNone(root)
        self.assertEqual(
            root, "e13a7ff32c9c1f59df2d785a1436fc2f5489c469babe9d62283474c4b8e66b81"
        )

    def test_leave_change_changes_the_root(self):
        height = 3
        leaves_1 = [1, 3, 3, 7, 4, 2, 0, 6]
        leaves_2 = leaves_1[:-1] + [1]

        self.assertNotEqual(MerkleTree(height, leaves_1), MerkleTree(height, leaves_2))

    def test_merkle_path(self):
        height = 3
        tree = MerkleTree(height, list(range(9)))
        expected_path = [
            {"level": 3, "index": 5},
            {"level": 2, "index": 2},
            {"level": 1, "index": 1},
        ]
        self.assertEqual(tree.get_merkle_path_of_node(3, 5), expected_path)

    def test_get_merkle_proof(self):
        leaves = [1, 3, 3, 7, 4, 2, 0, 6]
        height = 3

        tree = MerkleTree(height, leaves)
        leaf_level = 3
        leaf_index = 5
        merkle_proof = tree.get_merkle_proof(leaf_level, leaf_index)

        # Check the root
        self.assertEqual(merkle_proof["root"], tree.root())

        # Verify the leaf index
        self.assertEqual(merkle_proof["index"], leaf_index)

        # Check the leaf value
        self.assertEqual(merkle_proof["value"], leaves[leaf_index])

        # Verify the siblings of the leaf's merkle path
        expected_siblings = [
            tree.node(3, 4),  # sibling of N(3,5)
            tree.node(2, 3),  # sibling of N(2,2)
            tree.node(1, 0),  # sibling of N(1,1)
        ]
        self.assertEqual(merkle_proof["siblings"], expected_siblings)


if __name__ == "__main__":
    unittest.main()
