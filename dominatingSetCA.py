import itertools

def validateRow(s, n):
    for i in range(n):
        if s[i] == 0 and s[(i-1)%n] == 0 and s[(i-2)%n] == 0:
            return False
        if s[i] == 0 and s[(i-1)%n] == 0 and s[(i+1)%n] == 0:
            return False
        if s[i] == 0 and s[(i+1)%n] == 0 and s[(i+2)%n] == 0:
            return False
    return True




class OrbitTable:
    def __init__(self, n, s):
        self.n = n
        self.s = s
        self.table = [s]
        self.snakes = {}
        self.sum = []
        self.tickertape = []
        self.rows = 0
        self.snakeCount = 0
        self.isReduced = True
        self.slither = ''
        
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
        for a in self.table:
            for b in a:
                self.tickertape.append(b)
        
    def fillInSnake(self, i, j, c):
        self.snakes[(i,j)] = c
        flag = False
        if j < n-1:
            if self.table[i][j+1] == 0:
                self.snakes[(i,j+1)] = c
                flag = True
        else:
            if self.table[i+1][0] == 0:
                self.snakes[(i+1, 0)] = c
                flag = True
        if not flag:
            return False
        #take 0 step, options are (i-2%rows, j)
        if self.fillInSnake((i-2)%self.rows,j,c):
            return True
        #take 1 step
        
        #take 2 step
    
    def markSnakes(self):
        for i in range(self.rows):
            for j in range(self.n):
                if (i,j) in self.snakes:
                    continue
                if self.table[i][j] == 1:
                    self.snakes[(i,j)] = -1
                if self.tickertape[i*self.n + j] == 0 and self.tickertape[(i*self.n + j - 1)%len(self.tickertape)] == 1 and self.tickertape[(i*self.n + j + 1)%len(self.tickertape)] == 1:
                    self.snakes[(i,j)] = -2
                    self.isReduced = False
                else:
                    self.fillInSnake(i, j)
              
    def printTablePlainText(self):
        for m in self.table:
            for i in range(self.n):
                print(m[i], end=' ')
            print('')
          
            
            
for i in range(1,15):
    n = i
    states = list(map(list, itertools.product([0, 1], repeat=n)))
    

    orbits = []
    for x in states:
        if not validateRow(x, n):
            states.remove(x)
            continue
        t = OrbitTable(n, x)
        t.simulate()
        t.markSnakes()
        orbits.append(t)
        for y in t.table:
            states.remove(y)
    count = 0
    for x in orbits:
        if(x.isReduced):
            print(x.rows)
