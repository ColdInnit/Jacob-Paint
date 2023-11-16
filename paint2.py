import time

import pygame.display
from pygame import *
from math import *
from sympy import symbols
from sympy.solvers import solve

main = init()
window = display.set_mode((900, 900), RESIZABLE)
clock = time.Clock()
window.fill("white")
start = True
icon = image.load("icon.png")
display.set_icon(icon)
display.set_caption("Jacob Paint")

drawingListCircles = []
drawingListLines = []

def drawButton(colour, coordx, coordy, radius, isHover):
      if isHover:
            grey = (180, 180, 180)
      else:
            grey = (115, 115, 115)
            
      draw.circle(window, grey, (coordx, coordy), radius)
      draw.circle(window, colour, (coordx, coordy), radius - 3)


def isHover(cursorx, cursory, coordx, coordy):
      diffx = abs(cursorx - coordx)
      diffy = abs(cursory - coordy)
      
      if sqrt(diffx**2 + diffy**2) <= 18:
            return True
      else:
            return False
      
def fill(colour, startPos):
      
      toCheck = []
      toColour = []
      x, y = startPos
      originColour = Surface.get_at((x, y))
      visited = []
      toCheck.append(startPos)
      
      while len(toCheck) > 0:
            current = toCheck[0]
            toCheck.pop()
            pixelColour = Surface.get_at((current))
            if pixelColour == originColour:
                  toColour.append(current)
                  
                  upPos = current + (0, 1)
                  rightPos = current + (1, 0)
                  downPos = current + (0, -1)
                  leftPos = current + (-1, 0)
                  
                  if Surface.get_at((upPos)) == originColour:
                        toCheck.append(upPos)
                  if Surface.get_at((rightPos)) == originColour:
                        toCheck.append(rightPos)
                  if Surface.get_at((downPos)) == originColour:
                        toCheck.append(downPos)
                  if Surface.get_at((leftPos)) == originColour:
                        toCheck.append(leftPos)
                  
      
colourList = ["red","orange","yellow","green","blue","purple","pink","black","white"]
drawColour = "black"

window.fill("white")

while True:
      
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  quit()
                  
      window.fill("white")
      
      cursorx, cursory = mouse.get_pos()
      
      if mouse.get_pressed(num_buttons=3)[0]:
            
            drawingListCircles.append((window, drawColour, (cursorx, cursory), 5))
            
            if not start:
            
                  drawingListLines.append((window, drawColour, (cursorx, cursory), (prevCursorx, prevCursory), 13))
                  
            start = False
                  
      else : start = True
      
      for circle in drawingListCircles:
            draw.circle(circle[0], circle[1], circle[2], circle[3])
      for line in drawingListLines:
            draw.line(line[0], line[1], line[2], line[3], line[4])
      
      prevCursorx, prevCursory = cursorx, cursory
      
      draw.polygon(window, "white", ((0,0), (63, 0), (63, window.get_height()), (0, window.get_height())))
      
      y = 30
      for colour in colourList:
            isHoverVar = isHover(cursorx, cursory, 30, y)
            drawButton(colour, 30, y, 17, isHoverVar)
            y+=45
            
            if isHoverVar and mouse.get_pressed(num_buttons=3)[0]:
                  drawColour = colour
            
      draw.line(window,"black", (64, 0), (64, window.get_height()), 5)
      draw.line(window, "black", (0, y - 15), (64, y - 15), 5)
      

      pygame.display.flip()
      clock.tick(144)
      
      