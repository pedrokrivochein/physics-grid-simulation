import pygame
import sys
import random

from pygame import mouse
from block import Block, BlockState, blocksList, getBlock

window_height = 800
window_width = 800

background = [0, 0, 0] #Black

defaultBlock = [10, 10, 10]

cellSize = 5 #Size of the grid cell

baseCells = [[0 for x in range(window_width)] for y in range(window_width)] #Store grid cell colors

started = False
mousePressed = False

selectedBlock = blocksList[0]

def main():
    global screen, started, cellSize, selectedBlock, mousePressed
    pygame.init()

    screen = pygame.display.set_mode((window_width, window_height))

    #Setup Fonts
    gitHubFont = pygame.font.SysFont('arial', 20, bold = False)
    smallFont = pygame.font.SysFont('arial', 20, bold = True)
    font = pygame.font.SysFont('arial', 38)

    #Menu Texts
    clickToStart = font.render('Click on the screen or on the buttons below', True, [0, 0, 0])

    resetButton = pygame.Rect(10, 10, 80, 20)
    resetText = smallFont.render('Reset', True, [0, 0, 0])

    gitHubText = gitHubFont.render('Source Code: github.com/pedrokrivochein/physics-grid-simulation', True, [0, 0, 0])

    blocksButtons = []
    blocksText = []
    for x in range(len(blocksList)):
        blocksButtons.append(pygame.Rect(10 + 92 * x, window_height - 40, 80, 20))
        blocksText.append(smallFont.render(blocksList[x].name, True, [0, 0, 0]))

    pygame.display.set_caption('Physics Grid Simulation')

    screen.fill(background)

    definebaseCells()

    start_time = pygame.time.get_ticks()
    while True:
        drawGrid()

        now = pygame.time.get_ticks()
        if now - start_time > 0.2:
            simulatePhysics()
            start_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
                if(not started):
                    started = True

                for x in range(len(blocksButtons)):
                    if(blocksButtons[x].collidepoint(event.pos)):
                        selectedBlock = blocksList[x]
                        mousePressed = False
                        break
                
                if(resetButton.collidepoint(event.pos)):
                    definebaseCells()
                    mousePressed = False
                    break

            if event.type == pygame.MOUSEBUTTONUP:
                mousePressed = False

        if(not started):
            screen.blit(clickToStart,(window_width / 2.0 - 312, window_height / 2.0 - 80))

        pygame.draw.rect(screen, [255, 255, 255], resetButton)
        screen.blit(resetText, [10, 10])

        screen.blit(gitHubText, [0, window_height - 20])

        for x in range(len(blocksList)):
            pygame.draw.rect(screen, blocksList[x].color, blocksButtons[x])
            screen.blit(blocksText[x], [10 + 92 * x, window_height - 40])

        if(mousePressed and hasattr(event, 'pos')):
            xH = event.pos[0] - event.pos[0] % 20
            yH = event.pos[1] - event.pos[1] % 20
            if(baseCells[xH][yH] == defaultBlock):
                for x in range(-20, 20, cellSize):
                    for y in range(-20, 20, cellSize):
                        if (x * x + y * y < (20 * 20) - 120):
                            baseCells[xH - x][yH - y] = selectedBlock.color

        pygame.display.update()

def definebaseCells(): #Define an initial random type of block to each cell.
    for x in range(0, window_width, cellSize):
        for y in range(0, window_height, cellSize):
            baseCells[x][y] = defaultBlock

def drawGrid():
    for x in range(0, window_width, cellSize):
        for y in range(0, window_height, cellSize):
            cell = pygame.Rect(x, y, cellSize, cellSize)
            pygame.draw.rect(screen, baseCells[x][y], cell)

def simulatePhysics():
    for x in range(window_width - cellSize, 0, -cellSize):
        for y in range(window_height - cellSize, 0, -cellSize):
            blockHolder = getBlock(baseCells[x][y])

            if(blockHolder.state == BlockState.SolidGravity):
                solidGravitySimulation(x, y, blockHolder)
            elif(blockHolder.state == BlockState.Liquid):
                liquidSimulation(x, y, blockHolder)
            elif(blockHolder.state == BlockState.Gas):
                gasSimulation(x, y, blockHolder)
            
            if(blockHolder.name == 'Fire'):
                fireSimulation(x, y)

            if(blockHolder.name == 'Lava'):
                lavaSimulation(x, y)
            
            if(blockHolder.flamable):
                flamableSimulation(x, y, blockHolder)

def solidGravitySimulation(x, y, _block):
    #Bottom
    if(y + cellSize < window_height):
        if(baseCells[x][y + cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x][y + cellSize] = _block.color
            return
        elif(getBlock(baseCells[x][y]).state != BlockState.Liquid and getBlock(baseCells[x][y + cellSize]).state == BlockState.Liquid):
            baseCells[x][y] = baseCells[x][y + cellSize]
            baseCells[x][y + cellSize] = _block.color
            return
            
    #Bottom-Left
    if(x - cellSize >= 0 and y + cellSize < window_height):
        if(baseCells[x - cellSize][y + cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x - cellSize][y + cellSize] = _block.color
            return
        elif(getBlock(baseCells[x][y]).state != BlockState.Liquid and getBlock(baseCells[x - cellSize][y + cellSize]).state == BlockState.Liquid):
            baseCells[x][y] = baseCells[x - cellSize][y + cellSize]
            baseCells[x - cellSize][y + cellSize] = _block.color
            return

    #Bottom-Right
    if(x + cellSize < window_width and y + cellSize < window_height):
        if(baseCells[x + cellSize][y + cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x + cellSize][y + cellSize] = _block.color
            return
        elif(getBlock(baseCells[x][y]).state != BlockState.Liquid and getBlock(baseCells[x + cellSize][y + cellSize]).state == BlockState.Liquid):
            baseCells[x][y] = baseCells[x + cellSize][y + cellSize]
            baseCells[x + cellSize][y + cellSize] = _block.color
            return

def liquidSimulation(x, y, _block):
    #Bottom
    if(y + cellSize < window_height):
        if(baseCells[x][y + cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x][y + cellSize] = _block.color
            return
        elif(getBlock(baseCells[x][y]).state != BlockState.Liquid and getBlock(baseCells[x][y + cellSize]).state == BlockState.Liquid):
            baseCells[x][y] = baseCells[x][y + cellSize]
            baseCells[x][y + cellSize] = _block.color
            return
            
    #Bottom-Left
    if(x - cellSize >= 0 and y + cellSize < window_height):
        if(baseCells[x - cellSize][y + cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x - cellSize][y + cellSize] = _block.color
            return
        elif(getBlock(baseCells[x][y]).state != BlockState.Liquid and getBlock(baseCells[x - cellSize][y + cellSize]).state == BlockState.Liquid):
            baseCells[x][y] = baseCells[x - cellSize][y + cellSize]
            baseCells[x - cellSize][y + cellSize] = _block.color
            return

    #Bottom-Right
    if(x + cellSize < window_width and y + cellSize < window_height):
        if(baseCells[x + cellSize][y + cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x + cellSize][y + cellSize] = _block.color
            return
        elif(getBlock(baseCells[x][y]).state != BlockState.Liquid and getBlock(baseCells[x + cellSize][y + cellSize]).state == BlockState.Liquid):
            baseCells[x][y] = baseCells[x + cellSize][y + cellSize]
            baseCells[x + cellSize][y + cellSize] = _block.color
            return

    #Left
    if(x - cellSize >= 0):
        if(baseCells[x - cellSize][y] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x - cellSize][y] = _block.color
            return
        elif(getBlock(baseCells[x][y]).state != BlockState.Liquid and getBlock(baseCells[x - cellSize][y]).state == BlockState.Liquid):
            baseCells[x][y] = baseCells[x - cellSize][y]
            baseCells[x - cellSize][y] = _block.color
            return

    #Right
    if(x + cellSize < window_width):
        if(baseCells[x + cellSize][y] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x + cellSize][y] = _block.color
            return
        elif(getBlock(baseCells[x][y]).state != BlockState.Liquid and getBlock(baseCells[x + cellSize][y]).state == BlockState.Liquid):
            baseCells[x][y] = baseCells[x + cellSize][y]
            baseCells[x + cellSize][y] = _block.color
            return

def gasSimulation(x, y, _block):
    #Up
    if(y - cellSize < window_height):
        if(baseCells[x][y - cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x][y - cellSize] = _block.color
            return
            
    #Up-Left
    if(x - cellSize >= 0 and y - cellSize < window_height):
        if(baseCells[x - cellSize][y - cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x - cellSize][y - cellSize] = _block.color
            return

    #Up-Right
    if(x + cellSize < window_width and y - cellSize < window_height):
        if(baseCells[x + cellSize][y - cellSize] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x + cellSize][y - cellSize] = _block.color
            return

    #Left
    if(x - cellSize >= 0):
        if(baseCells[x - cellSize][y] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x - cellSize][y] = _block.color
            return

    #Right
    if(x + cellSize < window_width):
        if(baseCells[x + cellSize][y] == defaultBlock):
            baseCells[x][y] = defaultBlock
            baseCells[x + cellSize][y] = _block.color
            return

timeFlamable = [[0 for x in range(window_width)] for y in range(window_width)] #2 loops needed to pass and clear the fire.

for x in range(0, window_width, cellSize):
    for y in range(0, window_height, cellSize):
        timeFlamable[x][y] = 0

def flamableSimulation(x, y, _block):
    #Bottom
    if(y + cellSize < window_height):
        if(getBlock(baseCells[x][y + cellSize]).causeFire):
            timeFlamable[x][y] += 1
            if(timeFlamable[x][y] == 2):
                timeFlamable[x][y] = 0
                baseCells[x][y] = blocksList[7].color
            return
            
    #Bottom-Left
    if(x - cellSize >= 0 and y + cellSize < window_height):
        if(getBlock(baseCells[x - cellSize][y + cellSize]).causeFire):
            timeFlamable[x][y] += 1
            if(timeFlamable[x][y] == 2):
                timeFlamable[x][y] = 0
                baseCells[x][y] = blocksList[7].color
            return

    #Bottom-Right
    if(x + cellSize < window_width and y + cellSize < window_height):
        if(getBlock(baseCells[x + cellSize][y + cellSize]).causeFire):
            timeFlamable[x][y] += 1
            if(timeFlamable[x][y] == 2):
                timeFlamable[x][y] = 0
                baseCells[x][y] = blocksList[7].color
            return

    #Left
    if(x - cellSize >= 0):
        if(getBlock(baseCells[x - cellSize][y]).causeFire):
            timeFlamable[x][y] += 1
            if(timeFlamable[x][y] == 2):
                timeFlamable[x][y] = 0
                baseCells[x][y] = blocksList[7].color
            return

    #Right
    if(x + cellSize < window_width):
        if(getBlock(baseCells[x + cellSize][y]).causeFire):
            timeFlamable[x][y] += 1
            if(timeFlamable[x][y] == 2):
                timeFlamable[x][y] = 0
                baseCells[x][y] = blocksList[7].color
            return
    
    #Up
    if(y - cellSize < window_height):
        if(getBlock(baseCells[x][y - cellSize]).causeFire):
            timeFlamable[x][y] += 1
            if(timeFlamable[x][y] == 2):
                timeFlamable[x][y] = 0
                baseCells[x][y] = blocksList[7].color
            return
            
    #Up-Left
    if(x - cellSize >= 0 and y - cellSize < window_height):
        if(getBlock(baseCells[x - cellSize][y - cellSize]).causeFire):
            timeFlamable[x][y] += 1
            if(timeFlamable[x][y] == 2):
                timeFlamable[x][y] = 0
                baseCells[x][y] = blocksList[7].color
            return

    #Up-Right
    if(x + cellSize < window_width and y - cellSize < window_height):
        if(getBlock(baseCells[x + cellSize][y - cellSize]).causeFire):
            timeFlamable[x][y] += 1
            if(timeFlamable[x][y] == 2):
                timeFlamable[x][y] = 0
                baseCells[x][y] = blocksList[7].color
            return

timeFire = [[0 for x in range(window_width)] for y in range(window_width)] #2 loops needed to clear the fire.

for x in range(0, window_width, cellSize):
    for y in range(0, window_height, cellSize):
        timeFire[x][y] = 0

def fireSimulation(x, y):
    timeFire[x][y] += 1
    if(timeFire[x][y] == 2):
        baseCells[x][y] = defaultBlock
        timeFire[x][y] = 0

def lavaSimulation(x, y):
    #Bottom
    if(y + cellSize < window_height):
        if(getBlock(baseCells[x][y + cellSize]).color == blocksList[0].color):
            baseCells[x][y + cellSize] = blocksList[2].color
            
    #Bottom-Left
    if(x - cellSize >= 0 and y + cellSize < window_height):
        if(getBlock(baseCells[x - cellSize][y + cellSize]).color == blocksList[0].color):
            baseCells[x - cellSize][y + cellSize] = blocksList[2].color

    #Bottom-Right
    if(x + cellSize < window_width and y + cellSize < window_height):
        if(getBlock(baseCells[x + cellSize][y + cellSize]).color == blocksList[0].color):
            baseCells[x + cellSize][y + cellSize] = blocksList[2].color

    #Left
    if(x - cellSize >= 0):
        if(getBlock(baseCells[x - cellSize][y]).color == blocksList[0].color):
            baseCells[x - cellSize][y] = blocksList[2].color

    #Right
    if(x + cellSize < window_width):
        if(getBlock(baseCells[x + cellSize][y]).color == blocksList[0].color):
            baseCells[x + cellSize][y] = blocksList[2].color
    
    #Up
    if(y - cellSize < window_height):
        if(getBlock(baseCells[x][y - cellSize]).color == blocksList[0].color):
            baseCells[x][y - cellSize] = blocksList[2].color
            
    #Up-Left
    if(x - cellSize >= 0 and y - cellSize < window_height):
        if(getBlock(baseCells[x - cellSize][y - cellSize]).color == blocksList[0].color):
            baseCells[x - cellSize][y - cellSize] = blocksList[2].color

    #Up-Right
    if(x + cellSize < window_width and y - cellSize < window_height):
        if(getBlock(baseCells[x + cellSize][y - cellSize]).color == blocksList[0].color):
            baseCells[x + cellSize][y - cellSize] = blocksList[2].color

main()