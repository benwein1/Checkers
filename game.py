import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, win):
        #פעולה בונה למחלקה, בעלת יכולת הפעלה עצמית כאשר העצם מזומן וחלון בה ייפתח המשחק
        self._init()
        self.win = win

    def update(self):
        #פעולה אשר מעדכנת את מצב המשחק על הלוח
        self.board.draw(self.win) #ציור הלוח על מסך המשחק
        self.draw_valid_moves(self.valid_moves) #
        pygame.display.update() #עדכון מסך המשחק

    def _init(self):
        #פעולה המגדירה את מצב הלוח,תור המתחיל ומצב בחירת הכלי בתחילת משחק
        self.selected = None #אף כלי לא נבחר
        self.board = Board() #לוח מוגדר במצב התחלתי
        self.turn = RED #תור השחקן האדום
        self.valid_moves = {}

    def winner(self):
        #פעולה המחזירה את מנצח המשחק בלוח המשחק
        return self.board.winner()

    def reset(self):
        #פעולה המאתחלת את מצב הלוח
        self._init()

    def select(self, row, col):
        #פעולה הבודקת האם הכלי שנבחר הוא של השחקן שתור, ואם תורו היא תראה את המהלכים האפשריים שלו ותראה אם המשבצת שנלחצה היא חלק מהמהלכים החוקיים היא תזיז את הכלי לשם
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        #אם יש כלי במשבצת שנבחרה (נלחצה) והכלי הוא של השחקן שתורו הכלי ייבחר והאופציות למהלך חוקי שלו יישמרו
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        #פעולה הגורמת להזזת כלי שנבחר
        piece = self.board.get_piece(row, col) #בחירת הכלי במערך הלוח לפי המיקום בלוח שהתקבל
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col) #הזזת השחקן הנבחר למקום שהתקבל בלוח במידה והוא מהמהלכים החוקיים של הכלי הנבחר
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        # פעולה המציירת את העיגול הכחול על משבצת אליה שחקן יכול לנוע
        # מעבר על כל מהלך ברשימת המהלכים האפשריים moves וציור עיגול כחול בה
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        #פעולה המשנה את תור המשחק לאחר שנעשה מהלך(מאדום ללבן ולהפך)
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_turn(self):
        #פעולה המחזירה למי שייך התור הנוכחי
        return self.turn

    def get_board(self):
        #פעולה המחזירה את מצב הלוח הנוכחי
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()