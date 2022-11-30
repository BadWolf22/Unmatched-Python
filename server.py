import eventlet
import socketio
import json
#import gameManager


#player1Connected=False
#player2Connected=False
#gameStarted=False

#if player1Connected==True and player2Connected==True and gameStarted==False:
    #gameStarted=True
    #gameManager.startGame()


DEBUG = True

sio = socketio.Server()
app = socketio.WSGIApp(sio)

roomList = list()

clients = dict()

@sio.event
def connect(sid, environ):
    if DEBUG: print('connect ', sid)
    clients[sid] = dict()

@sio.event
def disconnect(sid):
    if DEBUG: print('disconnect ', sid)
    del clients[sid]

@sio.on("char")
def my_char(sid, data):
    sio.emit("char", data, room=clients[sid]["room"], skip_sid=sid)


@sio.on("message")
def my_message(sid, data):
    try:
        sio.emit("message", (sid, data), room=clients[sid]["room"], skip_sid=sid)
        if DEBUG: print(sid, "says:", data)
    except:
        if DEBUG: print("message attempt while not in a room")

@sio.on("joinroom")
def join_room(sid, name):
    if DEBUG: print(sid, name)
    if name not in roomList:
        roomList.append(name)
    clients[sid]["room"] = name
    sio.enter_room(sid, name)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)