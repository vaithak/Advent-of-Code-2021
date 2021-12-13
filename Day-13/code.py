def process_fold(coords, fold_dir, magnitude):
    new_coords = {}
    for coord in coords.keys():
        if fold_dir == 'x':
            if coord[0] < magnitude:
                new_coords[coord] = True
            else:
                new_coords[(2*magnitude-coord[0], coord[1])] = True
        else:
            if coord[1] < magnitude:
                new_coords[coord] = True
            else:
                new_coords[(coord[0], 2*magnitude-coord[1])] = True
    return new_coords

def plot_coords(coords):
    xs = [coord[0] for coord in coords.keys()]
    ys = [coord[1] for coord in coords.keys()]
    x_min, x_max, y_min, y_max = min(xs), max(xs), min(ys), max(ys)
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            if (x,y) in coords:
                print('#', end='')
            else:
                print('.', end='')
        print()

coords = {}
with open("input.txt") as f:
    # read coordinates.
    for line in f:
        if line == "\n":
            break
        x, y = line.strip().split(',')
        coords[(int(x), int(y))] = True
    # read folds.
    i = 1
    for line in f:
        axis = line.strip().split(' ')[-1]
        dir = axis[0]
        mag = axis[2:]
        coords = process_fold(coords, dir, int(mag))
        print(f"\tafter fold {i}: {len(coords)} are visible.")
        i += 1
plot_coords(coords)
