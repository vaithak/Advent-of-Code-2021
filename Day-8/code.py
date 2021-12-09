def F_1():
    with open("input.txt") as f:
        res = 0
        for line in f:
            _, out = line.split('|')
            strs = out.strip().split(' ')
            for str in strs:
                segments = len(str.strip())
                if segments == 2 or segments == 3 or segments == 4 or segments == 7:
                    res += 1
        print("\tres: ", res)

print("Part 1:")
F_1()

##### Part 2:

# A state represents one digit on a seven segment display
class State:
    def __init__(self, str, num=None):
        self.char_map = {}
        self.num = num
        for char in str:
            self.char_map[char] = True

    def __str__(self):
        return str(self.num)

    def contains(self, char):
        return (char in self.char_map[char])

    def equal(self, another_state):
        return self.char_map == another_state.char_map

    def __len__(self):
        return len(self.char_map)

    def matches(self, str):
        if len(str) != len(self.char_map):
            return False
        for char in str:
            if char not in self.char_map:
                return False
        return True

    def union(self, another_state):
        out_state_str = ""
        for char in "abcdefg":
            if (char in self.char_map) or (char in another_state.char_map):
                out_state_str += char
        return State(out_state_str)

    def intersect(self, another_state):
        out_state_str = ""
        for char in "abcdefg":
            if (char in self.char_map) and (char in another_state.char_map):
                out_state_str += char
        return State(out_state_str)

# this function returns an unprocessed (.num = None) invalid state whose union with 
# operand_state is equal to the result_state.
def find_state_with_unions(invalid_states, operand_state, result_state):
    for inv_state in invalid_states:
        if (inv_state.num == None):   # unprocessed state
            if inv_state.union(operand_state).equal(result_state):
                return inv_state
    return None


# this function returns an unprocessed (.num = None) invalid state whose intersection with 
# operand_state is equal to the result_state.
def find_state_with_intersects(invalid_states, operand_state, result_state):
    for inv_state in invalid_states:
        if (inv_state.num == None):   # unprocessed state
            if inv_state.intersect(operand_state).equal(result_state):
                return inv_state
    return None


def process_line(inp_strs, out_strs):
    invalid_states = [State(s) for s in inp_strs]
    num_invalid_state_map = [None]*10
    # now you have to map each number to an invalid state.
    for inv_state in invalid_states:
        # first find 1,4,7,8
        if len(inv_state) == 2:
            inv_state.num = 1
            num_invalid_state_map[1] = inv_state
        elif len(inv_state) == 3:
            inv_state.num = 7
            num_invalid_state_map[7] = inv_state
        elif len(inv_state) == 4:
            inv_state.num = 4
            num_invalid_state_map[4] = inv_state
        elif len(inv_state) == 7:
            inv_state.num = 8
            num_invalid_state_map[8] = inv_state
    # 6 is the only unprocessed number whose union with 1 is 8.
    operations = [
        [6, 'union'       , 1, 8], # 6 is the only unprocessed number whose union with 1 is 8.
        [9, 'intersection', 4, 4], # 9 is the only unprocessed number whose intersection with 4 is 4.
        [5, 'union'       , 1, 9], # 5 is the only unprocessed number whose union with 1 is 9.
        [3, 'union'       , 4, 9], # 3 is the only unprocessed number whose union with 4 is 9.
        [0, 'union'       , 3, 8], # 0 is the only unprocessed number whose union with 3 is 8.
        [2, 'union'       , 4, 8], # 2 is the only unprocessed number.
    ]
    for operation in operations:
        to_find, op, operand, result = operation
        if op == "union":
            inv_state = find_state_with_unions(invalid_states, num_invalid_state_map[operand], num_invalid_state_map[result])
        elif op == "intersection":
            inv_state = find_state_with_intersects(invalid_states, num_invalid_state_map[operand], num_invalid_state_map[result])
        inv_state.num = to_find
        num_invalid_state_map[to_find] = inv_state
    # find the number for out_strs using the processed mapping.
    mult_factor = 1000
    res = 0
    for s in out_strs:
        for guess_state in invalid_states:
            if guess_state.matches(s):
                res += guess_state.num*mult_factor
                break
        mult_factor //= 10
    print(res)
    return res


def F_2():
    # valid_states = [
    #     State("abcefg", 0), State("cf", 1)    , State("acdeg", 2), State("acdfg", 3)  , State("bcdf", 4)  ,
    #     State("abdfg", 5) , State("abdefg", 6), State("acf", 7)  , State("abcdefg", 8), State("abcdfg", 9),
    # ]
    res = 0
    with open("input.txt") as f:
        for line in f:
            inp, out = line.split('|')
            inp_strs = inp.strip().split(' ')
            out_strs = out.strip().split(' ')
            res += process_line(inp_strs, out_strs)
    print("\tres: ", res)


print("Part 2:")
F_2()
