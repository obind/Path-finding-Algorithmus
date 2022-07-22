#Goal: find shortest path from point A to B
# requierment: no brute force 

#Node is everthing you can visit = vertex
#Node in this graph is a Letter (f, G. H)

#Egdges connect nodes  

#a-star path finding alrgotrithm
#informed search algorithm means: no brute force requiered 
#using heuristic function
#manhattan distance

#g score 
#the shortest way ist the score 

#start node have 0 score
#every other node is set infinity
import pygame
import math 
from queue import PriorityQueue

#setup the the dispaly
WIDTH= 800
#this are the dimensions
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorith")


RED = (255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 255, 0)
YELLOW=(255, 255, 0)
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
PURPLE=(128, 0, 128)
ORANGE=(255, 165, 0)
GREY=(128, 128, 128)
TURQUOISE=(64, 224, 208)

#to keep track of the color of the spots
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col 
    
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color==TURQUOISE
    
    def reset(self):
        self.color = WHITE
    
    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self,grid): 
        self.neighbors = []
        if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_barrier(): #Down
            self.neighbors.append(grid[self.row + 1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows -1 and not grid[self.row][self.col + 1].is_barrier(): #Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEft
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1- y2)

def reconstruct_path(came_from, current, draw):
    while current  in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    #Efficent way to get the minimum element from this queue
    open_set = PriorityQueue()
    #start by putting the start node in the open set
    open_set.put((0, count, start))
    #keeps track from where we came from
    came_from = {}
    #keeps track of the current shortest distance from start 
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start]= 0
    #keeps track of the predictet distance 
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start]= h(start.get_pos(), end.get_pos())

    #see if something is in the open hash
    open_set_hash = {start}

#while the open set is empty make sure not quitting game
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        #open_set is a priority queue (Warteschlange)
        current = open_set.get()[2]
        open_set_hash.remove(current)   

        # if found end we are finished
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        #consider all the neigbors of the current node to calc the tentaive g score
        for neighbor in current.neighbors:
            temp_g_score= g_score[current] + 1
        #if less than the g_score in the table: Update because better way
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()   
    return False 

#making grid
def make_grid(rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)
        return grid

def draw_grid(win, rows, width): 
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i *gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j* gap, 0), (j * gap, width))

#Drawfunction
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
#draw grid line on top
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap 
    col = x // gap

    return row, col

#can be changed ROWS 
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True

    while run:
            draw(win, grid, ROWS, width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]: #LEft
                    pos= pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]

                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]: #Right
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                    if event.key == pygame.K_c:
                        start = None
                        end= None
                        grid = make_grid(ROWS, width)   

    pygame.quit()

main(WIN, WIDTH)



