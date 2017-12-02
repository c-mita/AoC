"""
Discs - (#positions, pos @ t=0)
(5, 2)
(13, 7)
(17, 10)
(3, 2)
(19, 9)
(7, 0)
"""

def calc_disc_position(npos, pos0, t):
    return (pos0 + t) % npos

def find_time(discs):
    t = 0
    while True:
        t2 = t
        for disc in discs:
            t2 += 1
            if calc_disc_position(disc[0], disc[1], t2):
                break
        else:
            return t
        t += 1

#discs = [(5, 4), (2, 1)]
discs = [(5, 2), (13, 7), (17, 10), (3, 2), (19, 9), (7, 0)]
print find_time(discs)
discs = [(5, 2), (13, 7), (17, 10), (3, 2), (19, 9), (7, 0), (11, 0)]
print find_time(discs)
