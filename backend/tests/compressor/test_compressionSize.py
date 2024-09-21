from snipe.compressor.dict_encoder import fc_encode, fc_decode
import sys
import unittest

class TestCompressionSize(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        word_list = [
            "uncover",
            "unwind",
            "unleash",
            "undergo",
            "misplace",
            "mislead",
            "misprint",
            "rebuild",
            "reconnect",
            "recharge",
            "disapprove",
            "disappear",
            "disagree",
            "preheat",
            "precede",
            "predict",
            "submerge",
            "subdivide",
            "subdue",
            "subside",
        ]

        doc_data = [
            {"doc_freq": 45, "docs_id": 977431},
            {"doc_freq": 27, "docs_id": 916571},
            {"doc_freq": 2, "docs_id": 189674},
            {"doc_freq": 43, "docs_id": 591712},
            {"doc_freq": 86, "docs_id": 694281},
            {"doc_freq": 62, "docs_id": 824056},
            {"doc_freq": 37, "docs_id": 207520},
            {"doc_freq": 40, "docs_id": 289228},
            {"doc_freq": 97, "docs_id": 451078},
            {"doc_freq": 79, "docs_id": 621632},
            {"doc_freq": 12, "docs_id": 800178},
            {"doc_freq": 74, "docs_id": 279956},
            {"doc_freq": 27, "docs_id": 212947},
            {"doc_freq": 27, "docs_id": 261627},
            {"doc_freq": 22, "docs_id": 528220},
            {"doc_freq": 84, "docs_id": 15844},
            {"doc_freq": 78, "docs_id": 209039},
            {"doc_freq": 42, "docs_id": 581930},
            {"doc_freq": 7, "docs_id": 206837},
            {"doc_freq": 12, "docs_id": 654361},
        ]

        cls.data = {}

        for word, doc in zip(word_list, doc_data):
            cls.data[word] = doc
    
    def test_compare_compressed_size(self):
        compressed_words_str = fc_encode(self.data)
        words_dict = fc_decode(compressed_words_str)

        compressed_str_size = sys.getsizeof(compressed_words_str)
        decompressed_dict_size = sys.getsizeof(words_dict) / 2
        self.assertLess(a=compressed_str_size, b=decompressed_dict_size, 
                        msg=f"compressed size: {compressed_str_size}\ndecompressed size: {decompressed_dict_size}")

if __name__ == "__main__":
    unittest.main()
