import os
from flask import Flask, jsonify, request, abort, url_for as flask_url_for

from tictactoe import TicTacToe

app = Flask(__name__)

def url_for(*args, **kwargs):
    return flask_url_for(*args, _external=True, **kwargs)

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
        ],
        'links': [
            {'rel': ['self'], 'href': url_for('home')},
            {'rel': ['games'], 'href': url_for('games')},
            {'rel': ['github'], 'href': 'https://github.com/ryanhiebert'},
            {'rel': ['source'], 'href': 'https://github.com/ryanhiebert/api'},
        ]
    })

@app.route('/games')
def games():
    return jsonify({
        'links': [
            {'rel': ['home'], 'href': url_for('home')},
            {'rel': ['tictactoe'], 'href': url_for('tictactoe', state=str(TicTacToe()))}
        ]
    })

@app.route('/games/tictactoe/<state>')
def tictactoe(state):
    len(state) == 9 or abort(404)
    all(s in 'xo-' for s in state) or abort(404)
    if (not state.count('x') == state.count('o') and
            not state.count('x')  == state.count('o') + 1):
        abort(404)

    board = TicTacToe(state)

    move = request.args.get('move', '')
    if move:
        if board.completed():
            abort(422)
        move = 'abc'.index(move[0]), '012'.index(move[1])
        if move not in board.empty():
            abort(422)

        board = board.move(move)

    board_dict = {
        'class': 'tictactoe-board',
        'properties': {
            'repr': str(board),
            'turn': board.turn(),
            'winner': board.winner(),
            'completed': board.completed(),
        },
        'links': [
            {'rel': ['self'], 'href': url_for('tictactoe', state=str(board))},
        ]
    }

    if not board.completed():
        board_dict['actions'] = [
            {
                'name': 'tictactoe-move',
                'title': 'Make your move',
                'method': 'GET',
                'href': url_for('tictactoe', state=str(board)),
                'fields': [
                    {
                        'name': 'move',
                        'type': 'select',
                        'options': [
                            {'value': 'abc'[r] + str(c)} for r,c in board.empty()
                        ]
                    }
                ]
            }
        ]

    return jsonify(board_dict)


if __name__ == '__main__':
    app.run(debug=True)
