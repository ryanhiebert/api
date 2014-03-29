import os
from flask import Flask, jsonify, request, abort

from tictactoe import TicTacToe

app = Flask(__name__)

def siren(view):
    """Decorator to make a jsonify response use siren media type"""
    def _siren(*args, **kwargs):
        response = view(*args, **kwargs)
        response.mimetype = 'application/vnd.siren+json'
        return response
    return _siren

@app.route('/')
def home():
    return jsonify({
        'properties': {
            'name': 'Ryan Hiebert',
            'age': 25,
            'interests': [
                'repeatable deployments',
                'hypermedia api design',
                'personal finance',
                'doing better than just "Don\'t be evil"',
                'helping people win with money',
                'immutability in programming languages',
                'learning forever more',
                'being a better human being',
                'changing my family\'s financial legacy',
            ]
        },
        'actions': [
            {
                'name': 'right-for-you',
                'title': 'Why I\'m the right person to work for you',
                'method': 'GET',
                'href': '/right-for-you',
                'fields': [
                    {
                        'name': 'company',
                        'type': 'text',
                    }
                ]
            }
        ]
    })

@app.route('/games/tictactoe')
def tictactoe():
    board = TicTacToe()

    return jsonify({
        'actions': [
            {
                'name': 'tictactoe-move',
                'title': 'Make your move',
                'method': 'GET',
                'href': 'tictactoe/{}'.format(board),
                'fields': [
                    {
                        'name': 'player',
                        'type': 'text',
                        'value': board.turn(),
                    },
                    {
                        'name': 'move',
                        'type': 'text',
                        'options': [
                            'a0', 'a1', 'a2',
                            'b0', 'b1', 'b2',
                            'c0', 'c1', 'c2',
                        ]
                    }
                ]
            }
        ],
        'links': [
            {'rel': ['self'], 'href': '/games/tictactoe/{}'.format(board)},
        ]
    })

@app.route('/games/tictactoe/<state>')
def tictactoe_move(state):
    len(state) == 9 or abort(404)
    all(s in 'xo-' for s in state) or abort(404)
    if (not state.count('x') == state.count('o') and
            not state.count('x')  == state.count('o') + 1):
        abort(404)

    board = TicTacToe(state)

    player = request.args.get('player', '')
    move = request.args.get('move', '')
    if player and move:
        if board.completed():
            abort(422)
        move = 'abc'.index(move[0]), '012'.index(move[1])
        if move not in board.empty():
            abort(422)
        if player not in ('x', 'o'):
            abort(422)

        board = board.move(player, move)

    return jsonify({
        'class': 'tictactoe-board',
        'properties': {
            'repr': str(board),
            'turn': board.turn(),
            'winner': board.winner(),
            'completed': board.completed(),
        },
        'actions': [
            {
                'name': 'tictactoe-move',
                'title': 'Make your move',
                'method': 'GET',
                'href': '/games/tictactoe/{}'.format(board),
                'fields': [
                    {
                        'name': 'player',
                        'type': 'text',
                        'value': board.turn(),
                    },
                    {
                        'name': 'move',
                        'type': 'text',
                        'options':
                            ['abc'[r]+str(c) for r,c in board.empty()]
                    }
                ]
            }
        ],
        'links': [
            {'rel': ['self'], 'href': '/games/tictactoe/{}'.format(board)},
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)
