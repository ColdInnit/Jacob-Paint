# @formatter:off

import pygame.display
from pygame import *
from math import *

# initialising variables
main = init()
clock = time.Clock()
window = display.set_mode((900, 900), RESIZABLE)
window.fill("white")
icon = image.load("icon.png")
display.set_icon(icon)
display.set_caption("Jacob Paint")
drawingSurface = Surface((900, 900))
drawingSurface.fill("white")

start = True
drawingList = []
fillBool = False

def drawButton(colour, coordx, coordy, radius, isHover, circleColourPicker = "grey"):
      if isHover:
            if circleColourPicker == ("red"):
                  circleColour = (200, 8, 8)
            else:
                  circleColour = (180, 180, 180)
      else:
            if circleColourPicker == ("red"):
                  circleColour = (150, 8, 8)
            else:
                  circleColour = (115, 115, 115)
            
      draw.circle(window, circleColour, (coordx, coordy), radius)
      draw.circle(window, colour, (coordx, coordy), radius - 3)


def isHover(cursorx, cursory, coordx, coordy):
      diffx = abs(cursorx - coordx)
      diffy = abs(cursory - coordy)
      
      if sqrt(diffx**2 + diffy**2) <= 18:
            return True
      else:
            return False
      
def fill(colour, startPos):

      newColour = window.map_rgb(colour)
      surfArray = surfarray.pixels2d(window)
      originColour = surfArray[startPos]
      toCheck = [startPos]
      
      while len(toCheck) > 0:
            
            x, y = toCheck.pop()
            
            try:  # Add a try-except block in case the position is outside the surface.
                  if surfArray[x, y] != originColour:
                        continue
            except IndexError:
                  continue
            
            surfArray[x, y] = newColour
            
            toCheck.append((x + 1, y))
            toCheck.append((x - 1, y))
            toCheck.append((x, y + 1))
            toCheck.append((x, y - 1))
            
            
      surfarray.blit_array(drawingSurface, surfArray)
    
      
colourList = [(255,0,0),(255, 165, 0),(255,255,0),(0,255,50),(0,50,255),(255, 0, 255),(255, 192, 255),(0, 0, 0), (255, 255, 255)]
drawColour = (0, 0, 0)


while True:
                  
      window.fill("white")
      
      cursorx, cursory = mouse.get_pos() # get mouse coordinates for drawing
      
      # drawing
      
      if mouse.get_pressed(num_buttons=3)[0] and not fillBool:
            
            # draws lines and circles for a cleaner looking line
            draw.circle(drawingSurface, drawColour, (cursorx, cursory), 5)
            
            if not start: # a line is only drawn if it isn't the first frame of drawing, so it has coordinates to start from
            
                  draw.line(drawingSurface, drawColour, (cursorx, cursory), (prevCursorx, prevCursory), 13)
                  
            start = False
            
      else : start = True
      
      prevCursorx, prevCursory = cursorx, cursory # storing the coords of current mouse pos for use next frame
      
      window.blit(drawingSurface, (0, 0)) # push drawings onto window
      
      # UI
      
      draw.polygon(window, "white", ((0,0), (63, 0), (63, window.get_height()), (0, window.get_height()))) # fills the UI section with white so it cant be drawn on
      
      draw.line(window,"black", (64, 0), (64, window.get_height()), 5)
      draw.line(window, "black", (0, 420), (64, 420), 5)
      
      # drawing colour picker buttons
      y = 30
      for colour in colourList:
            isHoverVar = isHover(cursorx, cursory, 30, y)
            
            if colour == drawColour:
                  circleColour = "red"
            else: circleColour = "grey"
            
            drawButton(colour, 30, y, 17, isHoverVar, circleColour)
            y+=45 # every button is 45 pixels below the last
            
            # checking if the user is hovering over the button currently being drawn
            if isHoverVar and mouse.get_pressed(num_buttons=3)[0]:
                  drawColour = colour
            
      isHoverVar = isHover(cursorx,cursory,30,y+15)
      
      # makes the fill button green or red depending on if the tool is currently active
      if fillBool: fillButtonColour = "green"
      else: fillButtonColour = "red"
      
      drawButton(fillButtonColour, 30, y+15, 17, isHoverVar) # fill tool button
      
      # input checking
      
      for event in pygame.event.get():
            if event.type == pygame.QUIT: # close button
                  quit()
            if event.type == pygame.KEYDOWN: # fill tool hotkey
                  if event.key == K_f:
                        fill(drawColour, mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN: # fill tool if the button has been pressed
                  if fillBool:
                        fill(drawColour, mouse.get_pos())
            if event.type == MOUSEBUTTONDOWN and isHoverVar: # activates / deactives fill tool
                  if fillBool: fillBool = False
                  else: fillBool = True
      
      display.flip()
      clock.tick(300)
