"""
A simple guestbook flask app.
"""
import flask
from index import Index
from sign import Sign
from health_endpoints import register_health_endpoints

app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/sign',
                 view_func=Sign.as_view('sign'),
                 methods=['GET', 'POST'])

# Register health check endpoints
register_health_endpoints(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
