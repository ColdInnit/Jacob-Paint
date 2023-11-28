# @formatter:off
import math

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
drawingSurface = Surface((836, 900))
drawingSurface.fill("white")
drawingSurface2 = Surface((836, 900))
cursorSurface = Surface((836, 900), flags = SRCALPHA)
cursorSurface.fill((0,0,0,0))
uploadSurface = Surface((836, 900))

undoArray = []

start = True
drawingList = []
fillBool = False
radius = 5

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

      newColour = drawingSurface.map_rgb(colour)
      surfArray = surfarray.pixels2d(drawingSurface)
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
      cursorSurface.fill((0,0,0,0))
      
      cursorx, cursory = mouse.get_pos()# get mouse coordinates for drawing
      drawingCursorx = cursorx - 64
      
      # drawing
      
      draw.circle(cursorSurface, drawColour, (drawingCursorx, cursory), radius)
      
      if mouse.get_pressed(num_buttons=3)[0] and not fillBool:
            
            # draws lines and circles for a cleaner looking line
            draw.circle(drawingSurface, drawColour, (drawingCursorx, cursory), radius)
            
            if not start: # a line is only drawn if it isn't the first frame of drawing, so it has coordinates to start from
            
                  draw.line(drawingSurface, drawColour, (drawingCursorx, cursory), (prevCursorx, prevCursory), ceil(radius*2.5))
                  
            start = False
            
      else:
            if not start:
                  start = True
                  drawingSnapshot = drawingSurface
                  if len(undoArray) >= 3:
                        undoArray.pop(0)
                        undoArray.append(drawingSnapshot)
                  else:
                        undoArray.append(drawingSnapshot)
      
      prevCursorx, prevCursory = drawingCursorx, cursory # storing the coords of current mouse pos for use next frame
      
      window.blit(drawingSurface, (64, 0)) # push drawings onto window
      window.blit(cursorSurface, (64, 0))
      
      # UI
      
      draw.polygon(window, "white", ((0,0), (63, 0), (63, window.get_height()), (0, window.get_height()))) # fills the UI section with white so it cant be drawn on
      
      draw.line(window,"black", (64, 0), (64, window.get_height()), 5)
      draw.line(window, "black", (0, 420), (64, 420), 5)
      draw.line(window, "black", (0, 480), (64, 480), 5)
      draw.line(window, "black", (0, 720), (64, 720), 5)

      
      # drawing colour picker buttons
      y = 30
      for colour in colourList:
            isHoverVar_colour = isHover(cursorx, cursory, 30, y)
            
            if colour == drawColour:
                  circleColour = "red"
            else: circleColour = "grey"
            
            drawButton(colour, 30, y, 17, isHoverVar_colour, circleColour)
            y+=45 # every button is 45 pixels below the last
            
            # checking if the user is hovering over the button currently being drawn
            if isHoverVar_colour and mouse.get_pressed(num_buttons=3)[0]:
                  drawColour = colour
            
      isHoverVar_fill = isHover(cursorx,cursory,30,y+15)
      
      # makes the fill button green or red depending on if the tool is currently active
      if fillBool: fillButtonColour = "green"
      else: fillButtonColour = "red"
      
      y += 15
      drawButton(fillButtonColour, 30, y, 17, isHoverVar_fill) # fill tool button
      
      buttonRadius = 5
      y += 15
      for x in range(0,5):
            y+=45
            isHoverVar_size = isHover(cursorx, cursory, 30, y)
            drawButton("white", 30, y, buttonRadius, isHoverVar_size)
            buttonRadius += 2
            
            if isHoverVar_size:
                  radius = buttonRadius - 3
                  
      
      y+=60
      isHoverVar_save = isHover(cursorx, cursory, 30, y)
      drawButton("white", 30, y, 17, isHoverVar_save)
      
      y+=60
      isHoverVar_upload = isHover(cursorx, cursory, 30, y)
      drawButton("white", 30, y, 17, isHoverVar_upload)
      
      
      # input checking
      for event in pygame.event.get():
            if event.type == pygame.QUIT: # close button
                  quit()
            if event.type == pygame.KEYDOWN: # fill tool hotkey
                  if event.key == K_f:
                        fill(drawColour, (drawingCursorx, cursory))
                  if key.get_mods() & KMOD_CTRL == 64:
                        if event.key == K_z:
                              if len(undoArray) > 0:
                                    drawingSurface.fill("white")
                                    drawingSurface.blit(drawingSnapshot, (0,0))
                                    
                              
            if event.type == pygame.MOUSEBUTTONDOWN: # fill tool if the button has been pressed
                  if fillBool and cursorx > 64:
                        fill(drawColour, (drawingCursorx, cursory))
                  elif isHoverVar_fill:
                        if fillBool: fillBool = False
                        else: fillBool = True
                  elif isHoverVar_save:
                        image.save(drawingSurface, "drawing.png")
                  elif isHoverVar_upload:
                        uploadImage = image.load("drawing.png")
                        drawingSurface.fill((0,0,0))
                        drawingSurface.blit(uploadImage, (0,0))
                        
            if event.type == VIDEORESIZE:
                  cursorSurface = transform.scale(drawingSurface, (event.w, event.h))
                  drawingSurface = transform.scale(drawingSurface, (event.w, event.h))
                  
      
      
      display.flip()
      clock.tick(300)
