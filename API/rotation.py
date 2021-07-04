import pygame


class rotation:
    left, right, up, down = False, False, False, False

    def rotate(self, object, pos_x, pos_y, screen, last_rotation, angle):
        global left, right, up, down
        if left:
            pos_x -= 2
            if last_rotation != 'left':
                while angle < 180:
                    rotated_image = pygame.transform.rotate(rotated_image, 1)
                    angle += 1
                screen.blit(rotated_image, (pos_x, pos_y))
                angle = 0
                last_rotation = 'left'
                pygame.display.update()
        if right:
            pos_x += 2
            if last_rotation != 'right':
                rotated_image = pygame.transform.rotate(rotated_image, angle)
                screen.blit(rotated_image, (pos_x, pos_y))
            last_rotation = 'right'
            angle = 0
            pygame.display.update()
        if up:
            pos_y -= 2
            if last_rotation != 'up':
                while angle < 270:
                    rotated_image = pygame.transform.rotate(rotated_image, 1)
                    angle += 1
                screen.blit(rotated_image, (pos_x, pos_y))
                last_rotation = 'up'
                angle = 0
                pygame.display.update()

        if down:
            pos_y += 2
            if last_rotation != 'down':
                while angle < 90:
                    rotated_image = pygame.transform.rotate(rotated_image, 1)
                    angle += 1
                    pygame.display.update()
                last_rotation = 'down'
                screen.blit(rotated_image, (pos_x, pos_y))
