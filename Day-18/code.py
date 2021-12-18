import math
import copy

DEBUG = False

def add(left_node, right_node):
    res = ExpressionTree(magnitude=0)
    res.left = left_node
    res.right = right_node
    left_node.parent = res
    right_node.parent = res
    res.height = 1+max(left_node.height, right_node.height)
    return res

class ExpressionTree:
    def __init__(self, magnitude=0):
        self.magnitude = magnitude
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    def is_leaf(self):
        return (self.left is None) and (self.right is None)

    def __str__(self):
        if self.is_leaf():
            return str(self.magnitude)
        return f"[{self.left},{self.right}]"

    def find_smallest_node_subtree(node):
        if node is None:
            return None
        curr_node = node
        while curr_node.left is not None:
            curr_node = curr_node.left
        return curr_node

    def find_largest_node_subtree(node):
        if node is None:
            return None
        curr_node = node
        while curr_node.right is not None:
            curr_node = curr_node.right
        return curr_node

    def find_predecessor(node):
        if node.left is not None:
            return ExpressionTree.find_largest_node_subtree(node.left)
        curr_node = node
        while curr_node.parent is not None and curr_node.parent.left == curr_node:
            curr_node = curr_node.parent
        if curr_node.parent is None:
            return None
        return ExpressionTree.find_largest_node_subtree(curr_node.parent.left)

    def find_successor(node):
        if node.right is not None:
            return ExpressionTree.find_smallest_node_subtree(node.right)
        curr_node = node
        while curr_node.parent is not None and curr_node.parent.right == curr_node:
            curr_node = curr_node.parent
        if curr_node.parent is None:
            return None
        return ExpressionTree.find_smallest_node_subtree(curr_node.parent.right)

    def find_first_split_node(self):
        if self.is_leaf():
            return self if self.magnitude >= 10 else None
        curr_guess = self.left.find_first_split_node()
        if curr_guess is None:
            curr_guess = self.right.find_first_split_node()
        return curr_guess

    def explode(node):
        l_val, r_val = node.left.magnitude, node.right.magnitude
        # del node.left
        # del node.right
        node.left, node.right = None, None
        node.magnitude = 0
        node.height = 0
        # modify all nodes height upto root.
        temp_parent = node.parent
        while temp_parent is not None:
            temp_parent.height = 1+max(temp_parent.left.height, temp_parent.right.height)
            temp_parent = temp_parent.parent
        # add left_val.
        predecessor = ExpressionTree.find_predecessor(node)
        if predecessor is not None:
            predecessor.magnitude += l_val
        # add right_val.
        successor = ExpressionTree.find_successor(node)
        if successor is not None:
            successor.magnitude += r_val

    def split(node):
        l_val, r_val = math.floor(node.magnitude/2), math.ceil(node.magnitude/2)
        node.left = ExpressionTree(magnitude=l_val)
        node.right = ExpressionTree(magnitude=r_val)
        node.left.parent = node
        node.right.parent = node
        node.magnitude = 0
        while node is not None:
            node.height = 1+max(node.left.height, node.right.height)
            node = node.parent

    def find_first_explode_node(self, max_height):
        if self.height <= max_height:   return None
        elif self.height == 1:          return self
        # search in left and right nodes.
        check_explode_node = self.left.find_first_explode_node(max_height-1)
        if check_explode_node is None:
            check_explode_node = self.right.find_first_explode_node(max_height-1)
        return check_explode_node

    def reduce(self):
        continue_flag = True
        while continue_flag:
            explode_node = self.find_first_explode_node(max_height=4)
            if explode_node is not None:
                if DEBUG:
                    print("After Exploding node ", explode_node, end=":\t")
                ExpressionTree.explode(explode_node)
                if DEBUG:
                    print(self)
                continue
            split_node = self.find_first_split_node()
            if split_node is not None:
                if DEBUG:
                    print("After Splitting node ", split_node, end=":\t")
                ExpressionTree.split(split_node)
                if DEBUG:
                    print(self)
                continue
            continue_flag = False # both explode_node and split_node are none.

    def compute_magnitude(self):
        if self.is_leaf():
            return self.magnitude
        return 3*self.left.compute_magnitude() + 2*self.right.compute_magnitude()


def parse(str, idx):
    curr_node = ExpressionTree(magnitude=0)
    if str[idx] <= '9' and str[idx] >= '0':
        magnitude = 0
        while(str[idx] <= '9' and str[idx] >= '0'):
            magnitude = 10*magnitude + int(str[idx])
            idx += 1
        curr_node.magnitude = magnitude
        curr_node.height = 0
        return curr_node, idx

    # read the left child.
    assert str[idx]=='['
    curr_node.left, idx = parse(str, idx+1)
    curr_node.left.parent = curr_node
    
    # read the right child.
    assert(str[idx]==',')
    curr_node.right, idx = parse(str, idx+1)
    curr_node.right.parent = curr_node

    assert(str[idx]==']')
    curr_node.height = 1+max(curr_node.left.height, curr_node.right.height)
    return curr_node, idx+1


################################ Part 1: #################################
def F_1():
    result_expression = None
    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            curr_expression, idx = parse(line, 0)
            assert idx == len(line)
            if result_expression is None:
                result_expression = curr_expression
            else:
                result_expression = add(result_expression, curr_expression)
                result_expression.reduce()

    if result_expression is not None:
        print(f"\tResult expression: {result_expression}")
        print(f"\tFinal magnitude: {result_expression.compute_magnitude()}")
    else:
        print(f"\tError !!! Something Failed.")

print("Part 1:")
F_1()

################################ Part 2: #################################
def find_result(L, R):
    res = add(L, R)
    res.reduce()
    return res.compute_magnitude()

def F_2():
    best_result = {'L': None, 'R': None, 'magnitude': 0}
    expressions_list = []
    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            curr_expression, idx = parse(line, 0)
            assert idx == len(line)
            expressions_list.append(curr_expression)
    for i in range(len(expressions_list)):
        for j in range(len(expressions_list)):
            if i == j:
                continue
            temp_magnitude = find_result(copy.deepcopy(expressions_list[i]), copy.deepcopy(expressions_list[j]))
            if temp_magnitude > best_result['magnitude']:
                best_result['magnitude'] = temp_magnitude
                best_result['L'] = str(expressions_list[i])
                best_result['R'] = str(expressions_list[j])

    print(f"\tL: {best_result['L']}, R: {best_result['R']}\n\tMagnitude: {best_result['magnitude']}")

print("Part 2:")
F_2()
