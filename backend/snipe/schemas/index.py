from fastavro import parse_schema

"""
Dictionary Index
Byte Struct:
    Main: <1>,<partial_term>,<prefix_len>,<doc_freq>,<docs_id>
    Tail(s): <0>,<suffix>,<prefix_len>,<doc_freq>,<docs_id>  
"""
dict_idx_schema = {"name": "DictIndex", "type": "bytes"}
dict_idx_psch = parse_schema(dict_idx_schema)


"""
Docs Index
Store a list of byte sequences
Each byte sequence represent for docs per word
"""
docs_idx_schema = {"name": "DocsIdx", "type": "bytes"}
docs_idx_psch = parse_schema(docs_idx_schema)


"""
KGram Index
Struct:
    Key: k gram
    Value: byte sequence represent an ordered list of words
"""
kg_idx_schema = {"name": "KGramIndex", "type": "map", "values": "bytes"}
kg_idx_psch = parse_schema(kg_idx_schema)


"""
Term Position Index
Stuct:
    - pid: hash key built from term & doc_id
    (more importance, higher score, and can be added on)
    - pos_idx: byte sequence represent 
    for positions of the term in the associated doc
"""
term_pos_idx_schema = {
    "name": "TermPosIndex",
    "type": "record",
    "fields": [
        {"name": "pid", "type": "int"},
        {"name": "pos_idx", "type": "bytes"},
    ],
}
term_pos_idx_psch = parse_schema(term_pos_idx_schema)


"""
UrlMap Index
"""
urlmap_idx_schema = {
    "name": "UrlMap",
    "type": "record",
    "fields": [{"name": "url", "type": "string"}, {"name": "title", "type": "string"}],
}
urlmap_idx_psch = parse_schema(urlmap_idx_schema)
