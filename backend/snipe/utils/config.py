import os


class Config:
    def __init__(self, config):
        # Dataset
        self.dataset_dir = config["DATASET"]["DATASET_DIR"]

        # Indexer
        indexer_keys = [
            "TITLE_INDEX",
            "HEADER_INDEX",
            "STR_INDEX",
            "TEXT_INDEX",
            "POS_INDEX",
            "URL_MAP",
            "SIMI_MAP",
        ]
        self.index_ext = config["INDEXER"]["INDEX_EXT"]
        self.index_dir = config["INDEXER"]["INDEX_DIR"]

        for key in indexer_keys:
            setattr(self, f"{key.lower()}", config["INDEXER"][key] + self.index_ext)
            setattr(
                self,
                f"{key.lower()}_path",
                os.path.join(self.index_dir, getattr(self, f"{key.lower()}")),
            )

        self.batch_name = config["INDEXER"]["BATCH_NAME"]
        self.batch_size = int(config["INDEXER"]["BATCH_SIZE"])

        # Searcher
        self.top_k = int(config["SEARCHER"]["TOP_K"])
        self.page_size = int(config["SEARCHER"]["PAGE_SIZE"])

        # Process
        self.threads = int(config["PROCESS"]["THREADS"])

        # Test
        self.test_output_dir = config["TEST"]["TEST_OUTPUT_DIR"]
        self.test_ext = config["TEST"]["TEST_EXT"]
        self.test_query = config["TEST"]["TEST_QUERY"] + self.test_ext
        self.test_result = config["TEST"]["TEST_RESULT"] + self.test_ext
        self.test_query_path = os.path.join(self.test_output_dir, self.test_query)
        self.test_result_path = os.path.join(self.test_output_dir, self.test_result)
        self.soft_spd_limit = int(config["TEST"]["SOFT_SPD_LIMIT"])
        self.hard_spd_limit = int(config["TEST"]["HARD_SPD_LIMIT"])
