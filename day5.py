orders = {}

def apply_ordering(orders, pages,count=0):
    all = {p:i for i,p in enumerate(pages)}
    seen = {}
    for (i,p) in enumerate(pages):
        if p in orders: 
            for o in orders[p]:
                if o not in seen and o in all:
                    pages[all[o]],pages[i] = pages[i],pages[all[o]]
                    return apply_ordering(orders,pages,count+1)           
        seen[p]=i
    
    return int(pages[(len(pages)-1)//2]),count

with open("inputs/day5.txt") as file:
    for f in file:
        f = f.strip()
        if f == "":
            break
        (prev,later) = f.split("|")
        orders[int(later)] = orders.get(int(later),[]) + [int(prev)]


    correct_total = 0
    corrected_total = 0 
    for f in file:
        pages = [int(p) for p in f.strip().split(',')]
        mid,count = apply_ordering(orders,pages)
        if count == 0:
            correct_total += mid
        else: 
            corrected_total += mid


print(correct_total)
print(corrected_total)
