# -*- coding: utf-8 -*-
# @Author: Kali
# @Date:   2016-12-13 11:11:07
# @Last Modified by:   Marte
# @Last Modified time: 2016-12-14 15:48:03

import pygame
import random
import copy
'''
        初始蛇的长度  10 10 也就是蛇的 X Y 坐标  窗体的大小为 500   500
'''
class snake:
    def __init__(self):
        """
        init the snake
        """
        self.poslist = [[10,10]]
    def position(self):
        """
        return the all of the snake's point
        """
        return self.poslist

    def gowhere(self,where):
        """
        change the snake's point to control the snake's moving direction
        """
        pos = len(self.poslist) - 1

        while pos > 0:
            self.poslist[pos] = copy.deepcopy(self.poslist[pos-1])
            pos -= 1
            print 'location' + `self.poslist[pos]`

        if where is 'U':
            self.poslist[pos][1]    -= 10
            if self.poslist[pos][1]  < 0:
                self.poslist[pos][1] = 500

        if where is 'D':
            self.poslist[pos][1]    += 10
            if self.poslist[pos][1]  > 500:
                self.poslist[pos][1] = 0

        if where is 'L':
            self.poslist[pos][0]    -= 10
            if self.poslist[pos][0]  < 0:
                self.poslist[pos][0] = 500

        if where is 'R':
            self.poslist[pos][0]    += 10
            if self.poslist[pos][0]  > 500:
                self.poslist[pos][0] = 0

    def eatfood(self,foodpoint):
        """
        eat the food and add point to snake
        """
        self.poslist.append(foodpoint)

# food Unit
class food:
    def __init__(self):
        """
        init the food's point
        """
        self.x = random.randint(10,490)
        self.y = random.randint(10,490)
    def display(self):
        """
        init the food's point and return the point
        """
        self.x = random.randint(10,490)
        self.y = random.randint(10,490)
        return self.position()
    def position(self):
        """
        return the food's point
        """
        return [self.x,self.y]
# food Done

# main Unit
def main():
    # 初始小蛇方向
    moveup = False
    movedown = False
    moveleft = False
    moveright = True

    pygame.init()

    clock   = pygame.time.Clock()
    screen  = pygame.display.set_mode((500,500),0,32)
    restart = True

    '''
            首先设置蛇的一个运行方向  接下来判断键盘事件在决定蛇的运行方向
            蛇可以运行起来了  那么接下来就是 吃食物增加自己的长度 和 不吃食物在不同的位置显示
    '''
    while restart:

        # 创建食物和小蛇
        sk = snake()
        fd = food()

        # 初始化标题 和 蛇的运行方向
        screentitle = pygame.display.set_caption("eat snake")
        sk.gowhere('R')
        running = True

        while running:
            # fill the background is white
            screen.fill([255,255,255])
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                # judge the down key
                if event.type == pygame.KEYDOWN:
                    # 上键
                    if event.key == pygame.K_UP:
                        moveup    = True
                        movedown  = False
                        moveleft  = False
                        moveright = False
                    # 下键
                    if event.key == pygame.K_DOWN:
                        moveup    = False
                        movedown  = True
                        moveleft  = False
                        moveright = False
                    # 左键
                    if event.key == pygame.K_LEFT:
                        moveup    = False
                        movedown  = False
                        moveleft  = True
                        moveright = False
                    #右键
                    if event.key == pygame.K_RIGHT:
                        moveup    = False
                        movedown  = False
                        moveleft  = False
                        moveright = True
            # where the snake goes
            time_pass = clock.tick(20)
            if moveup:
                sk.gowhere('U')
            if movedown:
                sk.gowhere('D')
            if moveleft:
                sk.gowhere('L')
            if moveright:
                sk.gowhere('R')

            # draw the food
            poslist   = sk.position()
            foodpoint = fd.position()
            fdrect = pygame.draw.circle(screen,[255,0,0],foodpoint,15,0)

            # draw the snafe
            # pygame.draw.circle()用来画圆形，具体包括五个参数：(1)画圆的表面，在本例中用screen创建了一个窗口，所以是画在screen表面上。(2)用什么颜色来画，如用红色[255,0,0]。(3)在什么位置画，[top,left]。(4)直径。(5)线宽，其中0表示完成填充。
            snaferect = []
            for pos in poslist:
                snaferect.append(pygame.draw.circle(screen,[255,0,0],pos,5,0))
                print 'snake ' + `snaferect`
                # crash test if the snake eat food
                if fdrect.collidepoint(pos):
                    foodpoint = fd.display()
                    sk.eatfood(foodpoint)
                    fdrect = pygame.draw.circle(screen,[255,0,0],foodpoint,15,0)
                    break
            # crash test if the snake crash itsself
            headrect = snaferect[0]
            count = len(snaferect)
            while count > 1:
                if headrect.colliderect(snaferect[count-1]):
                    running = False
                count -= 1
            pygame.display.update()

        # game over background
        pygame.font.init()
        screen.fill([100,0,0])
        font = pygame.font.Font(None,48)
        text = font.render("Game Over !!!",True,(255,0,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(text,textRect)

        # keydown r restart,keydown n exit
        while 1:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart = True
                    del sk
                    del fd
                    break
                if event.key == pygame.K_n:
                    restart = False
                    break
            pygame.display.update()


if __name__=='__main__':
    main()
