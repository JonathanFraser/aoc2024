with open("inputs/day11.txt") as f:
    nums = f.read().strip().split(' ')

cache = {}

def walk(number: str, depth=0):
    if depth == 0:
        return 1
    
    if (number, depth) in cache:
        return cache[(number, depth)]
    
    if number == "0":
        retval = walk("1", depth-1)
        cache[(number, depth)] = retval
        return retval
    
    if len(number) %2 == 0:
        n1 = walk(number[:len(number)//2], depth-1)
        n = number[len(number)//2:].lstrip('0')
        n2 = walk(n if n else "0", depth-1)
        retval = n1 + n2
        cache[(number, depth)] = retval
        return retval
    
    retval = walk(str(int(number)*2024), depth-1)
    cache[(number, depth)] = retval
    return retval

count = 0 
count_far = 0 
for i in nums:
    count += walk(i,25)
    count_far += walk(i,75)
print(count)
print(count_far)