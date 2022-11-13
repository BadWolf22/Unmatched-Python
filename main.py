# This file is for debug purposes *only*
# It starts both the client and the server. When the client is closed, both the client and server are stopped!

import os

# https://stackoverflow.com/a/11615580
os.system("start cmd /c python server.py")
os.system("start cmd /c python client.py")
os.system("start /wait cmd /c python client.py")