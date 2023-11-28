# @formatter:off

import pygame.display
import tkinter as tk
from pygame import *
from math import *
from tkinter.filedialog import asksaveasfilename, askopenfilename

# initialising variables
tkinter = tk.Tk()
tkinter.withdraw()
main = init()
clock = time.Clock()
window = display.set_mode((900, 900), RESIZABLE)
window.fill("white")
icon = image.load("icon.png")
display.set_icon(icon)
display.set_caption("Jacob Paint")
drawingSurface = Surface((833, 900))
drawingSurface.fill("white")
cursorSurface = Surface((833, 900), flags = SRCALPHA)
cursorSurface.fill((0,0,0,0))

fillIcon = transform.scale(image.load("fillIcon.png"), (20,20))
importIcon = transform.scale(image.load("importIcon.png"), (18,18))
saveIcon = transform.scale(image.load("saveIcon.png"), (18,18))

blankSurface = Surface((833, 900))
blankSurface.fill("white")
undoArray = [blankSurface]

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

prevCursorx, prevCursory = 0, 0

while True:

      # input checking
      for event in pygame.event.get():

            if event.type == pygame.QUIT: # close button
                  quit()

            if event.type == pygame.KEYDOWN: # fill tool hotkey
                  if event.key == K_f:
                        fill(drawColour, (drawingCursorx, cursory))
                  if key.get_mods() & KMOD_CTRL == 64:
                        if event.key == K_z:
                              if len(undoArray) > 1:
                                    undoArray.pop(0)
                                    drawingSurface.fill("white")
                                    drawingSurface.blit(undoArray[0], (0, 0))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # fill tool if the button has been pressed
                  if fillBool and cursorx > 64:
                        fill(drawColour, (drawingCursorx, cursory))
                        if len(undoArray) >= 20:
                              undoArray.pop(19)
                              undoArray.insert(0, drawingSurface.copy())
                        else:
                              undoArray.insert(0, drawingSurface.copy())
                  elif isHoverVar_fill:
                        if fillBool: fillBool = False
                        else: fillBool = True
                  elif isHoverVar_save:
                        path = asksaveasfilename()
                        if path != "":
                              image.save(drawingSurface, path+".png")
                              tkinter.destroy()
                  elif isHoverVar_upload:
                        path = askopenfilename(filetypes=[("Image Files", "*.png")])
                        if path != "":
                              uploadImage = image.load(path)
                              drawingSurface.fill((0,0,0))
                              drawingSurface.blit(uploadImage, (0,0))

            if event.type == VIDEORESIZE:
                  cursorSurface = Surface((window.get_width(), window.get_height()), flags=SRCALPHA)
                  drawingSurface = transform.scale(drawingSurface, (event.w, event.h))
      
      window.fill("white")
      cursorSurface.fill((255,255,255,0))
      
      cursorx, cursory = mouse.get_pos() # get mouse coordinates for drawing
      drawingCursorx = cursorx - 67

      path = ""

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
                  if len(undoArray) >= 20:
                        undoArray.pop(19)
                        undoArray.insert(0, drawingSurface.copy())
                  else:
                        undoArray.insert(0, drawingSurface.copy())
      
      prevCursorx, prevCursory = drawingCursorx, cursory # storing the coords of current mouse pos for use next frame

      # window.blit(drawingSurface, (64, 0)) # push drawings onto window
      window.blit(drawingSurface, (67, 0))
      window.blit(cursorSurface, (67, 0))


      # UI
      
      draw.polygon(window, "white", ((0,0), (63, 0), (63, 825), (0, 825))) # fills the UI section with white so it cant be drawn on
      
      draw.line(window,"black", (64, 0), (64, 825), 5)
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
      window.blit(fillIcon, (19, y-12))
      
      buttonRadius = 5
      y += 15
      for x in range(0,5):
            y+=45
            isHoverVar_size = isHover(cursorx, cursory, 30, y)
            drawButton("white", 30, y, buttonRadius, isHoverVar_size)
            buttonRadius += 2
            
            if isHoverVar_size and mouse.get_pressed(num_buttons=3)[0]:
                  radius = buttonRadius - 3
                  
      
      y+=60
      isHoverVar_save = isHover(cursorx, cursory, 30, y)
      drawButton("white", 30, y, 17, isHoverVar_save)
      window.blit(saveIcon, (21, y-9))
      
      y+=45
      isHoverVar_upload = isHover(cursorx, cursory, 30, y)
      drawButton("white", 30, y, 17, isHoverVar_upload)
      window.blit(importIcon, (20, y-10))

      draw.line(window, "black", (0, 825), (64, 825), 5)

      display.flip()
      clock.tick(300)
