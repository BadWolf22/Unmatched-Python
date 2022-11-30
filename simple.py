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

menus = (mainMenu, roomMenu, charMenu, gameMenu)

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
    players[character] = Character.assignCharacter('characters/phineasFerb.json')
    print(character)
######################################


def connect_to_server(*args):
    # print(f"Connecting to: {serverIP.get_value()}")
    sio.connect(args[0].get_value())
    mainMenu.toggle()
    make_roomMenu()
    pass


def connect_to_room(*args):
    sio.emit("joinroom", args[0].get_value())
    roomMenu.toggle()
    make_charMenu()
    pass

players = dict()

def select_character(*args):
    global players
    sio.emit("char", args[0])
    charMenu.toggle()
    make_gameMenu()
    pass

def send_message():
    sio.emit("message", "hiii")
    pass


def change_resolution():
    global RESOLUTION_INDEX
    RESOLUTION_INDEX = (RESOLUTION_INDEX + 1) % len(RESOLUTIONS)
    pygame.display.set_mode(RESOLUTIONS[RESOLUTION_INDEX])
    for menu in menus:
        menu.resize(surface.get_width(), surface.get_height())
    pass


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
    charMenu.add.button("Char1", select_character, "char1")
    charMenu.add.button("Char2", select_character, "char2")
    charMenu.add.button("Quit", pygame_menu.events.EXIT)
    charMenu.mainloop(surface)

def make_gameMenu():
    enemy_info = make_cardArea("#ff0000", "enemy")
    your_info = make_cardArea("#00aa00", "player")
    your_info.translate(0, surface.get_height() - your_info.get_height())
    map_area = make_mapArea(enemy_info.get_height()+your_info.get_height())

    # gameMenu.add.button(
    #     "test", send_message, float=True, align=pygame_menu.locals.ALIGN_LEFT
    # ).translate(300, 300)

    gameMenu.mainloop(surface)

def make_cardArea(color, prefix):
    card_area = gameMenu.add.frame_h(
        background_color=color,
        float=True,
        height=int(surface.get_height() / 5),
        width=surface.get_width(),
    ).set_margin(0, 0)
    area_draw = gameMenu.add.button("Draw: 30", button_id=prefix+"Draw").set_selection_effect(None)
    area_hand = gameMenu.add.frame_h(
        frame_id=prefix+"Hand",
        background_color="#0000aa",
        height=card_area.get_height()-40,
        width=surface.get_width()+1000,
        padding=0,
        max_width=surface.get_width()-400
    )

    area_disc = gameMenu.add.button("Discard: " + "00", button_id=prefix+"Disc").set_selection_effect(None)

    # players[prefix].deck.draw(gameMenu, area_hand, prefix)
    # players[prefix].deck.draw(gameMenu, area_hand, prefix)
    # players[prefix].deck.draw(gameMenu, area_hand, prefix)
    # players[prefix].deck.draw(gameMenu, area_hand, prefix)
    # players[prefix].deck.draw(gameMenu, area_hand, prefix)
    # players[prefix].deck.draw(gameMenu, area_hand, prefix)
    # players[prefix].deck.draw(gameMenu, area_hand, prefix)

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

def make_mapArea(minusHeight):
    mapArea = gameMenu.add.frame_h(
        float=True,
        frame_id="map",
        height=surface.get_height()-minusHeight,
        width=surface.get_width(),
        padding=0,
    ).set_margin(0, 0).translate(0, minusHeight/2)
    my_map = Map("maps/default.json", gameMenu, mapArea)
    return mapArea, my_map

# temp = gameMenu.add.image(
#     image_path="characters\paganini.jpg"
# )
# temp.resize(temp.get_width()/temp.get_height()*100, 100)


make_mainMenu()
# make_gameMenu()
sio.disconnect()
