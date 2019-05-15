from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Label, messagebox, simpledialog
from Map_2048 import MapClass
from UI_2048 import UI

root = Tk()                                     # tkinter 객체 생성

n = int(simpledialog.askstring(title="2048 Game",
                               prompt="\t게임을 선택하세요.\t\t\n" "\t3 X 3 -> 3입력",
                               parent=root,
                               initialvalue="4"))
MARGIN = 15                                     # 게임 판 상하좌우 마진 길이
WIDTH = MARGIN * 2 + 400                        # 게임 판 가로 세로 길이
HEIGHT = MARGIN * 2 + 400
SIDE = ((WIDTH - 2 * MARGIN) / n)-0.6
# 게임 판 내 셀의 가로 세로 길이

UI_size = (MARGIN, WIDTH, HEIGHT, SIDE)

map_ = MapClass(n)                              # 맵클래스 객체 생성
UI(parent=root, game=map_, n=n, UI_size=UI_size)                               # UI 객체 생성
root.geometry("%dx%d" % (WIDTH, HEIGHT + 150))  # tkinter 의 가로 세로 길이 설정
root.mainloop()                                 # gui 실행