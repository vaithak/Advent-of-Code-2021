import copy
import heapq
from typing import Dict, Any, Tuple, List

Position = Tuple[int, int]

RECURSION_LEVEL = 0
INFINITY = 1e5
ROOMS_NUM = 4
GATEWAY_SLOTS = 3 + 2*ROOMS_NUM
# ROOM_SLOTS = 2
ROOM_SLOTS = 4

LOCATION_GATEWAY = 0

# starting config of each room. Each room is filled from bottom to top.
# START_ROOMS = [['C', 'D'], ['C', 'B'], ['A', 'D'], ['B', 'A']]
START_ROOMS = [['C', 'D', 'D', 'D'], ['C', 'B', 'C', 'B'], ['A', 'A', 'B', 'D'], ['B', 'C', 'A', 'A']]
START_ROOMS = [['A', 'D', 'D', 'B'], ['D', 'B', 'C', 'C'], ['C', 'A', 'B', 'B'], ['A', 'C', 'A', 'D']]
# START_ROOMS = [['A', 'B'], ['D', 'C'], ['C', 'B'], ['A', 'D']]
# START_ROOMS = [['A', 'B'], ['B', 'A'], ['C', 'C']]

type_char_energy_map = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

def type_char_to_num(ch):
    return ord(ch) - ord('A')

def gateway_slot_above_room(room_num):
    return 2 + 2*room_num

################################################################################
class Game:
    def __init__(self, area_map):
        # self.amphipods = amphipods
        assert len(area_map) == ROOMS_NUM+1
        self.area_map = area_map    # area_map contains Gateway as the first list and rooms from index = 1.
        self.energy_used = 0

    def __str__(self):
        s = ['\n', '#']
        s.append(''.join(self.area_map[LOCATION_GATEWAY]))
        s.append('#\n')
        for slot_idx in range(ROOM_SLOTS-1, -1, -1):
            if slot_idx == ROOM_SLOTS-1:
                s.append("###")
            else:
                s.append("  #")
            for location in range(1, ROOMS_NUM+1):
                s.append(self.area_map[location][slot_idx])
                s.append("#")
            if slot_idx == ROOM_SLOTS-1:
                s.append("##")
            s.append("\n")
        s.append("  " + '#'*(2*ROOMS_NUM+1))
        return ''.join(s)


    def get_amphipods(self) -> List[Tuple[int, int]]:
        amphipods = []
        for i in range(ROOMS_NUM+1):
            for j in range(len(self.area_map[i])):
                if self.area_map[i][j] != '.':
                    amphipods.append((i, j))
        return amphipods

    def lowest_empty_slot(self, room_num):
        room = self.area_map[room_num+1]
        for i in range(ROOM_SLOTS):
            if room[i] == '.':
                return i
            elif type_char_to_num(room[i]) != room_num:
                return None
        return None

    def is_finished(self) -> bool:
        for room_num in range(1, ROOMS_NUM+1):
            for slot_idx in range(ROOM_SLOTS):
                if type_char_to_num(self.area_map[room_num][slot_idx]) != (room_num-1):
                    return False
        return True

    def is_done(self, amphipod: Tuple[int, int]) -> bool:
        room_num, idx = amphipod
        if room_num == LOCATION_GATEWAY:
            return False
        if type_char_to_num(self.area_map[room_num][idx]) != (room_num-1):
            return False
        for i in range(idx):
            if type_char_to_num(self.area_map[room_num][i]) != (room_num-1):
                return False
        return True

    # checks if move is possible and return number of steps if possible.
    def is_possible_move_and_steps(self, move: Tuple[Position, Position]) -> Tuple[int, bool]:
        source, target = move
        num_steps = 0
        # check no obstacle in up.
        gateway_start_slot = -1
        if source[0] != LOCATION_GATEWAY:   # means a room.
            curr_location, curr_room_slot = source
            curr_room_num = curr_location-1
            for slot_idx in range(curr_room_slot+1, ROOM_SLOTS):
                if self.area_map[curr_location][slot_idx] != '.':
                    return -1, False
            gateway_start_slot = gateway_slot_above_room(curr_room_num)
            if self.area_map[LOCATION_GATEWAY][gateway_start_slot] != '.':
                return -1, False
            num_steps += ROOM_SLOTS - curr_room_slot
        else:
            gateway_start_slot = source[1]
        # check no obstacle down.
        gateway_end_slot = -1
        if target[0] != LOCATION_GATEWAY:
            end_location, end_room_slot = target
            end_room_num = end_location-1
            gateway_end_slot = gateway_slot_above_room(end_room_num)
            for slot_idx in range(ROOM_SLOTS-1, end_room_slot-1, -1):
                if self.area_map[end_location][slot_idx] != '.':
                    return -1, False
            num_steps += ROOM_SLOTS - end_room_slot
        else:
            gateway_end_slot = target[1]
        # check no obstacle horizontal.
        if gateway_start_slot < gateway_end_slot:
            for idx in range(gateway_start_slot+1, gateway_end_slot+1):
                if self.area_map[LOCATION_GATEWAY][idx] != '.':
                    return -1, False
                num_steps += 1
        elif gateway_start_slot > gateway_end_slot:
            for idx in range(gateway_start_slot-1, gateway_end_slot-1, -1):
                if self.area_map[LOCATION_GATEWAY][idx] != '.':
                    return -1, False
                num_steps += 1
        return num_steps, True
    
    def possible_moves(self) -> List[Tuple[Tuple[Position, Position], int]]:
        moves = []
        for amphipod_pos in self.get_amphipods():
            if not self.is_done(amphipod_pos):
                location, idx = amphipod_pos
                target_room_num = type_char_to_num(self.area_map[location][idx])
                # check if can move to it's room.
                guess_slot = self.lowest_empty_slot(target_room_num)
                if guess_slot is not None:
                    to_position = (target_room_num+1, guess_slot)
                    move = (amphipod_pos, to_position)
                    steps, possible = self.is_possible_move_and_steps(move)
                    if possible:
                        return [(move, steps)]
                # otherwise can only move to some place in Gateway.
                if location != LOCATION_GATEWAY:
                    for i in range(GATEWAY_SLOTS):
                        if self.area_map[LOCATION_GATEWAY][i] == '.':
                            to_position = (LOCATION_GATEWAY, i)
                            move = (amphipod_pos, to_position)
                            steps, possible = self.is_possible_move_and_steps(move)
                            if possible:
                                moves.append((move, steps))
        return moves

    def make_move(self, move: Tuple[Position, Position], steps: int):
        from_pos, to_pos = move
        to_location, to_idx = to_pos
        from_location, from_idx = from_pos
        amphipod_char = self.area_map[from_location][from_idx]
        self.energy_used += type_char_energy_map[amphipod_char]*steps
        # make changes for to_pos.
        self.area_map[to_location][to_idx] = amphipod_char
        # make changes for from_pos.
        self.area_map[from_location][from_idx] = '.'

    def state(self):
        return ''.join([''.join(x) for x in self.area_map])

    # override the comparison operator
    def __lt__(self, nxt) -> bool:
        return self.energy_used < nxt.energy_used

################################################################################
# Djikstra's algorithm
def djikstra(start_game: Game) -> int:
    heap = []
    heapq.heappush(heap, start_game)
    visited = {}
    values = {}
    while len(heap) > 0:
        curr_game = heapq.heappop(heap)
        curr_state = curr_game.state()
        if curr_state in visited:
            continue
        visited[curr_state] = True
        if curr_game.is_finished():
            return curr_game.energy_used
        # try more moves.
        possible_moves = curr_game.possible_moves()
        if len(possible_moves) == 0:
            continue
        for move, steps in possible_moves:
            new_game = copy.deepcopy(curr_game)
            new_game.make_move(move, steps)
            new_state = new_game.state()
            if (new_state not in values) or (values[new_state] > new_game.energy_used):
                values[new_state] = new_game.energy_used
                heapq.heappush(heap, new_game)
    return None

################################################################################
# Parse starting positions and create Game.
area_map = [['.']*GATEWAY_SLOTS]
area_map.extend(START_ROOMS)
start_game = Game(area_map)
print(start_game)
# print(start_game.possible_moves())
res = djikstra(start_game)
print(res)
