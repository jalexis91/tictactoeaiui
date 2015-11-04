'''
Created on Oct 22, 2015

@author: Alexis
'''

from socketIO_client import SocketIO, BaseNamespace

def on_aimove(*args):
    print 'got ai move: ', args[0] # gets first arg (i.e. the move we want)
    socketIO.emit('robot_move_complete') # send msg to img processor when done
    # making move so that it knows to start looking for moves again

socketIO = SocketIO('Localhost', 3000, BaseNamespace)
socketIO.on('aimove', on_aimove)
socketIO.wait()
