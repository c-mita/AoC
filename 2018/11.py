def cell_power(x, y, s_value):
    r = x + 10
    p = r * y + s_value
    p *= r
    v = (p // 100) % 10
    return v - 5

s_value = 9110
#s_value = 18

grid_power = {(x, y):cell_power(x, y, s_value) for x in range(1, 301) for y in range(1, 301)}

subgrids = [(x, y) for x in range(1, 298) for y in range(1, 298)]

best_grid = max(subgrids, key=lambda x0y0: sum(grid_power[(x, y)] for x in range(x0y0[0], x0y0[0]+3) for y in range(x0y0[1], x0y0[1]+3)))
print(best_grid)


integral_grid = {}
for x in range(1, 301):
    for y in range(1, 301):
        v = grid_power[(x, y)]
        integral_grid[(x, y)] = v + integral_grid.get((x, y-1), 0) + integral_grid.get((x-1, y), 0) - integral_grid.get((x-1, y-1), 0)

#print integral_grid[(32, 44)] - integral_grid[(32+3, 44)] - integral_grid[(32, 44+3)] + integral_grid[(32+3, 44+3)]
#print integral_grid[(1, 1)]

best_score = 0
best_grid = None
for n in range(1, 300):
    for x in range(1, 301-n):
        for y in range(1, 301-n):
            score = integral_grid.get((x-1, y-1), 0) - integral_grid.get((x-1+n, y-1), 0) - integral_grid.get((x-1, y-1+n), 0) + integral_grid.get((x-1+n, y-1+n), 0)
            if best_score < score:
                best_score = score
                best_grid = (x, y, n)
print(best_score)
print(best_grid)
