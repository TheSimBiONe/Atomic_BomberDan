class Bonus(pygame.sprite.Sprite):
    def __init__(self, bomber_, x, y):
        super().__init__(all_sprites, bonuses)
        sheet = self.cut_sheet(pygame.transform.scale(load_image('Bonuses.png'), (225, 80)), 3, 1)
        self.sheets = {
            'bomb': sheet[0],
            'flame': sheet[1],
            'speed': sheet[2]
        }
        self.bomber = bomber_
        self.rect = pygame.Rect(x, y, 80, 80)
        self.type = choice(['bomb', 'bomb', 'flame', 'flame', 'speed'])
        self.image = self.sheets[self.type]