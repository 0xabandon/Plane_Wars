import pygame
from game_sprites import *

class PlaneGame(object):
    """主游戏"""
    def __init__(self):
        print("游戏初始化")
        # 窗口绘制
        self.windows = pygame.display.set_mode(WINDOWS_RECT.size, flags=0, depth=0)
        # 创建时钟
        self.clock = pygame.time.Clock()
        #调用私有方法，精灵和精灵组的创建
        self.__creat_sprites()
        #设置创建敌机
        pygame.time.set_timer(ENEMY_EVENT,1000)
        #设置发射子弹
        pygame.time.set_timer(HERO_FIRE_EVENT,500)
    def __creat_sprites(self):
        #创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1,bg2)
        #创建英雄精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        #创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
    def start_game(self):
        print("游戏开始...")
        #游戏循环
        while True:
            # 设置帧率
            self.clock.tick(FRAME_PER_SEC)
            #事件监听
            self.__event_handler()
            #碰撞检测
            self.__check_collide()
            #更新/绘制精灵组
            self.__update_sprites()
            #更新显示
            pygame.display.update()
    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否为退出
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            #创建敌机
            elif event.type == ENEMY_EVENT:
                #print("敌机出场...")
                # 创建敌机精灵
                enemy = Enemy()
                #将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)
            #发射子弹
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
        #使用键盘提供的方法获取键盘按键(按键元组)
        keys_pressed = pygame.key.get_pressed()
        #判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        elif keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_UP]:
            self.hero.speed_2 = -2
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed_2 = 2
        else:
            self.hero.speed = 0
            self.hero.speed_2 = 0
    def __check_collide(self):
        #子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        #敌机摧毁英雄
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        if len(enemies) > 0:
            #英雄牺牲
            self.hero.kill()
            #结束游戏
            PlaneGame.__game_over()
    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.windows)

        self.enemy_group.update()
        self.enemy_group.draw(self.windows)

        self.hero_group.update()
        self.hero_group.draw(self.windows)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.windows)
    #静态方法
    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()





if __name__ == '__main__':
    #创建游戏对象
    game = PlaneGame()
    #启动游戏
    game.start_game()