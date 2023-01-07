import socket
import select
from numpy import byte

#הגדרת הפורטים של השרת והלקוח (שרירותי)
SERVER_PORT = 31240
CLIENT_PORT = 25436


class Client():
    # מחלקה המגזירה את הלקוח ואת הפעולות שלי בכדי להעביר ולקבל מידע על מהלכים שמתרחשים
    __socket = None

    def __init__(self, ip, port=SERVER_PORT) -> None:
        # הגדרת סוקט ללקוח שדרכו יעביר ויקבל את המידע
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect server
        self.__socket.connect((ip, port)) #חיבור הסוקט לכתובת הip והפורט שנקלטים (הפורט שיקבל תמיד יהיה של השרת אותו הגדרנו במקרה הזה)
        self.__socket.settimeout(0.5)

    def send_turn(self, x, y):
        #פעולה שתשלח אל השרת(השחקן היריב) שיעורי XY על הלוח

        data_to_send = f"{x},{y}".encode() #העברת הערכים שהתקבלו לפורמט השליחה בביטים utf-8 בכדי לשלוח לשרת
        self.__socket.send(len(data_to_send).to_bytes(1, 'little')) # שליחה דרך הסוקט של אורך ההודעה בבייטים
        self.__socket.send(data_to_send) #שליחת ההודעה בutf-8 דרך הסוקט


    def get_turn(self):
        #פעולה שתקבל דרך הסוקט ערכי XY ששלח השרת (השחקן היריב)
        try:
            length_of_data = self.__socket.recv(1) #קבלה מהסוקט את גודל ההודעה שהתקבלה בשביל לקרוא אותה
            x, y = self.__socket.recv(int.from_bytes(length_of_data, 'little')).decode().split(',') #קבלת הערכים מהסוקט ושמירה שלהם בנפרד ללא הפסיק בX ו-Y
           #הפיכה של הערכים לint והחזרה שלהם
            return (int(x), int(y))
        except socket.timeout:
            return None

    def close_client(self):
        #פעולה הסוגרת את סוקט הלקוח וכך בעצם גם את החיבור
        self.__socket.close()


class Server():
    # members
    #מחלקה המגדירה את השרת ופעולות שיכול לעשות בכדי להעביר ולקבל את המידע הרצוי
    __socket = None
    __conn = None
    __client_addr = None

    def __init__(self, listen_port=SERVER_PORT) -> None:
        #פעולה המפעילה את את השרת
        # יוצרת לו סוקט
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # ומחברת אותו לפורט השרת שהגדרנו מראש (תמיד אותו פורט)
        self.__socket.bind(('', listen_port))

    def wait_for_connections(self):
        """
        non blocking genereator funciton for wating a connection
        the funciton returnes true if a connectino was made and false otherwise
        """
        self.__socket.listen(5)
        read_list = [self.__socket]
        while self.__conn is None:
            yield False
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is self.__socket:
                    self.__conn, self.__client_addr = self.__socket.accept()
            print(self.__conn)
        self.__conn.settimeout(0.5)
        yield True

    def send_turn(self, x, y):
        # פעולה שתשלח אל הלקוח(השחקן היריב) שיעורי XY על הלוח
        data_to_send = f"{x},{y}".encode() #קידוד הערכים לutf-8 בכדי לשלוח ללקוח את הערכים
        self.__conn.sendall(len(data_to_send).to_bytes(1, 'little')) #שליחה של אורך ההודעה הרצויה לשליחה בבייטים
        self.__conn.sendall(data_to_send) #שליחת ההודעה ובה ערכי הXY ללקוח


    # this function is blocking. you might want to consider calling it with a thread
    # with the following syntax:
    # example for running this method from main.py
    # threading.Thread(targer=lambda: opponent.get_turn()).start()
    def get_turn(self):
        #פעולה שתקבל דרך הסוקט ערכי XY ששלח הלקוח (השחקן היריב)
        try:
            length_of_data = self.__conn.recv(1) #קבלה של אורך ההודעה שהתקבלה מהלקוח דרך החיבור
            x, y = self.__conn.recv(int.from_bytes(length_of_data, 'little')).decode().split(',') #קבלת הערכים מהסוקט ושמירה שלהם בנפרד ללא הפסיק בX ו-Y
            # הפיכה של הערכים לint והחזרה שלהם
            return (int(x), int(y))
        except socket.timeout:
            return None

    def close_client(self):
    #פעולה הסוגרת את החיבור בסוקט
        self.__socket.close()