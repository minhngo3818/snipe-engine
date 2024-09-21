from posting import PostingList
from text_acq import read_page
from text_tranf import tokenize_context
from urllib.parse import urlparse
from snipe.schemas.preindex import (
    plist_preidx_parsed_schema, 
    urlmap_preidx_parsed_schema
)
from fastavro import writer
import json

# Description:
#   - Index urlmap data for url retrieval based on document id
#   - Categorize posting list based on different type of text
class Preindex:
    categories = ["title", "header", "str", "text"]

    def __init__(self, config, batch_docs, batch_id):
        self.config = config
        self.batch_docs = batch_docs
        self.batch_id = batch_id
        self.urlmap = []

        self.preindex_map = {key: PostingList() for key in self.categories}

    def __get_doc_stream(self):
        for doc in self.batch_docs:
            with open(doc, "r") as file:
                data = json.load(file)
            yield data

    def process(self):
        for i, doc_data in enumerate(self.__get_doc_stream()):
            self.urlmap.append(
                {
                    "id": i + self.batch_id,
                    "url": doc_data["url"],
                    "title": urlparse(doc_data["url"]).netloc,
                }
            )

            preindex_data = read_page(doc_data["content"])

            for key, context in preindex_data.items():
                tokenized_data = tokenize_context(context)
                self.preindex_map[key].add(tokenized_data, i + self.batch_id)

    def dump(self):
        for key in self.categories:
            serialized_data = self.preindex_map[key].to_dict()
            
            with open(f"{key}.avro", "wb") as data_out:
                writer(data_out, plist_preidx_parsed_schema, serialized_data)

        with open(f"{self.config.urlmap}.avro", "wb") as urlmap_out:
            writer(urlmap_out, urlmap_out, self.urlmap)