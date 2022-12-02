import heapq

def parse_file(filename):
    blocks = []
    block = []
    blocks.append(block)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                block.append(int(line))
            else:
                block = []
                blocks.append(block)
    return blocks

blocks = parse_file("01_input.txt")

# Part 1
sums = [sum(block) for block in blocks]
print(max(sums))

# Part 2
# Sorting would be simpler, but a priority queue scores more nerd points
pq = [-s for s in sums]
heapq.heapify(pq)
m1, m2, m3 = -heapq.heappop(pq), -heapq.heappop(pq), -heapq.heappop(pq)
print(m1 + m2 + m3)
