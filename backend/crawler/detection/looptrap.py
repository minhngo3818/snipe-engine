from utils import get_url_component_list
from bintrees import FastAVLTree    # Use avl for quick find
import hashlib
import os
import pickle


TOLERANT = 0.9


def is_depth_trap(path, url_len):
    # Check too long url or repeated pattern (false urls)

    # 2000 is typical path length for modern browser
    # cited https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    # Check path length
    if url_len > 1800:
        return True

    # Check similar path
    path_segments = path.strip("/").split("/")
    count_similar = 0
    i = 0
    while count_similar == 0 and i < len(path_segments) - 1:
        if path_segments[i] == path_segments[i + 1]:
            count_similar += 1
        i += 1

    return count_similar > 0

"""
    @summary: simhash url to prevent ininite trap
"""
class SimhashUrl:
    def __init__(self):
        self.file_path = os.path.join("data", "simhash_url.pkl")
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        try:
            with open(self.file_path, "rb") as file:
                self.loaded_urls = pickle.load(file)
                self.tree = FastAVLTree(self.loaded_urls)
        except FileNotFoundError:
            self.loaded_urls = {}
            self.tree = FastAVLTree()

    def simhash_prehash_sha256_bin(self, token, hash_size):
        # Pre-hash value by hash token with sha256 algorithm (ensure uniqueness)
        # Convert to base 64bit which is supposed to efficient size to simhash
        hash_sha256 = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16) % (2 ** hash_size)
        return bin(hash_sha256)[2:].zfill(hash_size)

    def simhash(self, parsed_url, hash_size=64):
        # Simhash algorithm
        # Use prehash sha256 and convert o binary string and then hash into finger print
        finger_print = [0] * hash_size

        url_component_list = get_url_component_list(parsed_url)
        bin_hash_token = ""
        for piece in url_component_list:
            bin_hash_token = self.simhash_prehash_sha256_bin(piece, hash_size)

        for i in range(hash_size):
            finger_print[i] += (1 if bin_hash_token[i] == '1' else -1)

        for i in range(hash_size):
            temp = finger_print[i]
            finger_print[i] = 1 if temp > 0 else 0

        hash_bin_str = ''.join(map(str, finger_print))
        return hash_bin_str

    def simhash_check_exist(self, parsed_url, hash_size=64) -> bool:
        # Check page similarity using hamming distance
        # Return true if the similarity is greater than tolerant
        # If the finger print is not in avl tree return false
        
        finger_print_str = self.simhash(parsed_url)
        finger_print_bin = int(finger_print_str, 2) # Convert to binary number
        result = False
        try:
            existed_finger_print = self.tree.floor_item(finger_print_bin)
            existed_finger_print_str = int(existed_finger_print[1], 2)
            xor_result = finger_print_bin ^ existed_finger_print_str
            hamming_distance = bin(xor_result).count('1')
            similarity = (1 - hamming_distance / hash_size) * 100
            result = similarity > TOLERANT
        except KeyError as e:
            pass
        self.tree[finger_print_bin] = finger_print_str
        self.save()
        return result

    def save(self):
        # Store finger print in avl tree
        with open(self.file_path, "wb") as file:
            pickle.dump(self.tree, file)


simhash_url = SimhashUrl()

