import itertools
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-n", type = int, default = 7, help = "number of nodes")
parser.add_argument("-row", type = str, default = "1111111", help = "starting row")
parser.add_argument("-oper", type = str, default = "all", help = "operation to perform")

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
        self.snakeCount = 1
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
        self.calcSums()
    
    def calcSums(self):
        for i in range(self.n):
            s = 0
            for j in range(self.rows):
                s += self.table[j][i]
            self.sum.append(s)
            
            
            
    def fillInSnake(self, i, j, c, prev):
        if self.table[i][j] == 1:
            return False
        if (i, j) in self.snakes:
            return True
        flag = False
            
        if j < self.n-1:
            if self.table[i][j+1] == 0:
                self.snakes[(i,j)] = c
                self.snakes[(i,j+1)] = c
                flag = True
        else:
            if self.table[(i+1)%self.rows][0] == 0:
                self.snakes[(i,j)] = c
                self.snakes[(i+1, 0)] = c
                flag = True
        if not flag:
            if i == 0 and j == 0 and self.table[0][1]:
                i = self.rows-1
                j = self.n-1
                self.snakes[(i,j)] = c 
                self.snakes[(0,0)] = c
                flag = True
        if not flag:
            return False
        if self.snakeCount == 1:
            self.slither += prev
                #take 2 step
        if j < self.n-3 and self.fillInSnake((i-2)%self.rows,j+3, c, '2'):
            return True
        if j >= self.n-3 and self.fillInSnake((i-1)%self.rows,(j+3)%self.n,c, '2'):
            return True
    
        #take 0 step, options are (i-2%rows, j)
        if j < self.n - 1 and self.fillInSnake((i-2)%self.rows,j+1,c,'0'):
            return True
        if j == self.n - 1 and self.fillInSnake((i-1)%self.rows,0,c,'0'):
            return True
        #take 1 step
        if j < self.n - 2 and self.fillInSnake((i-2)%self.rows,j+2,c,'1'):
            return True
        if j >= self.n-2 and self.fillInSnake((i-1)%self.rows,(j+2)%self.n,c,'1'):
            return True

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
                    if self.fillInSnake(i, j, self.snakeCount, ''):
                        self.snakeCount += 1
              
    def printTablePlainText(self):
        for m in self.table:
            for i in range(self.n):
                print(m[i], end='')
            print('')
            
            
            
    def printTableLatex(self):
        print('\\begin{figure}[!ht]')
        print('\\begin{center}')
        print('\\setlength{\\tabcolsep}{2.5pt}')
        print('\\renewcommand{\\arraystretch}{.4}')
        print('\\begin{tabular}{',end='')
        for _ in range(self.n+1):
            print('c',end='')
        print('}')
        print('$x$',end='')
        for i in range(1,self.n+1):
            print(' & $v_{' + str(i)+'}$', end='')
        print(' \\Bstrut')
        print('\\\\\\hline')
        for i in range(self.rows):
            print('$x^{(' + str(i) + ')}$', end='')
            for j in range(self.n):
                c = self.snakes[(i,j)]
                if c == -1:
                    print(' & \\1', end='')
                elif c == -2:
                    print(' & \\0', end='')
                else:
                    print(' & {\\color{color' + str(c) + '}\\0}', end = '')
            print(' \\\\')
        print('\\hline \\Tstrut')
        print('{\\bf Sum:} ', end='')
        for i in range(self.n):
            print('& \\bf{' + str(self.sum[i]) + '}', end='')
        print('\n\\end{tabular}')
        print("\\newline")
        print(self.slither)
        print('\\end{center}')
        print('\\end{figure}')
                
        
def singleRow():
    x = []
    for y in args.row:
        x.append(int(y))
    t = OrbitTable(args.n, x)
    t.simulate()
    t.markSnakes()
    t.printTableLatex()

def allOrbitsForGivenN():
    n = args.n
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
        x.printTableLatex()
        
        
if args.oper = "all":
    allOrbitsForGivenN()
elif args.oper == "row":
    singleRow()
