from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Home Page</h1>";

@app.route('/tasks')
def getTask():
    return "<h1>Tasks Page</h1>";


if __name__ == '__main__':
    app.run(port=8000, debug=True)


