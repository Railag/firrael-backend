#!flask/bin/python
from flask import Flask, jsonify


import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket

cherrypy.config.update({'server.socket_port': 9000})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

import codecs

class Root(object):
    @cherrypy.expose
    def index(self):
        return codecs.open("index.html", 'r', 'utf-8')

    @cherrypy.expose
    def ws(self):
        # you can access the class instance through
        handler = cherrypy.request.ws_handler

cherrypy.quickstart(Root(), '/', config={'/ws': {'tools.websocket.on': True,
                                                 'tools.websocket.handler_cls': EchoWebSocket}})

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


from flask import abort

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    length = 0;
    for l in task:
        length += 1;
    if length == 0:
        abort(404)
    print("Task id is %d" % task_id)
    print(task)
    print(task[0])
    return jsonify({'task': task[0]})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/', methods=['GET'])
def get_default_tasks():
    return jsonify({'tasks': tasks})


app.run(host='0.0.0.0', debug=True)
