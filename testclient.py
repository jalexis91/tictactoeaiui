# ECEN 404
# Team 2
# Matthew Fischer

import socket
from threading import Thread
from Adafruit_PWM_Servo_Driver import PWM
from socketIO_client import SocketIO, BaseNamespace
import time

base = 15                               # channel number for base                               
shld = 14                               # channel number for shoulder
elbow = 13                              # channel number for elbow
wrist = 12                              # channel number for wrist
pinch = 11                              # channel number for the wrist

#lastmove[9]                             # keeps hold of moves made by the robot to prevent playing in the same position on accident

basePos = 0                             #Keeps track of the position of the base servo           
shldPos = 0                             #Keeps track of the position of the shld servo
elbowPos = 0                            #Keeps track of the position of the elbow servo
wristPos = 0                            #Keeps track of the position of the wrist servo
pinchPos = 600                          #Keeps track of the position of the pinch servo


def setServoPulse(channel,pulse):   
    pulseLength = 1000000
    pulseLength /= 100
    pulseLength /= 4096
    pulse *=1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)
def stamp(shldPos):
    s = shldPos
    for i in range(0, 60, 5):
        s = s - 5
        pwm.setPWM(shld, 0, s)
        time.sleep(.1)
    time.sleep(1)
    for j in range(0, 60, 5):
        s = s + 5
        pwm.setPWM(shld, 0, s)
        time.sleep(.1)

    pwm.setPWM(shld,0, shldPos)

def start():
    # this is the starting position for the arm to move to during startup
    print('Initiate Start-up')  
##    for k in range(700,625,-10):    
##        pwm.setPWM(elbow, 0, k) 
##        time.sleep(.1)  
##    for j in range(400,645,5):
##        pwm.setPWM(shld, 0, j)
##        time.sleep(.1)
##    for i in range(600,250,-10):
##        pwm.setPWM(base, 0, i)
##        time.sleep(.1)
##    pwm.setPWM(wrist,0, 250)
##    time.sleep(1)
##    pwm.setPWM(pinch, 0, 600)
##    time.sleep(1)
    pwm.setPWM(base, 0, 250)
    pwm.setPWM(shld, 0, 640)
    pwm.setPWM(elbow, 0, 625)
    pwm.setPWM(wrist, 0, 250)

    basePos = 250
    shldPos = 64
    elbowPos = 625
    wristPos = 250

def moveRest(basePos, shldPos, elbowPos, wristPos, pinchPos):

    print('Returning Home')
    print 'BasePos', basePos
    print 'Shoulder Pos', shldPos
    print 'Elbow Pos', elbowPos
    print 'Wrist Pos', wristPos
    
    # Shoulder position reset **********************************************************
    if shldPos < 640:
            print('Shoulder Position is less than Rest Position')
            for i in range(shldPos, 640, 10):
                pwm.setPWM(shld, 0, i)
                time.sleep(.1)
    else:
            print('Shoulder Position is greater than Rest Position')
            for i in range(shldPos, 640, -10): #it should not be able to get here technically
                pwm.setPWM(shld, 0, i)
                time.sleep(.1)
    # Elbow Position reset **************************************************************
    if elbowPos < 625:
            print('Elbow Position is less than Rest Position')
            for j in range(elbowPos, 625, 10):
                pwm.setPWM(elbow, 0, j)
                time.sleep(.1)
    else:
            print('Elbow Position is greater than Rest Position')
            for i in range(elbowPos, 625, -10): 
                pwm.setPWM(elbow, 0, i)
                time.sleep(.1)
    # Base Position Reset ***************************************************************
    for k in range(basePos, 250, -10):
        pwm.setPWM(base,0, k)
        time.sleep(.1)
    pwm.setPWM(wrist, 0, 250)
    
    #i Shouldnt have to update pinch ever
        
def move1():
    # moves to position 1 of the game board
    print('Moving to position 1!')
    w = 380 #posotion for the wirst
    pwm.setPWM(wrist, 0, w)
    wristPos = w
    time.sleep(.1)
	
    for i in range(0, 45, 5):  #trying to move all the servos at the same time for step 1
        b = 250 + i
        pwm.setPWM(base, 0, b)
        s = 645 - i
        pwm.setPWM(shld, 0, s)
        e = 625 - i
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
    
    for i in range(0, 40, 5):  #trying to move all the servos at the same time for step 2
        b = 290 + i
        pwm.setPWM(base, 0, b)
        s = 605 - i
        pwm.setPWM(shld, 0, s)
        time.sleep(.1)
        shldPos = s
        
    for i in range(0, 260, 10):  #trying to move all the servos at the same time for step 3
        b = 325 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b

    stamp(shldPos)

    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)

def move2():
    # moves to position 2 of the game board
    print('Moving to position 2!')
    w = 380 #posotion for the wirst
    pwm.setPWM(wrist, 0, w)
    time.sleep(.1)
    wristPos = w
    
    for i in range(0, 45, 5):  #trying to move all the servos at the same time for step 1
        b = 250 + i
        pwm.setPWM(base, 0, b)
        s = 645 - i
        pwm.setPWM(shld, 0, s)
        e = 625 - i
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
    
    for i in range(0, 40, 5):  #trying to move all the servos at the same time for step 2
        b = 290 + i
        pwm.setPWM(base, 0, b)
        s = 605 - i
        pwm.setPWM(shld, 0, s)
        time.sleep(.1)
        shldPos = s
        
    for i in range(0, 300, 5):  #trying to move all the servos at the same time for step 3
        b = 325 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b

    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)

def move3():
    # moves to position 3 of the game board
    print('Moving to position 2!')
    
    w = 380 #posotion for the wirst
    pwm.setPWM(wrist, 0, w)
    time.sleep(.1)
    wristPos = w
    for i in range(0, 50, 10):  #trying to move all the servos at the same time for step 1
        b = 250 + i
        pwm.setPWM(base, 0, b)
        s = 645 - i
        pwm.setPWM(shld, 0, s)
        e = 625 - i
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
    
    for i in range(0, 30, 5):  #trying to move all the servos at the same time for step 2
        b = 290 + i
        pwm.setPWM(base, 0, b)
        s = 605 - i
        pwm.setPWM(shld, 0, s)
        time.sleep(.1)
        shldPos = s
        
    for i in range(0, 350, 5):  #trying to move all the servos at the same time for step 3
        b = 325 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b

    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)

def move4():
    # moves to position 4 of the game board
    print('Moving to position 4!')
    pwm.setPWM(wrist, 0, 440)
    time.sleep(.1)
    wristPos = 440
    for i in range(0, 80, 5):  #trying to move all the servos at the same time for step 1
        b = 250 + i
        pwm.setPWM(base, 0, b)
        s = 645 - i
        pwm.setPWM(shld, 0, s)
        e = 625 + i
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
        shldPos = s
        
    for i in range(0, 240, 5):  #trying to move all the servos at the same time for step 3
        b = 325 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b

    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)

        
def move5():
        # moves to position 5 of the game board
    print('Moving to position 5!')
        
    pwm.setPWM(wrist,0, 440)  ## sets the position of the wrist
    wristPos = 440
    #Stage 1
    for i in range(0, 80, 10):
        b = 250 + i
        s = 645 - i
        e = 625 + i
        pwm.setPWM(base, 0, b)
        pwm.setPWM(shld, 0, s)
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        shldPos = s
    #stage 2
    for i in range(0, 20, 10):
        b = 320 + i
        e = 695 + i
        pwm.setPWM(base, 0, b)
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
    #stage 3
    for i in range(0, 300, 10):
        b = 330 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b
        
    #Here i need to call the stamp function whenever that is actally made
    #time.sleep(2)
    #not i return to rest
    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)


def move6():
        # moves to position 6 of the game board
    print('Moving to position 6!')
    
    pwm.setPWM(wrist,0, 440)  ## sets the position of the wrist
    wristPos = 440
    
    #Stage 1
    for i in range(0, 80, 10):
        b = 250 + i
        s = 645 - i
        e = 625 + i
        pwm.setPWM(base, 0, b)
        pwm.setPWM(shld, 0, s)
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
        shldPos = s
    #stage 2
    for i in range(0, 360, 10):
        b = 330 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b
    #Here i need to call the stamp function whenever that is actally made
    time.sleep(2)
    #not i return to rest
    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)

def move7():
        # moves to position 7 of the game board
    print('Moving to position 7!')
    
    pwm.setPWM(wrist, 0, 440)
    wristPos = 440
    #stage 1
    for i in range(0, 50, 5):
        b = 250 + i
        s = 645 - i
        e = 625 + i
        pwm.setPWM(base, 0, b)
        pwm.setPWM(shld, 0, s)
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        shldPos = s
    #stage 2
    for i in range(0, 110, 5):
        b = 295 + i
        e = 670 + i
        pwm.setPWM(base, 0, b)
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
    #stage 3
    for i in range(0, 150, 10):
        b = 400 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b
    #wait for action...
    time.sleep(2)
    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)
	
def move8():
    print('Moving to position 8!')
    
    pwm.setPWM(wrist, 0, 475)
    wristPos = 475
    
    #stage 1
    for i in range(0, 40, 10):
        b = 250 + i
        s = 645 - i
        e = 625 + i
        pwm.setPWM(base, 0, b)
        pwm.setPWM(shld, 0, s)
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        shldPos = s
    #stage 2
    for i in range(0, 150, 5):
        b = 280 + i
        e = 655 + i
        pwm.setPWM(base, 0, b)
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
    #stage 3
    for i in range(0, 200, 10):
        b = 425 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b
    #wait for action...
	#time.sleep(2)
    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)
   
def move9():
        # moves to position 9 of the game board
    print('Moving to position 9!')

    pwm.setPWM(wrist, 0, 455)
    time.sleep(.5)
    wristPos = 455
    
    for i in range(0, 40, 5):  #tring to move all the servos at the same time for step 1
        b = 250 + i
        pwm.setPWM(base, 0, b)
        s = 645 - i
        pwm.setPWM(shld, 0, s)
        e = 625 + i
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        shldPos = s
    
    for i in range(0, 130, 5):  #tring to move all the servos at the same time for step 2
        b = 285 + i
        pwm.setPWM(base, 0, b)
        e = 660 + i
        pwm.setPWM(elbow, 0, e)
        time.sleep(.1)
        elbowPos = e
        
    for i in range(0, 300, 10):  #tring to move all the servos at the same time for step 3
        b = 410 + i
        pwm.setPWM(base, 0, b)
        time.sleep(.1)
        basePos = b
    
    moveRest(basePos,shldPos,elbowPos,wristPos,pinchPos)

def on_aimove(*args):
    print 'got ai move: ', args[0] # gets first arg (i.e. the move we want)
    #while 1:
    x = args[0] #int(input("Please enter a position number (1-9)"))
    if x == "11":
        move1()
    elif x == "12":
        move2()
    elif x == "13":
        move3()
    elif x == "21":
        move4()
    elif x == "22":
        move5()
    elif x == "23":
        move6()
    elif x == "31":
        move7()
    elif x == "32":
        move8()
    elif x == "33":
        move9()
    else:
        print("please print a valid number next time!")

    socketIO.emit('robot_move_complete') # send msg to img processor when done
    # making move so that it knows to start looking for moves again

pwm = PWM(0x40)
pwm.setPWMFreq(100)
start()
socketIO = SocketIO('Localhost', 3000, BaseNamespace)
socketIO.on('aimove', on_aimove)
socketIO.wait()
