DEBUG = False

orientations = [
    [1, 2, 3], [1, -2, -3], [-1, 2, -3], [-1, -2, 3],
    [1, 3, -2], [1, -3, 2], [-1, 3, 2], [-1, -3, -2],
    [2, 1, -3], [2, -1, 3], [-2, 1, 3], [-2, -1, -3],
    [2, 3, 1], [2, -3, -1], [-2, 3, -1], [-2, -3, 1],
    [3, 1, 2], [3, -1, -2], [-3, 1, -2], [-3, -1, 2],
    [3, 2, -1], [3, -2, 1], [-3, 2, 1], [-3, -2, -1],
]

def sign(x):
    return 1 if x>=0 else -1

def manhattan_dist(tup1, tup2):
    return abs(tup1[0]-tup2[0]) + abs(tup1[1]-tup2[1]) + abs(tup1[2]-tup2[2])

def calculate_translation(beacon_1, beacon_2, orientation):
    beacon_1_list = list(beacon_1)
    beacon_2_list = list(beacon_2)
    for i in range(3):
        beacon_2_list[i] = beacon_2[abs(orientation[i])-1]*sign(orientation[i])
    return (beacon_1_list[0]-beacon_2_list[0], beacon_1_list[1]-beacon_2_list[1], beacon_1_list[2]-beacon_2_list[2])

class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
    
    def __len__(self):
        return len(self.beacons)

    def __str__(self):
        return '\n\t'.join([str(s) for s in self.beacons])

    def merge_beacons(self, other_scanner):
        for beacon in other_scanner.beacons:
            self.beacons.add(beacon)

    def find_translation_if_overlap(self, other_scanner, orientation):
        translation_freq_map = {}
        for beacon_self in self.beacons:
            for beacon_other in other_scanner.beacons:
                curr_translation = calculate_translation(beacon_self, beacon_other, orientation)
                translation_freq_map[curr_translation] = translation_freq_map.get(curr_translation, 0) + 1
                if translation_freq_map[curr_translation] >= 12:
                    return curr_translation, True
        return None, False

    """ 
    returns (orientation, translation), True tuple if the two scanners have >= 12 overlapping beacons.
    else returns (None, None), False.
    """
    def find_overlap_beacons(scanner1, scanner2):
        for orientation in orientations:
            translation, is_overlap = scanner1.find_translation_if_overlap(scanner2, orientation)
            if is_overlap:
                return orientation, translation, True
        return None, None, False

    def tranform_beacons(self, orientation, translation):
        updated_beacons = set()
        for beacon in self.beacons:
            transformed_beacon = [None]*3
            for i in range(3):
                transformed_beacon[i] = beacon[abs(orientation[i])-1]*sign(orientation[i])
                transformed_beacon[i] += translation[i]
            updated_beacons.add(tuple(transformed_beacon))
        self.beacons = updated_beacons

    def combine(self, other_scanner):
        orientation, translation, success = Scanner.find_overlap_beacons(self, other_scanner)
        if not success:
            return None, False
        print(f"Combining using translation: {translation}, orientation: {orientation}")
        other_scanner.tranform_beacons(orientation, translation)
        self.merge_beacons(other_scanner)
        return translation, True

def read_scanner(file):
    line = file.readline()
    if not line.startswith("---"):
        return None, False
    beacons = set()
    for line in file:
        line = line.strip()
        if len(line) == 0:
            break
        beacon = tuple([int(x) for x in line.split(',')])
        beacons.add(beacon)
    return Scanner(beacons), True

def main():
    scanners_list = []
    scanners_tranlation = [(0,0,0)]

    with open("input.txt") as f:
        continue_flag = True
        while continue_flag:
            curr_scanner, continue_flag = read_scanner(f)
            if not continue_flag:
                break
            scanners_list.append(curr_scanner)
    bool_done = [False]*len(scanners_list)

    for i in range(len(scanners_list)-1):
        for i in range(1, len(scanners_list)):
            if not bool_done[i]:
                translation, success = scanners_list[0].combine(scanners_list[i])
                if success:
                    bool_done[i] = True
                    scanners_tranlation.append(translation)
                    print(f"combined scanner 0 and scanner {i}\n")
    if DEBUG:
        print("Final beacons list: \n\t", scanners_list[0], sep='')
    print("Number of beacons: ", len(scanners_list[0]))

    ################################ Part 2: ##############################
    best_dist, best_pair = -1, (-1, -1)
    for i in range(len(scanners_tranlation)):
        for j in range(i+1, len(scanners_tranlation)):
            curr_dist = manhattan_dist(scanners_tranlation[i], scanners_tranlation[j])
            if curr_dist > best_dist:
                best_dist = curr_dist
                best_pair = (i, j)
    print(f"Farthest scanners are {best_pair} with distance {best_dist}")

if __name__ == "__main__":
    main()
