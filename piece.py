from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame


class Piece:
    PADDING = 15 #מרחק בין קצה המשבצת לכלי
    OUTLINE = 2

    def __init__(self, row, col, color):
        # פעולה המגדירה את תכונות הכלי (מיקום במערך הלוח, צבע, האם מלך ומיקום במרחב)
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        # פעולה המחשבת את מיקום אמצע הכלי לפי השורה והטור בו הוא נמצא
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 #חישוב ערך הXY של מרכז הכלי
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        #פעולה ההופכת חייל מרגיל למלך
        self.king = True

    def draw(self, win):
        #ציור הכלי בתוך המשבצת
        radius = SQUARE_SIZE // 2 - self.PADDING #הגדרת גודל רדיוס הכלי (חצי מאורך המשבצת פחות המרחק שקבענו מקצה המשבצת)
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)  # ציור ה"גבול" של העיגול בצבע אפור כך שיבדיל אותו מהלוח
        pygame.draw.circle(win, self.color, (self.x, self.y), radius) # ציור עיגול בצבע הכלי
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2)) #אם הכלי הוא מלך ציור הכתר במרכז העיגול

    def move(self, row, col):
        #פעולה המעדכנת את מיקום הכלי לאחר תזוזה
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        #פעולה המחזירה סטרינג של צבע הכלי (rgb) כאשר כלי "מודפס" ומציגה אותו כך
        return str(self.color)