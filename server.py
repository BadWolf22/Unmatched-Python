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

roomList = dict()

clients = dict()

@sio.event
def connect(sid, environ):
    if DEBUG: print('connect ', sid)
    clients[sid] = dict()

@sio.event
def disconnect(sid):
    if DEBUG: print('disconnect ', sid)
    if "room" in clients[sid]:
        sio.emit("sevent_win", room=clients[sid]["room"], skip_sid=sid)
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
        roomList[name] = 0
    if (roomList[name] < 2): 
        roomList[name] += 1
        clients[sid]["room"] = name
        sio.enter_room(sid, name)
        sio.emit("sevent_roomAccept", room=sid)
        if (roomList[name] == 2): sio.emit("sevent_gameStart", room=name)
    else:
        sio.emit("sevent_roomFull", room=sid)


# This is really lazy implementation because we are not worried about cheating right now.
# This implementation also would not work with more than 2 players in a room.
@sio.on("cevent_move")
def cevent_move(sid, nodeNum):
    sio.emit("sevent_move", nodeNum, room=clients[sid]["room"], skip_sid=sid)
    return
@sio.on("cevent_attack")
def cevent_attack(sid, attackVal):
    sio.emit("sevent_attack", attackVal, room=clients[sid]["room"], skip_sid=sid)
    return
@sio.on("cevent_defend")
def cevent_defend(sid, damageTaken):
    return
@sio.on("cevent_endTurn")
def cevent_endTurn(sid):
    sio.emit("sevent_startTurn", room=clients[sid]["room"], skip_sid=sid)
    return

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)