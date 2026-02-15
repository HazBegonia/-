class Trie:
    def __init__(self):
        self.ALL_CHAR = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
        self.char_to_index = {
            ch: i for i, ch in enumerate(self.ALL_CHAR)
        }
        self.SIGMA = len(self.ALL_CHAR)
        self.tr = [[-1] * self.SIGMA]
        self.cnt = [[]]
        self.idx = 0

    def insert(self, S: str, id: str):
        p = 0
        for ch in S:
            u = self.char_to_index[ch]
            if self.tr[p][u] == -1:
                self.idx += 1
                self.tr.append([-1] * self.SIGMA)
                self.cnt.append([]) 
                self.tr[p][u] = self.idx
            p = self.tr[p][u]
            self.cnt[p].append(id)

    def remove(self, S: str, id: str):
        p = 0
        for ch in S:
            u = self.char_to_index[ch]
            if self.tr[p][u] == -1:
                return
            p = self.tr[p][u]
            if id in self.cnt[p]: 
                self.cnt[p].remove(id)

    def query(self, S: str) -> tuple:
        p = 0
        for ch in S:
            u = self.char_to_index[ch]
            if self.tr[p][u] == -1:
                return ()
            p = self.tr[p][u]
        return tuple(self.cnt[p])

tr = Trie()
tr.insert('12', '1')
tr.insert('123', '2')
tr.insert('2', '3')
tr.insert('114514', '4')
print(tr.query('12'))