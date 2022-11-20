import eventlet
import socketio
import json

DEBUG = False

sio = socketio.Server()
app = socketio.WSGIApp(sio)

publicRooms = list()
privateRooms = list()

clients = dict()

@sio.event
def connect(sid, environ):
    if DEBUG: print('connect ', sid)
    sio.emit("roomlist", json.dumps(publicRooms), room=sid)

@sio.event
def disconnect(sid):
    if DEBUG: print('disconnect ', sid)



@sio.on("message")
def my_message(sid, data):
    try:
        sio.emit("message", (sid, data), room=clients[sid]["room"], skip_sid=sid)
        if DEBUG: print(sid, "says:", data)
    except:
        if DEBUG: print("message attempt while not in a room")

@sio.on("joinroom")
def join_room(sid, name, public):
    if DEBUG: print(sid, name, public)
    clients[sid] = dict()
    clients[sid]["room"] = name
    sio.enter_room(sid, name)
    if name not in publicRooms or name not in privateRooms:
        if public: publicRooms.append(name)
        else: privateRooms.append(name)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)