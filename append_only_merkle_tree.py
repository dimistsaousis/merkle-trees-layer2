from zero_merkle_tree import ZeroMerkleTree


class AppendOnlyMerkleTree(ZeroMerkleTree):
    def __init__(self, height: int):
        super().__init__(height)
        # create a dummy proof of all zero hashes for initialization
        self.last_proof = {
            "root": self.node_store.zero_hashes[self.height],
            "siblings": self.node_store.zero_hashes[: self.height],
            "index": -1,
            "value": self.node_store.zero_hashes[self.height],
        }

    def append_leaf(self, leaf_value: str) -> dict:
        old_merkle_path = self.compute_merkle_path_from_proof(
            self.last_proof["siblings"],
            self.last_proof["index"],
            self.last_proof["value"],
        )
        old_root = self.last_proof["root"]
        # Old value will aways be empty since it's an append only tree
        old_value = 0
        prev_index = self.last_proof["index"]
        #  append only tree new index is always the previous index + 1
        new_index = prev_index + 1
        # keep track of the old siblings so we can use them for our delta merkle proof
        old_siblings = self.last_proof["siblings"]
        siblings = []
        multiplier = 1

        for level in range(self.height):
            # get the index of the previous leaf's merkle path node on the current level
            prev_level_index = prev_index // multiplier
            # get the index of the new leaf's merkle path node on the current level
            new_level_index = new_index // multiplier

            if new_level_index == prev_level_index:
                # if the merkle path node index on this level DID NOT change, we can reuse the old sibling
                siblings.append(old_siblings[level])
            else:
                # if the merkle path node index on this level DID change, we need to check if the new merkle path node index is a left or right hand node
                if new_level_index % 2 == 0:
                    # if the new merkle path node index is even, the new merkle path node is a left hand node,
                    # so merkle path node's sibling is a right hand node,
                    # therefore our sibling has an index greater than our merkle path node,
                    # so the sibling must be a zero hash
                    siblings.append(self.node_store.zero_hashes[level])
                else:
                    # if the new merkle path node is odd, then its sibling has an index one less than it, so its sibling must be the previous merkle path node on this level
                    siblings.append(old_merkle_path[level])

            multiplier *= 2

        new_root = self.compute_merkle_root_from_proof(siblings, new_index, leaf_value)
        self.last_proof = {
            "root": new_root,
            "siblings": siblings,
            "index": new_index,
            "value": leaf_value,
        }
        return {
            "index": self.last_proof["index"],
            "siblings": siblings,
            "oldRoot": old_root,
            "oldValue": old_value,
            "newRoot": new_root,
            "newValue": leaf_value,
        }
