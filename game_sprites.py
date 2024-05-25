import pygame

#屏幕大小的常量
WINDOWS_RECT = pygame.Rect(0,0,512,768)
#帧率设置
FRAME_PER_SEC = 60

class GameSprite(pygame.sprite.Sprite):
    """游戏精灵"""
    def __init__(self,image_name,speed=1):
        #调用父类初始化方法
        super().__init__()
        #定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

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