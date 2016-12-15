# -*- coding: cp936 -*-
'''
@小五义 http://www.cnblogs.com/xiaowuyi
一个超级简单的游戏
左右键控制小人移动去接空中下来的金币，接住金币得5分，接不住游戏结束，金币速度会随着level的关数
而越来越快
'''
import pygame,sys,os,random
pygame.init()

class rect():#画出小人
    def __init__(self,filename,initial_position):
        self.image=pygame.image.load(filename)
        self.rect=self.image.get_rect()
        self.rect.topleft=initial_position
        
class goldrect(pygame.sprite.Sprite):#绘出金币
    def __init__(self,gold_position,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('image\\gold.png')
        self.rect=self.image.get_rect()
        self.rect.topleft=gold_position
        self.speed=speed
    def move(self):
        self.rect=self.rect.move(self.speed)

        
        


def drawback(): #绘出背景图片
    my_back=pygame.image.load('image\\qi3.jpg') 
    bakscreen.blit(my_back,[0,0])

        
def loadtext(levelnum,score,highscore):#绘出成绩、level、最高分等
    my_font=pygame.font.SysFont(None,24)
    levelstr='Level:'+str(levelnum)
    text_screen=my_font.render(levelstr, True, (255, 0, 0))
    bakscreen.blit(text_screen, (650,50))
    highscorestr='Higescore:'+str(highscore)
    text_screen=my_font.render(highscorestr, True, (255, 0, 0))
    bakscreen.blit(text_screen, (650,80))
    scorestr='Score:'+str(score)
    text_screen=my_font.render(scorestr, True, (255, 0, 0))
    bakscreen.blit(text_screen, (650,110))    

def loadgameover(scorenum,highscore):#绘出GAME OVER
    my_font=pygame.font.SysFont(None,50)
    levelstr='GAME OVER'
    over_screen=my_font.render(levelstr, True, (255, 0, 0))
    bakscreen.blit(over_screen, (300,240))
    highscorestr='YOUR SCORE IS '+str(scorenum)
    over_screen=my_font.render(highscorestr, True, (255, 0, 0))
    bakscreen.blit(over_screen, (280,290))
    if scorenum>int(highscore):#写入最高分
        highscorestr='YOUR HAVE GOT THE HIGHEST SCORE!'
        text_screen=my_font.render(highscorestr, True, (255, 0, 0))
        bakscreen.blit(text_screen, (100,340))
        highfile=open('highscore','w')
        highfile.writelines(str(scorenum))  
        highfile.close()  
    
def gethighscore(): #读取最高分
    if os.path.isfile('highscore'):
        highfile=open('highscore','r')
        highscore=highfile.readline() 
        highfile.close() 
    else:
        highscore=0
    return highscore
                  
bakscreen=pygame.display.set_mode([800,600])
bakscreen.fill([0,160,233])
pygame.display.set_caption('Dig!Dig!')
drawback()



levelnum=1 #level
scorenum=0 #得分
highscore=gethighscore()#最高分
ileft=1  #记录向左移动步数，用来控制图片
iright=10 #记录向右移动步数，用来控制图片
x=100
y=450
filename='image\\1.png'
backimg_ren=rect(filename,[x,y])
bakscreen.blit(backimg_ren.image,backimg_ren.rect)
loadtext(levelnum,scorenum,highscore)
goldx=random.randint(50,580)
speed=[0,levelnum]
mygold=goldrect([goldx,100],speed) 
pygame.display.update()

while True:
    if scorenum>0 and scorenum/50.0==int(scorenum/50.0):#当得分是50的倍数时修改level
        levelnum=scorenum/50+1
        speed=[0,levelnum]
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    #make gold    

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:#按下左键

        drawback()  
        loadtext(levelnum,scorenum,highscore)

        if iright > 14 :iright=10
        iright=iright+1
        filename='image\\'+str(iright)+'.png'
        if x<50 :
            x=50
        else:
            x=x-10

        backimg_surface=rect(filename,[x,y])
        bakscreen.blit(backimg_surface.image,backimg_surface.rect)

        
    if pressed_keys[pygame.K_RIGHT]:#按下右键

        drawback()
        loadtext(levelnum,scorenum,highscore)

        if ileft > 4 :ileft=0
        ileft=ileft+1
        filename='image\\'+str(ileft)+'.png'
        if x>560:
            x=560
        else:
            x=x+10

        backimg_surface=rect(filename,[x,y])
        bakscreen.blit(backimg_surface.image,backimg_surface.rect)

    drawback()
    loadtext(levelnum,scorenum,highscore)
    mygold.move()
    bakscreen.blit(mygold.image,mygold.rect) 
    
    backimg_surface=rect(filename,[x,y])
    bakscreen.blit(backimg_surface.image,backimg_surface.rect)
    if mygold.rect.top>600:#判断金币是否着地，一但着地，游戏结束
        loadgameover(scorenum,highscore)
    if mygold.rect.colliderect(backimg_surface.rect):#判断金币是否与小人碰撞，如果碰撞表示小人接到金币
        scorenum+=5
        loadtext(levelnum,scorenum,highscore)
        goldx=random.randint(50,580)
        mygold=goldrect([goldx,100],speed) 
    pygame.display.update()
