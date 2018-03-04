

class Snake:

    def __init__(self, data):
        self.body = []
        self.health = data.get('health')
        self.id = data.get('id')
        for pos in data.get('body', {}).get('data', []):
            self.body.append((pos.get('x'), pos.get('y')))

    @property
    def head(self):
        return self.body[0]

    def apply_to_board(self, board, remove_tail):
        i = 1
        for body in self.body:
            if remove_tail and i == len(self.body):
                continue
            board[body[1]][body[0]] = -i
            i += 1

    def print_snake(self):
        print("printing snake: " + self.id)
        print(self.body)
        print(self.health)