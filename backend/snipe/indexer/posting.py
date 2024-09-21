from collections import defaultdict


class DocNode:
    def __init__(self, doc_id, term_freq, positions):
        self.id = doc_id
        self.term_freq = term_freq
        self.pos_idx = positions
        self.next = None


class DocList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add(self, new_node):
        if not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = self.tail.next

    def remove(self, doc_id):
        prev = None
        current = self.head

        while current:
            if current.id == doc_id:
                if not self.prev:
                    self.head = current.next
                else:
                    prev.next = current.next

                current = None
                break
            else:
                prev = current
                current = current.next

    def get(self, doc_id):
        current = self.head

        while current:
            if current.id == doc_id:
                return current
            else:
                current = current.next

    def to_list(self):
        current = self.head
        result = []

        while current:
            result.append(
                {
                    "id": current.id,
                    "term_freq": current.term_freq,
                    "pos_idx": current.pos_idx,
                }
            )
            current = current.next

        return result


class PostingList:
    def __init__(self):
        self.p_list = defaultdict(lambda: {"doc_freq": 0, "docs": None})

    def add(self, token_map, doc_id):
        for token in token_map.keys():
            new_node = DocNode(doc_id, len(token_map[token]), token_map[token])

            if token not in self.p_list:
                self.p_list[token] = {"doc_freq": 0, "docs": DocList()}

            self.p_list[token]["doc_freq"] += 1
            self.p_list[token]["docs"].add(new_node)

    def to_dict(self):
        result = {}
        for key, value in self.p_list.items():
            result[key] = {
                "doc_freq": value["doc_freq"],
                "docs": value["docs"].to_list(),
            }

        return result

    def view(self):
        print(self.p_list)
