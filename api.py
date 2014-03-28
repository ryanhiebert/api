import os
from flask import Flask, jsonify

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
            ]
        },
        'actions': [
            {
                'name': 'right-for-you',
                'title': 'Why I\'m the right person to work for you',
                'method': 'GET',
                'href': '/right-for-you',
                'fields': {
                    'name': 'company',
                    'type': 'text',
                }
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
