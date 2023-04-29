'''
The goal of this project is to create a simple game of snake
using GUI to create a nice user interface, 2d animations using shapes
and various functions and methods to give the user control of the game
and score the progress. GOOD LUCK ME!
'''

from tkinter import *
import random


'''Here are the things we will need outside of the Tkinter window'''

'''constants'''
'''These are defined befor everything else, and can be easily
referred to in the code to keep values similar across the entire code.'''
GAME_WIDTH = 700    #Width of the game window
GAME_HEIGHT = 700   #Height of the game window
SPEED = 100          #The update speed of the window
SPACE_SIZE = 50     #The size of the objects in the window
#this will also be useful for defining a limited number of places
#objects can spawn, see more in the fruits class
BODY_PARTS = 3      #The amount of body parts the snake starts with
SNAKE_COLOR = "#00FF00" #the color of the snake
FOOD_COLOR = "#FF0000"  #Color of the food objects
BACKGROUND_COLOR = "black"

'''classes'''
'''In this instance, we will need 2 classes'''
class Snake:
    #As usual, create a constructor.
    def __init__(self):
        #set constructor objects body_size to value of BODY_PARTS
        self.body_size = BODY_PARTS
        #We need a list of coordinates, for now its empty to be set below
        self.coordinates = []
        #we need a list of squares, for now its empty to be set below
        self.squares = []

        #to create a list of coordinates
        #we will form a itteration loop in range 0-value of BODY_PARTS
        for i in range(0, BODY_PARTS):
            #for each itteration, append coordinates with new list
            #start at 0,0 so the snake appears in the top left
            self.coordinates.append([0,0])
        #                        list ^
        #Note that we use x, y because of the list above
        #list V
        for x, y in self.coordinates: #This foor loop will handle creating new squares to form the snake
            #each square will be created with tkinter,
            # they will start at x(0) y(0)
            # and have the size of x(0)+SPACE_SIZE(50), and y(0)+SPACE_SIZE(50)
            # Furthermore they will have a fill color of our defined SNAKE_COLOR
            # and assign them a tag called snek for easy refference in code.
            square = canvas.create_rectangle(x, y,  #spawn coordinates(0,0)
                                             x + SPACE_SIZE, #size x axis (0+50)
                                             y + SPACE_SIZE, #size y axis (0+50)
                                             fill = SNAKE_COLOR, #color (green)
                                             tag='snek')    #tag for referrence
            #append the square with the new square.
            self.squares.append(square)

class Food:
    #First, we create the constructor:
    def __init__(self):
        #Here, we define a spawn point for the object.
        '''
        Note that in order to bring some ease of access
        to the game and prevent things from spawning on every
        single pixel, dividing the game space up in chunks will
        make it much more playable, this can be done by dividing
        the play space, eg. GAME_WIDTH(700) with SPACE_SIZE(50) = 14
        possible places to spawn in the game x axis.
        -1 to make it exclusive(exluding the far borders)
        *SPACE_SIZE to scale it depending on the object size in the game
        '''
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) -1) * SPACE_SIZE
        '''repeat for y axis'''
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) -1) * SPACE_SIZE

        #Now that we generated a set of coordinates to spawn
        #we tell the object to spawn there:
        self.coordinates = [x, y]

        canvas.create_oval(x, y, (x + SPACE_SIZE), (y + SPACE_SIZE), fill=FOOD_COLOR, tag="food")

'''functions'''
'''We will need a variety of functions to take care of different parts'''
'''of the game.'''
#First, is the next_function, to handle each move
def next_turn(snake, food):

    #first, we need to unpack the coordinates of the head of the snake
    #the first square, and asign them to coordinates x, and y
    x, y = snake.coordinates[0]
    #From here we create some if/else statements
    #to determine which way were going in the space
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction =="left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    #now insert the direction to the coordinates of the snake
    #at index 0 (the head, first square)
    snake.coordinates.insert(0,(x,y))

    #and create a new square(snake tail) at the start location.
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

    #update the existing list with a new square
    snake.squares.insert(0, square)

    #Check if snake x,y coordinates == food x,y coordinates
    #if they do, they are overlapping, and snake ate fruit.
    if x == food.coordinates[0] and y == food.coordinates[1]:
        #so when they overlap, we grab the global score
        global score
        #increment it by 1
        score += 1
        #and update the label with the new score
        label.config(text="Score:{}".format(score))
        #we also delete the canvas using the tag
        canvas.delete("food")
        #and create a new one using the class(AMAZING!)
        food = Food()
    #If we do NOT eat food, we instead update the snake
    else:
        #We delete the last part of the snake in the list
        #both its coordinates
        del snake.coordinates[-1]

        #its canvas entry
        canvas.delete(snake.squares[-1])

        #and the list entry
        del snake.squares[-1]

    #lastly, check for a collision with the check_collisions function, with the argument of snake
    if check_collisions(snake):
        #if its True(you collide) its game over bro
        game_over()
    else:

        #After doing this, we wanna do it again, we do this with window.after
        #with arguments SPEED(game speed), next_turn(the function repeats),
        #with arguments snake, food
        window.after(SPEED,next_turn, snake, food)

#This function will handle the direction controls of the snake
def change_direction(new_direction):

    #first pass in the old direction from global, so we can change it.
    global direction

    #basically we want to check if the new and old directions conflict
    #if they dont, we will reassign the direction from global
    if new_direction == 'left':
        if direction !='right':
            direction = new_direction

    #We do this for all of them
    elif new_direction == 'right':
        if direction !='left':
            direction = new_direction

    elif new_direction == 'up':
        if direction !='down':
            direction = new_direction

    elif new_direction == 'down':
        if direction !='up':
            direction = new_direction

#This function will handle collision checks between the walls and the snake
def check_collisions(snake):
    #first, unpack the x and y coordinates of the snake head(first square index 0 of list)
    x, y = snake.coordinates[0]

    #For the x axis, check if the x values goes below 0(left of screen) or higher than the game_width(right of screen)
    if x < 0 or x >= GAME_WIDTH:
        print("COLLISION DETECTED, GAME OVER") #Testing purposes we print to console if this is detected
        #Return function as True if this is detected
        return True
    #same here
    elif y < 0 or y >= GAME_HEIGHT:
        print("COLLISION DETECTED, GAME OVER") #Testing purposes we print to console if htis is detected.
        #return function as true if detected
        return True

    #to check if the snake touches itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Body bite! Game over!")
            #return function as true if detected
            return True
    #return function as False if none of the above is detected
    return False

#the game_over function will handle what happens in the event of a game_over, the cleanup function basically
def game_over():
    #delete the entire canvas
    canvas.delete(ALL)
    #create a new canvas with some text.
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,
                       font = ('consolas',60), text="GAME OVER MAN!", fill="red",tag='game over')

'''Tkinter GUI'''
'''And here, the GUI set starts:'''

window = Tk()
window.title("DKM Snek game!")  #Set window title
window.resizable(False, False)  #set rezisability on X and Y axis.

score = 0   #Initial score at the start of the game
direction = 'down' #Initial direction of movement at start

#Label that will handle the display of the score
label = Label(window, text="Score:{}".format(score),font=('consolas',40))
label.pack()

#This here will be the game window, where the snake will move around
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

#update the window, so that it renders everything till here
window.update()

#The below code will find the size of the screen
#and the window of the game
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#We then define x and y as the screen width/height divided by 2 and minus each other
#This is effectively the center of the screen, on any screen.
x = int((screen_width/2) - (screen_width/2))
y = int((screen_height/2) - (screen_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#We also need to bind some keys to control the snake
#this can be done by using a lambda function, that calls the
#change_direction funtions, when a button is pressed(event)
window.bind('<Left>', lambda event:change_direction('left'))
window.bind('<Right>', lambda event:change_direction('right'))
window.bind('<Up>', lambda event:change_direction('up'))
window.bind('<Down>', lambda event:change_direction('down'))

#Now we create the snake object, using the class/constructor we made
#up top.

snake = Snake()

#And again, for the food object, using the Food class/constructor.
food = Food()

#call the next_turn function to initate the, well... next turn.
next_turn(snake, food)

window.mainloop()

'''BOOM done, I did iiit :3'''