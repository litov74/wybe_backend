import eventlet
import socketio
import variables
from helper import Helper
import concurrent.futures as cf
import logging
import threading

logger_format = '%(asctime)s:%(threadName)s:%(message)s'
logging.basicConfig(format=logger_format, level=logging.INFO, datefmt="%H:%M:%S")

io = socketio.Server()
app = socketio.WSGIApp(io)



@io.event
async def connect(sid, environ):
    userId = environ['HTTP_USERID']

    variables.userIds[sid] = userId
    variables.socketIds[userId] = sid
    variables.userRelationships[sid] = environ['HTTP_REMOTEID']

    await print('connect', sid)


@io.event
async def touches(sid, data):
    socketId = Helper.get_socket_id(variables.userRelationships[sid])
    await io.emit('remoteTouches', data=data, to=socketId)
    await print(data)


@io.event
async def disconnect(sid):
    userId = Helper.get_user_id(sid)
    remoteId = variables.userRelationships[sid]

    try:
        socketId = Helper.get_socket_id(remoteId)
        await io.emit('finish', to=socketId)
    except:
        pass

    del variables.userIds[sid]
    del variables.socketIds[userId]
    del variables.userRelationships[sid]

    await print('disconnect', sid)

eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)


if __name__ == "__main__":
    logging.info("Server has started")
    with cf.ProcessPoolExecutor as executor:
        out = executor.submit(connect, touches, disconnect)
        eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)

