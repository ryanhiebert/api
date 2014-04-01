import os
from flask import Flask, jsonify, request, abort, url_for as flask_url_for
from flask.ext.mail import Mail, Message
from flask.ext.heroku import Heroku

from tictactoe import TicTacToe

app = Flask(__name__)
heroku = Heroku(app)
mail = Mail(app)

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
            'email': 'ryan@ryanhiebert.com',
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
            },
            {
                'name': 'contact',
                'title': 'Get in touch with me!',
                'method': 'POST',
                'href': url_for('contact'),
                'fields': [
                    {
                        'name': 'from',
                        'type': 'email',
                    },
                    {
                        'name': 'message',
                        'type': 'text',
                    }
                ]
            },
            {
                'name': 'contact',
                'title': 'Get in touch with me!',
                'method': 'GET',
                'href': url_for('contact'),
                'fields': [
                    {
                        'name': 'from',
                        'type': 'email',
                    },
                    {
                        'name': 'message',
                        'type': 'text',
                    }
                ]
            },
        ],
        'links': [
            {'rel': ['self'], 'href': url_for('home')},
            {'rel': ['games'], 'href': url_for('games')},
            {'rel': ['github'], 'href': 'https://github.com/ryanhiebert'},
            {'rel': ['source'], 'href': 'https://github.com/ryanhiebert/api'},
            {'rel': ['right-for-you-simple'], 'href': url_for('right_for_you') + '?company=simple'},
        ]
    })

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        sender = request.args.get('from', '')
        message = request.args.get('message', '')
    elif request.method == 'POST':
        sender = request.form.get('from', '')
        message = request.form.get('message', '')

    if not message:
        message = '--- NO MESSAGE ENTERED ---'

    body = '''
    Someone visited your contact page from IP: {}

    They claimed to send the message to you from: {}

    This is their message to you:
    {}
    '''.format(request.remote_addr, sender, message)

    msg = Message(
        body,
        sender=('RyanHiebert API', 'contact@api.ryanhiebert.com'),
        recipients=['ryan@ryanhiebert.com'])

    if not sender == 'cowpie':
        mail.send(msg)

    return jsonify({
        'links': [
            {'rel': ['self'], 'href': url_for('contact')},
            {'rel': ['self'], 'href': url_for('home')}
        ],
        'actions': [
            {
                'name': 'contact',
                'title': 'Get in touch with me!',
                'method': 'POST',
                'href': url_for('contact'),
                'fields': [
                    {
                        'name': 'from',
                        'type': 'email',
                    },
                    {
                        'name': 'message',
                        'type': 'text',
                    }
                ]
            },
            {
                'name': 'contact',
                'title': 'Get in touch with me!',
                'method': 'GET',
                'href': url_for('contact'),
                'fields': [
                    {
                        'name': 'from',
                        'type': 'email',
                    },
                    {
                        'name': 'message',
                        'type': 'text',
                    }
                ]
            },
        ]
    })

@app.route('/right-for-you')
def right_for_you():
    company = request.args.get('company', '')
    if company not in ('simple', 'Simple'):
        abort(404)
    else:
        return jsonify({
            'properties': {
                'reasons': [
                    {
                        'reason': 'Accounting and personal finance have long been an active interest of mine.',
                        'support': [
                            'I have been working on an accounting API for some time, '
                                'all in my free time, mostly iterating and discarding and '
                                'reworking the models, over and over again. It’s still mostly '
                                'vaporware, but the models I’m currently iterated to are '
                                'available at https://github.com/ryanhiebert/finances.',
                            'I took an accounting course for the purpose of understanding '
                                'the domain better to make a personal finance software package.',
                            'I want to make a personal finance application that both has a simple '
                                'front-end for everyday users, and also has a fundamentally solid model '
                                'that can be extended to an interface that would please a professional '
                                'accountant.',
                        ]
                    },
                    {
                        'reason': 'I constantly am looking to build solid, reliable, testable, readable, '
                                    'and beautiful code. This has lead me down the path of immutable, '
                                    'mostly functional programming.',
                        'support': [
                            'Python has been my go-to language for a while, but its pervasive mutability '
                                'has had me designing a language that I would find both beautiful, simple, '
                                'and safe. See the repository for this vaporware at https://github.com/ryanhiebert/brooke.',
                            'I believe that high-order thinking helps the problem to fall away from the '
                                'implementation, so that you can concentrate on the problem you’re looking '
                                'to solve, instead of having to solve the problem of your tool simultaneously.',
                            'Rich Hickey has inspired me that programming can be right and correct. '
                                'I love re-watching videos of talks that he has given.'
                        ]
                    },
                    {
                        'reason': 'Simple has inspired me that a company can be '
                                    'successful, beautiful, ethical, and revolutionary.',
                        'support': [
                            'Simple is clearly a place that I would love to work, and where I would be '
                                'inspired to work for the mission and vision of the company.',
                            'Let me show you that I’m worth a risk, and that I '
                                'will be a valuable addition to your team.',
                        ]
                    }
                ]
            },
            'links': [
                {'rel': ['self'], 'href': url_for('right_for_you') + '?company=simple'},
                {'rel': ['home'], 'href': url_for('home')},
                {'rel': ['project'], 'href': 'https://github.com/ryanhiebert/finances'},
                {'rel': ['project'], 'href': 'https://github.com/ryanhiebert/brooke'}
            ],
            'actions': [],
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
            {'rel': ['games'], 'href': url_for('games')}
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
    app.run(debug=True, port=int(os.environ.get('PORT', '5000')), host='0.0.0.0')
