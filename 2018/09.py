class Node(object):
    __slots__ = ('value', 'next', 'prev')
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev


def play_game(n_players, max_count):
    # marble state will be a circular doubly linked list
    scores = [0] * n_players
    current_node = Node(0)
    current_node.next = current_node
    current_node.prev = current_node
    for iteration in xrange(1, max_count + 1):
        if iteration % 23 == 0:
            current_player = (iteration - 1) % len(scores)
            scores[current_player] += iteration
            for n in xrange(7):
                current_node = current_node.prev
            scores[current_player] += current_node.value
            current_node.prev.next = current_node.next
            current_node.next.prev = current_node.prev
            current_node = current_node.next
        else:
            left_node = current_node.next
            right_node = left_node.next

            new_node = Node(iteration)
            left_node.next = new_node
            new_node.prev = left_node
            new_node.next = right_node
            right_node.prev = new_node
            current_node = new_node

    return scores


test_params = (9, 25)
test_params = (13, 7999)
game_params = (468, 71010)

params = game_params
scores = play_game(*params)
print max(scores)


fuck_off_params = params[0], params[1] * 100
scores = play_game(*fuck_off_params)
print max(scores)
