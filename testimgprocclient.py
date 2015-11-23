'''
Created on Nov 21, 2015

@author: Alexis
'''
import numpy as np

from socketIO_client import SocketIO, BaseNamespace

game_status = 'new' # statuses are new, none, inprogress, reset
boardisclear = True
oldgamestate = ['empty','empty','empty','empty','empty','empty','empty','empty','empty']
currgamestate = ['empty','empty','empty','empty','empty','empty','empty','empty','empty']
emptystate = ['empty','empty','empty','empty','empty','empty','empty','empty','empty']
boardstate = 0
newestmove = 0
convertedmove = 0
robotmovecomplete = True
getusermovetriggered = False

# nvm, will prob be replaced by on_getusermove
def on_robotcomplete(*args):
    global robotmovecomplete
    print 'Robot move completed, ready to look for user moves'
    robotmovecomplete = True
    check_robotcomplete()
    #run_image_processor() # this will be the function that does the image processing stuff
    
def check_robotcomplete():
    global robotmovecomplete
    global getusermovetriggered
    if(robotmovecomplete == True): # if robot is done, start looking for new user move
        if(getusermovetriggered == True):
            robotmovecomplete = False
            getusermovetriggered = False
            run_image_processor()

def on_getusermove(*args):
    global getusermovetriggered
    getusermovetriggered = True
    print 'get user move request received from server'
    check_robotcomplete()

def on_gameresetcomplete(*args):
    print 'received game_reset_complete event'
    
def on_getboardstate(*args):
    global boardisclear
    global boardstate
    print 'AI/UI is asking for board state'
    run_image_processor_forboardstate()
    if(boardisclear):
        boardstate = '1' # board is empty -- need to reset stuff here
    else:
        boardstate = '1' # board is not empty -- for testing purposes we make it 1; otherwise should be 0
    socketIO.emit('curr_board_state', boardstate)
    
def run_image_processor_forboardstate():
    global oldgamestate
    global currgamestate
    global emptystate
    global boardisclear
    global robotmovecomplete
    
    '''
    
    #x[0:3], y[0:3], image
    x, y, img= find_board2.board_lines('stamp1.jpg')

    #define the sections of our board
    #x1, y1, x2, y2
    section = []
    section.append(img[y[0]:y[1], x[0]:x[1]])#section[0]
    section.append(img[y[0]:y[1], x[1]:x[2]])#section[1]
    section.append(img[y[0]:y[1], x[2]:x[3]])#section[2]
    section.append(img[y[1]:y[2], x[0]:x[1]])#section[3]
    section.append(img[y[1]:y[2], x[1]:x[2]])#section[4]
    section.append(img[y[1]:y[2], x[2]:x[3]])#section[5]
    section.append(img[y[2]:y[3], x[0]:x[1]])#section[6]
    section.append(img[y[2]:y[3], x[1]:x[2]])#section[7]
    section.append(img[y[2]:y[3], x[2]:x[3]])#section[8]

    #save board sections for debugging
    cv2.imwrite('section_0.jpg',section[0]) #save section[0]
    cv2.imwrite('section_1.jpg',section[1]) #save section[1]
    cv2.imwrite('section_2.jpg',section[2]) #save section[2]
    cv2.imwrite('section_3.jpg',section[3]) #save section[3]
    cv2.imwrite('section_4.jpg',section[4]) #save section[4]
    cv2.imwrite('section_5.jpg',section[5]) #save section[5]
    cv2.imwrite('section_6.jpg',section[6]) #save section[6]
    cv2.imwrite('section_7.jpg',section[7]) #save section[7]
    cv2.imwrite('section_8.jpg',section[8]) #save section[8]

    is_x = np.zeros((9,1)) #is this section an X shape?
    is_circle = np.zeros((9,1)) #is this section a circle shape?
    #0 for false and 1 for true

    #set size of lines you want to find
    minLineLength = 5
    maxLineGap = 25
    kernel = np.ones((3,3),np.float32)/9 #kernel smoothing
    k = 0 #loop iterator
    while(k < 9): #9 sections
        #check for circle shapes
        image = cv2.imread('section_%d.jpg'%k,0)
        image = cv2.filter2D(image,-1,kernel) #apply kernel
        circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
        if circles is None: #if array is empty, do nothing
            pass #do nothing
        else:
            is_circle[k] = 1 #we found a circle here
        #sharpen image using blur and unsharp method
        #gaussian_1 = cv2.GaussianBlur(image, (9,9), 10.0)
        #unsharp_image = cv2.addWeighted(image, 1.5, gaussian_1, -0.5, 0, image)
        #apply otsu's robust method for determining dual threshold value
        th, bw = cv2.threshold(image,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #Convert color to gray, image or section[k]?
        #gray = cv2.cvtColor(section[k],cv2.COLOR_BGR2GRAY)
        #unsharp_image is already in grayscale, no need to convert
        #apply filter to find stamp pieces, histogram equalization on greyscale
        #gray = cv2.equalizeHist(gray)
        #hist_eq = cv2.equalizeHist(unsharp_image)
        #edge detection (input,threshold1,threshold2,size_for_sobel_operator)
        #edges = cv2.Canny(gray,50,150,apertureSize = 3)
        edges = cv2.Canny(image,th/2,th) #Otsu's method
        cv2.imwrite('edges_test%d.jpg'%k,edges) #save our image of edges
        #find lines (edges,min_pixels,min_degrees,min_intersections,lineLength,LineGap)
        lines = cv2.HoughLinesP(edges,1,np.pi/180,50,minLineLength,maxLineGap)
        #draw all the lines that lines finds, find slopes of lines
        i = len(lines)
        j = 0
        #slope = np.zeros((lines.shape[0], lines.shape[1], 9)) #(lines found, 1, slope)
        print(lines.shape)
        while(j < i):
            #check for X shapes using line detection
            for x1,y1,x2,y2 in lines[j]: #let's look at the lines in each section
                cv2.line(section[k],(x1,y1),(x2,y2),(0,255,0),2)#green lines
                if (x2 - x1) == 0:
                    slope = 999 #almost infinite slope
                else:
                    slope = (y2 - y1)/float((x2 - x1)) #slope of line
                if ((abs(slope) > 0.05) & (abs(slope) < 20)): #can change the slope factor later
                    is_x[k] = 1 #we found something that might be an X
                j = j + 1
        print("total lines found in section [",k,"] = ",j) #how many lines?
        k = k + 1
    cv2.imwrite('houghlines6.jpg',img) #all the lines we detect saved here
    '''
    #write output
    p_out = ['X','empty','empty','empty','O','empty','empty','empty','empty']
    '''k = 0
    while(k<9):
        if (is_x[k] == 1):
            p_out.append('X')
        elif (is_circle[k] == 1):
            p_out.append('O')
        else:
            p_out.append('empty')    
        k = k + 1
    print('p_out = ', p_out)'''
        
    if(p_out==emptystate):
        robotmovecomplete = True
        boardisclear = True
    else:
        boardisclear = False

    
def run_image_processor():
    global oldgamestate
    global currgamestate
    global emptystate
    global boardisclear
    global robotmovecomplete
    
    '''
    #x[0:3], y[0:3], image
    x, y, img= find_board2.board_lines('stamp1.jpg')

    #define the sections of our board
    #x1, y1, x2, y2
    section = []
    section.append(img[y[0]:y[1], x[0]:x[1]])#section[0]
    section.append(img[y[0]:y[1], x[1]:x[2]])#section[1]
    section.append(img[y[0]:y[1], x[2]:x[3]])#section[2]
    section.append(img[y[1]:y[2], x[0]:x[1]])#section[3]
    section.append(img[y[1]:y[2], x[1]:x[2]])#section[4]
    section.append(img[y[1]:y[2], x[2]:x[3]])#section[5]
    section.append(img[y[2]:y[3], x[0]:x[1]])#section[6]
    section.append(img[y[2]:y[3], x[1]:x[2]])#section[7]
    section.append(img[y[2]:y[3], x[2]:x[3]])#section[8]

    #save board sections for debugging
    cv2.imwrite('section_0.jpg',section[0]) #save section[0]
    cv2.imwrite('section_1.jpg',section[1]) #save section[1]
    cv2.imwrite('section_2.jpg',section[2]) #save section[2]
    cv2.imwrite('section_3.jpg',section[3]) #save section[3]
    cv2.imwrite('section_4.jpg',section[4]) #save section[4]
    cv2.imwrite('section_5.jpg',section[5]) #save section[5]
    cv2.imwrite('section_6.jpg',section[6]) #save section[6]
    cv2.imwrite('section_7.jpg',section[7]) #save section[7]
    cv2.imwrite('section_8.jpg',section[8]) #save section[8]

    is_x = np.zeros((9,1)) #is this section an X shape?
    is_circle = np.zeros((9,1)) #is this section a circle shape?
    #0 for false and 1 for true

    #set size of lines you want to find
    minLineLength = 5
    maxLineGap = 25
    kernel = np.ones((3,3),np.float32)/9 #kernel smoothing
    k = 0 #loop iterator
    while(k < 9): #9 sections
        #check for circle shapes
        image = cv2.imread('section_%d.jpg'%k,0)
        image = cv2.filter2D(image,-1,kernel) #apply kernel
        circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
        if circles is None: #if array is empty, do nothing
            pass #do nothing
        else:
            is_circle[k] = 1 #we found a circle here
        #sharpen image using blur and unsharp method
        #gaussian_1 = cv2.GaussianBlur(image, (9,9), 10.0)
        #unsharp_image = cv2.addWeighted(image, 1.5, gaussian_1, -0.5, 0, image)
        #apply otsu's robust method for determining dual threshold value
        th, bw = cv2.threshold(image,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #Convert color to gray, image or section[k]?
        #gray = cv2.cvtColor(section[k],cv2.COLOR_BGR2GRAY)
        #unsharp_image is already in grayscale, no need to convert
        #apply filter to find stamp pieces, histogram equalization on greyscale
        #gray = cv2.equalizeHist(gray)
        #hist_eq = cv2.equalizeHist(unsharp_image)
        #edge detection (input,threshold1,threshold2,size_for_sobel_operator)
        #edges = cv2.Canny(gray,50,150,apertureSize = 3)
        edges = cv2.Canny(image,th/2,th) #Otsu's method
        cv2.imwrite('edges_test%d.jpg'%k,edges) #save our image of edges
        #find lines (edges,min_pixels,min_degrees,min_intersections,lineLength,LineGap)
        lines = cv2.HoughLinesP(edges,1,np.pi/180,50,minLineLength,maxLineGap)
        #draw all the lines that lines finds, find slopes of lines
        i = len(lines)
        j = 0
        #slope = np.zeros((lines.shape[0], lines.shape[1], 9)) #(lines found, 1, slope)
        print(lines.shape)
        while(j < i):
            #check for X shapes using line detection
            for x1,y1,x2,y2 in lines[j]: #let's look at the lines in each section
                cv2.line(section[k],(x1,y1),(x2,y2),(0,255,0),2)#green lines
                if (x2 - x1) == 0:
                    slope = 999 #almost infinite slope
                else:
                    slope = (y2 - y1)/float((x2 - x1)) #slope of line
                if ((abs(slope) > 0.05) & (abs(slope) < 20)): #can change the slope factor later
                    is_x[k] = 1 #we found something that might be an X
                j = j + 1
        print("total lines found in section [",k,"] = ",j) #how many lines?
        k = k + 1
    cv2.imwrite('houghlines6.jpg',img) #all the lines we detect saved here
    '''
    #write output
    p_out = ['X','empty','empty','empty','O','empty','empty','empty','empty']
    '''k = 0
    while(k<9):
        if (is_x[k] == 1):
            p_out.append('X')
        elif (is_circle[k] == 1):
            p_out.append('O')
        else:
            p_out.append('empty')    
        k = k + 1
    print('p_out = ', p_out)'''
        
    if(p_out==emptystate):
        robotmovecomplete = True
        boardisclear = True
    else:
        boardisclear = False

    if(p_out!=currgamestate):
        find_most_recent(p_out)
    
def convert_newestmove(newest_move):
    global convertedmove
    if(newest_move==1):
        convertedmove = 11
    elif(newest_move==2):
        convertedmove = 12
    elif(newest_move==3):
        convertedmove = 13
    elif(newest_move==4):
        convertedmove = 21
    elif(newest_move==5):
        convertedmove = 22
    elif(newest_move==6):
        convertedmove = 23
    elif(newest_move==7):
        convertedmove = 31
    elif(newest_move==8):
        convertedmove = 32
    elif(newest_move==9):
        convertedmove = 33
    else:
        print 'error with convert_newestmove!!'
    socketIO.emit('new_user_move_found', convertedmove)

# find the most recent move made    
def find_most_recent(p_out):
    global oldgamestate
    global currgamestate
    global emptystate
    global newestmove
    oldgamestate = np.empty_like(currgamestate)
    oldgamestate[:] = currgamestate
    currgamestate = np.empty_like(p_out)
    currgamestate[:] = p_out
    for x in range(0,9):
        if(oldgamestate[x] != currgamestate[x] and currgamestate[x] != 'empty'): # game states are X, O, and empty
            newestmove = x+1 # add 1 to the index to get the board val 1 through 9 rather than 0 through 8
    convert_newestmove(newestmove)

socketIO = SocketIO('Localhost', 3000, BaseNamespace)
socketIO.on('robot_move_complete', on_robotcomplete) # on bot finish do stuff
socketIO.on('game_reset_complete', on_gameresetcomplete)
socketIO.on('get_board_state', on_getboardstate)
socketIO.on('get_user_move', on_getusermove)
socketIO.wait()
