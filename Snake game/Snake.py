from turtle import color
import PySimpleGUI as sg
from time import time
from random import randint


# function to Convert position to pixel
def Convert_pos_to_pixel(cell):
    #size of the apple corresponding to the cell size
    tl = cell[0]*CELL_SIZE,cell[1]*CELL_SIZE 
    br = tl[0]+CELL_SIZE, tl[1]+CELL_SIZE
    return tl,br

def place_apple():
    apple_pos = randint(0, CELL_NUM-1),randint(0, CELL_NUM-1) # when the apple is eaten, it is placed in a random postion in other cells
    while apple_pos in snake_body: # to avoid the apple being on the snake, we create a while loop
        apple_pos = randint(0, CELL_NUM-1),randint(0, CELL_NUM-1)
    return apple_pos

#game constansts
FIELD_SIZE =400 # the size of  the frame
CELL_NUM =20    # Number cells in the frame
CELL_SIZE = FIELD_SIZE/CELL_NUM # for the numbear of pixels per cell
score = 0 # inital value of the score

#Snake itself
snake_body =[(4,4),(3,4),(2,4)] #The snake body is a list that is made up 3 tuples(the head, and the body, and the tail)
Directions ={'Left':(-1,0),'Right':(1,0),'Up':(0,1),'Down':(0,-1)}
direction =Directions['Up']

#Apple
apple_pos = place_apple() # coordinates for the apple position on the graph to a random position when the place apple function is called
apple_eaten =False


sg.theme('Green') # the frame of the game
field = sg.Graph( # this initiates the graph in pysimplegui
    canvas_size= (FIELD_SIZE,FIELD_SIZE),
    graph_bottom_left= (0,0), # the left buttom coordinate origin
    graph_top_right= (FIELD_SIZE,FIELD_SIZE), # the rigth top coordinate origin
    background_color= 'black' # the background color o the game
)
layout=[
    [sg.Text('Score:',font = 'Franklin 15'), sg.Text('output',key = 'Output1',font = 'Franklin 15')],
    [field]
    ]

window = sg.Window('Snake', layout,return_keyboard_events= True)

start_time =time ()
while True:
    event, values =window.read(timeout= 10)
    if event == sg.WIN_CLOSED:break
    #Setting the keyboard input direction
    if event == 'Left:37':direction =Directions['Left']
    if event == 'Up:38':direction = Directions['Up']
    if event == 'Right:39':direction =Directions['Right']
    if event == 'Down:40':direction =Directions['Down']

    time_since_start = time () - start_time # to give you the time elapsed since star
    if time_since_start >= 0.2: # speed of the snake
        start_time = time() 

        #apple snake collision
        if snake_body[0] == apple_pos:
            apple_pos = place_apple()
            apple_eaten = True
            if apple_eaten == True:
                score = score + 1

        window['Output1'].update(score)
               # print(output1)

            


        #snake update /positioning the snake
        new_head = (snake_body[0][0]+ direction[0],snake_body[0][1]+ direction[1])
        snake_body.insert(0,new_head) # growth o snake
        if not apple_eaten:
            snake_body.pop()
        apple_eaten = False

        #Check death
        if not 0<= snake_body[0][0] <= CELL_NUM -1 or \
            not 0<= snake_body[0][1] <= CELL_NUM -1 or \
            snake_body[0] in snake_body[1:]:
            break

       
        field.DrawRectangle((0,0),(FIELD_SIZE,FIELD_SIZE),'black') # This eliminates the body in the previous cell using a black fr

        #size of the apple corresponding to the cell size
        tl,br =Convert_pos_to_pixel(apple_pos) #calling the covert function
        field.DrawRectangle(tl,br,'red')
    #draw snake
    for index,part in enumerate(snake_body):
        tl, br = Convert_pos_to_pixel(part)
        color = 'yellow' if index == 0 else 'green' # give the head of the snake color yellow and the rest of the body should be green
        field.DrawRectangle(tl,br,color)
window.close()