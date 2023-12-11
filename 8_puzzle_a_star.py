import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.heuristic = self.calculate_heuristic()

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def calculate_heuristic(self):
        h = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    goal_row, goal_col = divmod(self.state[i][j] - 1, 3)
                    h += abs(i - goal_row) + abs(j - goal_col)
        return h

    def generate_children(self):
        children = []
        zero_row, zero_col = next((i, j) for i, row in enumerate(self.state) for j, val in enumerate(row) if val == 0)

        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        for move in moves:
            new_row, new_col = zero_row + move[0], zero_col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [row.copy() for row in self.state]
                new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
                children.append(PuzzleNode(new_state, self, move, self.cost + 1))

        return children

def get_user_input():
    print("Nhap trang thai hien tai(0 tuong trung cho o trong):")
    initial_state = []
    for i in range(3):
        row = list(map(int, input().split()))
        initial_state.append(row)

    print("Nhap trang thai dich(0 truong trung cho o trong):")
    goal_state = []
    for i in range(3):
        row = list(map(int, input().split()))
        goal_state.append(row)

    return initial_state, goal_state

def a_star(initial_state, goal_state):
    initial_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)

    open_set = [initial_node]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)
        if current_node.state == goal_node.state:
            path = []
            while current_node:
                path.append((current_node.move, current_node.state))
                current_node = current_node.parent
            return list(reversed(path))

        closed_set.add(tuple(map(tuple, current_node.state)))

        for child in current_node.generate_children():
            if tuple(map(tuple, child.state)) not in closed_set:
                heapq.heappush(open_set, child)

    return None

# Example usage:
initial_state, goal_state = get_user_input()

solution = a_star(initial_state, goal_state)

if solution:
    for move, state in solution:
        print(f"Di chuyen: {move}\n{state}\n")
else:
    print("Khong co buoc giai nao duoc tim thay.")
