import sys
from gevent import monkey
from socketio.server import SocketIOServer
from socketio import socketio_manage
from flask import Flask, request, render_template
from werkzeug.debug import DebuggedApplication
from socketio.namespace import BaseNamespace

monkey.patch_all()

class Namespace(BaseNamespace):

    def __init__(self, *args, **kwargs):
        print '\nNamespace.__init__(args=%s, kwargs=%s)' % (
            repr(args), repr(kwargs))
        super(Namespace, self).__init__(*args, **kwargs)

    def recv_connect(self):
        print '\nNamespace.recv_connect()'

    def recv_disconnect(self):
        print '\nNamespace.recv_disconnect()'
        self.disconnect()

    def on_foo(self, msg):
        print '\nNamespace.on_foo(): msg=%s' % repr(msg)
        self.emit('bar', {'data': 'some server data'})

def index():
    print '\nindex()'
    return render_template('index.html')

def debug():
    print '\ndebug()'
    0/1

def run_socketio(path):
    print '\nrun_socketio(path=%s)' % repr(path)
    socketio_manage(request.environ, {'/api': Namespace}, request)

if __name__ == '__main__':
    app = Flask(__name__)
    app.route('/')(index)
    app.route('/debug')(debug)
    app.route('/socket.io/<path:path>')(run_socketio)

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.debug = True
        app = DebuggedApplication(app, evalex=True)

    server = SocketIOServer(('127.0.0.1', 8080), app,
        resource='socket.io', policy_server=False)
    print '\nserver.serve_forever()'
    server.serve_forever()
