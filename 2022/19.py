"""
Part 1 and Part 2 are basically the same (2 goes a little deeper in our walk).
Perform a depth-first walk of options for building robots.
At each step of the walk, our potential graph edges are building each of the
possible robots (if possible), with some optimizations.
 * If a geode cracking robot can be built quicker than any other robot, don't
   consider the other robots.
 * Track the best result so far and compare that to the maximum potential
   result at the current state; if the best result cannot be beaten don't
   proceed any further.
 * Check to see if the current set of robots has already been reached but at
   a sooner time-stamp - if so, stop
Building nothing is also an option, but is "terminal"; just return how many
geodes would get mined given the current state for the remaining time.

~ 2 seconds on a Macbook; not great, not terrible.
"""


import collections
import re
import math

OreRobotCost = collections.namedtuple("OreRobotCost", ["ore"])
ClayRobotCost = collections.namedtuple("ClayRobotCost", ["ore"])
ObsidianRobotCost = collections.namedtuple("ObsidianRobotCost", ["ore", "clay"])
GeodeRobotCost = collections.namedtuple("GeodeRobotCost", ["ore", "obsidian"])
RobotCosts = collections.namedtuple("RobotCosts", ["ore_robot", "clay_robot", "obsidian_robot", "geode_robot"])

def parse_file(filename):
    costs = []
    with open(filename) as f:
        for line in f:
            n, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = map(int, re.findall("[0-9]+", line))
            ore_robot = OreRobotCost(ore_ore)
            clay_robot = ClayRobotCost(clay_ore)
            obs_robot = ObsidianRobotCost(obs_ore, obs_clay)
            geo_robot = GeodeRobotCost(geo_ore, geo_obs)
            costs.append(RobotCosts(ore_robot, clay_robot, obs_robot, geo_robot))
    return costs


def most_geodes(robot_costs, max_time=24):
    def time_required(target, current, robots):
        if current >= target:
            return 0
        delta = target - current
        time = math.ceil(delta / robots)
        return time

    # no point building robots when we already produce what we might need each step
    max_ore_c = max(robot_costs.ore_robot.ore,
            robot_costs.clay_robot.ore,
            robot_costs.obsidian_robot.ore,
            robot_costs.geode_robot.ore
    )
    max_clay_c = robot_costs.obsidian_robot.clay
    max_obsidian_c = robot_costs.geode_robot.obsidian
    def options(robots, minerals):
        # work out how much time to build each of the possible robots
        ore, clay, obsidian, geodes = minerals
        ore_r, clay_r, obsidian_r, geode_r = robots
        t_geode = 0x7FFFFFFF
        # if we can build a geode robot before any other robot, it doesn't
        # make sense to build anything else
        if ore_r and obsidian_r:
            # build a geode robot
            cost_ore = robot_costs.geode_robot.ore
            cost_obs = robot_costs.geode_robot.obsidian
            t_ore = time_required(cost_ore, ore, ore_r)
            t_obs = time_required(cost_obs, obsidian, obsidian_r)
            t = max(t_ore, t_obs) + 1
            n_ore = ore + ore_r * t - cost_ore
            n_clay = clay + clay_r * t
            n_obs = obsidian + obsidian_r * t - cost_obs
            n_geo = geodes + geode_r * t
            t_geode = t
            yield (n_ore, n_clay, n_obs, n_geo), (ore_r, clay_r, obsidian_r, geode_r + 1), t
        if ore_r and clay_r and obsidian_r < max_obsidian_c:
            # build an obsidian robot
            cost_ore = robot_costs.obsidian_robot.ore
            cost_clay = robot_costs.obsidian_robot.clay
            t_ore = time_required(cost_ore, ore, ore_r)
            t_obs = time_required(cost_clay, clay, clay_r)
            t = max(t_ore, t_obs) + 1
            n_ore = ore + ore_r * t - cost_ore
            n_clay = clay + clay_r * t - cost_clay
            n_obs = obsidian + obsidian_r * t
            n_geo = geodes + geode_r * t
            if t < t_geode:
                yield (n_ore, n_clay, n_obs, n_geo), (ore_r, clay_r, obsidian_r + 1, geode_r), t
        if ore_r and clay_r < max_clay_c:
            # build a clay robot
            cost_ore = robot_costs.clay_robot.ore
            t = time_required(cost_ore, ore, ore_r) + 1
            n_ore = ore + ore_r * t - cost_ore
            n_clay = clay + clay_r * t
            n_obs = obsidian + obsidian_r * t
            n_geo = geodes + geode_r * t
            if t < t_geode:
                yield (n_ore, n_clay, n_obs, n_geo), (ore_r, clay_r + 1, obsidian_r, geode_r), t
        if ore_r and ore_r < max_ore_c:
            # build an ore robot
            cost_ore = robot_costs.ore_robot.ore
            t = time_required(cost_ore, ore, ore_r) + 1
            n_ore = ore + ore_r * t - cost_ore
            n_clay = clay + clay_r * t
            n_obs = obsidian + obsidian_r * t
            n_geo = geodes + geode_r * t
            if t < t_geode:
                yield (n_ore, n_clay, n_obs, n_geo), (ore_r + 1, clay_r, obsidian_r, geode_r), t

    def max_potential(robots, minerals, time):
        # assuming we build geode robots as fast as possible
        # what is the maximum number of geodes attainable?
        # time is time remaining
        _ore, _clay, _obs, geodes = minerals
        _r_ore, _r_clay, _r_obs, r_geode = robots
        # "time - 1" because a robot doesn't collect anything the turn it is built
        # so we have to consider one fewer time-step for the maximum
        # ((1+k) + (2+k) + ... (n+k) == (1+2+...+n) + (n*k)
        max_geode = (time * (time - 1)) // 2 + time * r_geode + geodes
        return max_geode

    seen = {}
    def dfs(robots, minerals, time, best=0):
        # check to see if we've reached this amount of robots
        # any earlier before, if we have, we prune this branch
        # by just returning 0
        # remember time is "time remaining", so the test looks backwards
        if robots in seen and seen[robots] > time:
            return (0, ())
        seen[robots] = time
        seen[(robots, minerals)] = time
        null_result = minerals[-1] + robots[-1] * time
        results = [(null_result, ())]
        for option in options(robots, minerals):
            option_m, option_r, option_t = option
            ntime = time - option_t
            if ntime < 0:
                continue
            if max_potential(option_r, option_m, ntime) < best:
                continue
            potential = dfs(option_r, option_m, ntime, best)
            best = max(potential[0], best)
            results.append(potential)
        chain = ((robots, minerals, time),) + max(results)[1]
        return max(results)[0], chain

    return dfs((1, 0, 0, 0), (0, 0, 0, 0), max_time)


blueprints = parse_file("19_input.txt")
q = 0
for n, blueprint in enumerate(blueprints):
    geodes, chain = most_geodes(blueprint)
    q += (n + 1) * geodes
print(q)

q = 1
for n, blueprint in enumerate(blueprints[:3]):
    geodes, chain = most_geodes(blueprint, max_time=32)
    q *= geodes
print(q)
