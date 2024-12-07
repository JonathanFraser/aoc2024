def find_set(test_value, ns, operators=""):

    if len(ns) == 1:
        return  [operators] if test_value == ns[0] else [] 
    
    retval = []

    n = ns[0]
    ns = ns[1:]

    add1 = ns.copy()
    add1[0] = n + ns[0]
    retval += find_set(test_value,add1,operators+"+")

    # Try multiplying 
    mult1 = ns.copy()
    mult1[0] = n * ns[0]
    retval += find_set(test_value,mult1,operators+"*")

    #try concatenating
    concat1 = ns.copy()
    concat1[0] = int(str(n) + str(ns[0]))
    retval += find_set(test_value,concat1,operators+"c")
 
    return retval

part1_accum : int = 0 
part2_accum : int = 0

with open("inputs/day7.txt") as f:
    for l in f:
        (test_value, numbers) = l.strip().split(":")
        tv = int(test_value)
        ns = [int(n) for n in numbers.strip().split(" ")]
        possibilities = find_set(int(test_value),ns)
        normal_solves = len([p for p in possibilities if "c" not in p])
        #print("{tv}: {count}".format(tv=tv,count=possibilities))
        if normal_solves > 0:
            part1_accum += tv

        if possibilities:
             part2_accum += tv

print(part1_accum)
print(part2_accum)
