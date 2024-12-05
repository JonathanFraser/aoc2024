
def increasing(s):
    return [i > 0 for i in s]

def decreasing(s):
    return [i < 0 for i in s]

def inrange(s): 
    return list([abs(i) >= 1 and abs(i) <= 3 for i in s])

def delta(s):
    return list([s[i + 1] - s[i] for i in range(len(s) - 1)])

def evaluate_report(report):
    deltas = delta(report)
    if (all(increasing(deltas)) or all(decreasing(deltas))) and all(inrange(deltas)):
        return 1
    return 0


simple_count = 0
total_count = 0
with open("inputs/day2.txt") as file:
    for line in file:
        report = list([int(i) for i in line.split()])
        is_safe = evaluate_report(report)
        if is_safe: 
            simple_count += 1
            total_count += 1
            continue

        for i in range(len(report)):
            new_report = report[:i] + report[i + 1:]
            is_safe = evaluate_report(new_report)
            if is_safe:
                total_count += 1
                break

print(simple_count)
print(total_count)
