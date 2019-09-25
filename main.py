import pygame
from scipy.linalg import lu

# adds 1 around choosen square, calculations are done in mod2, 0 means that square is off, 1 is on
def light_up(xx,yy):
    for ro in range(-1, 2):
        grid[xx + ro][yy] = divmod(grid[xx + ro][yy] + 1, 2)[1]
    for co in range(-1, 2):
        grid[xx][yy + co] = divmod(grid[xx][yy + co] + 1, 2)[1]
    grid[xx][yy] = divmod(grid[xx][yy] + 1, 2)[1]  # adds again 1 in the middle, to allow easy use of loops above


# initialise pygame
pygame.init()
pygame.display.set_caption("lightsOut")
clock = pygame.time.Clock()

windowSize = [400, 400]  # windows size
screen = pygame.display.set_mode(windowSize)  # display mode
myFont = pygame.font.SysFont("Times New Roman", 18)  # font

width = 16  # size of the grid in px
height = 16  # size of the grid in px
margin = 1  # margin between the grid
distance = 100  # distance between main and solved grid

hSize = 3  # amount of squares height
wSize = 3  # amount of squares width

# create basic colors
c_red = (255, 0, 0)
c_blue = (0, 0, 255)
c_green = (0, 255, 0)
c_white = (255, 255, 255)
c_black = (0, 0, 0)
c_yellow = (255, 240, 2)

color = c_white  # initialize basic color of the grid

grid = []  # create blank game grid
result = []  # create blank result grid
b = []  # create ordered grid
gauss = []  # gaussian elimination grid, not used for now

mouseState = "nothing"  # checks what action was performed by mouse
LEFT = 1  # lmb
RIGHT = 3  # rmb
leftHold = False
rightHold = False

# created arrays have two additional rows and collumns,
# which are never used, but negate the need for special cases for corners and sides

# two dimensional array of the grid and grid data
for column in range(wSize+2):
    grid.append([])
    for row in range(hSize+2):
        grid[column].append([])
        grid[column][row] = 0  # initialise turned off tiles

# two dimensional array of the result
for column in range(wSize+2):
    result.append([])
    for row in range(hSize+2):
        result[column].append([])
        result[column][row] = 0  # initialise turned off result tiles

# array for ordering the grid
for row in range(hSize + 2):
    for column in range(wSize + 2):
        b.append([])

# gaussian grid, not used for now
for column in range(wSize*wSize+2):
    gauss.append([])
    for row in range(hSize*hSize+2):
        gauss[column].append([])
        gauss[column][row] = 0  # initialise turned off result tiles

# gaussian grid fill, not used for now
for column in range(1, wSize*wSize+1):
    for row in range(1, hSize*hSize+1):
        if column == row:
            gauss[column][row] = 1
        if row != divmod(row, wSize)[0]*wSize and row == column-1:
            gauss[column][row] = 1
        if column != divmod(column, hSize)[0]*hSize and column == row-1:
            gauss[column][row] = 1
        if column > wSize and row == column-wSize:
            gauss[column][row] = 1
        if row > hSize and column == row-hSize:
            gauss[column][row] = 1

while True:  # initial loop ________________________________________________________________________________
    screen.fill(c_black)

    # define step stuff
    # mouse position
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]  # x position of the mouse
    mouse_y = pos[1]  # y position of the mouse

    xPos = int(mouse_x / (height + margin))  # read x cell
    yPos = int(mouse_y / (width + margin))  # read y cell

    # drawing main grid and tile color change
    for column in range(1, wSize+1):
        for row in range(1, hSize+1):
            curTile = grid[column][row]  # read type of the current tile
            if grid[column][row] == 0:
                color = c_white
            elif grid[column][row] == 1:
                color = c_yellow

            # draw main tile rectangle
            pygame.draw.rect(screen, color, (margin + (width + margin) * column, margin + (height + margin) * row, width, height))

    # drawing solved grid and tile change
    for column in range(1, wSize + 1):
        for row in range(1, hSize + 1):
            if result[column][row] == 0:
                color = c_white
            elif result[column][row] == 1:
                color = c_green

            # draw solved tile rectangle
            pygame.draw.rect(screen, color, (margin + (width + margin) * column, distance + margin + (height + margin) * row, width, height))

    # calculate the solution
    # grid enumerator
    for row in range(1, hSize+1):
        for column in range(1, wSize+1):
            b[column+(row-1)*wSize] = grid[column][row]

    result[1][1] = divmod(b[1]+b[3]+b[6]+b[7]+b[8], 2)[1]
    result[2][1] = divmod(b[5]+b[7]+b[8]+b[9], 2)[1]
    result[3][1] = divmod(b[1]+b[3]+b[4]+b[8]+b[9], 2)[1]
    result[1][2] = divmod(b[3]+b[5]+b[6]+b[9], 2)[1]
    result[2][2] = divmod(b[2]+b[4]+b[5]+b[6]+b[8], 2)[1]
    result[3][2] = divmod(b[1]+b[4]+b[5]+b[7], 2)[1]
    result[1][3] = divmod(b[1]+b[2]+b[6]+b[7]+b[9], 2)[1]
    result[2][3] = divmod(b[1]+b[2]+b[3]+b[5], 2)[1]
    result[3][3] = divmod(b[2]+b[3]+b[4]+b[7]+b[9], 2)[1]

    # check if something happened//////////////////////////////////////////////////////////////////////////////
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:  # checks mouse left click
            mouseState = "clickLeft"
            leftHold = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:  # checks mouse left up
            mouseState = "upLeft"
            leftHold = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:  # checks mouse right click
            mouseState = "clickRight"
            rightHold = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:  # checks mouse right up
            mouseState = "upRight"
            rightHold = False
        else:
            mouseState = "nothing"

        if mouseState == "clickRight":
            if mouse_x < (width+margin)*(wSize+1) and mouse_y < (width+margin)*(hSize+1):
                if mouse_x > (width + margin) and mouse_y > (width + margin):
                    if grid[xPos][yPos] == 0:
                        grid[xPos][yPos] = 1
                    elif grid[xPos][yPos] == 1:
                        grid[xPos][yPos] = 0
                slv = lu(gauss, permute_l=True)
                print(slv)

        if mouseState == "clickLeft":
            if mouse_x < (width+margin)*(wSize+1) and mouse_y < (width+margin)*(hSize+1):
                if mouse_x > (width + margin) and mouse_y > (width + margin):
                    light_up(xPos, yPos)

    # pygame clock///////////////////////////////////////////////////////////////////////////////////
    clock.tick(60)
    pygame.display.flip()
