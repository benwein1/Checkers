import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800 #גודל חלון המשחק (אורך ורוחב)
ROWS, COLS = 8, 8 # כמות השורות והטורים של המשבצות
SQUARE_SIZE = WIDTH//COLS # גודל האורך והרוחב של משבצת בלוח(100 על 100)

FPS = 60

# rgb של הצבעים בהם אשתמש
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25)) #תמונה של כתר שתופיע על כלי שהופך למלך

# fonts
INPUT_FIELD_FONT = pygame.font.Font('freesansbold.ttf', 20)
TEXT_FONT = pygame.font.Font('freesansbold.ttf', 70)

# stages
ENTRANCE = 0
GAME = 1

#opponent mode
SERVER = 0
CLIENT = 1