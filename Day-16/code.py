LITERAL_PACKET = 4

hex_binary_map = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110",
    "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011", "C": "1100", "D": "1101",
    "E": "1110", "F": "1111",
}

def hex_to_bit_str(hex_str):
    res = []
    for char in hex_str:
        res.append(hex_binary_map[char])
    return ''.join(res)

class Packet:
    def __init__(self, type, version, value=0):
        self.sub_packets = []
        self.version = version
        self.type = type
        self.value = value

    def __str__(self):
        return f"Type: {self.type}, Version: {self.version}, Value: {self.value}, Subpackets: {self.sub_packets}"

    def add_subpacket(self, sub_packet):
        self.sub_packets.append(sub_packet)
    
    def assign_value(self, value):
        self.value = value

    def version_sum(self):
        res = self.version
        for subpacket in self.sub_packets:
            res += subpacket.version_sum()
        return res

    def compute_value(self):
        if self.type == 0:
            for subpacket in self.sub_packets:
                self.value += subpacket.value
        elif self.type == 1:
            self.value = 1
            for subpacket in self.sub_packets:
                self.value *= subpacket.value
        elif self.type == 2:
            self.value = min([subpacket.value for subpacket in self.sub_packets])
        elif self.type == 3:
            self.value = max([subpacket.value for subpacket in self.sub_packets])
        elif self.type == 5:
            if self.sub_packets[0].value > self.sub_packets[1].value:
                self.value = 1
        elif self.type == 6:
            if self.sub_packets[0].value < self.sub_packets[1].value:
                self.value = 1
        elif self.type == 7:
            if self.sub_packets[0].value == self.sub_packets[1].value:
                self.value = 1

def read_operator_packet(binary_str, start=0):
    # read first three chars for version.
    version = int(binary_str[start:start+3], 2)
    type = int(binary_str[start+3:start+6], 2)
    assert(type != LITERAL_PACKET)
    packet = Packet(type, version)
    # read more metadata.
    I = int(binary_str[start+6], 2)
    if I == 0:  L_bits = 15
    else:       L_bits = 11
    L = int(binary_str[start+7:start+7+L_bits], 2)
    # read sub packets.
    curr_start = start+7+L_bits
    end = start+7+L_bits+L
    counter = 0
    while (L_bits == 15 and curr_start < end) or (L_bits == 11  and counter < L):
        sub_type = int(binary_str[curr_start+3:curr_start+6], 2)
        if sub_type == LITERAL_PACKET:  sub_packet, sub_end = read_literal_packet(binary_str, curr_start)
        else:                           sub_packet, sub_end = read_operator_packet(binary_str, curr_start)
        packet.add_subpacket(sub_packet)
        curr_start = sub_end
        counter += 1

    packet.compute_value()
    return packet, curr_start


def read_literal_packet(binary_str, start=0):    
    # read first three chars for version.
    version = int(binary_str[start:start+3], 2)
    type = int(binary_str[start+3:start+6], 2)
    assert(type == LITERAL_PACKET)
    packet = Packet(type, version, 0)
    # read bits in groups of 5.
    literal_str = []
    continue_flag = True
    curr_idx = start+6
    while continue_flag:
        curr_str = binary_str[curr_idx:curr_idx+5]
        if curr_str[0] == '0':
            continue_flag = False
        literal_str.append(curr_str[1:])
        curr_idx += 5

    packet.assign_value(int(''.join(literal_str), 2))
    return packet, curr_idx

def main():
    input_hex_str = ""
    with open('input.txt') as f:
        input_hex_str = f.readline().strip()
    input_bin_str = hex_to_bit_str(input_hex_str)

    # Assuming that root packet is an operator.
    root_packet, _ = read_operator_packet(input_bin_str)
    print("Version sum: ", root_packet.version_sum())
    print("Final value: ", root_packet.value)

if __name__ == "__main__":
    main()
