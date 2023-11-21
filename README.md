# netty
[![CodeFactor](https://www.codefactor.io/repository/github/enbyte/netty/badge/main)](https://www.codefactor.io/repository/github/enbyte/netty/overview/main)  ![Python3](https://camo.githubusercontent.com/7bd92a3fe06a0419e93f81a09888a1f8a2ca0837d51dcb739356dddd537c1b73/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332d626c75652e7376673f763d31)

[![forthebadge](https://forthebadge.com/images/featured/featured-powered-by-electricity.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/featured/featured-gluten-free.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/approved-by-veridian-dynamics.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/as-seen-on-tv.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/compatibility-ie-6.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/designed-in-ms-paint.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/does-not-contain-treenuts.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/eicar-antivirus-test-string.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/gluten-free.svg)](https://forthebadge.com)  
[![forthebadge](https://forthebadge.com/images/badges/reading-6th-grade-level.svg)](https://forthebadge.com)  


A simple python library for networking to run chatrooms and small gameservers. Not extremely complex, but allows for simple game servers and chat rooms to be hosted.

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
Now, we have a client and a server, but they aren't doing anything when they get a message. To do this, we need to add a `on_receive` argument to the client and server.
The `on_receive` is called whenever the client or server receives a packet. 
The client function takes one argument, the message. 
The message is of type `netty.handle.Message` and has a time, uid, and the data sent.

MORE DOCUMENTATION COMING SOON
==============================
