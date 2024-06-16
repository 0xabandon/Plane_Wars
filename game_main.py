import pygame
import sys
import traceback
import game_hero
import game_enemy
import game_bullet
import game_supply
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

# 屏幕大小的常量
WINDOWS_SIZE = width, height = 480, 852
# 帧率常量
FRAME_PER_SEC = 60
# 绘制窗口
windows = pygame.display.set_mode(WINDOWS_SIZE)
# 设置标题
pygame.display.set_caption("飞机大战 ")
# 创建背景
background = pygame.image.load("./image/background.png").convert()
# 设置颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

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
user_get_over = pygame.mixer.Sound("sound\\game_over.wav")
user_get_over.set_volume(volume)
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

def inc_speed(target, inc):
    for each in target:
        each.speed += inc

def main():
    # 背景音乐
    pygame.mixer.music.play(-1)
    # 创建英雄
    hero = game_hero.Hero(WINDOWS_SIZE)
    # 创建敌机
    enemies = pygame.sprite.Group()
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)
    boss_enemies = pygame.sprite.Group()
    add_boss_enemies(boss_enemies, enemies, 2)
    # 创建子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(game_bullet.Bullet1(hero.rect.midtop))
    # 创建子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullet2.append(game_bullet.Bullet2((hero.rect.centerx - 33, hero.rect.centery)))
        bullet2.append(game_bullet.Bullet2((hero.rect.centerx + 30, hero.rect.centery)))
    # 击中图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    hero_destroy_index = 0
    # 用于切换图片
    switch_image = True
    # 延迟
    delay = 100
    # 用于阻止重复打开记录文件
    record_score = 0
    recorded = False
    # 游戏结束画面
    gameover_font = pygame.font.Font("font/字魂50号-白鸽天行体.ttf", 48)
    again_image = pygame.image.load("image/btn_finish.png").convert_alpha()
    again_rect = again_image.get_rect()
    # 创建时钟
    clock = pygame.time.Clock()
    # 超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1
    # 是否使用超级子弹
    is_double_bullet = False
    # 解除我方无敌状态定时器
    INVINCIBLE_TIME = USEREVENT + 2
    # 统计得分
    score = 0
    score_font = pygame.font.Font("./font/字魂50号-白鸽天行体.ttf", 36)
    # 标志是否暂停
    paused = False
    pause_nor_image = pygame.image.load("./image/game_pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("./image/game_pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("./image/game_resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("./image/game_resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image
    # 设置难度等级
    level = 1
    # 全屏炸弹
    bomb_image = pygame.image.load("./image/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("./font/字魂50号-白鸽天行体.ttf", 48)
    bomb_num = 3
    # 每30秒发一个补给包
    bullet_supply = game_supply.Bullet_Supply(WINDOWS_SIZE)
    bomb_supply = game_supply.Bomb_Supply(WINDOWS_SIZE)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
    # 生命数量
    life_image = pygame.image.load("./image/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        use_bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
            elif event.type == INVINCIBLE_TIME:
                hero.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)
        # 绘制背景
        windows.blit(background, (0, 0))
        # 根据得分增加难度
        if level == 1 and score > 50000:
            level = 2
            # 增肌3架小型飞机、2架中型飞机和1架boss
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_boss_enemies(boss_enemies, enemies, 1)
            # 提升小型飞机的速度
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            # 增肌5架小型飞机、3架中型飞机和2架boss
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_boss_enemies(boss_enemies, enemies, 2)
            # 提升小型飞机和中型飞机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 600000:
            level = 4
            # 增肌5架小型飞机、3架中型飞机和2架boss
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_boss_enemies(boss_enemies, enemies, 2)
            # 提升所有飞机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(boss_enemies, 1)
        elif level == 4 and score > 1000000:
            level = 5
            # 增肌5架小型飞机、3架中型飞机和2架boss
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_boss_enemies(boss_enemies, enemies, 2)
            # 提升所有飞机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(boss_enemies, 1)

        if life_num and not paused:
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
            # 绘制炸弹补给并检测
            if bomb_supply.active:
                bomb_supply.move()
                windows.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, hero):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
            # 绘制超级子弹补给并检测
            if bullet_supply.active:
                bullet_supply.move()
                windows.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, hero):
                    get_double_sound.play()
                    # 发射超级子弹
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False
            # 绘制英雄
            switch_image = not switch_image
            if hero.active:
                if switch_image:
                    windows.blit(hero.image1, hero.rect)
                else:
                    windows.blit(hero.image2, hero.rect)
            else:
                if not (delay % 3):
                    windows.blit(hero.destroy_images[hero_destroy_index], hero.rect)
                    hero_destroy_index = (hero_destroy_index + 1) & 4
                    if hero_destroy_index == 0:
                        life_num -= 1
                        hero.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)
                        '''print("Game Over!")
                        running = False'''
            # 发射子弹
            if not(delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((hero.rect.centerx - 33, hero.rect.centery))
                    bullets[bullet2_index + 1].reset((hero.rect.centerx + 30, hero.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(hero.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM
            # 检测子弹
            for b in bullets:
                if b.active:
                    b.move()
                    windows.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or boss_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            # 绘制敌机
            # BOSS飞机
            for each in boss_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        windows.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            windows.blit(each.image1, each.rect)
                        else:
                            windows.blit(each.image1, each.rect)
                    # 绘制血槽
                    pygame.draw.line(windows, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 生命大于20%显示绿色,否则为红色
                    energy_remain = each.energy / game_enemy.BossEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(windows, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                    # BOSS登场音
                    if each.rect.bottom == -50:
                        enemy2_appear_sound.play(-1)
                else:
                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            enemy2_down_sound.play()
                        windows.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) & 6
                        if e3_destroy_index == 0:
                            enemy2_appear_sound.stop()
                            score += 10000
                            each.reset()
            # 中型飞机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        windows.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        windows.blit(each.image, each.rect)
                    # 绘制血槽
                    pygame.draw.line(windows, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 生命大于20%显示绿色,否则为红色
                    energy_remain = each.energy / game_enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(windows, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                else:
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy1_down_sound.play()
                        windows.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) & 4
                        if e2_destroy_index == 0:
                            score += 5000
                            each.reset()
            # 小型飞机
            for each in small_enemies:
                if each.active:
                    each.move()
                    windows.blit(each.image, each.rect)
                else:
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            enemy0_down_sound.play()
                        windows.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) & 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()
            # 检测碰撞
            enemies_down = pygame.sprite.spritecollide(hero, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not hero.invincible:
                hero.active = False
                for e in enemies_down:
                    e.active = False
            # 绘制炸弹数量
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            bomb_text_rect = bomb_text.get_rect()
            windows.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            windows.blit(bomb_text, (20 + bomb_rect.width, height - 5 - bomb_text_rect.height))
            # 绘制得分
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            windows.blit(score_text, (10, 5))
        # 绘制剩余生命数量
        if life_num:
            for i in range(life_num):
                windows.blit(life_image, \
                             (width - 10 - (i + 1) * life_rect.width, \
                              height - 10 - life_rect.height))
        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()
            # 停止全部音效
            pygame.mixer.stop()
            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)
            if not recorded:
                recorded = True
                # 读取历史最高得分
                with open("record.txt", "r") as f:
                    record_str = f.read().strip()  # 去除字符串两端的空白字符
                    if record_str:
                        record_score = int(record_str)
                    else:
                        record_score = 0
                # 如果玩家得分高于历史最高分，则更新记录
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))
            # 绘制结束界面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            windows.blit(record_score_text, (10, 45))
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
            windows.blit(gameover_text1, gameover_text1_rect)
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
            windows.blit(gameover_text2, gameover_text2_rect)
            again_rect.left, again_rect.top = (width - again_rect.width) // 2, gameover_text2_rect.bottom + 50
            windows.blit(again_image, again_rect)
            # 检测用户鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击"重新开始"
                if again_rect.left < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数 ，重新开始游戏
                    main()
        # 绘制按钮
        windows.blit(paused_image, paused_rect)
        # 切换图片
        if not(delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100

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