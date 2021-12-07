def parse_file(filename):
    with open(filename) as f:
        return map(int, f.readlines()[0].strip().split(","))

points = parse_file("07_input.txt")

test_points = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]

"""
"sum(abs(xi - d)) for xi" is mimized when d is the median of all xi when there are an odd number of xi.
If there an even number of xi, it is mimized by value between the two "middle" xi
"""

points = sorted(points)
median = points[len(points) / 2]
total_distance = sum(abs(p - median) for p in points)
print(total_distance)


"""
Find d by minimizing:
sum(abs(xi - d) * (abs(xi - d) + 1))
==
sum((xi - d)**2 + abs(xi - d))

define d/dx(abs(x - d)) == sign(x - d) == 0 when x == d

(x - d)**2 + abs(x - d)
derivative wrt d
2(d - x) + sign(x - d)
2(d - x) + sign(x - d) == 0 when x - d == 0, x - d == 0.5, x -d == -0.5


Putting this into our sum:
0 = sum(2(d - xi)) + sum(sign(xi - d))
0 = 2 * sum(d - xi) + sum(sign(xi-d))

sum(xi) = 2 * sum(d) + sum(sign(xi - d))
sum(d) == n * d (n number of xi)

sum(xi) = n * d + sum(sign(xi - d))

d * n = sum(xi) - sum(sign(xi - d)

sum(sign(xi - d)) is bounded by +/-n

sum(xi) - n <= d * n <= sum(xi) + n

sum(xi)/n - 1 <= d <= sum(xi)/n + 1

Therefore: d == mean(x) +/- 1

Might be able reduce the checks for d by not looking in the direction _away_ from the median.
This is because sum(sign(xi-d)) is mimized when d is a median of all xi.

(Note we've ignored a division by 2, otherwise it would be +/- 0.5)
"""
mean = sum(points) / len(points)
centre = min([mean-1, mean, mean+1], key=lambda d: sum(abs(p - d) * (abs(p - d) + 1) for p in points))

total_distance = sum(int(0.5 * abs(p - centre) * (abs(p - centre) + 1)) for p in points)
print total_distance
