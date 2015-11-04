'''
Created on Oct 28, 2015

@author: Alexis
'''
from socketIO_client import SocketIO, BaseNamespace

game_status = 'new' # statuses are new, none, inprogress, reset
boardisclear = True
oldgamestate = [0,0,0,0,0,0,0,0,0]
currgamestate = [0,0,0,0,0,0,0,0,0]
boardstate = ''
newestmove = ''
robotmovecomplete = False
getusermovetriggered = False

# nvm, will prob be replaced by on_getusermove
def on_robotcomplete(*args):
    print 'Robot move completed, ready to look for user moves'
    robotmovecomplete = True
    check_robotcomplete()
    #run_image_processor() # this will be the function that does the image processing stuff
    
def check_robotcomplete():
    if(robotmovecomplete == True): # if robot is done, start looking for new user move
        if(getusermovetriggered == True):
            robotmovecomplete = False
            getusermovetriggered = False
            socketIO.emit('new_user_move_found', newestmove)
    else:
        ''' if robot isn't done yet set new listener inside this else
            socketIO.on('robot_move_complete', on_robotcomplete)
            if not done yet exit function and wait for robot complete event '''
    
def on_getusermove(*args):
    print 'get user move request received from server'
    getusermovetriggered = True
    check_robotcomplete()
    ''''if img processor has detected a new move it sends it to 
        the AI/UI; if it hasn't found a new move yet it keeps waiting
        before sending convert move to RC format '''

def on_gameresetcomplete(*args):
    print 'received game_reset_complete event'
    
def on_getboardstate(*args):
    print 'AI/UI is asking for board state'
    check_board_state()
    if(boardisclear):
        boardstate = '1' # board is empty -- need to reset stuff here
    else:
        boardstate = '0' # board is not empty
    socketIO.emit('curr_board_state', boardstate)  
    ''' when AI/UI asks for the board state send state
        as either 'empty' or 'notempty'  
        get this by running the img processor
        if board isn't empty ai/ui will alert the user that they need
        to clear the board before continuing
        make sure to only send curr_board_state when it is asked for
        otherwise it will restart the current game in the app '''
    
# run img processor stuff
def run_image_processor():
    imgprocessor_move = 'new stuff'
    boardisclear = True # change this based on img processor results
    socketIO.emit('usermove', imgprocessor_move) # if the board is empty, boardisclear is True; otherwise it's false
    #basically just emit 'usermove' with the new move value 
    #whenever you're ready to send your move
    
# check the board state to see if it is empty
def check_board_state():
    boardstate = ''
    boardisclear = True

# find the most recent move made    
def find_most_recent():
    for x in range(0,9):
        if(oldgamestate[x] != currgamestate[x] and currgamestate[x] != 'empty'): # game states are X, O, and empty
            newestmove = x+1 # add 1 to the index to get the board val 1 through 9 rather than 0 through 8

socketIO = SocketIO('Localhost', 3000, BaseNamespace)
socketIO.on('robot_move_complete', on_robotcomplete) # on bot finish do stuff
socketIO.on('game_reset_complete', on_gameresetcomplete)
socketIO.on('get_board_state', on_getboardstate)
socketIO.on('get_user_move', on_getusermove)
socketIO.wait()
