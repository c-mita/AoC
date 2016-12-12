import re

def is_abba(s):
    for i in range(len(s) - 3):
        a1, b1, b2, a2 = s[i], s[i+1], s[i+2], s[i+3]
        if a1 == a2 and b1 == b2 and a1 != b1:
            return True
    return False

def is_ssl(seq1s, seq2s):
    for s1 in seq1s:
        for i in range(len(s1) - 2):
            a1, b, a2 = s1[i], s1[i+1], s1[i+2]
            if a1 == a2 and a1 != b:
                for s2 in seq2s:
                    for j in range(len(s2) - 2):
                        if s2[j] == b and s2[j+1] == a1 and s2[j+2] == b:
                            return True
    return False


def process_address(addr):
    seq1s = re.split("\[.*?\]", addr)
    seq2s = re.findall("\[.*?\]", addr)
    return seq1s, seq2s

def is_addr_tls(addr):
    valid, invalid = process_address(addr)
    for s in invalid:
        if is_abba(s):
            return False
    for s in valid:
        if is_abba(s):
            return True
    return False

def is_addr_ssl(addr):
    seq1, seq2 = process_address(addr)
    return is_ssl(seq1, seq2)

def parse_file(filename):
    with open(filename) as f:
        return [line for line in f]

addrs = parse_file("7.txt")
tls = [addr for addr in addrs if is_addr_tls(addr)]
print len(tls)
ssl = [addr for addr in addrs if is_addr_ssl(addr)]
print len(ssl)
