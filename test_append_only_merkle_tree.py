import unittest
from append_only_merkle_tree import AppendOnlyMerkleTree


class TestAppendOnlyMerkleTree(unittest.TestCase):
    def setUp(self):
        self.tree = AppendOnlyMerkleTree(50)

    def test_append_leaf(self):
        delta_a = self.tree.append_leaf(8)
        delta_b = self.tree.append_leaf(9)

        self.assertTrue(self.tree.verify_delta_merkle_proof(delta_a))
        self.assertTrue(self.tree.verify_delta_merkle_proof(delta_b))

        self.assertEqual(delta_a["newRoot"], delta_b["oldRoot"])

        for i in range(50):
            self.assertTrue(
                self.tree.verify_delta_merkle_proof(self.tree.append_leaf(i))
            )


if __name__ == "__main__":
    unittest.main()
