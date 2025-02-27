from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

# Window dimensions and radius of the circular arena
W_Width, W_Height = 500, 500
RADIUS = 150  # Radius of the circular arena
button_x = 0
button_y = W_Height - 50
button_width = 50
button_height = 30
exit_button_size = 30
exit_button_x = W_Width - 40
exit_button_y = W_Height - 40

play_pause_button_x = (W_Width -30) // 2
play_pause_button_y = W_Height - 70
play_pause_button_size = 60
# Snake properties
snake = [(W_Width // 2, W_Height // 2 + RADIUS)]  # Initial position on the circle
snake_dir = (0, -1)  # Initial direction (down)
snake_speed = 3  # Speed of movement
food_x, food_y = None, None
food_eaten = True
pause=False
score=0
gameover=False

def draw_point(x, y,a=None):
    glBegin(GL_POINTS)
    if a:
        glColor3f(0, 0, 1)
    glVertex2i(x, y)
    glEnd()


def set_point_size(size):
    glPointSize(size)

def draw_circle_midpoint(xc, yc, r):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        draw_point(xc + x, yc + y)
        draw_point(xc - x, yc + y)
        draw_point(xc + x, yc - y)
        draw_point(xc - x, yc - y)
        draw_point(xc + y, yc + x)
        draw_point(xc - y, yc + x)
        draw_point(xc + y, yc - x)
        draw_point(xc - y, yc - x)

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
def check(x,y):

    if (125 <= x <= 195) and (275<=y<=285):  #food radius is 5
        return 1
    elif (185<= x <= 195) and (275 <= y <= 345):
        return 1
    elif (295 <= x <= 365) and (275<= y <= 285):
        return 1
    elif (295<= x <= 305) and (275 <= y <= 345):
        return 1
    elif (125 <= x < 195) and (215<= y <= 225):
        return 1
    elif (185<= x <= 195) and (155 <= y <= 225):
        return 1
    elif (295 <= x <= 365) and (215<= y <= 225):
        return 1
    elif (295<= x <= 305) and (155 <= y <= 225):
        return 1
    return 0

def spawn_food():
    global food_x, food_y, food_eaten
    if food_eaten:
        while True:
            angle = random.uniform(0, 2 * math.pi)
            radius = random.randint(10, RADIUS - 10)
            #while True:
            food_x = int(W_Width // 2 + radius * math.cos(angle))
            food_y = int(W_Height // 2 + radius * math.sin(angle))
            s=check(food_x,food_y)
            if s!=1:
                break

        food_eaten = False
def draw_line(x1, y1, x2, y2):
   # glBegin(GL_POINTS)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        draw_point(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
   # glEnd()


def barrier():
    if not gameover:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(1.0, 0, 0)

    draw_line(130, 280, 190, 280)
    draw_line(190, 280, 190, 340)

    draw_line(300, 280, 360, 280)
    draw_line(300, 280, 300, 340)

    draw_line(130, 220, 190, 220)
    draw_line(190, 220, 190, 160)

    draw_line(300, 220, 360, 220)
    draw_line(300, 220, 300, 160)

def draw_restart_button():
    global button_x,button_width,button_y,button_height
    glColor3f(0, 1, 1)
    draw_line(button_x + button_width+25, button_y + button_height //2,  button_x + button_width - button_height,  button_y + button_height // 2) #arrow line
    draw_line(button_x + button_width- button_height, button_y + button_height // 2, (button_x + button_width - button_height+button_x + button_width + button_height)/2,  (button_y + button_height // 2 ) +20)
    draw_line(button_x + button_width - button_height, button_y + button_height // 2,(button_x + button_width - button_height + button_x + button_width + button_height) / 2,(button_y + button_height // 2) - 20)



def draw_exit_button():
    glColor3f(1, 0, 0)
    draw_line(exit_button_x - exit_button_size // 2, exit_button_y - exit_button_size // 2,
              exit_button_x + exit_button_size // 2, exit_button_y + exit_button_size // 2)
    draw_line(exit_button_x + exit_button_size // 2, exit_button_y - exit_button_size // 2,
              exit_button_x - exit_button_size // 2, exit_button_y + exit_button_size // 2)


def draw_play_pause_button():
    global pause
    if not gameover:
        glColor3f(1, 0.75, 0)
        global pause
        if  not pause:
           draw_line(play_pause_button_x,490,play_pause_button_x,440)
           draw_line(play_pause_button_x+25, 490, play_pause_button_x+25, 440)


        else:
            draw_line(play_pause_button_x,490,play_pause_button_x,440)
            draw_line(play_pause_button_x, 490, play_pause_button_x+40, 465)
            draw_line(play_pause_button_x, 440, play_pause_button_x+40, 465)
def exit_game():
    print(f"Goodbye! Final Score: {score}")
    glutLeaveMainLoop()

def mouseListener(button, state, x, y):
    global pause,exit_button_x,exit_button_size,exit_button_y,W_Height



    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if button_x <= x <= button_x + button_width+27 and button_y <= W_Height - y <= button_y + button_height:
            #print("aaaaaqqq")
            restart_game()

        if (exit_button_x - exit_button_size // 2 <= x <= exit_button_x + exit_button_size // 2) and \
                (exit_button_y - exit_button_size // 2 <= W_Height - y <= exit_button_y + exit_button_size // 2):
            exit_game()


        if (play_pause_button_x <= x <= play_pause_button_x + play_pause_button_size) and \
                (play_pause_button_y <= W_Height - y <= play_pause_button_y + play_pause_button_size):
            if pause :
                pause=False
            else:
                pause=True
            print("Game Paused" if pause else "Game Resumed")

        glutPostRedisplay()

def restart_game():
    global snake, snake_dir, snake_speed, food_x, food_y, food_eaten,pause,gameover,score

    snake = [(W_Width // 2, W_Height // 2 + RADIUS)]  # Reset snake position

    snake_dir = (0, -1)  # Reset direction
    snake_speed = 3  # Reset speed
    food_x, food_y = None, None  # Clear food
    food_eaten = True  # Prepare to spawn new food
    score=0
    gameover=False
    glutPostRedisplay()
def move_snake():
    global snake, food_eaten,food_x,food_y,score,snake_speed
    if not gameover:
        if not pause:
        # Calculate new head position
            head_x, head_y = snake[0]
            dx, dy = snake_dir
            new_head_x = head_x + dx * snake_speed
            new_head_y = head_y + dy * snake_speed

            # Check if food is eaten
            if food_x and food_y and abs(new_head_x - food_x) < 5 and abs(new_head_y - food_y) < 5:
                snake.insert(0, (new_head_x, new_head_y))  # Grow snake
                food_eaten = True
                score+=1
                if score%3==0:
                    snake_speed+=1
                print(f"Food is eaten. Score is {score}")
            else:
                snake.pop()  # Remove previous  tail if no food eaten
                snake.insert(0, (new_head_x, new_head_y)) #add new headx,heady
def check_barrier():
    x,y=snake[0]
    if (127 <= x <= 193) and (277<=y<=283):  #snake radius is 3
        return True
    elif (187<= x <= 193) and (277 <= y <= 343):
        return True
    elif (297 <= x <= 363) and (277<= y <= 283):
        return True
    elif (297<= x <= 303) and (277 <= y <= 343):
        return True

    elif (127 <= x < 193) and (217<= y <= 223):
        return True
    elif (187<= x <= 193) and (157 <= y <= 223):
        return True
    elif (297 <= x <= 363) and (217<= y <= 223):
        return True
    elif (297<= x <= 303) and (157 <= y <= 223):
        return True
    return False

def check_collision():
    head_x, head_y = snake[0]
    # Check boundary collision
    if math.dist((head_x, head_y), (W_Width // 2, W_Height // 2)) > RADIUS:
        return True
    # Check self-collision
    if len(snake) > 1 and (head_x, head_y) in snake[1:]:
        return True
    return False

def update_direction(key, x, y):
    global snake_dir, pause,gameover # Ensure snake_dir is accessible globally if it's defined outside the function
    if not gameover:
        if not pause:
            if key == GLUT_KEY_RIGHT:  # Right arrow key
                snake_dir = (1, 0)
            elif key == GLUT_KEY_LEFT:  # Left arrow key
                snake_dir = (-1, 0)
            elif key == GLUT_KEY_UP:  # Up arrow key
                snake_dir = (0, 1)
            elif key == GLUT_KEY_DOWN:  # Down arrow key
                snake_dir = (0, -1)






def keyboardListener(key, x, y):
    global pause
    if not gameover:
        # Check if the key pressed is the space bar (' ')
        if key == b' ':
            pause = not pause  # Toggle pause state
            draw_play_pause_button()
            print("Game Paused" if pause else "Game Resumed")
        glutPostRedisplay()



def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw circular boundary
    if not gameover:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(1.0, 0, 0)
    draw_circle_midpoint(W_Width // 2, W_Height // 2, RADIUS)

    # Draw food
    glColor3f(0, 1.0, 0.0)
    set_point_size(5)  # Make the food more visible
    if food_x and food_y:
        draw_point(food_x, food_y)

    # Draw snake
    #glColor3f(0.0, 1.0, 0.0)
    set_point_size(3)  # Adjust snake visibility
    draw_restart_button()
    draw_exit_button()
    draw_play_pause_button()
    barrier()
    for segment in snake:
        draw_point(segment[0], segment[1],1)

    glFlush()

def timer(value):
    global food_x,food_y,gameover
    if not gameover:
        spawn_food()

        move_snake()
        if check_collision():
            print("Game Over!")
            gameover=True
        if check_barrier():
            print("Game Over!")
            gameover=True



    glutPostRedisplay()
    glutTimerFunc(100, timer, 0)

def keyboard(key, x, y):
    update_direction(key)

def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(W_Width, W_Height)
    glutCreateWindow(b"Circular Snake Game with Keyboard Controls")

    initialize()

    glutDisplayFunc(display)
    glutSpecialFunc(update_direction)  # Use glutSpecialFunc for special keys
    glutTimerFunc(100, timer, 0)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(keyboardListener)
    glutMainLoop()


if __name__ == "_main_":
    main()