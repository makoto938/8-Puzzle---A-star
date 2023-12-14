from collections import deque
import heapq
# import time

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

def read_state_from_file(file_path):
    with open(file_path, 'r') as file:
        state = []
        for i in range(3):
            row = list(map(int, file.readline().split()))
            state.append(row)
    return state

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


def dfs(initial_state, goal_state):
    initial_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)

    stack = [initial_node]
    visited = set()

    while stack:
        current_node = stack.pop()
        if current_node.state == goal_node.state:
            path = []
            while current_node:
                path.append((current_node.move, current_node.state))
                current_node = current_node.parent
            return list(reversed(path))

        visited.add(tuple(map(tuple, current_node.state)))

        for child in current_node.generate_children():
            if tuple(map(tuple, child.state)) not in visited:
                stack.append(child)

    return None

def bfs(initial_state, goal_state):
    initial_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)

    queue = deque([initial_node])
    visited = set()

    while queue:
        current_node = queue.popleft()
        if current_node.state == goal_node.state:
            path = []
            while current_node:
                path.append((current_node.move, current_node.state))
                current_node = current_node.parent
            return list(reversed(path))

        visited.add(tuple(map(tuple, current_node.state)))

        for child in current_node.generate_children():
            if tuple(map(tuple, child.state)) not in visited:
                queue.append(child)

    return None


def main():
    # Specify the file paths for the initial and goal states
    initial_state_file = "C:/Users/ASUS/Downloads/TTNT/bài tập lớn/initial_state.txt"
    goal_state_file = "C:/Users/ASUS/Downloads/TTNT/bài tập lớn/goal_state.txt"

    # Read initial and goal states from files
    initial_state = read_state_from_file(initial_state_file)
    goal_state = read_state_from_file(goal_state_file)

    print("Chon mot trong ba thuat toan:")
    print("1. A* Algorithm")
    print("2. Depth-First Search (DFS)")
    print("3. Breadth-First Search (BFS)")

    choice = input("Nhap lua chon (1, 2, hoac 3): ")

    if choice == "1":
        algorithm_function = a_star
        algorithm_name = "A* Algorithm"
    elif choice == "2":
        algorithm_function = dfs
        algorithm_name = "DFS"
    elif choice == "3":
        algorithm_function = bfs
        algorithm_name = "BFS"
    else:
        print("Lua chon khong hop le.")
        return
    
    # start_time = time.time()

    solution = algorithm_function(initial_state, goal_state)
    
    # end_time = time.time()
    # execution_time = end_time - start_time

    if solution:
        for move, state in solution:
            print(f"Di chuyen: {move}\n{state}")
        # print(f"Thoi gian chay cua {algorithm_name}: {execution_time:.6f} giay")    
    else:
        print("Khong co buoc giai nao duoc tim thay.")

if __name__ == "__main__":
    main()
