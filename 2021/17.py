"""
For Part 1:

Our project`ile's y velocity changes by -1 every frame.

Symmetry dictates that, for any y_vel > 0, the projectile will eventually pass
through y = 0 again and will have velocity (-y_vel - 1) when it does so.

Since the maximum height of the projectile correlates with the speed at this
time, we want the maximum speed possible that will cause our projectile to
still intersect the allowed y range in the very next time step.
Which means -y_vel - 1 == min(y_range)

Given a velocity, we know the maximum height via (n * (n + 1)) / 2
where n is the initial velocity.

So set -n to the minimum of the y range + 1.


For Part 2:
There may be a clever way of reducing this space, or even closed form solutions.
Or we could just start at the maximum allowed y and x velocities and simulate options
from there.
The maximum x_vel is simply max(x).
The minimum x_vel is the solution to (n*(n+1) / 2) == min(x)

Also, the projectile can be fired downwards, so we must consider negative y values.
In this case, the minimum y_val is simple min(y)
"""


TEST_BOUNDS = [20, 30], [-10, -5]
INPUT_BOUNDS = [236, 262], [-78, -58]

def projectile_hits_target(velocity, target):
    target_x, target_y = target
    min_x, max_x = min(target_x), max(target_x)
    min_y, max_y = min(target_y), max(target_y)

    px, py = 0, 0
    vx, vy = velocity
    while px <= max_x and py >= min_y:
        px, py = px + vx, py + vy
        vx = vx - 1 if vx > 0 else vx
        vy -= 1
        if (min_x <= px <= max_x) and (min_y <= py <= max_y):
            return True
    return False


bounds = INPUT_BOUNDS
bounds_x, bounds_y = bounds
min_y = min(bounds_y)
min_x, max_x = min(bounds_x), max(bounds_x)

n = -min_y - 1
print(n * (n+1) / 2)


max_vy = -min_y - 1
min_vy = min_y
max_vx = max_x

solutions = []
# Rather than solve the minimum x, we just check it actually satisifes our constraint
for vx in range(max_vx + 1):
    if (vx * (vx + 1)) / 2 < min_x:
        continue
    for vy in range(min_vy, max_vy + 1):
        if projectile_hits_target((vx, vy), bounds):
            solutions.append((vx, vy))
print(len(solutions))
