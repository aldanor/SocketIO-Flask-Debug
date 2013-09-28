SocketIO-Flask-Debug
====================

This is a minimal app to show how Flask debugging fails with Gevent-Socket.io.

What it does:
- when a socket is connected, the client sends "foo" to the server
- the server receives "foo" and sends "bar" back
- the client receives "bar" and pops up an alert

To start a server:
- with debug disabled: `python app.py`
- with debug enabled: `python app.py debug`

In either case, point the browser at http://127.0.0.1:8080 and see if you can get an alert when running the
server in debug mode.

To see if Werkzeug debugging works, browse to http://127.0.0.1:8080/debug.

Python dependencies: `flask`, `werkzeug`, `gevent`, `gevent-socketio`.
