import pygame
from checkers.game_utils.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game_utils.game import Game


FPS = 60

#הגדרת גודל החלון הנפתח ושם המשחק בקצה השמאלי העליון של החלון
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    # פעולה התחזיר את השורה והטור של המשבצת עליה לחץ העכבר
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    # התוכנית הראשית בה ירוץ המשחק ויפסיק\ימשיך לפי האירועים שקורים
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN) #הרצת המשחק בחלון הנפתח


    while run: #לולאה שתרוץ כל עוד המשחק רץ (run=true)
        clock.tick(FPS)

        #לולאה שרצה כאשר המשחק רץ ופועלת לפי האירועים המתאימים
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #אם האירוע הוא סגירה של חלון המשחק או סיום המשחק הריצה של המשחק מפסיקה והמשחק נעצר
                run = False #יציאה מהלולאה שמריצה את המשחק

            if event.type == pygame.MOUSEBUTTONDOWN:
                # ביצוע המהלך לפי הלחיצה של העכבר על המשבצת המסוימת שנבחרה
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)


        game.update() #עדכון המהלך שנעשה בלוח המשחק


    pygame.quit()


main()