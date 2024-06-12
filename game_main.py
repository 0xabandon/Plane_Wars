import pygame
import sys
import traceback
import game_hero
import game_enemy
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# 屏幕大小的常量
WINDOWS_SIZE = (480,852)
# 帧率常量
FRAME_PER_SEC = 60
# 绘制窗口
windows = pygame.display.set_mode(WINDOWS_SIZE)
# 设置标题
pygame.display.set_caption("飞机大战 ")
# 创建背景
backgroud = pygame.image.load("./image/background.png").convert()

# 设置音量
volume = 0.3
volume_2 = 0.3
# 载入音效
# 游戏开始页面音效
start_music = pygame.mixer.Sound("sound\\BGM_long.wav")
start_music.set_volume(volume)
# 游戏背景音乐
pygame.mixer.music.load("sound\\BGM.wav")
pygame.mixer.music.set_volume(volume_2)  # 音乐的音量设定，值在0到1
# 玩家死亡音效
user_getover = pygame.mixer.Sound("sound\\game_over.wav")
user_getover.set_volume(volume)
# 玩家获取炸弹道具音效
get_bomb_sound = pygame.mixer.Sound("sound\\get_bomb.wav")
get_bomb_sound.set_volume(volume)
# 玩家获取双倍炸弹音效
get_double_sound = pygame.mixer.Sound("sound\\get_double_laser.wav")
get_double_sound.set_volume(volume)
# 玩家开枪音效
bullet_sound = pygame.mixer.Sound("sound\\bullet.wav")
bullet_sound.set_volume(volume)
# 玩家中弹音效
get_bullet_sound = pygame.mixer.Sound("sound\\out_porp.wav")
get_bullet_sound.set_volume(volume)
# 按钮音效
button_sound = pygame.mixer.Sound("sound\\button.wav")
button_sound.set_volume(volume)
# 小型飞机毁灭音效
enemy0_down_sound = pygame.mixer.Sound("sound\\enemy0_down.wav")
enemy0_down_sound.set_volume(volume)
# 中型飞机毁灭音效
enemy1_down_sound = pygame.mixer.Sound("sound\\enemy1_down.wav")
enemy1_down_sound.set_volume(volume)
# 大型飞机毁灭音效
enemy2_down_sound = pygame.mixer.Sound("sound\\enemy2_down.wav")
enemy2_down_sound.set_volume(volume)
# 大型飞机出场音效
enemy2_appear_sound = pygame.mixer.Sound("sound\\big_plane_flying.wav")
enemy2_appear_sound.set_volume(volume)
# 使用全局炸弹音效
use_bomb_sound = pygame.mixer.Sound("sound\\use_bomb.wav")
use_bomb_sound.set_volume(volume)

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = game_enemy.SmallEnemy(WINDOWS_SIZE)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = game_enemy.MidEnemy(WINDOWS_SIZE)
        group1.add(e2)
        group2.add(e2)

def add_boss_enemies(group1, group2, num):
    for i in range(num):
        e3 = game_enemy.BossEnemy(WINDOWS_SIZE)
        group1.add(e3)
        group2.add(e3)

def main():
    pygame.mixer.music.play(-1)
    # 创建英雄
    hero = game_hero.Hero(WINDOWS_SIZE)
    swith_image = True
    # 创建敌机
    enemies = pygame.sprite.Group()
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)
    boss_enemies = pygame.sprite.Group()
    add_boss_enemies(boss_enemies, enemies, 2)
    # 击中图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    hero_destroy_index = 0
    # 延迟
    dalay = 100
    # 创建时钟
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # 键盘操作
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            hero.moveup()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            hero.movedown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            hero.moveleft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            hero.moveright()
        # 绘制背景
        windows.blit(backgroud,(0,0))
        # 绘制英雄
        swith_image = not swith_image
        if hero.active:
            if swith_image:
                windows.blit(hero.image1, hero.rect)
            else:
                windows.blit(hero.image2, hero.rect)
        else:
            if not (dalay % 3):
                windows.blit(hero.destroy_images[hero_destroy_index], hero.rect)
                hero_destroy_index = (hero_destroy_index + 1) & 4
                if hero_destroy_index == 0:
                    print("Game Over!")
                    running = False
        # 绘制敌机
        for each in boss_enemies:
            if each.active:
                each.move()
                if swith_image:
                    windows.blit(each.image1, each.rect)
                else:
                    windows.blit(each.image1, each.rect)
                if each.rect.bottom == -50:
                    enemy2_appear_sound.play(-1)
            else:
                if not(dalay % 3):
                    if e3_destroy_index == 0:
                        enemy2_down_sound.play()
                    windows.blit(each.destroy_images[e3_destroy_index], each.rect)
                    e3_destroy_index = (e3_destroy_index + 1) & 6
                    if e3_destroy_index == 0:
                        enemy2_appear_sound.stop()
                        each.reset()
        for each in mid_enemies:
            if each.active:
                each.move()
                windows.blit(each.image, each.rect)
            else:
                if not(dalay % 3):
                    if e2_destroy_index == 0:
                        enemy1_down_sound.play()
                    windows.blit(each.destroy_images[e2_destroy_index], each.rect)
                    e2_destroy_index = (e2_destroy_index + 1) & 4
                    if e2_destroy_index == 0:
                        each.reset()
        for each in small_enemies:
            if each.active:
                each.move()
                windows.blit(each.image, each.rect)
            else:
                if not(dalay % 3):
                    if e1_destroy_index == 0:
                        enemy0_down_sound.play()
                    windows.blit(each.destroy_images[e1_destroy_index], each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) & 4
                    if e1_destroy_index == 0:
                        each.reset()
        # 检测碰撞
        enemies_down = pygame.sprite.spritecollide(hero, enemies, False, pygame.sprite.collide_mask)
        if enemies_down:
            hero.active = False
            for e in enemies_down:
                e.active = False
        # 切换图片
        if not(dalay % 5):
            swith_image = not swith_image
        dalay -= 1
        if not dalay:
            dalay = 100

        pygame.display.flip()
        # 设置帧率
        clock.tick(FRAME_PER_SEC)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()