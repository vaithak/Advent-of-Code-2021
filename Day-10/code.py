error_points = {')': 3, ']': 57, '}':1197, '>':25137}
open_close_map = {'(':')', '[':']', '{':'}', '<':'>'}

def syntax_error_score(s):
    stack = []
    for char in s:
        if char in open_close_map:
            stack.append(char)
        elif len(stack)>0 and char==open_close_map[stack[-1]]:
            del stack[-1]
        else:
            return error_points[char], stack
    return 0, stack

def F_1():
    res = 0
    with open("input.txt") as f:
        for line in f:
            score, _ = syntax_error_score(line.strip())
            res += score
    print("\tres: ", res)

print("Part 1:")
F_1()


#### Part 2:
autocomplete_points = {')': 1, ']': 2, '}':3, '>':4}

def F_2():
    scores = []
    with open("input.txt") as f:
        for line in f:
            error_score, stack = syntax_error_score(line.strip())
            if error_score == 0:
                # complete or incomplete line
                res = 0
                while len(stack)>0:
                    res = 5*res + autocomplete_points[open_close_map[stack[-1]]]
                    del stack[-1]
                scores.append(res)
    n = len(scores)
    print("\tmedian of scores: ", sorted(scores)[(n-1)//2])

print("Part 2:")
F_2()
