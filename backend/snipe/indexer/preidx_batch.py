from concurrent.futures import ProcessPoolExecutor, wait
from preidx import Preindex

# TODO: find the purpose of preindex, otherwise remove it
class BatchPreindex:
    def __init__(self, config):
        self.config = config

    def batch_preindex(self, batch_docs, batch_id):
        preindex = Preindex(self.config, batch_docs, batch_id)
        preindex.process()

    def process(self):
        with ProcessPoolExecutor(max_workers=self.config.threads) as executor:
            future_tasks = []

            for i in range(0, len(self.docs), self.config.batch_size):
                batch_docs = self.docs[i : i + self.config.batch_size]
                batch_id = i
                task = executor.submit(self.batch_preindex, batch_docs, batch_id)
                future_tasks.append(task)

            wait(future_tasks)
