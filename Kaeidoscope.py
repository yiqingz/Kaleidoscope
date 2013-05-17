import pygame
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import math
import copy
from pygame.locals import *
from sys import exit
pygame.init()


##########################################################
#_________________     G L O B A L      _________________#
##########################################################

global img2
global img2_c
global img
global currentText
global textinput
global canvas
global userSize
global rect
global size
global userScale
global current_string
global error
global tipShow
global readShoe
global musicOn
readShow = False
tipShow = False
error = False
musicOn = True


##########################################################
#_________________    useful module     _________________#
##########################################################

#+++++++ input box module +++++++++++++

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message,canvas,clean):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  screen.blit(clean,(0,0))

  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (60,60,60)),
                ((screen.get_width() / 2) - 100,\
                 (screen.get_height() / 2) - 10))
  canvas.blit(screen,(a/2-200,b/2-180))
  pygame.display.flip()

def ask(screen, question,canvas,clean):
    global current_string
    b = False
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []#its in fact a list
    display_box(screen, question + "Type here: " +\
                string.join(current_string,""),canvas,clean)
    while 1:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == K_BACKSPACE:
                current_string = current_string[0:-1]
            elif e.type == pygame.KEYDOWN and e.key == K_RETURN:
                b = True
                break
            elif e.type == pygame.KEYDOWN:     #key press
                current_string += [e.unicode]
            display_box(screen, question + "Type here: " +\
                        string.join(current_string,""),canvas,clean)
        if b == True:
            b = False
            break 
    return string.join(current_string,"")

def main_save():
    global captialc
    textinput = pygame.Surface((400,153))
    textinput.blit(saveD,(0,0))
    currentText = ask(textinput,"",canvas,saveD)
    capitalc = False
    return currentText

def main_load():
    global capitalc
    textinput = pygame.Surface((400,153))
    textinput.blit(loadD,(0,0))
    currentText = ask(textinput,"",canvas,loadD)
    capitalc = False
    return currentText

def main_size():
    textinput = pygame.Surface((400,153))
    textinput.blit(sizeD,(0,0))
    currentText = ask(textinput,"",canvas,sizeD)
    return currentText

def main_scale():
    textinput = pygame.Surface((400,153))
    textinput.blit(scaleD,(0,0))
    currentText = ask(textinput,"",canvas,scaleD)
    return currentText

##########################################################
#_________________ 1. make hexagon unit _________________#
##########################################################

def makeRect(tri):
    tl_x = tri[0]
    tl_y = tri[1]
    size = tri[2]
    unitWidth = size
    unitHeight = size*((3**0.5)/2)
    rect = [tl_x,tl_y,unitWidth,unitHeight]
    return rect

def quad(surf):
    surfWidth = surf.get_width()
    surfHeight = surf.get_height()
    q = pygame.Surface((surfWidth*2, surfHeight*2))
    q.blit(surf,(0,0))
    q.blit(pygame.transform.flip(surf,1,0), (surfWidth,0))
    q.blit(pygame.transform.flip(surf,0,1), (0,surfHeight))
    q.blit(pygame.transform.flip(surf,1,1), (surfWidth,surfHeight))
    return q

###########################################################
### (1) form a simple triangle from area selected in the img

def makeRectUnit(surf, rect):
    # make a rectangle which the target triangle should be in
    dif = 5
    a = rect[2] + dif
    b = rect[3] + dif
    s = pygame.Surface((a,b))
    
    if rect[0] + rect[2] >= surf.get_width() or rect[0] < 0:
        if rect[0] < 0:
            rect[0] += surf.get_width()
        if rect[1] < 0 or rect[1] + rect[3] >= surf.get_height():
            if rect[1] + rect[3] >= surf.get_height():
                rect[1] -= surf.get_height()
            topHeight = rect[1] * -1
            bottomHeight = rect[3] - topHeight
            rightWidth = (rect[0]+rect[2]) - surf.get_width()
            leftWidth = rect[2] - rightWidth
            surfHeight = surf.get_height()
            surfWidth = surf.get_width()
            r1 = (0,surfHeight-topHeight,rightWidth,topHeight)
            r2 = (surfWidth-leftWidth,surfHeight-topHeight,leftWidth,topHeight)
            r3 = (surfWidth-leftWidth,0,leftWidth,bottomHeight)
            r4 = (0,0,rightWidth,bottomHeight)
            s.blit(surf,(0,0),r2)
            s.blit(surf,(r2[2],0),r1)
            s.blit(surf,(0,r2[3]),r3)
            s.blit(surf,(r3[2],r1[3]),r4)
        else:
            r2 = (0,rect[1],(rect[0]+rect[2])-surf.get_width(),rect[3])
            r1 = (rect[0],rect[1],rect[2] - r2[2],rect[3])
            s.blit(surf,(0,0),r1)
            s.blit(surf,(r1[2],0),r2)
            
        
    elif rect[1] + rect[3] > surf.get_height():
        topH = rect[1] +rect[3] - surf.get_height()
        botH = rect[3] - topH
        r2 = (rect[0],0,rect[2],topH)###
        r1 = (rect[0],rect[1],rect[2],botH+1)###
        s.blit(surf,(0,0),r1)
        s.blit(surf,(0,r1[3]),r2)
    elif rect[1] < 0:
        rect[1] += surf.get_height()
        r2 = (rect[0],0,rect[2],(rect[1]+rect[3])-surf.get_height())
        r1 = (rect[0],rect[1],rect[2],rect[3] - r2[3])
        s.blit(surf,(0,0),r1)
        s.blit(surf,(0,r1[3]),r2)
        
    else:
        s.blit(surf,(0,0),rect)
    return s

def transparent_unit(surf,tri):
    # shape the equilateral triangle unit
    if tri[2]>150:
        dif = 3 + (tri[2]-150)/40
    else:
        dif = 3

    tri0 = [tri[0],tri[1],tri[2]+dif]
    rect = makeRect(tri0)
    unit = makeRectUnit(surf,rect)
    
    screen = pygame.Surface((rect[2],rect[3]))
    img = pygame.Surface((rect[2],rect[3]))
    img.blit(unit,(0,0))

    # make an equilateral triangle mask
    mask = pygame.Surface((rect[2],rect[3]))
    mask.fill((0,0,0))
    mask.set_colorkey((0,0,255))
    red = pygame.Surface((rect[2],rect[3]))

    pygame.draw.polygon(red,(0,0,255),((rect[2]/2.0,0),\
                                       (0,rect[3]),(rect[2],rect[3])))
    mask.blit(red,(0,0))

    # only show the img inside the area of equilateral triangle
    screen.blit(img,(0,0))
    screen.blit(mask,(0,0))

    t_unit = pygame.Surface((rect[2],rect[3]))
    t_unit.set_colorkey((0,0,0))
    t_unit.blit(screen,(0,0))
    return t_unit

#++++++++++++++ rect making unit function +++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def sub(surf,rect):
    s = pygame.Surface((rect[2],rect[3]))
    if rect[0] + rect[2] >= surf.get_width() or rect[0] < 0:
      # if x flows out of the width of the picture
        if rect[0] < 0:
            rect[0] += surf.get_width()
        if rect[1] < 0 or rect[1] + rect[3] >= surf.get_height():
          # x and y both flow out
            if rect[1] + rect[3] >= surf.get_height():
                rect[1] -= surf.get_height()
            topHeight = rect[1] * -1
            bottomHeight = rect[3] - topHeight
            rightWidth = (rect[0]+rect[2]) - surf.get_width()
            leftWidth = rect[2] - rightWidth
            surfHeight = surf.get_height()
            surfWidth = surf.get_width()
            r1 = (0,surfHeight-topHeight,rightWidth,topHeight)
            r2 = (surfWidth-leftWidth,surfHeight-topHeight,leftWidth,topHeight)
            r3 = (surfWidth-leftWidth,0,leftWidth,bottomHeight)
            r4 = (0,0,rightWidth,bottomHeight)
            s.blit(surf,(0,0),r2)
            s.blit(surf,(r2[2],0),r1)
            s.blit(surf,(0,r2[3]),r3)
            s.blit(surf,(r3[2],r1[3]),r4)
        else:
          # x flows out, y doesn't
            r2 = (0,rect[1],(rect[0]+rect[2])-surf.get_width(),rect[3])
            r1 = (rect[0],rect[1],rect[2] - r2[2],rect[3])
            s.blit(surf,(0,0),r1)
            s.blit(surf,(r1[2],0),r2)
            
    # x doesn't flow out    
    elif rect[1] + rect[3] >= surf.get_height():
      # y flows out
        topH = rect[1] +rect[3] - surf.get_height()
        botH = surf.get_height() - rect[1]
        r2 = (rect[0],0,rect[2],topH)###
        r1 = (rect[0],rect[1],rect[2],botH)###
        s.blit(surf,(0,0),r1)
        s.blit(surf,(0,r1[3]),r2)
    elif rect[1] < 0:
      # the type in y smaller than 0
        rect[1] += surf.get_height()
        r2 = (rect[0],0,rect[2],(rect[1]+rect[3])-surf.get_height())
        r1 = (rect[0],rect[1],rect[2],rect[3] - r2[3])
        s.blit(surf,(0,0),r1)
        s.blit(surf,(0,r1[3]),r2)
        
    else:
      # both x, y inside the picture
        s.blit(surf,(0,0),rect)
    return s


########################################################
###(2) use symmetric to form triangle into symmetric hexagon

def Asymmetric(surf):
    # make a symmetric unit of the whole picture
    
    sWidth = surf.get_width()
    sHeight = surf.get_height()
    symUnitSurf = pygame.Surface((sWidth*2, sHeight*2))
    
    symUnitSurf.blit(surf,(0,0)) # blit the original img at (0,0)
    symUnitSurf.blit(pygame.transform.flip(surf,0,1), (0,sHeight))
        # |_____flip the img vertically

    unitSurf = pygame.Surface((sWidth*2, sHeight*2))
    unitSurf.blit(pygame.transform.rotate(symUnitSurf,240),\
                  (-sWidth/4, -sHeight/2))
    unitSurf.set_colorkey((0,0,0))

    mask = pygame.Surface((sWidth*2, sHeight*2))
    mask.set_colorkey((0,0,0))
    mask.blit(symUnitSurf,(0,0))
    unitSurf.blit(mask,(0,0))
    #unitSurf.blit(pygame.transform.rotate(symUnitSurf,120),(0,0))

    return unitSurf

def Bsymmetric(surf,rect):
    size = rect[2]
    
    dif = -(size/100+1)
    sWidth = surf.get_width()
    sHeight = surf.get_height()

    bSym = pygame.Surface((sWidth,sHeight))
    bSym.blit(pygame.transform.flip(surf,0,1),(0,dif))
    bSym.set_colorkey((0,0,0))
    bSym.blit(surf,(0,0))
    return bSym

def unitHexagon(surf,rect):
    tunit = transparent_unit(surf,rect)
    hexUnit = Bsymmetric(Asymmetric(tunit),rect)
    return hexUnit

##########################################################
#_________________ 2. paste full picture ________________#
##########################################################

def trans_blit(surf,target,position):
    # blit surfaces with black area shown as transparent
    surf.set_colorkey((0,0,0))
    surf.blit(target,position)
    return surf

def makeHexList(rect,screen):
    hexWidth = rect[2]
    hexHeight = rect[2] *(3**0.5)/2
    sWidth = screen.get_width()
    sHeight = screen.get_height()
    
    xHexNum = int(sWidth/(3*hexWidth/2))+1
    if sWidth % (3*hexWidth/2) != 0:
        xHexNum += 1

    yHexNum = int(sHeight/hexHeight)+1
    if sHeight % hexHeight != 0:
        yHexNum += 1

    sList =[]
    for y in range(yHexNum):
        row = []
        for x in range(xHexNum):
            row.append(copy.deepcopy(rect))
        sList.append(row)
    return sList

def hexPaste(screen,rect,rl):
    size = rect[2]
    hexaWidth = rect[2]*2
    hexaHeight = rect[2]*(3**0.5)
    x = -3*size/2
    y = -hexaHeight/2
    x0= 0
    y0= 0
    hexaUnit = unitHexagon(img,rect)
    for row in rl:
        for i in xrange(len(row)):
            
            if i % 2 == 0:
                screen.blit(hexaUnit,(x,y))
                x += size * 3
            else:
                screen.blit(hexaUnit,(x0,y0))
                x0+= size * 3
            
        x = -3*size/2
        x0= 0
        y += hexaHeight
        y0+= hexaHeight
    return

#++++++++++++++++++ rectangle +++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++

##can prob increase speed by making these 'rects' only be left/top
def makeRectList(r,screen):
    xChunkNum = int(screen.get_width() / (r[2] * 2))
    if screen.get_width() % (r[2]*2) != 0:
        xChunkNum += 1
    yChunkNum = int(screen.get_height() / (r[3]*2))
    if screen.get_height() % (r[3]*2) != 0:
        yChunkNum += 1
    rl = []
    for y in xrange(yChunkNum):
        row = []
        for x in xrange(xChunkNum):
            row.append(copy.deepcopy(r))
        rl.append(row)
    return rl

def rectPaste(screen,rl):
    x = 0
    y = 0
    for row in rl:
        for r in row:
            s = sub(img,r)
            q = quad(s)
            screen.blit(q,(x,y))
            x += q.get_width()
        x = 0
        y += q.get_height()
    return

##########################################################
#_____________________ 3. tool bars _____________________#
##########################################################

def load_tools(canvas):
    w = canvas.get_width()
    h = canvas.get_height()

    toolBar = pygame.Surface((w+10,110))
    pygame.draw.rect(toolBar,(200,200,200),(0,0,w+10,110))
    pygame.draw.rect(toolBar,(0,0,0),(0,3,w+10,103))
    toolBar.set_alpha(190)
    canvas.blit(toolBar,(0,h-125))
    caption(canvas)
    
    loadimg = pygame.image.load("loadimg.png").convert_alpha()
    trans_blit(canvas,loadimg,(20,h-120))
    
    saveimg = pygame.image.load("saveimg.png").convert_alpha()
    trans_blit(canvas,saveimg,(120,h-120))

    readimg = pygame.image.load("readW.png").convert_alpha()
    trans_blit(canvas,readimg,(220,h-110))
    
    return

def caption(canvas):
    w = canvas.get_width()
    h = canvas.get_height()
    caption = pygame.image.load("caption.png").convert_alpha()
    canvas.blit(caption,(w/2 -160,h-125))
    
    rectJ = pygame.image.load("rect.png").convert_alpha()
    canvas.blit(rectJ,(w/2 +110,h-120))
    hexJ = pygame.image.load("hex.png").convert_alpha()
    canvas.blit(hexJ,(w/2 +117,h-70))
    sizeJ = pygame.image.load("size.png").convert_alpha()
    canvas.blit(sizeJ,(w/2 +180,h-120))
    scaleJ = pygame.image.load("scale.png").convert_alpha()
    canvas.blit(scaleJ,(w/2 +180,h-70))
    musicJ = pygame.image.load("musicD.png").convert_alpha()
    canvas.blit(musicJ,(w/2 +250,h-70))
    return

def thumbNail(img,canvas,rect):
    img0 = quad(img)
    img1 = quad(img)
    img1.set_alpha(95)
    w = img0.get_width()
    h = img0.get_height()
    c = 100.0/w
    # c = 1

    thumbH = int(c*h)
    area = rect
    piece = pygame.Surface((rect[2],rect[3]))

    if shape == False:
        piece.blit(makeRectUnit(img0, rect),(0,0))
    else:
        piece.blit(sub(img0, rect),(0,0))
    
    thumb = pygame.Surface((w,h))
    thumb.blit(img1, (0,0))
    thumb.blit(piece,(rect[0]%w,rect[1]%h))

    thumbH = int(c*h)
    thumbScreen = pygame.Surface((100,thumbH))
    #thumbScreen = pygame.Surface((w,thumbH))
    thumbScreen.blit(pygame.transform.scale(thumb,(100,thumbH)),(0,0))
    #thumbScreen.blit(pygame.transform.scale(thumb,(w,thumbH)),(0,0))
    #canvas.blit(thumbScreen,(0,0))
    canvas.blit(thumbScreen,(canvas.get_width()-120,\
                             (canvas.get_height()-70)-h*c/2))
    return

def toolBar(canvas,img,rect):
    load_tools(canvas)
    thumbNail(img,canvas,rect)
    return
    

##########################################################
#_______________ 4. main loop of the game _______________#
##########################################################

#+++++++++++++++ various control functions+++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def rectControl(rl):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
        add = 1
        for row in rl[1:len(rl)]:
            for r in row:
                r[0] += add
                r[1] += add
            add+=1
    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
        add = 1
        for row in rl[1:len(rl)]:
            for r in row:
                r[0] -= add
                r[1] -= add
            add+=1
    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
        add = 1
        for row in rl:
            for r in row[1:len(row)]:
                r[0] += add
                r[1] += add
                add+=1
            add = 1
    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        add = 1
        for row in rl:
            for r in row[1:len(row)]:
                r[0] -= add
                r[1] -= add
                add+=1
            add = 1
    return

def pressButton_shape(shape):
    global tipShow
    w = canvas.get_width()
    h = canvas.get_height()
    
    # button data
    rect_rect = [(w/2+110,h-120),(w/2+160,h-70)]
    hex_rect = [(w/2+117,h-70),(w/2+167,h-20)]
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x = (pygame.mouse.get_pos())[0]
        y = (pygame.mouse.get_pos())[1]

        if (x >= rect_rect[0][0]) and (y >= rect_rect[0][1])\
           and (x <= rect_rect[1][0]) and (y <= rect_rect[1][1]):
            # press the button "rectangle"
            shape = True
            tipShow = not(tipShow)
            
        elif (x >= hex_rect[0][0]) and (y >= hex_rect[0][1])\
           and (x <= hex_rect[1][0]) and (y <= hex_rect[1][1]):
            shape = False
    return shape

def pressButton_img(imageControl):
    global readShow
    global musicOn
    w = canvas.get_width()
    h = canvas.get_height()
    
    # button data
    load_rect = [(20,h-120),(90,h-30)]
    save_rect = [(120,h-120),(210,h-30)]
    read_rect = [(220,h-120),(320,h-20)]
    size_rect = [(w/2 +180,h-120),(w/2 +240,h-60)]
    scale_rect = [(w/2 +180,h-70),(w/2 +240,h-10)]
    music_rect = [(w/2 +250,h-70),(w/2 + 300, h-20)]
    
    if event.type == MOUSEBUTTONDOWN :
        x = (pygame.mouse.get_pos())[0]
        y = (pygame.mouse.get_pos())[1]

        if (x >= load_rect[0][0]) and (y >= load_rect[0][1])\
           and (x <= load_rect[1][0]) and (y <= load_rect[1][1]):
            imageControl = "load"

        if (x >= save_rect[0][0]) and (y >= save_rect[0][1])\
           and (x <= save_rect[1][0]) and (y <= save_rect[1][1]):
            imageControl = "save"

        if (x >= read_rect[0][0]) and (y >= read_rect[0][1])\
           and (x <= read_rect[1][0]) and (y <= read_rect[1][1]):
            readShow = not(readShow)

        if (x >= size_rect[0][0]) and (y >= size_rect[0][1])\
           and (x <= size_rect[1][0]) and (y <= size_rect[1][1]):
            imageControl = "size"

        if (x >= scale_rect[0][0]) and (y >= scale_rect[0][1])\
           and (x <= scale_rect[1][0]) and (y <= scale_rect[1][1]):
            imageControl = "scale"
            
        if (x >= music_rect[0][0]) and (y >= music_rect[0][1])\
           and (x <= music_rect[1][0]) and (y <= music_rect[1][1]):
            musicOn = not(musicOn)
            
    return imageControl

#++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++

#______________ initialize ______________

#shape = True # False---hexagon type
              # True---rectangle type
              
xScroll = False
yScroll = False
shape = False
imageControl = ""
userSize = 60


#_________________________________________

canvas = pygame.display.set_mode((900,700))
pygame.display.set_caption("Kaleidoscope")
a = canvas.get_width()
b = canvas.get_height()

pygame.mixer.music.load("tada tada.mp3")
pygame.mixer.music.play(10)

screen = pygame.Surface((a,b))
screen.fill((0,0,0))
imgControl = ""
img2 = pygame.image.load('1.jpg').convert()
img2_c = img2
img = quad(img2)

userScale = img.get_width()


#________________ make invisable surfs_________________

loadD = pygame.image.load("loadD.png").convert_alpha()
saveD = pygame.image.load("saveD.png").convert_alpha()
sizeD = pygame.image.load("sizeD.png").convert_alpha()
scaleD = pygame.image.load("scaleD.png").convert_alpha()
errorD = pygame.image.load("errorD.png").convert_alpha()

tipW = pygame.image.load("tipW.png").convert_alpha()
tipD = pygame.image.load("tipD.png").convert_alpha()
tipD.blit(tipW,(0,0))

readD = pygame.image.load("readD.png").convert_alpha()
musicD = pygame.image.load("musicD.png").convert_alpha()
musicD2 = pygame.image.load("musicD2.png").convert_alpha()

if shape == False:
    # hex
    tri=[120,120,userSize]
    rect = makeRect(tri)
    rl = makeHexList(rect,screen)
else:
    #rect
    rect = [0,0,userSize,userSize/2]
    rl = makeRectList(rect,screen)
    
##################################################################
#_______________________ running part ___________________________#


while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN and
            event.key == pygame.K_ESCAPE):
            pygame.quit()
            
        # set the imageControl
        imageControl = pressButton_img(imageControl)
            
        # decide the shape
        shape0 = shape
        shape = pressButton_shape(shape)
        if shape != shape0:
            if shape == False:
                # hex
                tri=[rect[0],rect[1],rect[2]]
                rect = makeRect(tri)
                rl = makeHexList(rect,screen)
            else:
                #rect
                rl = makeRectList(rect,screen)
        
        if event.type == pygame.QUIT:
            running = False

        # is rectangular style, do some extra movement~~
        if shape == True:
            rectControl(rl)                    

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            xScroll = 'l'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            xScroll = 'r'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            yScroll = 'u'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            yScroll = 'd'
        
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT and\
           xScroll == 'l':
            xScroll = False
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT and\
           xScroll == 'r':
            xScroll = False
        if event.type == pygame.KEYUP and event.key == pygame.K_UP and\
           yScroll == 'u':
            yScroll = False
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN and\
           yScroll == 'd':
            yScroll = False

    # out of the loop now
    if shape == False:
        hexPaste(screen,rect,rl)
    else:
        rectPaste(screen,rl)

    for row in rl:
        for rect in row:
            if xScroll == 'l':
                rect[0] -= 1
                if rect[0] < 0:
                    rect[0] += img.get_width()
            if xScroll == 'r':
                rect[0] += 1
                if rect[0] >= img.get_width():
                    rect[0] -= img.get_width()
            if yScroll == 'u':
                rect[1] -= 1
                if rect[1] < 0:
                    rect[1] += img.get_height()
            if yScroll == 'd':
                rect[1] += 1
                if rect[1] >= img.get_height():
                    rect[1] -= img.get_height()

    canvas.blit(screen,(0,0))
    toolBar(canvas,img2,rect)
    
    # input box
    error0 = error
    if imageControl == "load":
        cText = main_load()
        try:
          img2 = pygame.image.load(cText).convert_alpha()
          img2_c = img2
        except:
          pass
        imageControl = ""
        
    elif imageControl == "save":
        try:
            cText = main_save()
            cText += ".JPG"
            pygame.image.save(screen,cText)
        except:
            pass
        imageControl = ""
        
    elif imageControl == "size":
        cText = main_size()
        try:
            if int(cText) > 0 and int(cText) < userScale and\
               int(cText) < 351:
                error = False
                userSize = int(cText)
                if shape == False:
                    # hex
                    tri[2]=userSize
                    rect = makeRect(tri)
                    rl = makeHexList(rect,screen)
                else:
                    #rect
                    rect[2] = userSize
                    rect[3] = userSize/2
                    rl = makeRectList(rect,screen)
            else:
                error = True
        except:
            pass
        imageControl = ""
        
    elif imageControl == "scale":
        w = img2_c.get_width()
        h = img2_c.get_height()
        cText = main_scale()

        try:
            if int(cText) > userSize:
                error = False
                userScale = int(cText)
                userHeight = int((1.0*userScale/w)*(h))
                scaleT = (userScale,userHeight)
                img1 = pygame.Surface(scaleT)
                img1.blit(pygame.transform.scale(img2_c,scaleT),(0,0))
                img2 = img1
                canvas.blit(img,(0,0))
            else:
                error = True
        except:
            pass
        imageControl = ""
        
          
        
       
        
    img = quad(img2)
    if error == True:
        canvas.blit(errorD,(a/2-200,b/2-180))
    if shape == True and tipShow == True: #special rectangle way of play!!!
        canvas.blit(tipD,(a/2-200,20))
    if readShow == True:
        canvas.blit(readD,(a/2-200,20))
    if musicOn == False:
        pygame.mixer.music.pause()
        canvas.blit(musicD2,(a/2 +250,b-70))
    elif musicOn == True:
        pygame.mixer.music.unpause()
        canvas.blit(musicD,(a/2 +250,b-70))
        
  
    pygame.display.flip()

pygame.display.flip()
