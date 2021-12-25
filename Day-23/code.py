import copy
import heapq
from typing import Dict, Any, Tuple, List

Position = Dict[str, Any]

RECURSION_LEVEL = 0
INFINITY = 1e5
ROOMS_NUM = 4
GATEWAY_SLOTS = 3 + 2*ROOMS_NUM
ROOM_SLOTS = 2

LOCATION_GATEWAY = 0
LOCATION_ROOM = 1

# starting config of each room. Each room is filled from bottom to top.
START_ROOMS = [['C', 'D'], ['C', 'B'], ['A', 'D'], ['B', 'A']]
# START_ROOMS = [['A', 'B'], ['D', 'C'], ['C', 'B'], ['A', 'D']]
# START_ROOMS = [['A', 'B'], ['B', 'A'], ['C', 'C'], ['B', 'A']]

################################################################################
class Amphipod:
    def __init__(self, type_char: str, position: Position, is_done: bool):
        self.type_num = ord(type_char) - ord('A')
        self.move_energy = 10**self.type_num
        self.position = position
        self.is_done = is_done
        self.energy = 0
    
    def __str__(self):
        return f"type_num: {self.type_num}"

    # move is a tuple of positions, specifying from and to. Returns the energy diff because of this move.
    def make_move(self, move: Tuple[Position, Position], steps: int):
        assert self.position == move[0]
        energy_diff = self.move_energy*steps
        self.energy += energy_diff
        self.position = move[1]
        return energy_diff

    # Returns the energy diff because of undoing this move (will be negative).
    def undo_move(self, last_move: Tuple[Position, Position], steps: int):
        assert last_move[1] == self.position
        energy_diff = self.move_energy*steps
        self.energy -= energy_diff
        self.position = last_move[0]
        return energy_diff

################################################################################  
class Room:
    def __init__(self, num: int):
        self.room_num = num
        self.slots = [None]*ROOM_SLOTS # each slot either contains an Amphipod or is None (empty).
    
    # returns the lowest empty slot where it's amphipod can move to. All the slots below it must be
    # already filled by the amphipods of type same as room number.
    def lowest_empty_slot(self):
        for i in range(ROOM_SLOTS):
            if self.slots[i] is None:
                return i
            elif self.slots[i].type_num != self.room_num:
                return None
        return None

    def gateway_slot_above_room(room_num):
        return 2 + 2*room_num

    def fill_slot(self, i, amphipod):
        assert self.slots[i] is None
        self.slots[i] = amphipod

    def empty_slot(self, i):
        assert self.slots[i] is not None
        self.slots[i] = None

################################################################################
class Game:
    def __init__(self, amphipods: Amphipod, rooms: List[Room]):
        self.amphipods = amphipods
        self.rooms = rooms
        self.gateway = [None]*GATEWAY_SLOTS # each slot either contains an Amphipod or is None (empty).
        self.energy_used = 0
        self.remaining_amphipods = 0
        self.cache = {}
        for amphipod in self.amphipods:
            if amphipod.is_done == False:
                self.remaining_amphipods += 1

    def is_finished(self):
        return self.remaining_amphipods == 0

    # checks if move is possible and return number of steps if possible.
    def is_possible_move_and_steps(self, move: Tuple[Amphipod, Position, Position]) -> Tuple[int, bool]:
        amphipod, source, target = move
        if amphipod.is_done:
            return -1, False
        num_steps = 0
        # check no obstacle in up.
        gateway_start_slot = -1
        if source['location'] == LOCATION_ROOM:
            curr_room_num, curr_room_slot = source['coords']
            for slot_idx in range(curr_room_slot+1, ROOM_SLOTS):
                if self.rooms[curr_room_num].slots[slot_idx] is not None:
                    return -1, False
            gateway_start_slot = Room.gateway_slot_above_room(curr_room_num)
            if self.gateway[gateway_start_slot] is not None:
                return -1, False
            num_steps += ROOM_SLOTS - curr_room_slot
        else:
            gateway_start_slot = source['coords'][1]
        # check no obstacle down.
        gateway_end_slot = -1
        if target['location'] == LOCATION_ROOM:
            end_room_num, end_room_slot = target['coords']
            gateway_end_slot = Room.gateway_slot_above_room(end_room_num)
            for slot_idx in range(ROOM_SLOTS-1, end_room_slot-1, -1):
                if self.rooms[end_room_num].slots[slot_idx] is not None:
                    return -1, False
            num_steps += ROOM_SLOTS - end_room_slot
        else:
            gateway_end_slot = target['coords'][1]
        # check no obstacle horizontal.
        if gateway_start_slot < gateway_end_slot:
            for idx in range(gateway_start_slot+1, gateway_end_slot+1):
                if self.gateway[idx] is not None:
                    return -1, False
                num_steps += 1
        elif gateway_start_slot > gateway_end_slot:
            for idx in range(gateway_start_slot-1, gateway_end_slot-1, -1):
                if self.gateway[idx] is not None:
                    return -1, False
                num_steps += 1
        return num_steps, True
    
    def possible_moves(self) -> List[Tuple[Tuple[Amphipod, Position, Position], int]]:
        moves = []
        for amphipod in self.amphipods:
            if not amphipod.is_done:
                # check if can move to it's room.
                guess_slot = self.rooms[amphipod.type_num].lowest_empty_slot()
                if guess_slot is not None:
                    to_position = {
                        'location': LOCATION_ROOM,
                        'coords': (amphipod.type_num, guess_slot),
                    }
                    move = (amphipod, amphipod.position, to_position)
                    steps, possible = self.is_possible_move_and_steps(move)
                    if possible:
                        # moves.append((move, steps))
                        # continue
                        # print(move)
                        return [(move, steps)]
                # otherwise can only move to some place in Gateway.
                if amphipod.position['location'] == LOCATION_ROOM:
                    for i in range(GATEWAY_SLOTS):
                        if self.gateway[i] is None:
                            to_position = {
                                'location': LOCATION_GATEWAY,
                                'coords': (-1, i),
                            }
                            move = (amphipod, amphipod.position, to_position)
                            steps, possible = self.is_possible_move_and_steps(move)
                            if possible:
                                moves.append((move, steps))
        return moves

    def make_move(self, move: Tuple[Amphipod, Position, Position], steps: int):
        amphipod, from_pos, to_pos = move
        self.energy_used += amphipod.make_move((from_pos, to_pos), steps)
        # make changes for from_pos.
        if from_pos['location'] == LOCATION_ROOM:
            room_num, room_slot = from_pos['coords']
            self.rooms[room_num].empty_slot(room_slot)
        else:
            gateway_slot = from_pos['coords'][1]
            self.gateway[gateway_slot] = None
        # make changes for to_pos.
        if to_pos['location'] == LOCATION_ROOM:
            room_num, room_slot = to_pos['coords']
            self.rooms[room_num].fill_slot(room_slot, amphipod)
            amphipod.is_done = True
            self.remaining_amphipods -= 1
        else:
            gateway_slot = to_pos['coords'][1]
            self.gateway[gateway_slot] = amphipod

    def undo_move(self, move: Tuple[Amphipod, Position, Position], steps: int):
        amphipod, from_pos, to_pos = move
        self.energy_used -= amphipod.undo_move((from_pos, to_pos), steps)
        # make changes for from_pos.
        if from_pos['location'] == LOCATION_ROOM:
            room_num, room_slot = from_pos['coords']
            self.rooms[room_num].fill_slot(room_slot, amphipod)
        else:
            gateway_slot = from_pos['coords'][1]
            self.gateway[gateway_slot] = amphipod
        # make changes for to_pos.
        if to_pos['location'] == LOCATION_ROOM:
            room_num, room_slot = to_pos['coords']
            assert room_num == amphipod.type_num
            self.rooms[room_num].empty_slot(room_slot)
            amphipod.is_done = False
            self.remaining_amphipods += 1
        else:
            gateway_slot = to_pos['coords'][1]
            self.gateway[gateway_slot] = None

    def state(self):
        s = ['\n', '#']
        for gateway_idx in range(GATEWAY_SLOTS):
            if self.gateway[gateway_idx] is None:
                s.append('.')
            else:
                s.append(str(self.gateway[gateway_idx].type_num))
        s.append("#")
        for slot_idx in range(ROOM_SLOTS-1, -1, -1):
            s.append("\n")
            s.append("#"); s.append("#"); s.append("#")
            for room_idx in range(ROOMS_NUM):
                if self.rooms[room_idx].slots[slot_idx] is None:
                    s.append('.')
                else:
                    s.append(str(self.rooms[room_idx].slots[slot_idx].type_num))
                s.append('#')
            s.append("#"); s.append("#")
        return ''.join(s)

    # override the comparison operator
    def __lt__(self, nxt) -> bool:
        return self.energy_used < nxt.energy_used

    def find_solution(self, upper_bound_energy=INFINITY) -> Tuple[int, bool]:
        pass
        ################################
        # global RECURSION_LEVEL
        # if RECURSION_LEVEL % 40 == 0:
        #     print(RECURSION_LEVEL, end=',')
        # RECURSION_LEVEL += 1
        # if RECURSION_LEVEL % 1000 == 0:
        #     print()
        ################################
        # if upper_bound_energy < 0:      return -1, False
        # if self.is_finished():          return  0, True
        # curr_state = self.state()
        # if curr_state in self.cache:
        #     if self.cache[curr_state][0] <= upper_bound_energy:
        #         return self.cache[curr_state]
        #     else:
        #         return -1, False
        # # print("reached")
        # # try more moves.
        # possible_moves = self.possible_moves()
        # if len(possible_moves) == 0:    return -1, False
        # status = False
        # for move, steps in possible_moves:
        #     # print(curr_state, move[0], move[1], move[2], steps)
        #     # print()
        #     self.make_move(move, steps)
        #     curr_res, curr_status = self.find_solution(upper_bound_energy-energy)
        #     status = status or curr_status
        #     if (curr_status == True):
        #         upper_bound_energy = curr_res + energy
        #     self.undo_move(move, steps)
        # if status:
        #     self.cache[curr_state] = upper_bound_energy, status
        # return upper_bound_energy, status

################################################################################
# Djikstra's algorithm
def djikstra(start_game: Game) -> int:
    heap = []
    heapq.heappush(heap, start_game)
    visited = {}
    while len(heap) > 0:
        curr_game = heapq.heappop(heap)
        if curr_game.is_finished():
            return curr_game.energy_used
        visited[curr_game.state()] = True
        # try more moves.
        possible_moves = curr_game.possible_moves()
        if len(possible_moves) == 0:
            continue
        for move, steps in possible_moves:
            new_game = copy.deepcopy(curr_game)
            print(curr_game.state())
            new_game.make_move(move, steps)
            print(curr_game.state())
            print(new_game.state())
            if new_game.state() in visited:
                continue
            heapq.heappush(heap, new_game)
    return None

################################################################################
# Parse starting positions and create Game.
amphipods = []
rooms_with_amphipods = [Room(i) for i in range(ROOMS_NUM)]
for room_num in range(ROOMS_NUM):
    for slot_num in range(ROOM_SLOTS):
        type_char = START_ROOMS[room_num][slot_num]
        curr_amphipod = Amphipod(
            type_char, 
            position={
                'location': LOCATION_ROOM,
                'coords': (room_num, slot_num),
            },
            is_done=False
        )
        # check if these amphipod is already in right place.
        is_done = (curr_amphipod.type_num == room_num)
        if slot_num != 0:
            is_done = is_done and rooms_with_amphipods[room_num].slots[slot_num-1].is_done
        curr_amphipod.is_done = is_done
        # add amphipod to room and array.
        rooms_with_amphipods[room_num].fill_slot(slot_num, curr_amphipod)
        amphipods.append(curr_amphipod)

start_game = Game(amphipods, rooms_with_amphipods)
res = djikstra(start_game)
print(res)
# print(game.state())
# res, status = game.find_solution()
# if status == True:
#     print(f"\tTotal energy used: {res}")
# else:
#     print("\tOops!!! No solution found")
# print(game.cache["\n#...1.......#\n###1#2#.#3###\n###0#3#2#0###"])
