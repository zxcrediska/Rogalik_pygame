import sys
import csv
from random import choice, randint
import pygame
import os
from math import hypot


pygame.init()

WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
FPS = 120
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def get_map_name():
    filename = ['map1.txt', 'map2.txt', 'map3.txt']
    global count_level_game
    if not os.path.isfile("data/" + filename[count_level_game]):
        print("ERROR")
        terminate()
    return filename[count_level_game]


def load_map(filename):
    file = "data/" + filename
    with open(file, 'r') as mapFile:
        level_map = mapFile.readlines()

    max_width = max(map(len, level_map)) - 1

    return list(map(lambda x: x.strip().ljust(max_width, '.'), level_map))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):  # если файл не существует, то выходим
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def start_screen():
    font_path = os.path.join('data', 'joystix monospace.ttf')
    params = (True, (255, 255, 255))
    font = pygame.font.Font(font_path, 25)
    fon = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    global count_level_game

    with open('info.csv', "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lvl_game = int(row["lvl_game"])
            lvl_hero = int(row['lvl_hero'])
            exp_hero = int(row['exp_hero'])

    pygame.draw.rect(screen, (0, 31, 92), (440, 310, 150, 70), 30)
    pygame.draw.rect(screen, (255, 0, 0), (440, 430, 150, 70), 30)

    if lvl_game == 0 and lvl_hero == 1 and exp_hero == 0:
        text_surface = font.render('Играть', *params)
        screen.blit(text_surface, (450, 265))
    else:
        text_surface = font.render('Продолжить', *params)
        screen.blit(text_surface, (420, 265))
        pygame.draw.rect(screen, (255, 186, 0), (50, 700, 120, 70), 30)
        text_surface = font.render('Новая игра', *params)
        screen.blit(text_surface, (15, 650))

    text_surface = font.render('Выход', *params)
    screen.blit(text_surface, (460, 515))

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 430:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 500:
                        terminate()
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 310:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 380:
                        with open('info.csv', "r", newline="") as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                count_level_game = int(row["lvl_game"])
                                info = generate_map(load_map(get_map_name()))
                                info[0].level = int(row['lvl_hero'])
                                info[0].exp = int(row['exp_hero'])
                                return info[0], info[1], info[2]
                if not (lvl_game == 0 and lvl_hero == 1 and exp_hero == 0):
                    if pygame.mouse.get_pos()[0] >= 50 and pygame.mouse.get_pos()[1] >= 700:
                        if pygame.mouse.get_pos()[0] <= 170 and pygame.mouse.get_pos()[1] <= 770:
                            with open('info.csv', 'w', newline='') as f:
                                columns = ['lvl_game', 'lvl_hero', 'exp_hero']
                                writer = csv.DictWriter(f, fieldnames=columns)
                                writer.writeheader()

                                info = {"lvl_game": 0, "lvl_hero": 1, 'exp_hero': 0}
                                writer.writerow(info)
                            info = generate_map(load_map(get_map_name()))
                            return info[0], info[1], info[2]
        pygame.display.flip()
        clock.tick(FPS)


def dead_screen():
    font_path = os.path.join('data', 'joystix monospace.ttf')
    params = (True, (255, 0, 0))
    font = pygame.font.Font(font_path, 50)
    fon = pygame.transform.scale(load_image('lose.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    pygame.draw.rect(screen, (0, 255, 0), (440, 350, 150, 70), 30)
    pygame.draw.rect(screen, (255, 0, 0), (440, 480, 150, 70), 30)

    text_surface = font.render('Игра окончена', *params)
    screen.blit(text_surface, (275, 180))

    params = (True, (255, 255, 255))
    font = pygame.font.Font(font_path, 25)

    text_surface = font.render('Возродиться', *params)
    screen.blit(text_surface, (410, 300))
    text_surface = font.render('Выход', *params)
    screen.blit(text_surface, (460, 570))

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 480:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 550:
                        terminate()
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 350:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 420:
                        for group in groups:
                            for sp in group:
                                sp.kill()
                        global player, level_x, level_y
                        player, level_x, level_y = generate_map(load_map(get_map_name()))
                        return
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    font_path = os.path.join('data', 'joystix monospace.ttf')
    params = (True, (255, 255, 255))
    font = pygame.font.Font(font_path, 40)
    fon = pygame.transform.scale(load_image('win.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    global count_level_game, player, level_x, level_y

    pygame.draw.rect(screen, (255, 0, 0), (440, 550, 150, 70), 30)

    text_surface = font.render('Поздравляю!', *params)
    screen.blit(text_surface, (350, 150))

    with open('info.csv', 'w', newline='') as f:
        columns = ['lvl_game', 'lvl_hero', 'exp_hero']
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        if count_level_game == 1 or count_level_game == 0:
            info = {"lvl_game": count_level_game + 1, "lvl_hero": player.level, 'exp_hero': player.exp}
        else:
            count_level_game = -1
            info = {"lvl_game": count_level_game, "lvl_hero": 1, 'exp_hero': 0}
        writer.writerow(info)

    if count_level_game == 1 or count_level_game == 0:
        pygame.draw.rect(screen, (128, 0, 255), (440, 370, 150, 70), 30)

        font = pygame.font.Font(font_path, 20)
        text_surface = font.render(f'Ты прошел {count_level_game + 1} уровень', *params)
        screen.blit(text_surface, (355, 210))

        font = pygame.font.Font(font_path, 25)
        text_surface = font.render('Следующий уровень', *params)
        screen.blit(text_surface, (350, 320))

        count_level_game += 1

    else:
        pygame.draw.rect(screen, (255, 186, 0), (440, 370, 150, 70), 30)

        font = pygame.font.Font(font_path, 20)
        text_surface = font.render(f'Ты прошел игру', *params)
        screen.blit(text_surface, (415, 210))

        font = pygame.font.Font(font_path, 25)
        text_surface = font.render('Новая игра', *params)
        screen.blit(text_surface, (405, 320))

    text_surface = font.render('Выход', *params)
    screen.blit(text_surface, (460, 640))

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 550:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 620:
                        terminate()
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 370 and count_level_game != -1:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 440:
                        for group in groups:
                            for sp in group:
                                sp.kill()
                        player, level_x, level_y = generate_map(load_map(get_map_name()))
                        with open('info.csv', "r", newline="") as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                player.level = int(row['lvl_hero'])
                                player.exp = int(row['exp_hero'])
                        return
                if pygame.mouse.get_pos()[0] >= 440 and pygame.mouse.get_pos()[1] >= 370 and count_level_game == -1:
                    if pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] <= 440:
                        with open('info.csv', 'w', newline='') as f:
                            columns = ['lvl_game', 'lvl_hero', 'exp_hero']
                            writer = csv.DictWriter(f, fieldnames=columns)
                            writer.writeheader()

                            info = {"lvl_game": 0, "lvl_hero": 1, 'exp_hero': 0}
                            writer.writerow(info)
                        count_level_game = 0
                        info = generate_map(load_map(get_map_name()))
                        return info[0], info[1], info[2]
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(boxes_group, all_sprites)
        elif tile_type == 'border':
            super().__init__(border_group, all_sprites)
        elif tile_type == 'portal':
            super().__init__(portal_group, all_sprites)
        else:
            super().__init__(ground_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    left_go = [pygame.transform.scale(load_image(f'hero_left\hero_go_{i}.png', color_key=-1),
               (32, 50)) for i in range(1, 7)]
    left_attack = [pygame.transform.scale(load_image(f'hero_left\hero_attack_{i}.png', color_key=-1),
                   (32, 50)) for i in range(1, 4)]
    left_attack[1] = pygame.transform.scale(load_image(f'hero_left\hero_attack_{1}.png', color_key=-1), (32, 50))
    left_attack[2] = pygame.transform.scale(load_image(f'hero_left\hero_attack_{2}.png', color_key=-1), (45, 52))
    left_stand = [pygame.transform.scale(load_image(f'hero_left\hero_stand_{i}.png', color_key=-1),
                  (32, 50)) for i in range(1, 7)]
    left_death = [pygame.transform.scale(load_image(f'hero_left\hero_dead_left_{i}.png', color_key=-1),
                                         (32, 50)) for i in range(1, 4)]

    right_go = [pygame.transform.scale(load_image(f'hero_right\hero_go_{i}.png', color_key=-1),
                (32, 50)) for i in range(1, 7)]
    right_attack = [pygame.transform.scale(load_image(f'hero_right\hero_attack_{i}.png', color_key=-1),
                    (32, 50)) for i in range(1, 4)]
    right_attack[1] = pygame.transform.scale(load_image(f'hero_right\hero_attack_{1}.png', color_key=-1), (32, 50))
    right_attack[2] = pygame.transform.scale(load_image(f'hero_right\hero_attack_{2}.png', color_key=-1), (45, 52))
    right_stand = [pygame.transform.scale(load_image(f'hero_right\hero_stand_{i}.png', color_key=-1),
                   (32, 50)) for i in range(1, 7)]
    right_death = [pygame.transform.scale(load_image(f'hero_right\hero_dead_{i}.png', color_key=-1),
                                          (32, 50)) for i in range(1, 4)]

    all_level = {1: [0, 3, 1],
                 2: [10, 4, 1],
                 3: [50, 5, 1],
                 4: [100, 5, 2],
                 5: [200, 6, 2]}

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = Hero.left_stand[0]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)

        self.left = True
        self.attack = False
        self.f = True
        self.shield = False
        self.death = False

        self.level = 1
        self.hp = self.all_level[self.level][1]
        self.max_hp = self.hp
        self.speed = 2
        self.attack_radius = 0
        self.exp = 0
        self.damage = self.all_level[self.level][2]

        self.frames = 0
        self.frames_attack = 0
        self.frames_shield = (FPS * 3) + 1
        self.frames_death = 0

    def update(self):
        change_x = change_y = 0
        # задается изменение картинки через каждые FPS // len(Hero.left_go) фреймов
        pic_ind = self.frames // (FPS // len(Hero.left_go))
        self.frames = (self.frames + 1) % FPS  # получаем числа из [0, FPS)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.attack = True

        if self.death:
            if self.frames_death < FPS:
                pic_ind = self.frames_death // (FPS // len(Hero.left_death))
                self.frames_death += 1
                self.image = Hero.left_death[pic_ind] if self.left else Hero.right_death[pic_ind]
            else:
                self.frames_death += 1
                if self.frames_death == FPS * 2:
                    self.death = False
                    dead_screen()

        elif self.attack:
            pic_ind = self.frames_attack // ((FPS // 2) // len(Hero.left_attack))
            if (not self.attack_radius) and self.f:
                self.attack_radius = AttackRadius(self.left)
                self.f = False

            self.frames_attack = (self.frames_attack + 1) % (FPS // 2)
            self.image = Hero.left_attack[pic_ind] if self.left else Hero.right_attack[pic_ind]
            if self.frames_attack == (FPS // 2) - 1:
                self.attack = False
                self.f = True
                self.frames_attack = 0
                if self.attack_radius:
                    self.attack_radius.kill()
                self.attack_radius = 0

        else:
            if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                self.image = Hero.left_go[pic_ind]
                self.left = True
                change_x = -self.speed
            if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                self.image = Hero.right_go[pic_ind]
                self.left = False
                change_x = self.speed
            if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                self.image = Hero.left_go[pic_ind] if self.left else Hero.right_go[pic_ind]
                change_y = -self.speed
            if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                self.image = Hero.left_go[pic_ind] if self.left else Hero.right_go[pic_ind]
                change_y = self.speed
            if not (pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]) and \
                    not (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]) and \
                    not (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]) and \
                    not (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]):
                self.image = Hero.left_stand[pic_ind] if self.left else Hero.right_stand[pic_ind]
            self.rect.x += change_x
            self.rect.y += change_y
            if pygame.sprite.spritecollideany(self, boxes_group):
                self.rect.x -= change_x
                self.rect.y -= change_y
            if pygame.sprite.spritecollideany(self, portal_group):
                win_screen()

        if self.shield:
            self.presence_shield()

    def presence_shield(self):
        # щит, спасающий игрока от постоянного получения урона
        self.frames_shield -= 1
        if self.frames_shield == FPS * 3:
            self.shield = True
            return True
        if self.frames_shield == 0:
            self.frames_shield = (FPS * 3) + 1
            self.shield = False
            return False
        else:
            return False

    def level_up(self):
        # увеличение уровня игрока
        if self.exp >= Hero.all_level[self.level + 1][0] and self.level < 6:
            self.level += 1
            self.max_hp = Hero.all_level[self.level][1]
            self.hp = self.max_hp
            self.damage = Hero.all_level[self.level][2]
            self.exp = 0

    def indicators(self):
        # отрисовка текущего количества хп, появляется только если очки здоровья не фулл
        if self.max_hp != self.hp:
            weight_hp_strip = round((40 / self.max_hp) * self.hp)
            pygame.draw.rect(screen, (pygame.Color('red')), (self.rect.x, self.rect.y - 9, 40, 4))
            pygame.draw.rect(screen, (pygame.Color('green')), (self.rect.x, self.rect.y - 9, weight_hp_strip, 4))

        # отрисовка опыта оставшегося до следующего уровня
        if self.level == 5:
            pygame.draw.rect(screen, (pygame.Color('white')), (self.rect.x, self.rect.y - 3, 40, 2))
        else:
            weight_exp_strip = round((40 / Hero.all_level[self.level + 1][0]) * self.exp)
            pygame.draw.rect(screen, (pygame.Color('black')), (self.rect.x, self.rect.y - 3, 40, 2))
            pygame.draw.rect(screen, (pygame.Color('white')), (self.rect.x, self.rect.y - 3, weight_exp_strip, 2))

        # отрисовка уровня персонажа
        font_path = os.path.join('data', 'joystix monospace.ttf')
        params = (True, (255, 255, 255))
        font = pygame.font.Font(font_path, 10)
        text_surface = font.render(f'{self.level}lv.', *params)
        screen.blit(text_surface, (self.rect.x - 35, self.rect.y - 9))


class Enemy(pygame.sprite.Sprite):
    left_go = [pygame.transform.scale(load_image(f'slime_left\slime_go_{i}.png', color_key=-1),
                                      (38, 56)) for i in range(1, 13)]
    left_stand = [pygame.transform.scale(load_image(f'slime_left\slime_stand_{i}.png', color_key=-1),
                                         (38, 56)) for i in range(1, 5)]
    left_stand[2] = pygame.transform.scale(load_image(f'slime_left\slime_stand_{3}.png', color_key=-1), (40, 70))
    left_stand[3] = pygame.transform.scale(load_image(f'slime_left\slime_stand_{4}.png', color_key=-1), (40, 75))
    left_death = [pygame.transform.scale(load_image(f'slime_left\slime_dead_{i}.png', color_key=-1),
                                         (38, 56)) for i in range(1, 6)]

    right_go = [pygame.transform.scale(load_image(f'slime_right\slime_go_{i}.png', color_key=-1),
                                       (38, 56)) for i in range(1, 13)]
    right_stand = [pygame.transform.scale(load_image(f'slime_right\slime_stand_{i}.png', color_key=-1),
                                          (38, 56)) for i in range(1, 5)]
    right_stand[2] = pygame.transform.scale(load_image(f'slime_right\slime_stand_{3}.png', color_key=-1), (40, 70))
    right_stand[3] = pygame.transform.scale(load_image(f'slime_right\slime_stand_{4}.png', color_key=-1), (40, 75))
    right_death = [pygame.transform.scale(load_image(f'slime_right\slime_dead_{i}.png', color_key=-1),
                                          (38, 56)) for i in range(1, 6)]

    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.route = choice(['right', 'left', 'up', 'down'])
        self.len_way = randint(100, 300)

        self.image = Enemy.left_stand[0]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)

        self.stand = False
        if self.route == 'right':
            self.left = False
        else:
            self.left = True
        self.death = False
        self.reclining = False

        self.hp = 5
        self.damage = 1
        self.max_hp = self.hp
        self.passed_now = 0
        self.speed = 1
        self.cycle_stand = 0

        self.frames = 0
        self.frames_stand = 0
        self.frames_death = 0
        self.frames_reclining = 0

    def update(self):
        x_change = y_change = 0
        pic_ind = self.frames // (FPS // len(Enemy.left_go))
        self.frames = (self.frames + 1) % FPS

        distance = hypot(abs(player.rect.x - self.rect.x), abs(player.rect.y - self.rect.y))

        if self.death:
            pic_ind = self.frames_death // ((FPS // 3) // len(Enemy.left_death))
            self.frames_death += 1
            self.image = Enemy.left_death[pic_ind] if self.left else Enemy.right_death[pic_ind]
            if self.frames_death == (FPS // 3) - 1:
                player.exp += 5
                player.level_up()
                self.kill()

        elif self.reclining:
            self.frames_reclining += 1
            self.rect.x -= 3 if player.left else -3
            if pygame.sprite.spritecollideany(self, boxes_group) or pygame.sprite.spritecollideany(self, border_group):
                self.rect.x -= 3 if player.left else -3
                self.reclining = False
            if self.frames_reclining == 20:
                self.reclining = False
                self.frames_reclining = 0

        elif distance < 200:
            if player.rect.x > self.rect.x:
                x_change += self.speed
                self.left = False
                self.image = Enemy.right_go[pic_ind]
            if player.rect.x < self.rect.x:
                x_change -= self.speed
                self.left = True
                self.image = Enemy.left_go[pic_ind]
            if player.rect.y > self.rect.y:
                y_change += self.speed
                self.image = Enemy.left_go[pic_ind] if self.left else Enemy.right_go[pic_ind]
            if player.rect.y < self.rect.y:
                y_change -= self.speed
                self.image = Enemy.left_go[pic_ind] if self.left else Enemy.right_go[pic_ind]
            self.rect.x += x_change
            self.rect.y += y_change
            if pygame.sprite.spritecollideany(self, boxes_group) or pygame.sprite.spritecollideany(self, border_group):
                self.rect.x -= x_change
                self.rect.y -= y_change
            if pygame.sprite.spritecollideany(self, attack_group):
                if player.attack_radius:
                    player.attack_radius.kill()
                self.reclining = True
                self.hp -= player.damage
                player.attack_radius = 0
                if self.hp <= 0:
                    self.death = True
            if pygame.sprite.spritecollideany(self, player_group):
                self.rect.x -= x_change
                self.rect.y -= y_change
                if player.presence_shield():
                    player.hp -= self.damage
                    if player.hp <= 0:
                        player.death = True

        else:
            if self.route == 'left' and not self.stand:
                x_change -= self.speed
                self.image = Enemy.left_go[pic_ind]
                self.passed_now += self.speed
            elif self.route == 'up' and not self.stand:
                y_change -= self.speed
                self.image = Enemy.left_go[pic_ind] if self.left else Enemy.right_go[pic_ind]
                self.passed_now += self.speed
            elif self.route == 'right' and not self.stand:
                x_change += self.speed
                self.image = Enemy.right_go[pic_ind]
                self.passed_now += self.speed
            elif self.route == 'down' and not self.stand:
                y_change += self.speed
                self.image = Enemy.left_go[pic_ind] if self.left else Enemy.right_go[pic_ind]
                self.passed_now += self.speed
            self.rect.x += x_change
            self.rect.y += y_change

            if pygame.sprite.spritecollideany(self, boxes_group) or pygame.sprite.spritecollideany(self, border_group):
                self.rect.x -= x_change
                self.rect.y -= y_change
                self.route = choice(['right', 'left', 'up', 'down'])
                self.len_way = randint(200, 400)

            if self.passed_now >= self.len_way:
                self.passed_now = 0
                self.route = choice(['right', 'left', 'up', 'down'])
                self.len_way = randint(200, 400)
                if self.route == 'right':
                    self.left = False
                if self.route == 'left':
                    self.left = True
                self.stand = True

            if self.stand:
                pic_ind = self.frames_stand // ((FPS - 40) // len(Enemy.left_stand))
                self.cycle_stand += 1
                self.frames_stand = (self.frames_stand + 1) % (FPS - 40)
                self.image = Enemy.left_stand[pic_ind] if self.left else Enemy.right_stand[pic_ind]
                if self.cycle_stand >= 360:
                    self.stand = False
                    self.cycle_stand = 0
                    self.frames_stand = 0

    def hp_strip(self):
        if self.max_hp != self.hp:
            weight_green_strip = round((40 / self.max_hp) * self.hp)
            pygame.draw.rect(screen, (pygame.Color('red')), (self.rect.x - 5, self.rect.y - 5, 40, 5))
            pygame.draw.rect(screen, (pygame.Color('green')), (self.rect.x - 5, self.rect.y - 5, weight_green_strip, 5))


class Bear(pygame.sprite.Sprite):
    left_go = [pygame.transform.scale(load_image(f'bear_right/bear_go_{i}.png', color_key=-1),
                                      (60, 65)) for i in range(1, 5)]
    left_stand = [pygame.transform.scale(load_image(f'bear_right/bear_{i}.png', color_key=-1),
                                         (60, 65)) for i in range(1, 5)]
    left_death = [pygame.transform.scale(load_image(f'bear_right/bear_death_{i}.png', color_key=-1),
                                         (60, 56)) for i in range(1, 4)]

    right_go = [pygame.transform.scale(load_image(f'bear_left/bear_go_{i}.png', color_key=-1),
                                       (60, 65)) for i in range(1, 5)]
    right_stand = [pygame.transform.scale(load_image(f'bear_left/bear_{i}.png', color_key=-1),
                                          (60, 65)) for i in range(1, 5)]
    right_death = [pygame.transform.scale(load_image(f'bear_left/bear_death_{i}.png', color_key=-1),
                                          (60, 56)) for i in range(1, 4)]

    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.route = choice(['right', 'left', 'up', 'down'])
        self.len_way = randint(100, 300)

        self.image = Enemy.left_stand[0]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)

        self.stand = False
        if self.route == 'right':
            self.left = False
        else:
            self.left = True
        self.death = False
        self.reclining = False

        self.hp = 15
        self.damage = 1.5
        self.max_hp = self.hp
        self.passed_now = 0
        self.speed = 1
        self.cycle_stand = 0

        self.frames = 0
        self.frames_stand = 0
        self.frames_death = 0
        self.frames_reclining = 0

    def update(self):
        x_change = y_change = 0
        pic_ind = self.frames // (FPS // len(Bear.left_go))
        self.frames = (self.frames + 1) % FPS

        distance = hypot(abs(player.rect.x - self.rect.x), abs(player.rect.y - self.rect.y))

        if self.death:
            pic_ind = self.frames_death // ((FPS // 2) // len(Bear.left_death))
            self.frames_death += 1
            self.image = Bear.left_death[pic_ind] if self.left else Bear.right_death[pic_ind]
            if self.frames_death == (FPS // 2) - 1:
                player.exp += 15
                player.level_up()
                self.kill()

        elif self.reclining:
            self.frames_reclining += 1
            self.rect.x -= 3 if player.left else -3
            if pygame.sprite.spritecollideany(self, boxes_group) or pygame.sprite.spritecollideany(self, border_group):
                self.rect.x -= 3 if player.left else -3
                self.reclining = False
            if self.frames_reclining == 20:
                self.reclining = False
                self.frames_reclining = 0

        elif distance < 250:
            if player.rect.x > self.rect.x:
                x_change += self.speed
                self.left = False
                self.image = Bear.right_go[pic_ind]
            if player.rect.x < self.rect.x:
                x_change -= self.speed
                self.left = True
                self.image = Bear.left_go[pic_ind]
            if player.rect.y > self.rect.y:
                y_change += self.speed
                self.image = Bear.left_go[pic_ind] if self.left else Bear.right_go[pic_ind]
            if player.rect.y < self.rect.y:
                y_change -= self.speed
                self.image = Bear.left_go[pic_ind] if self.left else Bear.right_go[pic_ind]
            self.rect.x += x_change
            self.rect.y += y_change
            if pygame.sprite.spritecollideany(self, boxes_group) or pygame.sprite.spritecollideany(self, border_group):
                self.rect.x -= x_change
                self.rect.y -= y_change
            if pygame.sprite.spritecollideany(self, attack_group):
                if player.attack_radius:
                    player.attack_radius.kill()
                self.reclining = True
                self.hp -= player.damage
                player.attack_radius = 0
                if self.hp <= 0:
                    self.death = True
            if pygame.sprite.spritecollideany(self, player_group):
                self.rect.x -= x_change
                self.rect.y -= y_change
                if player.presence_shield():
                    player.hp -= self.damage
                    if player.hp <= 0:
                        player.death = True

        else:
            if self.route == 'left' and not self.stand:
                x_change -= self.speed
                self.image = Bear.left_go[pic_ind]
                self.passed_now += self.speed
            elif self.route == 'up' and not self.stand:
                y_change -= self.speed
                self.image = Bear.left_go[pic_ind] if self.left else Bear.right_go[pic_ind]
                self.passed_now += self.speed
            elif self.route == 'right' and not self.stand:
                x_change += self.speed
                self.image = Bear.right_go[pic_ind]
                self.passed_now += self.speed
            elif self.route == 'down' and not self.stand:
                y_change += self.speed
                self.image = Bear.left_go[pic_ind] if self.left else Bear.right_go[pic_ind]
                self.passed_now += self.speed
            self.rect.x += x_change
            self.rect.y += y_change

            if pygame.sprite.spritecollideany(self, boxes_group) or pygame.sprite.spritecollideany(self, border_group):
                self.rect.x -= x_change
                self.rect.y -= y_change
                self.route = choice(['right', 'left', 'up', 'down'])
                self.len_way = randint(200, 400)

            if self.passed_now >= self.len_way:
                self.passed_now = 0
                self.route = choice(['right', 'left', 'up', 'down'])
                self.len_way = randint(200, 400)
                if self.route == 'right':
                    self.left = False
                if self.route == 'left':
                    self.left = True
                self.stand = True

            if self.stand:
                pic_ind = self.frames_stand // ((FPS - 40) // len(Bear.left_stand))
                self.cycle_stand += 1
                self.frames_stand = (self.frames_stand + 1) % (FPS - 40)
                self.image = Bear.left_stand[pic_ind] if self.left else Bear.right_stand[pic_ind]
                if self.cycle_stand >= 360:
                    self.stand = False
                    self.cycle_stand = 0
                    self.frames_stand = 0

    def hp_strip(self):
        if self.max_hp != self.hp:
            weight_green_strip = round((40 / self.max_hp) * self.hp)
            pygame.draw.rect(screen, (pygame.Color('red')), (self.rect.x - 5, self.rect.y - 5, 40, 5))
            pygame.draw.rect(screen, (pygame.Color('green')), (self.rect.x - 5, self.rect.y - 5, weight_green_strip, 5))


class AttackRadius(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__(attack_group, all_sprites)
        self.left = side
        if self.left:
            self.rect = pygame.Rect(player.rect.x - 30, player.rect.y, 30, player.rect.height)
        else:
            self.rect = pygame.Rect(player.rect.x + player.rect.width, player.rect.y, 30, player.rect.height)


def generate_map(level):
    new_player, x, y = None, None, None
    x_player = y_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'E':
                Tile('empty', x, y)
                x_enemy = x
                y_enemy = y
                Enemy(x_enemy, y_enemy)
            elif level[y][x] == 'B':
                Tile('empty', x, y)
                x_enemy = x
                y_enemy = y
                Bear(x_enemy, y_enemy)
            elif level[y][x] == '|':
                Tile('border', x, y)
            elif level[y][x] == 'P':
                Tile('portal', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                x_player = x
                y_player = y
    new_player = Hero(x_player, y_player)

    return new_player, x, y  # объект спрайт игрока, а также размер поля в клетках


class Camera:
    # зададим начальные значения смещения
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на значения смещения
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # задать смещению значения равные расстоянию от центра target до центра экрана
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


tile_images = {'wall': load_image('crate.png'),
               'border': load_image('grass3.png'),
               'empty': load_image('grass3.png'),
               'portal': load_image('portal.png')}

# группы спрайтов
all_sprites = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
attack_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()

groups = [all_sprites, boxes_group, player_group, enemies_group, ground_group, border_group, portal_group, attack_group]

tile_width = tile_height = 75

camera = Camera()

with open('info.csv', "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        count_level_game = int(row['lvl_game'])

# Вызов стартового окна
if count_level_game != -1:
    player, level_x, level_y = start_screen()
else:
    player, level_x, level_y = win_screen()

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    enemies_group.update()  # изменяем координаты всех врагов на карте
    player.update()  # изменить координаты персонажа (если нажата клавиша движения)

    ground_group.draw(screen)
    boxes_group.draw(screen)
    border_group.draw(screen)
    enemies_group.draw(screen)
    for i in enemies_group:
        i.hp_strip()
    player_group.draw(screen)
    attack_group.update()
    player.indicators()
    portal_group.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
