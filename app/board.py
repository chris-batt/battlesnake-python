from snake import Snake
from node import WeightNode
from const import DIRECTIONS
import copy


class Board:

    def __init__(self, data):
        self.width = data.get('width')
        self.height = data.get('height')
        self.board = []
        self.food = []
        self.snakes = []
        self.you = data.get("you", {}).get('id')
        for food in data.get('food', {}).get('data'):
            self.food.append((food.get('x'), food.get('y')))

        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append(0)

        for snake in data.get('snakes', {}).get('data', []):
            self.snakes.append(Snake(snake))

    def you_snake(self):
        for snake in self.snakes:
            if snake.id == self.you:
                return snake

    def fillWeights(self, fill_snake):
        board = copy.deepcopy(self.board)
        for snake in self.snakes:
            snake.apply_to_board(board, snake.id == fill_snake.id)

        for i in range(len(board)):
            s = ""
            for j in range(len(board[i])):
                s += "%2d "%board[i][j]
            print(s)

        node = WeightNode(fill_snake.head, 0)
        nodes = [node]
        visited = []
        while len(nodes) > 0:
            node = nodes[0]
            del nodes[0]
            if node.point in visited:
                continue
            board[node.point[1]][node.point[0]] = node.weight
            visited.append(node.point)
            for point in node.get_valid_neighbours(board):
                if point in visited:
                    continue
                nodes.append(WeightNode(point, node.weight + 1))
        return board

    def find_best_path(self, start, dest, board):
        print("Finding path from (%d, %d) to (%d, %d)" % (start[0], start[1], dest[0], dest[1]))
        if board[dest[0]][dest[1]] == 0:
            return None
        if start == dest:
            return None
        for i in range(len(board)):
            s = ""
            for j in range(len(board[i])):
                s += "%2d "%board[i][j]
            print(s)
        print(board[dest[1]][dest[0]])
        if board[dest[1]][dest[0]] < 0:
            return None
        curr = dest
        path = [curr]
        while curr != start:
            found_path = False
            for dir in DIRECTIONS:
                x = curr[0] + dir[0]
                y = curr[1] + dir[1]

                if y >= len(board) or y < 0 or x >= len(board[0]) or x < 0:
                    continue
                if board[y][x] != board[curr[1]][curr[0]]-1:
                    continue
                curr = (x,y)
                path.append(curr)
                found_path = True
                break
            if not found_path:
                print('no path')
                return None
        return_path = []
        for node in reversed(path):
            return_path.append(node)
        return return_path



    def simulateMove(self, snake, dir):
        pass

    def print_board(self):
        print(self.width)
        print(self.height)
        print(self.board)
        print(self.food)
        print(self.you)
        for snake in self.snakes:
            snake.print_snake()
