import random
import pygame

#屏幕大小的常量
WINDOWS_RECT = pygame.Rect(0,0,512,768)
#帧率设置
FRAME_PER_SEC = 60
#创建敌机的定时器常量
ENEMY_EVENT = pygame.USEREVENT
#英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    """游戏精灵"""
    def __init__(self,image_name,speed=1):
        #调用父类初始化方法
        super().__init__()
        #定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.speed_2 = speed

    def update(self):
        #在屏幕的垂直方向上移动
        self.rect.y += self.speed

class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self,is_alt=False):
        #调用父类的方法实现
        super().__init__("./图像素材/bg/background.png")
        #判断交替图像，设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        #调用父类的方法实现
        super().update()
        #判断是否移出屏幕，如果是，则设置到屏幕上方
        if self.rect.y >= WINDOWS_RECT.height:
            self.rect.y = -self.rect.height

class Enemy(GameSprite):
    """敌机精灵"""
    def __init__(self):
        #调用父类方法，创建敌机精灵，指定敌机图片
        super().__init__("./图像素材/enemy/enemy.png")
        #指定敌机初始随机速度
        self.speed = random.randint(1,3)
        #指定敌机初始随机位置
        self.rect.bottom = 0
        max_x = WINDOWS_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)

    def update(self):
        #调用父类方法，保持垂直飞行
        super().update()
        #判断是否飞出屏幕，是则从精灵组删除敌机
        if self.rect.y >= WINDOWS_RECT.height:
            #将精灵从所有组中删除
           self.kill()

    def __del__(self):
        #print("敌机被摧毁%s"%self.rect)
        pass

class Hero(GameSprite):
    """英雄精灵"""
    def __init__(self):
        #调用父类方法，设置英雄图片和速度
        super().__init__("./图像素材/hero/hero.png",speed=0)
        #指定英雄初始位置
        self.rect.centerx = WINDOWS_RECT.centerx
        self.rect.bottom = WINDOWS_RECT.bottom
        #创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        #英雄在水平方向移动
        self.rect.x += self.speed
        # 英雄在垂直方向移动
        self.rect.y += self.speed_2
        #控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > WINDOWS_RECT.right:
            self.rect.right = WINDOWS_RECT.right
        elif self.rect.top < WINDOWS_RECT.top:
            self.rect.top = WINDOWS_RECT.top
        elif self.rect.bottom > WINDOWS_RECT.bottom:
            self.rect.bottom = WINDOWS_RECT.bottom

    def fire(self):
        for i in (0,1,2):
            #创建子弹精灵
            bullet = Bullet()
            #设置精灵的位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            #将精灵添加到精灵组
            self.bullets.add(bullet)

class Bullet(GameSprite):
    """子弹精灵"""
    def __init__(self):
        #调用父类方法，设置子弹图片和速度
        super().__init__("./图像素材/bullet/bullet.png",speed=-2)

    def update(self):
        # 调用父类方法，让子弹沿垂直飞行
        super().update()
        # 判断子弹是否飞出屏幕，是则从精灵组删除敌机
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        #print("子弹被摧毁%s"%self.rect)
        pass