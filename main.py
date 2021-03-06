import pygame
import os
import sys
from random import choice


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, walls)
        self.image = pygame.transform.scale(load_image('Wall.png'), (80, 80))
        self.rect = pygame.Rect(x * 80, y * 80, 80, 80)
        self.x = x
        self.y = y

    def update(self):
        pass


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, bricks)

        # destroy animation
        self.sheet = self.cut_sheet(pygame.transform.scale(load_image('Brick.png'), (112 * 5, 16 * 5)), 7, 1)
        self.counter = 0
        self.cur_frame = 0
        self.destroyed = False

        # parameters
        self.rect.x = x * 80
        self.rect.y = y * 80
        self.image = self.sheet[0]

    def cut_sheet(self, sheet, columns, rows):
        group = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                group.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return group

    def destroy(self):
        self.destroyed = True
        self.cur_frame += 1

    def update(self):
        if self.destroyed:
            if self.cur_frame >= 7:
                create_bonus = choice([0, 0, 0, 0, 1])
                if create_bonus == 1:
                    Bonus(self.rect.x, self.rect.y)
                self.kill()
            elif self.counter % 5 == 0:
                self.image = self.sheet[self.cur_frame]
                self.cur_frame += 1
            self.counter += 1


class GameField:
    def __init__(self):
        self.width = 15
        self.height = 11
        self.board = [[0] * width for _ in range(height)]
        self.cell_size = 80
        with open('data/RoomSheet', 'r') as rs:
            room = rs.read().split('\n')
            for y in range(11):
                for x in range(15):
                    if room[y][x] == 'b':
                        Brick(x, y)
                    elif room[y][x] == 'w':
                        Wall(x, y)
                    elif room[y][x] == 'f':
                        Bomberman(x, y, 'Bomberman.png', pygame.K_r, pygame.K_g, pygame.K_f,
                                           pygame.K_d, pygame.K_s)
                    elif room[y][x] == 's':
                        Bomberman(x, y, 'Dan.png', pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN,
                                        pygame.K_LEFT, pygame.K_SLASH)


class Bomberman(pygame.sprite.Sprite):
    def __init__(self, x, y, picture, u, r, d, l, bomb):
        super().__init__(all_sprites, bombers)
        self.controls = (u, r, d, l, bomb)

        # size and hitbox
        self.mlt = 4
        sheet_ = self.cut_sheet(pygame.transform.scale(load_image(picture),
                                                       (204 * self.mlt, 27 * self.mlt)), 12, 1)
        self.rect = self.rect.move(x * 80, y * 80)
        self.hitbox = pygame.Rect(self.rect.x + 4 * self.mlt, self.rect.y + 16 * self.mlt,
                                  9 * self.mlt, 7 * self.mlt)

        # animation
        self.sheets = {
            'run_u': [sheet_[0]] + [sheet_[1]] + [sheet_[0]] + [sheet_[2]],
            'run_r': [sheet_[3]] + [sheet_[4]] + [sheet_[3]] + [sheet_[5]],
            'run_d': [sheet_[6]] + [sheet_[7]] + [sheet_[6]] + [sheet_[8]],
            'run_l': [sheet_[9]] + [sheet_[10]] + [sheet_[9]] + [sheet_[11]],
        }
        self.cur_frame = 0
        self.counter = 0
        self.group = self.sheets['run_d']
        self.image = self.group[self.cur_frame]

        # movement
        self.dx = 0
        self.dy = 0

        self.speed = 10
        self.collied = False

        # parameters
        self.bombs = 1
        self.flame = 80

    def cut_sheet(self, sheet, columns, rows):
        group = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                group.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return group

    def get_keys(self):
        keys = pygame.key.get_pressed()

        if keys[self.controls[0]]:
            self.dy = -self.speed
            self.dx = 0
            self.group = self.sheets['run_u']

        elif keys[self.controls[1]]:
            self.dy = 0
            self.dx = self.speed
            self.group = self.sheets['run_r']

        elif keys[self.controls[2]]:
            self.dy = self.speed
            self.dx = 0
            self.group = self.sheets['run_d']

        elif keys[self.controls[3]]:
            self.dy = 0
            self.dx = -self.speed
            self.group = self.sheets['run_l']

        else:
            self.dx = 0
            self.dy = 0
            self.cur_frame = -1

        if keys[self.controls[4]]:
            if self.bombs > 0:
                x = (self.rect.center[0] // 80) * 80
                y = ((self.rect.center[1] + 10) // 80) * 80
                if (x, y) not in [(i.rect.x, i.rect.y) for i in bombs.sprites()]:
                    Bomb(self, x, y, self.flame, 90)
                    self.bombs -= 1

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, (0, 0, 0), self.hitbox, 1)

    def update(self):
        self.get_keys()
        if self.cur_frame == -1:
            self.cur_frame = 0
            self.counter = 0
        else:
            if self.counter % 5 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.group)
            self.counter += 1

        if 0 < self.hitbox.x + self.dx < game.width * 80 - self.hitbox.width:
            self.rect.x += self.dx
        if 0 < self.hitbox.y + self.dy < game.height * 80 - self.hitbox.height:
            self.rect.y += self.dy

        self.hitbox.x, self.hitbox.y = self.rect.x + 4 * self.mlt, self.rect.y + 16 * self.mlt
        self.image = self.group[self.cur_frame]

        self.collied = False
        for wall in walls.sprites():
            if self.hitbox.colliderect(wall.rect):
                self.collied = True
                self.rect.x -= self.dx
                self.rect.y -= self.dy
                if self.dx != 0 and abs(self.hitbox.center[1] - wall.rect.center[1]) > 23:
                    self.rect.y += (self.hitbox.center[1] - wall.rect.center[1]) / \
                                   abs(self.hitbox.center[1] - wall.rect.center[1]) * self.speed
                elif self.dy != 0 and abs(self.hitbox.center[0] - wall.rect.center[0]) > 23:
                    self.rect.x += (self.hitbox.center[0] - wall.rect.center[0]) / \
                                   abs(self.hitbox.center[0] - wall.rect.center[0]) * self.speed

        if not self.collied:
            for brick in bricks.sprites():
                if self.hitbox.colliderect(brick.rect):
                    self.rect.x -= self.dx
                    self.rect.y -= self.dy

        if not self.collied:
            for bomb in bombs.sprites():
                if bomb != 0:
                    if self.hitbox.colliderect(bomb.rect) and bomb.do_push:
                        self.rect.x -= self.dx
                        self.rect.y -= self.dy

        for bonus in bonuses.sprites():
            if self.hitbox.colliderect(bonus.rect):
                bonus.upgrade(self)
                bonus.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, bomber_, x, y, flame, time):
        super().__init__(all_sprites, bombs)
        self.do_push = False

        # animation
        self.sheets = {
            'idle': self.cut_sheet(pygame.transform.scale(load_image('BombIdle.png'), (160, 80)), 2, 1),
            'explored': [pygame.transform.scale(load_image('exp1.png'), (80, 80)),
                         pygame.transform.scale(load_image('exp2.png'), (80, 80)),
                         pygame.transform.scale(load_image('exp3.png'), (80, 80))]
        }
        self.cur_frame = 0
        self.counter = 0
        self.group = self.sheets['idle']
        self.image = self.group[0]

        # parameters
        self.bomber = bomber_
        self.flame = flame
        self.time = time
        self.rect = pygame.Rect(x, y, 80, 80)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if len(list(filter(lambda b: self.rect.colliderect(b.hitbox), bombers.sprites()))) == 0:
            self.do_push = True

        if self.counter % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.group)
        self.counter += 1
        self.image = self.group[self.cur_frame]
        self.time -= 1

        if self.time == 15:
            self.group = self.sheets['explored']
            self.cur_frame = -1

        if self.time == 0:
            self.bomber.bombs += 1
            Flame(self.rect.x, self.rect.y, self.flame, 'up')
            Flame(self.rect.x, self.rect.y, self.flame, 'right')
            Flame(self.rect.x, self.rect.y, self.flame, 'down')
            Flame(self.rect.x, self.rect.y, self.flame, 'left')
            self.kill()

    def cut_sheet(self, sheet, columns, rows):
        group = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                group.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return group


class Flame(pygame.sprite.Sprite):
    def __init__(self, x, y, length, direct):
        super().__init__(all_sprites, flames)

        # animation
        self.sheets = {
            'up': (self.cut_sheet(pygame.transform.scale(load_image('Flame_u.png'), (72, 525)), 1, 5), 0, -80),
            'right': (self.cut_sheet(pygame.transform.scale(load_image('Flame_r.png'), (525, 72)), 5, 1), 80, 0),
            'down': (self.cut_sheet(pygame.transform.scale(load_image('Flame_d.png'), (72, 525)), 1, 5), 0, 80),
            'left': (self.cut_sheet(pygame.transform.scale(load_image('Flame_l.png'), (525, 72)), 5, 1), -80, 0),
        }
        self.group = self.sheets[direct][0]
        self.cur_frame = 0
        self.image = self.group[self.cur_frame]

        # parameters
        self.length = length
        self.distance = 0
        self.dx = self.sheets[direct][1]
        self.dy = self.sheets[direct][2]
        self.rect = pygame.Rect(0, 0, 80, 80)
        self.rect.center = (x + 40, y + 40)

    def update(self):
        global is_restart
        self.cur_frame = (self.cur_frame + 1) % len(self.group)
        self.image = self.group[self.cur_frame]
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.length <= abs(self.distance):
            self.kill()

        for bomber in bombers.sprites():
            if self.rect.colliderect(bomber.hitbox):
                bomber.kill()
                is_restart = True

        for wall in walls.sprites():
            if self.rect.colliderect(wall.rect):
                self.kill()

        for brick in bricks.sprites():
            if self.rect.colliderect(brick.rect):
                brick.destroy()
                self.kill()

        for bomb in bombs.sprites():
            if bomb != 0:
                if self.rect.colliderect(bomb.rect):
                    bomb.time = 16
                    self.kill()

        for bonus in bonuses.sprites():
            if self.rect.colliderect(bonus.rect):
                bonus.kill()
                self.kill()

        self.distance += self.dx + self.dy

    def cut_sheet(self, sheet, columns, rows):
        group = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                group.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return group


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, bonuses)
        sheet = self.cut_sheet(pygame.transform.scale(load_image('Bonuses.png'), (225, 80)), 3, 1)
        self.sheets = {
            'bomb': sheet[0],
            'flame': sheet[1],
            'speed': sheet[2]
        }
        self.rect = pygame.Rect(x, y, 80, 80)
        self.type = choice(['bomb', 'bomb', 'flame', 'flame', 'speed'])
        self.image = self.sheets[self.type]

    def cut_sheet(self, sheet, columns, rows):
        group = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                group.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return group

    def upgrade(self, bomber_):
        if self.type == 'bomb':
            bomber_.bombs += 1
        elif self.type == 'flame':
            bomber_.flame += 80
        elif self.type == 'speed':
            bomber_.speed += 2


fps = 60
clock = pygame.time.Clock()
size = width, height = 1200, 880

screen = pygame.display.set_mode(size)
screen.fill('ForestGreen')

all_sprites = pygame.sprite.Group()
bombers = pygame.sprite.Group()
walls = pygame.sprite.Group()
bricks = pygame.sprite.Group()
bombs = pygame.sprite.Group()
flames = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
game = GameField()

is_restart = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if is_restart:
        for bomber_ in bombers.sprites():
            bomber_.kill()
        for wall_ in walls.sprites():
            wall_.kill()
        for brick_ in bricks.sprites():
            brick_.kill()
        for bomb_ in bombs.sprites():
            bomb_.kill()
        for flame_ in flames.sprites():
            flame_.kill()
        for bonus_ in bonuses.sprites():
            bonus_.kill()
        game = GameField()
        is_restart = False

    # формирование кадра
    screen.fill((51, 118, 0))
    flames.update()
    bombers.update()
    bombs.update()
    bricks.update()
    bonuses.update()

    # изменение игрового мира
    walls.draw(screen)
    bricks.draw(screen)
    bonuses.draw(screen)
    bombs.draw(screen)
    bombers.draw(screen)
    flames.draw(screen)
    pygame.display.flip()

    # временная задержка
    clock.tick(fps)
