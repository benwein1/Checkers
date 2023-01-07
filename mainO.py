from aiohttp import client
import pygame
from game_utils.constants import CLIENT, SERVER, WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK, ROWS, COLS, GREY, FPS, \
    ENTRANCE, GAME
from game_utils.game import Game
from game_utils.board import Board
from checkers.networkingO import Client, Server
from checkers.entrence import show_entrance_screen, initialize_entrance

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # הגדרת גודל המסך
pygame.display.set_caption(f'Checkers')


def get_row_col_from_mouse(pos):
    # פעולה התחזיר את השורה והטור בלוח המשחק של הנקודה עליה לחץ העכבר
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def game_main_logic(window, events, game, our_color, opponent):
    our_turn = game.get_turn() == our_color  # תור המשחק יהיה לפי צבע השחקן שלך(כאשר תורך לשחק)
    # לולאה שרצה כאשר המשחק רץ ופועלת לפי האירועים המתאימים
    for event in events:
        # אם האירוע הוא סגירה של חלון המשחק או סיום המשחק הריצה של המשחק מפסיקה והמשחק נעצר
        if event.type == pygame.QUIT:
            exit(0)

        if our_turn and event.type == pygame.MOUSEBUTTONDOWN:
            # ביצוע המהלך לפי הלחיצה שלך על העכבר(בתורך) על המשבצת המסוימת שנבחרה
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)
            game.select(row, col)  # ביצוע המהלך לפי המשבצת שהתקבלה בלחיצה
            # שליחה ליריב את המיקום של המהלך שבוצע
            opponent.send_turn(row, col)

    if not our_turn:
        # כאשר לא תורך תקבל את ערכי המהלך שבוצע על ידי היריב ושמירה שלהם בturn
        turn = opponent.get_turn()
        if turn is not None:
            game.select(turn[0], turn[1])  # ביצוע של המהלך

    game.update()  # # עדכון המהלך שנעשה בלוח המשחק


def main():
    global WIN
    while True:
        # reinitiate on every iteration
        initialize_entrance()
        # התוכנית הראשית בה ירוץ המשחק ויפסיק\ימשיך לפי האירועים שקורים
        clock = pygame.time.Clock()
        game = Game(WIN)  # הרצת המשחק בחלון הנפתח
        # משתנה שברגע שתתבצע הבחירה באחת האופציות בהתחלה ישמור מה היריב שלך וכך יידע מה אתה (לקוח או שרת) וכך גם יגדיר את צבע השחקן שלך
        opponent = None
        our_color = None
        game_stage = ENTRANCE
        opponent_mode = None
        server_wait_connections_gen = None
        # try except everything to restart the game on error or disconnection
        try:
            while True:
                clock.tick(FPS)
                # entrance stage
                if ENTRANCE == game_stage:
                    # show entrence screen and tries getting server ip from user inputbox
                    server_ip = show_entrance_screen(WIN, pygame.event.get())
                    if server_ip is not None and server_ip != "server_mode":
                        opponent_mode = CLIENT
                        # close client in case a server is open
                        if opponent is not None:
                            opponent.close_client()

                        try:  # יצירת התחברות
                            opponent = Client(server_ip)  # הגדרת היריב כלקוח וחיבור באמצעות כתובת הIP שהוזנה
                            our_color = RED  # צבע השחקן שלך הוגדר כאדום (תתחיל במשחק)
                            game_stage = GAME
                        except Exception:
                            print("failed connecting")
                            opponent.close_client()

                    if server_ip == "server_mode":
                        if opponent_mode != SERVER:
                            opponent_mode = SERVER
                            server_wait_connections_gen = None
                            if opponent is not None:
                                opponent.close_client()
                            opponent = Server()

                        if server_wait_connections_gen is None:
                            server_wait_connections_gen = opponent.wait_for_connections()
                        if next(server_wait_connections_gen):
                            our_color = WHITE
                            game_stage = GAME

                # game stage
                if GAME == game_stage:
                    game_main_logic(WIN, pygame.event.get(), game, our_color, opponent)

                pygame.display.update()
        except BaseException as e:
            print(f"error {e}")
            opponent.close_client()
            if e is KeyboardInterrupt:
                pygame.quit()
                opponent.close_client()
                raise


if __name__ == "__main__":
    main()