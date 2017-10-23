import json
from flask import Flask, request, abort
from flask_cors import CORS
from librus import librus

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/auth", methods=['POST'])
def auth():
    data = request.get_json()
    login = data['login']
    password = data['password']

    result = librus.Librus(login, password).login()
    if result is None:
        abort(401)
    else:
        return json.dumps({"DZIENNIKSID": result})


class TimetableEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__ if isinstance(o, librus.Class) else o


@app.route("/timetable", methods=['POST'])
def timetable():
    try:
        login = request.form['login']
        password = request.form['password']
        l = librus.Librus(login, password)
        if l.login() is None:
            abort(401)

        return json.dumps(l.get_timetable(), cls=TimetableEncoder)
    except KeyError:
        cookie = request.form['cookie']
        return json.dumps(librus.Librus(cookie=cookie).get_timetable(), cls=TimetableEncoder)


if __name__ == '__main__':
    app.run(debug=True)
