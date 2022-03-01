import pygame as pg
from pygame.math import Vector2


pg.init()
IMAGE = pg.Surface((70, 110))
IMAGE.fill((0, 80, 180))
pg.draw.rect(IMAGE, (160, 160, 160), (0, 0, 20, 110))


class Entity(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = IMAGE
        self.rect = self.image.get_rect(center=pos)
        # A deflated copy of the rect as the hitbox.
        self.hitbox = self.rect.inflate(-40, -20)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)  # Actual center position.
        self.offset = Vector2(10, 0)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        # Add the offset to the pos to center the hitbox
        # at the blue part of the image.
        self.hitbox.center = self.pos + self.offset

    def flip(self):
        # Check which side the sprite is facing.
        if self.offset.x > 0:
            self.image = pg.transform.flip(IMAGE, True, False)
        else:
            self.image = IMAGE
        self.offset = -self.offset  # Invert the offset.


# This callback function is passed as the `collided`argument
# to pygame.sprite.spritecollide or groupcollide.
def collided(sprite, other):
    """Check if the hitboxes of the two sprites collide."""
    return sprite.hitbox.colliderect(other.hitbox)


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Entity((300, 200), all_sprites)
    player.flip()
    enemies = pg.sprite.Group(
        Entity((100, 250), all_sprites),
        Entity((400, 300), all_sprites),
    )

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEMOTION:
                player.pos = event.pos
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    player.flip()

        all_sprites.update()
        # Pass the custom collided callback function to spritecollide.
        collided_sprites = pg.sprite.spritecollide(player, enemies, False, collided)
        for sp in collided_sprites:
            print('Collision', sp)

        screen.fill((30, 30, 30))

        all_sprites.draw(screen)
        for sprite in all_sprites:
            # Draw rects and hitboxes.
            pg.draw.rect(screen, (0, 230, 0), sprite.rect, 2)
            pg.draw.rect(screen, (250, 30, 0), sprite.hitbox, 2)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()