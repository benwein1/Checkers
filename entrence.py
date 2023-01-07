import pygame
import socket
from game_utils.constants import INPUT_FIELD_FONT, TEXT_FONT, WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK, ROWS, COLS, \
    GREY, FPS
from game_utils.board import Board

SCREEN_STATE = {"ip_visible": False, "input_visible": False}
IP_INPUT_TEXT = ''
INPUT_DONE = False


def initialize_entrance():
    """
    call this function to initialize the state of this screen
    """
    global SCREEN_STATE, IP_INPUT_TEXT, INPUT_DONE
    SCREEN_STATE = {"ip_visible": False, "input_visible": False}
    IP_INPUT_TEXT = ''
    INPUT_DONE = False


def create_text_object(text, x=0, y=0, color=BLACK, background=None, font=TEXT_FONT):
    #פעולה היוצרת נתונים של טקסט להצגה על המסך
    text = font.render(text, True, color, background)
    textRect = text.get_rect()
    textRect.center = (x, y)
    return text, textRect


def render_input(window: pygame.Surface, event, handle_text_change, text, x, y, w, h, color):
    #פעולה היוצרת תיבת אינפוט להקלדה
    input_rect = pygame.Rect(x, y, w, h)
    base_font = INPUT_FIELD_FONT
    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_rect.collidepoint(event.pos):
            active = True
        else:
            active = False
    if event.type == pygame.KEYDOWN:
        # Check for backspace
        if event.key == pygame.K_BACKSPACE:
            # get text input from 0 to -1 i.e. end.
            handle_text_change(-1)
            text = text[:-1]
        # Unicode standard is used for string
        # formation
        else:
            handle_text_change(event.unicode)
            text += event.unicode

    # draw rectangle and argument passed which should
    # be on screen
    pygame.draw.rect(window, color, input_rect)
    textSurf, textRect = create_text_object(text, x + (w / 2), y + (h / 2), BLACK, None, INPUT_FIELD_FONT)
    window.blit(textSurf, textRect)


def render_button(window: pygame.Surface, msg, x, y, w, h, ic, ac, action=None):
#פעולה היוצרת כפתור שמבצע פעולה
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == True and action != None:
            action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))

    textSurf, textRect = create_text_object(msg, x + (w / 2), y + (h / 2), BLACK, None, INPUT_FIELD_FONT)
    window.blit(textSurf, textRect)


def draw_squares(self, win):
    # פעולה המציירת את לוח המשחק
    win.fill(BLACK)  # הגדרת רקע המסך כשחור
    for row in range(ROWS):
        for col in range(row % 2, COLS,
                         2):  # מעבר על המקומות המתאימים לפי לוח המשחק (row,col) וצביעת ריבועים אדומים לפי הגודל שהגדרנו
            pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def show_ip(window: pygame.Surface):
#פעולה המדפיסה את הip של המחשב
    # get ip
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    text, textRect = create_text_object(f"your ip: {local_ip}", 620, 590, BLACK, WHITE, INPUT_FIELD_FONT)
    window.blit(text, textRect)


def draw_background(window: pygame.Surface):
    #פעולה המציירת רקע של משבצות וכותבת את שם המשחק
    font1 = pygame.font.Font('freesansbold.ttf', 70)
    text, textRect = create_text_object("CHECKERS GAME", WIDTH // 2, HEIGHT // 2, RED, WHITE, TEXT_FONT)
    draw_squares(Board, window)
    window.blit(text, textRect)


def handle_ip_input_change(new_char):
    global IP_INPUT_TEXT
    if -1 == new_char:
        IP_INPUT_TEXT = IP_INPUT_TEXT[:-1]
    else:
        IP_INPUT_TEXT += new_char


def toggle_screen_state(key):
    """
    function toggles a screen state by key
    and turns all the other state to false
    """
    global SCREEN_STATE
    global INPUT_DONE
    SCREEN_STATE[key] = not SCREEN_STATE[key]
    for item, value in SCREEN_STATE.items():
        if item != key:
            SCREEN_STATE[item] = False
    if key != 'input_visible':
        INPUT_DONE = False


def mark_done():
    #סימון כפתור האישור כtrue
    global INPUT_DONE
    INPUT_DONE = True


def show_entrance_screen(window: pygame.Surface, events):
    """
    function handles a frame in the entrance screen
    if entered ip it will return the ip
    else it will return None
    """
    global SCREEN_STATE
    global IP_INPUT_TEXT
    global INPUT_DONE
    return_value = None
    for event in events:
        draw_background(window)

        render_button(window, "give ip to your friend!", 200, 570, 300, 60, WHITE, GREY,
                      lambda: toggle_screen_state("ip_visible"))
        render_button(window, "connect to your friend!", 200, 640, 300, 60, WHITE, GREY,
                      lambda: toggle_screen_state("input_visible")
                      )

        if SCREEN_STATE["ip_visible"]:
            show_ip(window)
            return_value = "server_mode"
        if SCREEN_STATE["input_visible"]:
            render_input(window, event, handle_ip_input_change, IP_INPUT_TEXT, 520, 640, 200, 60, WHITE)
            render_button(window, "DONE", 730, 640, 60, 60, WHITE, GREY, mark_done)

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if INPUT_DONE:
        return IP_INPUT_TEXT
    return return_value


def main():
    #לולאה שמראההאת מסך התפריט כל עו אין שינוי וmain לא התחיל לרוץ
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f'Checkers')
    while True:
        clock.tick(FPS)
        if show_entrance_screen(WIN, pygame.event.get()) is not None:
            return
        pygame.display.update()


if __name__ == "__main__":
    main()

















