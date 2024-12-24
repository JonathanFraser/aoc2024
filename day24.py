import re 

m = re.compile(r"(.{3}) (OR|AND|XOR) (.{3}) -> (.{3})")
key_m = re.compile(r"(x|y|z)(\d{2})")

values = {}
rules = []

with open("inputs/day24.txt", 'r') as file:
    for l in file:
        l = l.strip()
        if l == "": 
            break 
        key,value = l.split(":")
        i,g = key_m.match(key).groups()
        values[key] = (value.strip() == "1",int(g))
    
    for l in file:
        l = l.strip()
        if l == "": 
            break
        rules.append(m.match(l).groups())

aliases = {}
for r in rules: 
    (a,op,b,c) = r
    if op == "AND" and key_m.match(a) and key_m.match(b):
        _,v = key_m.match(a).groups()
        aliases[c] = "a"+v

    if op == "XOR" and key_m.match(a) and key_m.match(b):
        _,v = key_m.match(a).groups()
        aliases[c] = "p"+v

for r in rules:
    (a,op,b,c) = r
    if op == "OR":
        if a in aliases and aliases[a][0] == "a":
            ap = aliases[a]
            aliases[c] = "c"+ap[1:]
            continue 

        if b in aliases and aliases[b][0] == "a":
            bp = aliases[b]
            aliases[c] = "c"+bp[1:]
            continue

for r in rules: 
    (a,op,b,c) = r
    if a in aliases and b in aliases:
        key = aliases[a][0] + aliases[b][0]
        if key == "pc" or key == "cp":
            if key[0] == "p":
                l = a 
            else: 
                l = b
            if op == "AND":
                aliases[c] = "h"+aliases[l][1:]
                continue
            if op == "XOR":
                aliases[c] = "o"+aliases[l][1:]


def process(values,rules,swaps = {}):
    updated = True 
    pass_count = 0
    while updated:
        print("----")
        print("pass ",pass_count)
        print("----")
        updated = False
        for r in rules:
            (a,op,b,c) = r
            if c in swaps:
                c = swaps[c]

            if a in values and b in values and c not in values:
                (v1,g1) = values[a]
                (v2,g2) = values[b]
                if g1 != g2:
                    if g1+1 != g2 and g1 != g2+1:
                        raise Exception(f"Invalid gate ({c}), inputs {a} and {b} have different positions")

                aname = a 
                if a in aliases:
                    aname = a + " (" + aliases[a]+")"
                bname = b
                if b in aliases:
                    bname = b + " (" + aliases[b] + ")"
                cname = c
                if c in aliases:
                    cname = c + " ("+aliases[c]+")"
                print(f"Processing {aname} {op} {bname} -> {cname} : {max(g1,g2)}")
                if op == "AND":
                    values[c] = (v1 and v2,max(g1,g2))
                elif op == "OR":
                    values[c] = (v1 or v2,max(g1,g2))
                elif op == "XOR":
                    values[c] = ((v1 or v2) and not (v1 and v2),max(g1,g2))
                updated = True

        pass_count += 1

process(values,rules)


def intify(values):
    zvals = list([k for k in values.keys() if k[0] == 'z'])
    value = 0 
    for i in range(0,len(zvals)):
        zkey = "z{:02d}".format(i)
        v,g = values.get(zkey)

        if v:
            value += v << i
    return value

value = intify(values)
print(value)

swaps = {}
swaps["z07"] = "shj"
swaps["shj"] = "z07"
swaps["tpk"] = "wkb"
swaps["wkb"] = "tpk"
swaps["pfn"] = "z23"
swaps["z23"] = "pfn"
swaps["z27"] = "kcd"
swaps["kcd"] = "z27"

values2 = {}
for i in range(0,45):
    values2["x{:02d}".format(i)] = (False,i)
    values2["y{:02d}".format(i)] = (True,i)
values2["x00"] = (True,0)

process(values2,rules,swaps=swaps)

values3 = {}
for i in range(0,45):
    values3["x{:02d}".format(i)] = (i % 2 == 0 ,i)
    values3["y{:02d}".format(i)] = (i % 2 == 1,i)


process(values3,rules,swaps=swaps)

print("{:d}".format(intify(values)))
print("{:045b}".format(intify(values2)))
print("{:045b}".format(intify(values3)))

l = list(swaps.keys())
l.sort()
print(",".join(l))







            
