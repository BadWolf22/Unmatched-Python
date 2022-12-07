from os import environ, path

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import pygame_menu
from character import Character
from map import Map

RESOLUTIONS = [(600, 600), (800, 800), (1000, 1000), (1280, 720), (1920, 1080)]
RESOLUTION_INDEX = 0

pygame.init()
surface = pygame.display.set_mode(RESOLUTIONS[RESOLUTION_INDEX])


# Create a custom theme
my_theme = pygame_menu.themes.THEME_DARK.copy()
my_theme.title = False  # Hide the menu title

mainMenu = pygame_menu.Menu(
    title="Python Unmatched",
    width=surface.get_width(),
    height=surface.get_height(),
    theme=pygame_menu.themes.THEME_BLUE,
    mouse_motion_selection=True,
)
roomMenu = pygame_menu.Menu(
    title="Join a Game",
    width=surface.get_width(),
    height=surface.get_height(),
    theme=pygame_menu.themes.THEME_BLUE,
    mouse_motion_selection=True,
)
charMenu = pygame_menu.Menu(
    title="Select Your Character!",
    width=surface.get_width(),
    height=surface.get_height(),
    theme=pygame_menu.themes.THEME_BLUE,
    mouse_motion_selection=True,
)
gameMenu = pygame_menu.Menu(
    title="",
    width=surface.get_width(),
    height=surface.get_height(),
    theme=my_theme,
    mouse_motion_selection=True,
    center_content=False,
)
waitMenu = pygame_menu.Menu(
    title="Waiting for opponent!",
    width=surface.get_width(),
    height=surface.get_height(),
    theme=pygame_menu.themes.THEME_BLUE,
)

menus = (mainMenu, roomMenu, charMenu, waitMenu, gameMenu)

######################################
# Socket setup
import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("connection established", f"sid=`{sio.get_sid()}`")


@sio.event
def disconnect():
    print("disconnected from server")


@sio.on("message")
def my_message(sid, data):
    print(sid, "says:", data)


@sio.on("char")
def my_char(character):
    players["enemy"] = Character.assignCharacter("characters/phineasFerb.json")
    setup_hands()


@sio.on("sevent_roomAccept")
def room_accept():
    global roomStatus
    roomStatus = 1
    print("joining room")


@sio.on("sevent_roomFull")
def room_full():
    global roomStatus
    roomStatus = 2
    print("The room is full, please enter a new name!")


@sio.on("sevent_gameStart")
def start_game():
    waitMenu.set_onupdate(make_charMenu)

@sio.on("sevent_startTurn")
def start_turn():
    print("starting turn")
    global numActions
    numActions = 2

@sio.on("sevent_move")
def enemy_move(nodeNum):
    players["enemy"].mapNode = nodeNum
    print("Enemy moved to:", nodeNum)
    display_chars()

######################################

roomStatus = 0


def connect_to_server(*args):
    # print(f"Connecting to: {serverIP.get_value()}")
    sio.connect(args[0].get_value())
    mainMenu.toggle()
    make_roomMenu()


def connect_to_room(*args):
    global roomStatus
    sio.emit("joinroom", args[0].get_value())
    # necessary because otherwise rooms could have more than 2 people (which is bad rn)
    while roomStatus == 0:
        pass
    if roomStatus == 1:
        roomMenu.disable()
        make_waitMenu()
    else:
        roomStatus = 0


players = dict()
numActions = 0
attacking = False


def select_character(*args):
    global players
    sio.emit("char", args[0])
    players["player"] = Character.assignCharacter("characters/phineasFerb.json")
    setup_hands()
    charMenu.toggle()
    gameMenu.mainloop(surface)


def setup_hands():
    if len(players) == 2:
        for player in players:
            area_draw = gameMenu.get_widget(player + "Draw")
            area_hand = gameMenu.get_widget(player + "Hand")
            for i in range(5):
                card = players[player].deck.draw(gameMenu, area_draw, area_hand, player, card_press)

# When you press on a map node button!
def node_press(*args):
    global numActions
    global attacking
    if numActions == 0:
        return print("You have no turns right now!")
    dist = dist_between(players["player"].mapNode, args[0])
    print(dist, players["player"].moveDistance)
    # TODO: Check for attacking
    if dist > players["player"].moveDistance:
        return print("This is too far to move!")
    numActions -= 1
    sio.emit("cevent_move", args[0])
    players["player"].mapNode = args[0]
    display_chars()
    print("Moving to:", args[0])
    if numActions == 0:
        sio.emit("cevent_endTurn")

def dist_between(n1, n2):
    if n1 == None or n1 == n2: return 0
    global my_map
    q = [n1]
    tempNodes = dict()
    tempNodes[n1] = 0
    while len(q) > 0:
        curr = q.pop(0)
        for neighbor in my_map.data[str(curr)]["neighbors"]:
            if str(neighbor) not in tempNodes:
                tempNodes[neighbor] = tempNodes[curr] + 1
                if neighbor == n2: return tempNodes[neighbor]
                q.append(neighbor)

def display_chars():
    global my_map
    for node in range(my_map.data["nodeCount"]):
        gameMenu.get_widget(str(node)).set_title("")
    for player in players:
        try:
            gameMenu.get_widget(str(players[player].mapNode)).set_title(player[0])
        except:
            pass

# When you press on a card button!
def card_press(*args):
    global numActions
    global attacking
    if numActions == 0:
        return print("You have no turns right now!")
    if not attacking:
        return print("You may not play a card right now!")
    numActions -= 1
    # sio.emit("cevent_attack", args[1])
    print(args[0][0]=="p", args[1].value)
    if numActions == 0:
        sio.emit("cevent_endTurn")

def send_message():
    sio.emit("message", "hiii")


def change_resolution():
    global RESOLUTION_INDEX
    RESOLUTION_INDEX = (RESOLUTION_INDEX + 1) % len(RESOLUTIONS)
    pygame.display.set_mode(RESOLUTIONS[RESOLUTION_INDEX])
    for menu in menus:
        menu.resize(surface.get_width(), surface.get_height())


def make_mainMenu():
    serverIP = mainMenu.add.text_input("Server: ", default="http://localhost:5000")
    mainMenu.add.button("Connect", connect_to_server, serverIP)
    mainMenu.add.button("Change Resolution", change_resolution)
    mainMenu.add.button("Quit", pygame_menu.events.EXIT)
    mainMenu.mainloop(surface)


def make_roomMenu():
    roomID = roomMenu.add.text_input("Game Name: ", default="Type...")
    roomMenu.add.button("Join!", connect_to_room, roomID)
    roomMenu.add.button("Quit", pygame_menu.events.EXIT)
    roomMenu.mainloop(surface)


def make_charMenu():
    waitMenu.disable()
    charMenu.add.button("Char1", select_character, "char1")
    charMenu.add.button("Char2", select_character, "char2")
    charMenu.add.button("Quit", pygame_menu.events.EXIT)
    make_gameMenu()
    charMenu.mainloop(surface)


def make_waitMenu():
    waitMenu.mainloop(surface)


def make_gameMenu():
    enemy_info = make_cardArea("#ff0000", "enemy")
    your_info = make_cardArea("#00aa00", "player")
    your_info.translate(0, surface.get_height() - your_info.get_height())
    map_area = make_mapArea(enemy_info.get_height() + your_info.get_height())

    # gameMenu.add.button(
    #     "test", send_message, float=True, align=pygame_menu.locals.ALIGN_LEFT
    # ).translate(300, 300)


def make_cardArea(color, prefix):
    card_area = gameMenu.add.frame_h(
        background_color=color,
        float=True,
        height=int(surface.get_height() / 5),
        width=surface.get_width(),
    ).set_margin(0, 0)
    area_draw = gameMenu.add.button(
        "Draw: 30", button_id=prefix + "Draw"
    ).set_selection_effect(None)
    area_hand = gameMenu.add.frame_h(
        frame_id=prefix + "Hand",
        background_color="#0000aa",
        height=card_area.get_height() - 40,
        width=surface.get_width() + 1000,
        padding=0,
        max_width=surface.get_width() - 400,
    )

    area_disc = gameMenu.add.button(
        "Discard: " + "00", button_id=prefix + "Disc"
    ).set_selection_effect(None)

    card_area.pack(
        area_draw,
        align=pygame_menu.locals.ALIGN_LEFT,
        vertical_position=pygame_menu.locals.POSITION_CENTER,
    )
    card_area.pack(
        area_hand,
        align=pygame_menu.locals.ALIGN_CENTER,
        vertical_position=pygame_menu.locals.POSITION_CENTER,
    )
    card_area.pack(
        area_disc,
        align=pygame_menu.locals.ALIGN_RIGHT,
        vertical_position=pygame_menu.locals.POSITION_CENTER,
    )

    return card_area

my_map = None

def make_mapArea(minusHeight):
    mapArea = (
        gameMenu.add.frame_h(
            float=True,
            frame_id="map",
            height=surface.get_height() - minusHeight,
            width=surface.get_width(),
            padding=0,
        )
        .set_margin(0, 0)
        .translate(0, minusHeight / 2)
    )
    global my_map
    my_map = Map("maps/default.json", gameMenu, mapArea, node_press)
    return mapArea, my_map

# temp = gameMenu.add.image(
#     image_path="characters\paganini.jpg"
# )
# temp.resize(temp.get_width()/temp.get_height()*100, 100)


make_mainMenu()
# make_gameMenu()
sio.disconnect()
