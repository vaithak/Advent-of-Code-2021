def process_step(pairs_count, pairs_produce_map):
    updated_dict = {}
    for pair in pairs_count:
        if pair in pairs_produce_map:
            left_pair = pair[0]+pairs_produce_map[pair]
            right_pair = pairs_produce_map[pair]+pair[1]
            updated_dict[left_pair] = updated_dict.get(left_pair, 0) + pairs_count[pair]
            updated_dict[right_pair] = updated_dict.get(right_pair, 0) + pairs_count[pair]
    return updated_dict

# assumes length > 2.
def find_character_frequency(pairs_count):
    freq_map = {}
    for pair in pairs_count:
        freq_map[pair[0]] = freq_map.get(pair[0], 0) + pairs_count[pair]
        freq_map[pair[1]] = freq_map.get(pair[1], 0) + pairs_count[pair]
    for char in freq_map:
        freq_map[char] = (freq_map[char]+1)//2
    return freq_map

def F(steps):
    pairs_produce_map = {}
    pairs_count = {}    # map from pair of characters to their frequency count in template.
    template = ""
    with open("input.txt") as f:
        # read template.
        template = f.readline().strip()
        f.readline() # empty line.
        # read pairs.
        for line in f:
            pair, res = line.split("->")
            pairs_produce_map[pair.strip()] = res.strip()
    # execute steps.
    for i in range(0, len(template)-1):
        curr_pair = template[i:i+2]
        pairs_count[curr_pair] = pairs_count.get(curr_pair, 0) + 1
    for i in range(1, steps+1):
        pairs_count = process_step(pairs_count, pairs_produce_map)
        char_freq = find_character_frequency(pairs_count)
        length, min_freq, max_freq = sum(char_freq.values()), min(char_freq.values()), max(char_freq.values())
        if i%10 == 0:
            print(f"\tStep {i}: length = {length}, most_common-least_common={max_freq - min_freq}")


print("Part 1:")
F(10)

print("Part 2:")
F(40)
