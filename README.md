# Unmatched-Python
A version of the unmatched board game created in Python with custom characters and features.  
Built by Joel and Matthew for CS501.

# Contributing
Current required package installation.
```shell
pip install -r requirements.txt
```
Run a client instance with: `python client.py`.  
Run a server instance with: `python server.py`.  
Run a debug instance (1 server and 2 clients) with: `python main.py`.  


## PyGame not updated in Pip
It looks like Python 3.11 is too new, and so PIP has not been updated with the latest version of PyGame. So I grabbed the wheel file and installed it manually. Works like a charm. [Source](https://stackoverflow.com/a/69353414)  
```shell
pip install ./pygame-2.1.2-cp311-cp311-win_amd64.whl
```

## Python-Socketio
For client communication, we will be using the [Python-Socketio](https://python-socketio.readthedocs.io/en/latest/index.html) library.
