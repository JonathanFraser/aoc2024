options_count = 0 
matching = 0 

with open('inputs/day19.txt') as f:
    language = set([l.strip() for l in f.readline().strip().split(',')])
    f.readline()
 
    for l in f:
        w = l.strip()
        arr =[0]*(len(w)+10)
        arr[0] = 1
        for n in range(0,len(w)):
            for l in language:
                if w[n:].startswith(l):
                    arr[n+len(l)] += arr[n]

        options_count += arr[len(w)]
        if arr[len(w)] > 0:
            matching += 1

print(matching)
print(options_count)