def progress_state(state, e1_idx, e2_idx):
    e1_score, e2_score = state[e1_idx], state[e2_idx]
    s = e1_score + e2_score
    if s < 10:
        state.append(s)
    else:
        state.append(s / 10)
        state.append(s % 10)
    e1_idx = (e1_idx + e1_score + 1) % len(state)
    e2_idx = (e2_idx + e2_score + 1) % len(state)
    return state, e1_idx, e2_idx


def check_sublist(sl, l):
    return "".join(map(str, sl)) in "".join(map(str, l))

initial_state = [3, 7]

e1_idx, e2_idx = 0, 1

initial = 503761
state = list(initial_state)
while len(state) < initial + 10:
    state, e1_idx, e2_idx = progress_state(state, e1_idx, e2_idx)

print state[-10:]

state = list(initial_state)
e1_idx, e2_idx = 0, 1

target_list = [5, 0, 3, 7, 6, 1]
while not check_sublist(target_list, state[-(len(target_list) + 1):]):
    state, e1_idx, e2_idx = progress_state(state, e1_idx, e2_idx)

# have to check if it was reached by adding one score or two
if check_sublist(target_list, state[-len(target_list):]):
    print len(state) - len(target_list)
else:
    print len(state) - len(target_list) - 1
