from text_acq import get_page_list
from preidx_batch import BatchPreindex
from utils.config import Config

def run_indexer(config):
    docs = get_page_list(config.dataset)
    batch_preindex = BatchPreindex(config, docs)
    batch_preindex.process()