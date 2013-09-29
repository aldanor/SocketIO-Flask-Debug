from gevent import monkey
from socketio.server import SocketIOServer
from socketio import socketio_manage
from flask import Flask, request, render_template, Response
from debugger import SocketIODebugger
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

    def on_foo(self, msg=None):
        print '\nNamespace.on_foo(): msg=%s' % repr(msg)
        self.emit('bar', {'data': 'some server data'})

    def on_debug(self, msg=None):
        print '\nNamespace.on_debug()'
        raise Exception('in-namespace exception')


def index():
    print '\nindex()'
    return render_template('index.html')


def debug():
    print '\ndebug()'
    raise Exception('in-flask exception')


def run_socketio(path):
    print '\nrun_socketio(path=%s)' % repr(path)
    socketio_manage(request.environ, {'/api': Namespace}, request)
    return Response()


if __name__ == '__main__':
    app = Flask(__name__)
    app.route('/')(index)
    app.route('/debug')(debug)
    app.route('/socket.io/<path:path>')(run_socketio)
    app.debug = True

    app = SocketIODebugger(app, evalex=True, namespace=Namespace)

    server = SocketIOServer(('', 8080), app,
        resource='socket.io', policy_server=False)
    print '\nserver.serve_forever()'
    server.serve_forever()
