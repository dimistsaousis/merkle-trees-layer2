import unittest
from zero_merkle_tree import NodeStore, ZeroMerkleTree
from merkle_tree import MerkleTree


class TestNodeStore(unittest.TestCase):
    def setUp(self):
        self.node_store = NodeStore(height=4)

    def test_zero_hashes(self):
        # Ensuring zero hash computation is as expected.
        self.assertEqual(
            len(self.node_store.zero_hashes), 5
        )  # As height = 4, zero_hashes will have 5 elements.

    def test_set_and_get(self):
        self.node_store.set(2, 3, "test_value")
        self.assertEqual(self.node_store.get(2, 3), "test_value")

        # Ensure we get the correct zero hash for non-existent nodes.
        self.assertEqual(self.node_store.get(1, 1), self.node_store.zero_hashes[3])


class TestZeroMerkleTree(unittest.TestCase):
    def setUp(self):
        self.tree = ZeroMerkleTree(3)

    def test_set_leaf(self):
        delta_merkle_proof = self.tree.set_leaf(0, 10)
        tree = MerkleTree(3, [10, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(tree.root(), self.tree.root())
        self.assertTrue(self.tree.verify_delta_merkle_proof(delta_merkle_proof))

    def test_root(self):
        self.assertEqual(MerkleTree(3, [0 for _ in range(8)]).root(), self.tree.root())

    def test_node(self):
        tree = MerkleTree(3, [0 for _ in range(8)])
        for level in range(3):
            for index in range(2**level):
                self.assertEqual(tree.node(level, index), self.tree.node(level, index))
