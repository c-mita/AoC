"""
Eliminate every "other" elf

Part 1 is Josephus Problem
Solved by f(n) = 2l + 1 (where f(n) is safe position)
where n = 2**m + l and l < 2**m

For part 2 we create a doubly-linked-list representing the circle
and just remove the relevant elements in turn.
We hold "pointers" to the "HEAD" (current elf) and "Middle" (elf eliminated)
The middle pointer must be incremented twice when moving from odd to even

There is probably an adaptation to the Josephus Problem that allows the
solution to be better calculated (rather than a full simulation being run) but
this works well enough
"""

def find_p1_winner(n):
    high_bit = 1
    while high_bit < n:
        high_bit <<= 1
    high_bit >>= 1
    l = n - high_bit
    return 2 * l + 1


INDEX = 0
LEFT = 1
RIGHT = 2

def create_elves(n):
    elves = [{INDEX:i+1} for i in xrange(n)]
    for i in xrange(n):
        if i > 0: elves[i][RIGHT] = elves[i-1]
        if i < n-1: elves[i][LEFT] = elves[i+1]
    elves[0][RIGHT] = elves[-1]
    elves[-1][LEFT] = elves[0]
    return elves

def cull_elves(elves):
    n = len(elves)
    e0 = elves[0]
    em = elves[n//2]
    #print e0[INDEX], em[INDEX]
    while e0[LEFT] != e0[RIGHT] != e0:
        em[RIGHT][LEFT] = em[LEFT]
        em[LEFT][RIGHT] = em[RIGHT]
        em = em[LEFT]
        if n % 2 == 1:
            em = em[LEFT]
        n -= 1
        e0 = e0[LEFT]
        #print e0[INDEX], em[INDEX]
    return e0[INDEX]

n = 3005290
#n = 5
print find_p1_winner(n)
elves = create_elves(n)
print cull_elves(elves)
