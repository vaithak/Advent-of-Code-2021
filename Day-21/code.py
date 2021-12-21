import numpy as np
import copy

class Player:
    def __init__(self, pos, max_positions):
        self.pos = pos-1 # convert to 0-indexed
        self.mod = max_positions
        self.score = 0
        self.die_count = 0
        self.prev_state = None

    def __str__(self):
        return f"Position: {self.pos+1}, Score: {self.score}, Die Count: {self.die_count}, Mod: {self.mod}, Prev State: {self.prev_state}"

    def next_state(self, die_moves):
        self.prev_state = {
            'pos': self.pos,
            'score': self.score,
            'mod': self.mod,
            'die_count': self.die_count,
            'prev_state': self.prev_state
        }
        die_sum = sum(die_moves) % self.mod
        self.die_count += len(die_moves)
        self.pos = (self.pos + die_sum)%self.mod
        self.score += self.pos + 1
    
    def undo_state(self):
        self.pos        = self.prev_state['pos']
        self.score      = self.prev_state['score']
        self.mod        = self.prev_state['mod']
        self.die_count  = self.prev_state['die_count']
        self.prev_state = self.prev_state['prev_state']

################################ Part 1: #################################
def deterministic_die(sides):
    i = 1
    while True:
        yield i
        i += 1
        if i == sides+1:
            i = 1

def F_1(max_score):
    Player1 = Player(pos=2, max_positions=10)
    Player2 = Player(pos=1, max_positions=10)
    g = deterministic_die(sides=100)
    while Player1.score < max_score and Player2.score < max_score:
        Player1.next_state([g.__next__(), g.__next__(), g.__next__()])
        if Player1.score >= max_score:
            break
        Player2.next_state([g.__next__(), g.__next__(), g.__next__()])
        if Player2.score >= max_score:
            break
    print(f"\tdie count: {Player1.die_count + Player2.die_count}")
    print(f"\tscores: {Player1.score}, {Player2.score}")

print("Part 1:")
F_1(max_score=1000)

################################ Part 1: #################################
def quantum_die_tuples(curr_tuple, tuple_size, tuple_idx, sides, tuples):
    if tuple_idx == tuple_size:
        store_tuple = copy.deepcopy(curr_tuple)
        tuples.append(store_tuple)
        return
    for i in range(1, sides+1):
        curr_tuple[tuple_idx] = i
        quantum_die_tuples(curr_tuple, tuple_size, tuple_idx+1, sides, tuples)

def game_dfs(Player1, Player2, max_score, nodes, chance, saved_game_states):
    if Player1.score >= max_score:  return np.array([1, 0])
    if Player2.score >= max_score:  return np.array([0, 1])

    curr_game_state = (Player1.pos, Player2.pos, Player1.score, Player2.score, chance)
    if curr_game_state in saved_game_states:
        return saved_game_states[curr_game_state]

    wins = np.array([0, 0])
    if chance == 0:
        # Player1 will move.
        for node in nodes:
            Player1.next_state(node)
            wins += game_dfs(Player1, Player2, max_score, nodes, chance^1, saved_game_states)
            Player1.undo_state()
    else:
        # Player2 will move.
        for node in nodes:
            Player2.next_state(node)
            wins += game_dfs(Player1, Player2, max_score, nodes, chance^1, saved_game_states)
            Player2.undo_state()

    saved_game_states[curr_game_state] = wins
    return wins

def F_2(max_score):
    possibilities = []
    quantum_die_tuples([0]*3, tuple_size=3, tuple_idx=0, sides=3, tuples=possibilities)
    Player1 = Player(pos=2, max_positions=10)
    Player2 = Player(pos=1, max_positions=10)
    wins = game_dfs(Player1, Player2, max_score=max_score, nodes=possibilities, chance=0, saved_game_states={})
    print(f"\tWins: {wins}")

print("Part 2:")
F_2(max_score=21)
