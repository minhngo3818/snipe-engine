from fastavro import writer, reader
from snipe.schemas.index import kg_idx_psch

# TODO: review what is kgram indexer for
class KGramIndexer:
    def __init__(self, file_path, k=3):
        self.kg_map = {}
        self.k = k
        self.file_path = file_path

    def __get_grams(self, word):
        fm_word = f"${word}$"
        return [fm_word[i : i + self.k] for i in range(len(word) - self.k + 1)]

    def add_word(self, word):
        grams = self.__get_grams(word)

        for g in grams:
            if g not in self.kg_map:
                self.kg_map[g] = {}
            self.kg_map[g].add(word)

    def __to_dict_list(self):
        for k in list(self.kg_map.keys()):
            self.kg_map[k] = list(self.kg_map[k])

    def dump_data(self):
        with open(self.file_path, "wb") as avro_file:
            writer(avro_file, kg_idx_psch, self.kg_map)

    @staticmethod
    def load_data(self):
        with open(self.file_path, "rb") as avro_file:
            data = reader(avro_file, kg_idx_psch)

        return data
