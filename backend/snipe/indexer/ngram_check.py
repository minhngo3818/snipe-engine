from bintrees import FastAVLTree
import binascii
import hashlib
import pickle
import os


class NgramChecker:
    def __init__(self, config=None):
        self.n = 3
        self.selector = 4  # modulo factor to select a key
        self.tolerant = 0.85

        self.file_path = os.path.join(
            "assets", "cache", "ngram.pkl"
        )  # config.ngram_path
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        try:
            with open(self.file_path, "rb") as file:
                self.loaded_simidup = pickle.load(file)
                self.tree = FastAVLTree(self.loaded_simidup)
        except FileNotFoundError:
            self.loaded_simidup = {}
            self.tree = FastAVLTree()

    def create_ngram_fingerprint(self, token_list) -> str:
        finger_print = set()

        for i in range(len(token_list) - self.n + 1):
            ngram = "".join(token_list[i : i + self.n])
            crc_num = binascii.crc32(ngram.encode())
            if crc_num % self.selector:
                finger_print.add(crc_num)

        return finger_print

    def is_ngram_similar(self, set_1: set, set_2: set):
        join_count = len(set_1.intersection(set_2))
        union_count = len(set_1.union(set_2))

        if union_count == 0:
            return False

        return join_count / union_count > self.tolerant

    def save(self):
        # Save data in avl tree
        with open(self.file_path, "wb") as file:
            pickle.dump(self.tree, file)

    def ngram_compare(self, tokens):
        fg = self.create_ngram_fingerprint(tokens)
        fg_str = "".join(str(fg_item) for fg_item in list(fg))
        hash_fp = hashlib.sha256(fg_str.encode("utf-8")).hexdigest()
        result = False
        try:
            nearest_fg = self.tree.floor_item(hash_fp)[1]
            result = self.is_ngram_similar(fg, nearest_fg)
        except KeyError as e:
            pass
        self.tree[hash_fp] = fg
        self.save()
        return result

    def view_tree(self):
        print(self.tree)
