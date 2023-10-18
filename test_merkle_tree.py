import unittest
from merkle_tree import MerkleTree


class TestMerkleTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.leaves = [1, 3, 3, 7, 4, 2, 0, 6]
        cls.height = 3
        cls.tree = MerkleTree(cls.height, cls.leaves)

    def test_merkle_tree(self):
        root = self.tree.root()
        self.assertIsNotNone(root)
        self.assertEqual(
            root, "e13a7ff32c9c1f59df2d785a1436fc2f5489c469babe9d62283474c4b8e66b81"
        )

    def test_leave_change_changes_the_root(self):
        leaves_2 = self.leaves[:-1] + [1]
        tree_2 = MerkleTree(self.height, leaves_2)

        self.assertNotEqual(self.tree.root(), tree_2.root())

    def test_merkle_path(self):
        expected_path = [
            {"level": 3, "index": 5},
            {"level": 2, "index": 2},
            {"level": 1, "index": 1},
        ]
        self.assertEqual(self.tree.get_merkle_path_of_node(3, 5), expected_path)

    def test_merkle_proof(self):
        proof = self.tree.get_merkle_proof(3, 5)
        self.assertEqual(proof["root"], self.tree.root())
        self.assertEqual(proof["value"], self.leaves[5])
        self.assertEqual(proof["index"], 5)
        self.assertIsNotNone(proof["siblings"])

    def test_compute_merkle_root_from_proof(self):
        proof = self.tree.get_merkle_proof(3, 5)
        computed_root = self.tree.compute_merkle_root_from_proof(
            proof["siblings"], proof["index"], proof["value"]
        )
        self.assertEqual(computed_root, self.tree.root())

    def test_merkle_proof_verification(self):
        level, index = 3, 5

        # Generate a proof for a particular leaf node
        proof = self.tree.get_merkle_proof(level, index)

        # Check the validity of the proof
        self.assertTrue(self.tree.verify_merkle_proof(proof))

        # Modify the proof's root to an invalid value and test
        proof["root"] = "invalidrootvalue"
        self.assertFalse(self.tree.verify_merkle_proof(proof))

    def test_merkle_proof_calculation(self):
        level, index = 3, 5
        proof = self.tree.get_merkle_proof(level, index)

        # Use the proof details to compute the Merkle root
        computed_root = self.tree.compute_merkle_root_from_proof(
            proof["siblings"], proof["index"], proof["value"]
        )

        # The computed root should match the tree's root
        self.assertEqual(computed_root, self.tree.root())

    def test_get_delta_merkle_proof(self):
        level, index, new_value = 3, 5, 100

        proof = self.tree.get_merkle_proof(level, index)
        delta_proof = self.tree.get_delta_merkle_proof(level, index, new_value)

        # Assert the expected properties of the delta proof.
        self.assertEqual(delta_proof["index"], index)
        self.assertEqual(delta_proof["newValue"], new_value)
        self.assertEqual(delta_proof["siblings"], proof["siblings"])

    def test_verify_delta_merkle_proof(self):
        level, index, new_value = 3, 5, 100
        delta_proof = self.tree.get_delta_merkle_proof(level, index, new_value)
        self.assertTrue(self.tree.verify_delta_merkle_proof(delta_proof))


if __name__ == "__main__":
    unittest.main()
