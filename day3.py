import re

match = re.compile(r'(do|don\'t|mul)\(([1-9][0-9]{0,2},[1-9][0-9]{0,2}){0,1}\)')

text = open('inputs/day3.txt').read()
condtional_total = 0 
unconditional_total = 0
enabled = 1
# part 1: 179834255
# part 2: 80570939
def mul(m):
    global enabled
    global unconditional_total
    global condtional_total
    if m[0] == '':
        return 
    (a,b) = m[0].split(',')
    amount = int(a) * int(b)
    condtional_total += amount if enabled else 0
    unconditional_total += amount

def do(m):
    global enabled
    if m[0] == '':
        enabled = 1

def dont(m):
    global enabled
    if m[0] == '':
        enabled = 0

operations = {}
operations["mul"] = mul
operations["do"] = do
operations["don't"] = dont

for m in match.findall(text):
    operations[m[0]](m[1:])

print(unconditional_total)
print(condtional_total)
    