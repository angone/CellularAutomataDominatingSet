
class OrbitTable:
    def __init__(self, n, s):
        self.n = n
        self.s = s
        self.table = [s]
        self.snakes = {}
        self.sum = []
        self.tickertape = []
        self.rows = 1
        
    def update(self):
        last = self.table[len(self.table)-1][:]
        new = []
        for i in range(self.n):
            if last[i] == 0:
                last[i] = 1
                new.append(1)
            elif last[i] == 1 and last[(i-1)%self.n] == 0 and last[(i-2)%self.n] == 0:
                new.append(1)
            elif last[i] == 1 and last[(i-1)%self.n] == 0 and last[(i+1)%self.n] == 0:
                new.append(1)
            elif last[i] == 1 and last[(i+2)%self.n] == 0 and last[(i+1)%self.n] == 0:
                new.append(1)
            else:
                last[i] = 0
                new.append(0)
        self.table.append(new)
        self.rows += 1
        return
        
    def check_loop(self, m):
        for i in range(self.n):
            if self.table[m][i] != self.s[i]:
                return False
        return True
        
    def simulate(self):
        self.update()
        i = 1
        while not self.check_loop(i):
            self.update()
            i = i + 1
        self.table.pop(len(self.table)-1)
        
    def mark_snakes(self):
        
            
    def printTablePlainText(self):
        for m in self.table:
            for i in range(self.n):
                print(m[i], end=' ')
            print('')
            
test = OrbitTable(4, [1, 1, 1, 1])
test.simulate()
test.printTablePlainText()