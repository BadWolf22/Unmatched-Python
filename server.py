import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)



@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)



@sio.on("message")
def my_message(sid, data):
    print(sid, "says:", data)
    sio.emit("message", (sid, data), skip_sid=sid)



if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)