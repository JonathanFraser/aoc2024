import re
from typing import List

class Puter:
    A: int
    B: int
    C: int
    program: List[int]
    program_counter: int 

    def __init__(self,registers,program):
        self.A = registers['A']
        self.B = registers['B']
        self.C = registers['C']
        self.program = program
        self.program_counter = 0
        self.outputs = []

    def copy(self):
        p = Puter({'A':self.A,'B':self.B,'C':self.C},self.program)
        p.program_counter = self.program_counter
        p.outputs = self.outputs.copy()
        return p


    def decode_combo(self,opand):
        if opand == 7:
            raise Exception("Invalid combo opand")
        
        if opand == 6:
            return self.C 
        
        if opand == 5:
            return self.B
        
        if opand == 4:
            return self.A
        
        return opand


    def step(self):
        if self.program_counter >= len(self.program)-1:
            return False
        
        instr = self.program[self.program_counter]
        opand = self.program[self.program_counter+1]

        if instr == 0: #adv
            self.A = self.A // (1<<self.decode_combo(opand))
            self.program_counter += 2
            return True
        
        if instr == 1: #bxl
            self.B = self.B ^ opand
            self.program_counter += 2
            return True

        if instr == 2: #bst 
            self.B = self.decode_combo(opand) % 8
            self.program_counter += 2
            return True
        
        if instr == 3: #jnz
            if self.A == 0:
                self.program_counter += 2
                return True
            
            self.program_counter = opand
            return True
        
        if instr == 4: #bxc
            self.B = self.B ^ self.C 
            self.program_counter += 2
            return True
        
        if instr == 5: #out
            self.outputs.append(self.decode_combo(opand) % 8)
            self.program_counter += 2
            return True
        
        if instr == 6: #bdv
            self.B = self.A // (1 << self.decode_combo(opand))
            self.program_counter += 2
            return True

        if instr == 7: #cdv
            self.C = self.A // (1 << self.decode_combo(opand))
            self.program_counter += 2
            return True
        
    def run(self):
        while self.step():
            pass

        return self.outputs

rm = re.compile(r"Register ([ABC]): (\d+)")
pm = re.compile(r"Program: (.*)")


with open("inputs/day17.txt") as f:
    reg = {}
    (k,v) = rm.match(f.readline().strip()).groups()
    reg[k] = int(v)
    (k,v) = rm.match(f.readline().strip()).groups()
    reg[k] = int(v)
    (k,v) = rm.match(f.readline().strip()).groups()
    reg[k] = int(v)
    f.readline()
    prog = [int(d) for d in pm.match(f.readline().strip()).groups()[0].split(",")]
    puter = Puter(reg,prog)

print(",".join([str(d) for d in puter.copy().run()]))

def comput_a(values):
    return sum([v*(8**i) for (i,v) in enumerate(values)])

def run_values(values):
    a = comput_a(values)
    reg = {'A':a,'B':0,'C':0}
    puter = Puter(reg,prog)
    return puter.run()

def search_values(values,idx):
    if idx == -1:
        res = run_values(values)
        if len(res) == len(prog) and res == prog:
            return [comput_a(values)]
        return []
    
    retval = []
    for i in range(0,8):
        cp = values.copy()
        cp[idx] = i
        res = run_values(cp)
        if len(res) == len(prog) and res[idx:] == prog[idx:]:
            retval += search_values(cp,idx-1)
    
    return retval

values = [0 for d in range(0,len(prog))]
options = search_values(values,len(values)-1)

print(min(options))
            





