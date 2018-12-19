import operator
import re

TEST_INPUT = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""

sleep_durations = {}
sleep_minute_count = {}

with open("04_input.txt") as f:
    input_strings = [s.strip() for s in sorted(f.readlines())]
    #input_strings = [s.strip() for s in sorted(TEST_INPUT.split("\n"))][1:]

current_guard = None
awake_min = None
sleep_min = None
for s in input_strings:
    ints = re.findall("\d+", s)
    if "Guard" in s:
        current_guard = int(ints[-1])
        awake_min = int(ints[-1])
    elif "asleep" in s:
        sleep_min = int(ints[-1])
    elif "wakes" in s:
        awake_min = int(ints[-1])
        time = awake_min - sleep_min
        sleep_durations.setdefault(current_guard, []).append(time)
        minutes = sleep_minute_count.setdefault(current_guard, {})
        for m in xrange(sleep_min, awake_min):
            minutes.setdefault(m, 0)
            minutes[m] += 1
    else:
        raise ValueError("OOPS")

sleepiest_guard = max(sleep_durations, key=lambda k: sum(sleep_durations[k]))
sleepiest_worst_minute = max(sleep_minute_count[sleepiest_guard], key=lambda m: sleep_minute_count[sleepiest_guard][m])
sleepiest_worst_minute = max(sleep_minute_count[sleepiest_guard].iteritems(), key=operator.itemgetter(1))[0]
print sleepiest_guard, sleepiest_worst_minute
print sleepiest_guard * sleepiest_worst_minute

guard, worst_minute, worst_minute_count = max(((g, minute, count) for g in sleep_minute_count for (minute, count) in sleep_minute_count[g].iteritems()),
        key=operator.itemgetter(2))

print guard, worst_minute, worst_minute_count
print guard * worst_minute
