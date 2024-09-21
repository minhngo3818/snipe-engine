from io import StringIO
import zlib


def get_common_prefix_len(str1, str2):
    i = 0
    while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
        i += 1
    return i


def create_fc_str(header, prefix_len, short_wd, doc_freq, docs_id):
    # header: 1 - root word, 0 -following str
    # prefix_len: prefix length with previous word (0 if root word)
    # short_wd: word or suffix
    # doc_freq: doc frequency
    # docs_id: pointer to docs (posting list)

    return f"{header},{prefix_len},{short_wd},{doc_freq},{docs_id}\n"


def fc_encode(dict_map):
    # Use front coding to compress dictionary
    # Return comrpessed data as bytes with zlib support

    output = ""
    prev_word = None

    for word, value in dict_map.items():
        if not prev_word or prev_word[0] != word[0]:
            prev_word = word
            output += create_fc_str(
                1, 0, prev_word, value["doc_freq"], value["docs_id"]
            )
        else:
            prefix_len = get_common_prefix_len(prev_word, word)
            output += create_fc_str(
                1,
                prefix_len,
                prev_word[prefix_len:],
                value["doc_freq"],
                value["docs_id"],
            )

    return zlib.compress(output.encode("utf-8"))


def fc_decode(bin_dict_str):
    # Decompressed binary dict to dictionary

    # Convert compressed binary dict to string
    dict_str = zlib.decompress(bin_dict_str).decode("utf-8")

    # Create StringIO object for convenient parsing
    dict_stringio = StringIO(dict_str)

    output = {}
    prev_word = None

    for line in dict_stringio:
        parts = line.split(",")

        if int(parts[0]) == 1:
            prev_word = parts[2]
            output[prev_word] = {"doc_freq": int(parts[3]), "docs_id": int(parts[4])}
        else:
            prefix_len = int(parts[1])
            prev_word = prev_word[:prefix_len] + parts[2]
            output[prev_word] = {"doc_freq": int(parts[3]), "docs_id": int(parts[4])}

    return output
