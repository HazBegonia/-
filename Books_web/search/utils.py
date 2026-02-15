# search/utils.py

class BookTrie:
    def __init__(self):
        self.nodes = [{"next": {}, "ids": set()}]
        self.idx = 0

    def insert(self, title: str, upc: str):
        p = 0
        for ch in title.lower():
            if ch not in self.nodes[p]["next"]:
                self.idx += 1
                self.nodes.append({"next": {}, "ids": set()})
                self.nodes[p]["next"][ch] = self.idx
            p = self.nodes[p]["next"][ch]
            
            if len(self.nodes[p]["ids"]) < 20:
                self.nodes[p]["ids"].add(upc)

    def query(self, prefix: str):
        p = 0
        for ch in prefix.lower():
            if ch not in self.nodes[p]["next"]:
                return []
            p = self.nodes[p]["next"][ch]
        return list(self.nodes[p]["ids"])