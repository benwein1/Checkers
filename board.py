import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, CROWN
from .piece import Piece


class Board:
    def __init__(self):
        # בניית עצם הלוח והגדרת התכונות שלו, מערך הכלים וכמות הכלים והמלכים של כל משתתף
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()


    def draw_squares(self, win):
        # פעולה המציירת את לוח המשחק
        win.fill(BLACK) #הגדרת רקע המסך כשחור
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2): # מעבר על המקומות המתאימים לפי לוח המשחק (row,col) וצביעת ריבועים אדומים לפי הגודל שהגדרנו
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        # פעולה היוצרת רשימה של כלים מהכלים על הלוח באותו הצבע
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        # פעולה המקבלת כלי ומיקום בלוח ומשנה את מיקום הכלי למיקום שהתקבל בפעולה
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col) #זימון הפעולה המעדכנת מיקום כלי

        if row == ROWS - 1 or row == 0: #אם החייל הגיע לשורה האחרונה שלו הוא הופך למלך
            piece.make_king()
            #הוספת 1 לכמות המלכים של הצבע שבו התווסף מלך
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        #פעולה המחזירה את הכלי בשורה והטור המבוקשים
        return self.board[row][col]

    def create_board(self):
        #פעולה היוצרת את מערך הכלים על לוח המשחק
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                #מעבר על כל השורות במערך הלוח והצבת כלי במקום המתאים בשלוש השורות הראשונות ובשלוש השורות האחרונות
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)#הוספת 0 למערך שמתאר משבצת ריקה
                else:
                    self.board[row].append(0)

    def draw(self, win):
        #פעולה המציירת את הלוח ואת מערך הכלים על לוח המשחק במסך
        self.draw_squares(win) #ציור המשבצות בחלון בעזרת זימון הפעולה
        for row in range(ROWS):
            for col in range(COLS):
                # מעבר על כל הכלים במערך הכלים וציור שלהם על המשבצות בלוח
                piece = self.board[row][col]
                if piece != 0: #אם יש כלי כלומר שווה למשהו אחר מ-0
                 piece.draw(win)

    def remove(self, pieces):
        #פעולה המסירה כלי ממערך הכלים הנוכחי שהתקבל
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                #החסרה של הכלי מספירת הכלים שלו בלוח בצבע המתאים
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        #פעולה המחזירה את המנצח במשחק במידה ולשחקן היריב נאכלו כל הכלים
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        #פעולה
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        #פעולה המכניסה לרשימה את כל המהלכים האפשריים (התקדמות, אכילה , אכילה כפולה) של כלי לצד השמאלי שלו
        #כלומר כאשר אם לכלי יש את האופציה לאכול\לזוז\לאכול כפול וכולם מהלכים שמתחילים בתזוזה שמאלה הפעולה תשמור אותם ברשימה moves ותתזיר
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        # פעולה המכניסה לרשימה את כל המהלכים האפשריים (התקדמות, אכילה , אכילה כפולה) של כלי לצד הימני שלו
        # כלומר כאשר אם לכלי יש את האופציה לאכול\לזוז\לאכול כפול וכולם מהלכים שמתחילים בתזוזה ימינה הפעולה תשמור אותם ברשימה moves ותתזיר
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves









