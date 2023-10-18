# Merkle Trees

This repository contains Python implementations of various types of Merkle trees, including:

1. **MerkleTree**: A basic Merkle tree that allows you to create a Merkle tree, get the Merkle proof for a leaf, verify Merkle proofs, and more.

2. **ZeroMerkleTree**: An extension of the basic Merkle tree that is optimized for sparse data use case.

3. **AppendOnlyMerkleTree**: A further extension of the ZeroMerkleTree that maintains a minimal set of data necessary for leaf addition, making it suitable for use in layer-2 scaling solutions.

## MerkleTree (merkle_tree.py)

The `MerkleTree` class provides the basic functionality of a Merkle tree. Here are some key features:

- Create a Merkle tree with a given height and a list of leaves.
- Get the Merkle proof for a leaf node.
- Verify a Merkle proof for a leaf node.
- Compute the Merkle root from a provided Merkle proof.

## ZeroMerkleTree (zero_merkle_tree.py)

The `ZeroMerkleTree` class extends the basic Merkle tree optimised for sparse data.

- Set the value of a leaf node and update the corresponding nodes on the path of the leaf.
- Efficiently retrieve and compute values of nodes in the tree.
- Create delta Merkle proofs for leaf addition.
- Verify delta Merkle proofs.

## AppendOnlyMerkleTree (append_only_merkle_tree.py)

The `AppendOnlyMerkleTree` class further optimizes the Merkle tree for an "append-only" use case. It maintains a minimal set of data necessary for leaf addition and delta Merkle proofs. Key features include:

- Append a leaf to the tree, efficiently computing delta Merkle proofs.
- Maintain a minimal set of data for efficient storage and proof generation.
- Compute the root of the Merkle tree.

## Running Tests

To run the tests for these Merkle tree implementations, you can use the following command:

```bash
python -m unittest discover -s tests -v
```
