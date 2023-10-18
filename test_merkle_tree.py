# test_merkle_tree.py

import unittest
from merkle_tree import MerkleTree, get_merkle_path_of_node


class TestMerklePath(unittest.TestCase):
    def test_merkle_path(self):
        expected_path = [
            {"level": 3, "index": 5},
            {"level": 2, "index": 2},
            {"level": 1, "index": 1},
        ]
        self.assertEqual(get_merkle_path_of_node(3, 5), expected_path)


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


if __name__ == "__main__":
    unittest.main()
