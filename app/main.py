import bottle
import os
import random

from board import Board
from const import *



@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    board = Board(data)
    filled_board = board.fillWeights(board.you_snake())
    dest = board.food[0]
    if board.you_snake().health > 20:
        dest = board.you_snake().body[-1]
    head = board.you_snake().head
    path = board.find_best_path(head, dest, filled_board)
    if not path:
        print("no path going to dirs")
        dir = -1
        for dir in DIRECTIONS:
            x = head[0] + dir[0]
            y = head[1] + dir[1]
            if y >= board.height or y < 0 or x >= board.width or x < 0:
                continue
            if filled_board[y][x] < 0:
                continue
            break
        if dir == -1:
            dir = (-1, 0)
    else:
        dir = (path[1][0] - path[0][0], path[1][1] - path[0][1])
    print(dir)
    direction = {LEFT: "left",
     RIGHT: "right",
     UP: "up",
     DOWN: "down"}.get(DIRECTIONS.index(dir))

    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
