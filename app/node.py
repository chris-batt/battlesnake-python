from const import DIRECTIONS


class WeightNode:

    def __init__(self, point, weight):
        self.point = point
        self.weight = weight

    def get_valid_neighbours(self, board):
        neighbours = []
        for dir in DIRECTIONS:
            x = self.point[0] + dir[0]
            y = self.point[1] + dir[1]
            if y >= len(board) or y < 0 or x >= len(board[0]) or x < 0 or board[y][x] != 0:
                continue
            neighbours.append((x,y))
        return neighbours