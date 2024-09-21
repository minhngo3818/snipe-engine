from bintrees import FastAVLTree
import hashlib
import binascii
import os
import pickle

"""
    @summary: use 3gram algorithm to check unique content of a page
    ngram also ensure unique in position between token list
"""
class SimiDupNgram:
    def __init__(self):
        self.file_path = os.path.join("data", "simidup_ngram.pkl")
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        try:
            with open(self.file_path, "rb") as file:
                self.loaded_simidup = pickle.load(file)
                self.tree = FastAVLTree(self.loaded_simidup)
        except FileNotFoundError:
            self.loaded_simidup = {}
            self.tree = FastAVLTree()

    def ngram_to_crc_number(self, ngram):
        # Use crc method to calculate sum character of ngram
        crc32_checksum = binascii.crc32(ngram.encode())
        return crc32_checksum

    def ngram_fg(self, tokens, n=3):
        # Create a set of finger print of the page
        ngrams = []

        for i in range(len(tokens) - n + 1):
            gram = " ".join(map(str, tokens[i:i + n]))
            ngrams.append(gram)

        numeric_values = [self.ngram_to_crc_number(ngram) for ngram in ngrams]
        # Select certain number in a set with modulus of 4 
        # to acquire finger print set
        fg = [value for value in numeric_values if value % 4 == 0]
        return set(fg)

    def ngram_similarity(self, set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        if union == 0:
            return False

        prob = intersection / union
        return prob > 0.9

    def ngram_compare(self, tokens):
        # Find if the ngram fingerprint existed in the tree
        # Accept a list of raw tokens which possibly contains duplicates
        # but still main order of token in the text
        # Return true if it is, otherwise false
        
        fg = self.ngram_fg(tokens)
        fg_list = list(fg)
        fg_str = "".join(str(fg_item) for fg_item in fg_list)
        hash_fp = hashlib.sha256(fg_str.encode("utf-8")).hexdigest()
        result = False
        try:
            nearest_fg = self.tree.floor_item(hash_fp)[1]
            result = self.ngram_similarity(fg, nearest_fg)
        except KeyError as e:
            pass
        self.tree[hash_fp] = fg
        self.save()
        return result

    def save(self):
        # Save data in avl tree
        with open(self.file_path, "wb") as file:
            pickle.dump(self.tree, file)


simidup_ngram = SimiDupNgram()

