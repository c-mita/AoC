def parse_input(filename):
    points = []
    folds = []
    with open(filename) as f:
        for l in f:
            line = l.strip()
            if "fold" in line:
                axis, value = line[len("fold along "):].split("=")
                folds.append((axis, int(value)))
            elif line:
                points.append(tuple(map(int, line.split(","))))
    return points, folds


def perform_fold(points, fold):
    folded_points = set()
    axis, fold_line = fold
    for x, y in points:
        if axis == "x" and x > fold_line:
            dx = x - fold_line
            folded_points.add((fold_line - dx, y))
        elif axis == "y" and y > fold_line:
            dy = y - fold_line
            folded_points.add((x, fold_line - dy))
        else:
            folded_points.add((x, y))
    return folded_points


def points_to_string(points):
    max_x, max_y = 0, 0
    for (x, y) in points:
        if x > max_x: max_x = x
        if y > max_y: max_y = y
    point_array = [[" " for x in range(max_x + 1)] for y in range(max_y + 1)]
    for (x, y) in points:
        point_array[y][x] = "#"
    return "\n".join("".join(point_line) for point_line in point_array)


points, folds = parse_input("13_input.txt")
folded = perform_fold(points, folds[0])

point_set = {p for p in points}
for fold in folds:
    point_set = perform_fold(point_set, fold)

point_set_string = points_to_string(point_set)
print(point_set_string)
