ON, OFF = 1, 0
OP_MAP= {
	'on': ON,
	'off': OFF
}

def intersect_line(a, b):
	a1, a2 = a
	b1, b2 = b
	p1, p2 = 0, 0
	if (a2 < b1) or (a1 > b2):
		return None
	p1, p2 = max(a1, b1), min(a2, b2)
	return (p1, p2)
	
def form_ndcube(d_pairs):
	origin = [d_pair[0] for d_pair in d_pairs]
	lengths = [d_pair[1]-d_pair[0]+1 for d_pair in d_pairs]
	return NdCube(origin, lengths)
	
def parse_line(s):
	switch, coords = s.split(' ')
	if switch == 'on':  switch = ON
	else:               switch = OFF
	x_coords, y_coords, z_coords= coords.split(',')
	x_range = [int(x) for x in x_coords.split('=')[1].split('..')]
	y_range = [int(y) for y in y_coords.split('=')[1].split('..')]
	z_range = [int(z) for z in z_coords.split('=')[1].split('..')]
	return switch, form_ndcube([x_range, y_range, z_range])

# given a d*m number of lines for each dimension d.
# Required for this: https://pryp.in/blog/15/intersection-and-difference-of-two-rectangles.html
def form_line_pair_tuples(lines, curr_d, curr_pair_list, res):
	if curr_d == len(lines):
		res.append(curr_pair_list.copy())
		return
	for i in range(len(lines[curr_d])-1):
		curr_d_pair = (lines[curr_d][i], lines[curr_d][i+1]-1)
		curr_pair_list[curr_d] = curr_d_pair
		form_line_pair_tuples(lines, curr_d+1, curr_pair_list, res)

class NdCube:
	def __init__(self, origin, lengths):
		self.origin = origin
		self.lengths = lengths
		self.dim = len(origin)

	def __str__(self):
		return f"x={self.origin[0]}..{self.origin[0]+self.lengths[0]-1},y={self.origin[1]}..{self.origin[1]+self.lengths[1]-1},z={self.origin[2]}..{self.origin[2]+self.lengths[2]-1}"
	
	def __eq__(self, B):
		return self.origin == B.origin and self.lengths == B.lengths
		
	def volume(self):
		res = 1
		for len in self.lengths:
			res *= len
		return res
		
	def intersection(self, B):
		# iteratively intersect in each dimension.
		res_origin, res_lengths = [], []
		for d in range(self.dim):
			curr_int = intersect_line((self.origin[d], self.origin[d]+self.lengths[d]-1), (B.origin[d], B.origin[d]+B.lengths[d]-1))
			if curr_int is None:
				return None
			res_origin.append(curr_int[0])
			res_lengths.append(curr_int[1] - curr_int[0]+1)
		return NdCube(res_origin, res_lengths)
		
	def minus(self, B):
		intersect = self.intersection(B)
		if intersect is None:
			return [self]
		if self == intersect:
			return []
		# get all interesting lines in each dimension.
		lines = []
		for d in range(self.dim):
			d_lines = [self.origin[d]]
			if intersect.origin[d] != self.origin[d]:
				d_lines.append(intersect.origin[d])
			if intersect.origin[d]+intersect.lengths[d] != self.origin[d]+self.lengths[d]:
				d_lines.append(intersect.origin[d]+intersect.lengths[d])
			d_lines.append(self.origin[d]+self.lengths[d])
			lines.append(d_lines)
		# form ndcubes from the interesting lines.
		res = []
		line_pair_tuples = []
		form_line_pair_tuples(lines, curr_d=0, curr_pair_list=[None]*self.dim, res=line_pair_tuples)
		for line_pair_tuple in line_pair_tuples:
			curr_cube = form_ndcube(line_pair_tuple)
			if curr_cube != intersect:
				res.append(curr_cube)
		return res

def main():
	res_ndcubes = []
	# compute final result of nd cubes.
	with open("input.txt") as f:
		for line in f:
			inp_operation = parse_line(line.strip())
			op, inp_ndcube = inp_operation
			new_res_ndcubes = []
			for ndcube in res_ndcubes:
				new_ndcubes = ndcube.minus(inp_ndcube)
				new_res_ndcubes.extend(new_ndcubes)
			if op == ON:
				new_res_ndcubes.append(inp_ndcube)
			res_ndcubes = new_res_ndcubes
	# calculate total volume.
	res_volume = 0
	for nd_cube in res_ndcubes:
		res_volume += nd_cube.volume()
	print(f"\ttotal volume covered: {res_volume}")

if __name__ == "__main__":
	main()
