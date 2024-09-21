from fastavro import parse_schema


"""
Doc PreIndex
"""
doc_preidx_schema = {
    "name": "Doc",
    "type": "record",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "term_freq", "type": "int"},
        {"name": "pos_idx", "type": {"type": "array", "items": "int"}},
    ],
}
doc_preidx_parsed_schema = parse_schema(doc_preidx_schema)


"""
Posting List PreIndex
"""
plist_preidx_schema = {
    "name": "PostingList",
    "type": "map",
    "values": {
        "name": "Posting",
        "type": "record",
        "fields": [
            {"name": "doc_freq", "type": "int"},
            {"name": "docs", "type": {"type": "array", "items": "Doc"}},
        ],
    },
}
plist_preidx_parsed_schema = parse_schema(plist_preidx_schema)


"""
UrlMap Preindex
"""
urlmap_preidx_schema = {
    "name": "UrlMapPreidx",
    "type": "record",
    "values": [
        {"name": "id", "type": "int"},
        {"name": "url", "type": "string"},
        {"name": "title", "type": "string"},
    ],
}
urlmap_preidx_parsed_schema = parse_schema(urlmap_preidx_schema)
