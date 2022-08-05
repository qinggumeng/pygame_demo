import sys
import random
import os
import pygame

class Bullet:
  def __init__(self,x,y,s,i):
   self.x = x
   self.y = y
   self.s = s
   self.i = i

class Enemy:
  def __init__(self,x,y,s,i):
    self.x = x
    self.y = y
    self.s = s
    self.i = i
  
# 1.pygame的初始化
pygame.init()

# 2.创建一个窗口，设定宽高
screen = pygame.display.set_mode((350,512))

# 下面三句是播放音乐
pygame.mixer.init() 
bgmusic = pygame.mixer.music.load('audio/bgm.mp3')
bulletMusic = pygame.mixer.Sound('audio/bullet.mp3')
boomMusic = pygame.mixer.Sound('audio/boom.mp3')
pygame.mixer.music.play(loops=10000, start=0.0)

# 3.设置窗口标题
pygame.display.set_caption("飞机大战")

common_img = pygame.image.load('images/Common.png').convert()
common_img = pygame.transform.scale(common_img,(1500,1500))
common_img.set_colorkey(([0,0,0]))
failTip = pygame.Surface((330,294))
failTip.blit(common_img,(-10,-10))
bg = pygame.image.load('images/bg.jpg').convert()
hero = pygame.image.load('images/hero.png').convert()
hero = pygame.transform.scale(hero,(93,75))
hero.set_colorkey(([0,0,0]))

i = 0
isDown = False
heroPos = (120,380)

enemys = []

def createEnemy():
  for i in range(5):
    enemy = pygame.image.load('images/enemy.png').convert()
    enemy = pygame.transform.scale(enemy,(80,54))
    enemy.set_colorkey(([0,0,0]))
    enemys.append(Enemy((i%3)*100+20,-i*100-100,5,enemy))

createEnemy()

bullets = []

def createBullet():
  for i in range(1):
    bullet = pygame.image.load('images/bullet.png')
    bullet = pygame.transform.scale(bullet,(16,27))
    bullet.set_colorkey(([255,255,255]))   
    bullets.append(Bullet(heroPos[0]+38,heroPos[1]-30,10,bullet))
    bulletMusic.play()

createBullet()

booms = []

class Boom:
  def __init__(self,x,y,imgs):
    self.x = x
    self.y = y
    self.k = 0
    self.imgs = imgs

def createBoom(x,y):
  imgs = []
  for i in range(19):
    boom = pygame.image.load('images/explosion'+str(i+1)+'.png')
    imgs.append(boom)
  booms.append(Boom(x,y,imgs))

score = 0
isover = False

# 4.开启一个循环，使程序不停止运行
while True:
  for e in pygame.event.get():
    if(e.type==pygame.QUIT):
      pygame.quit()
      sys.exit()
    if(e.type==pygame.MOUSEBUTTONDOWN):
      print('鼠标被按下',e.pos)
      isDown = True
    if(e.type==pygame.MOUSEMOTION):
      if(isDown):
        heroPos = (e.pos[0]-45,e.pos[1]-37)
        #print('鼠标在移动',e.pos[0])
    if(e.type==pygame.MOUSEBUTTONUP):
      print('鼠标被松开')
      isDown = False
  if(isover):
    screen.blit(failTip,(10,100))
    myfont2 = pygame.font.SysFont("Arial", 28)
    font_surface2 = myfont.render("GAME OVER!", True, (255,255,255))
    screen.blit(font_surface2,(120,250))
    pygame.display.update()
    continue
  
  screen.blit(bg,(0,-i))
  screen.blit(bg,(0,512-i))
  for e in enemys:
    e.y = e.y + e.s
    if(e.y>=600):
      enemys.remove(e)
    else:
      screen.blit(e.i,(e.x,e.y)) 
      if(heroPos[0]>=e.x and heroPos[0]<=e.x+80 and heroPos[1]>=e.y and heroPos[1]<=e.y+54):
        isover = True
  if(len(enemys)==0):
    createEnemy() 
  screen.blit(hero,heroPos)
  
  for bb in booms:
    if(len(bb.imgs)==19):
      screen.blit(bb.imgs[bb.k%19],(bb.x,bb.y))
      bb.k = bb.k + 1
    if(bb.k==19):
      boomMusic.play()
      booms.remove(bb)

  for b in bullets:
    b.y = b.y - b.s
    if(b.y<=-50):
      bullets.remove(b)
    else:
      screen.blit(b.i,(b.x,b.y))
      for e in enemys:
        if(b.x>=e.x and b.x<=e.x+80 and b.y>=e.y and b.y<=e.y+54):
          bullets.remove(b)
          enemys.remove(e)
          createBoom(e.x,e.y) 
          score = score + 1    

  if(i%20==0):
    #createBoom(random.randint(20,300),random.randint(20,500))
    createBullet()
  i = (i - 1)% 512
  
  myfont = pygame.font.SysFont("Arial", 18) 
  font_surface = myfont.render(str(score), True, (255,255,255))
  screen.blit(font_surface,(10,10))
  pygame.display.update()
