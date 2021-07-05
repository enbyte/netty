# netty
[![CodeFactor](https://www.codefactor.io/repository/github/enbyte/netty/badge/main)](https://www.codefactor.io/repository/github/enbyte/netty/overview/main)  ![Python3](https://camo.githubusercontent.com/7bd92a3fe06a0419e93f81a09888a1f8a2ca0837d51dcb739356dddd537c1b73/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332d626c75652e7376673f763d31)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/enbyte/netty.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/enbyte/netty/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/enbyte/netty.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/enbyte/netty/context:python)


A simple python library for networking. Not extremely complex, but allows for simple game servers and chat rooms to be hosted.

# Documentation

This example will show you how to make a simple chat room with `netty`.

First, import netty:
```python
import netty
```
Then, choose a port and make a client and a server:
```python
import netty

PORT = 3000

client = netty.connection.Client('', PORT) # args: IP ('' for local), and port.

server = netty.connection.Server(PORT) # args: port to run the server on.
```
Now, we have a client and a server, but they aren't doing anything when they get a message. To do this, we need to add a `onReceive` argument to the client and server.
The `onReceive` is called whenever the client or server receives a packet. 
The client function takes one argument, the message. 
The message is of type `netty.handle.Message` and has a time, uid, and the data sent.

MORE DOCUMENTATION COMING SOON
==============================
