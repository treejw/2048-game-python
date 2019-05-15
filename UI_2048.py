from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Label, messagebox, simpledialog

class UI(Frame):
    def __init__(self, parent, game, n, UI_size):
        Frame.__init__(self, parent)
        self.game = game
        self.n = n
        self.parent = parent
        self.row, self.col = -1, -1
        (self.MARGIN, self.WIDTH, self.HEIGHT, self.SIDE) = UI_size
        self.__initUI()

    def __initUI(self):
        self.parent.title("2048")
        self.pack(fill=BOTH)
        self.title = Label(self, text='2048', font=("Verdana", 40, "bold"), fg="#715F56")
        self.title.grid(row=0, column=0, columnspan=3)

        restart_button = Button(self, text="Restart", command=self.restart, width=8, height=1, font=("Verdana", 12, "bold"), bg="#715F56", fg='white')
        back_button = Button(self, text="Back", command=self.back, width=8, height=1, font=("Verdana", 12, "bold"), bg="#715F56", fg='white')
        exit_button = Button(self, text="Exit", command=self.parent.destroy, width=8, height=1, font=("Verdana", 12, "bold"), bg="#715F56", fg='white')
        restart_button.grid(row=1, column=0)
        back_button.grid(row=1, column=1)
        exit_button.grid(row=1, column=2)

        self.canvas = Canvas(self, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.grid(row=2, column=0, columnspan=3)
        self.show_score = Label(self, text='score = '.format(self.game.score), font=("Verdana", 25, "bold"), fg="#715F56")
        self.__draw_grid()
        self.__draw_puzzle()

        self.parent.bind("<Key>", self.key)
        self.parent.bind("<Left>", self.GUI_arrow)
        self.parent.bind("<Right>", self.GUI_arrow)
        self.parent.bind("<Up>", self.GUI_arrow)
        self.parent.bind("<Down>", self.GUI_arrow)

    def restart(self):
        self.game.__init__(self.n)
        self.game.win_flag = False
        self.game.result = 'playing'
        self.__draw_puzzle()
        self.title.config(text='2048')

    def back(self):
        self.game.result = 'playing'
        self.game.Map = self.game.Map_prev.copy()
        self.game.score = self.game.score_prev
        self.__draw_puzzle()

    def key(self, event):
        self.game.step(event)
        self.__draw_puzzle()

    def GUI_arrow(self, event):
        self.game.step(event)
        self.__draw_puzzle()

    def __draw_grid(self):
        for i in range(self.n + 1):
            color = "#B6A59A"

            x0 = self.MARGIN + i * self.SIDE
            y0 = self.MARGIN
            x1 = self.MARGIN + i * self.SIDE
            y1 = self.HEIGHT - self.MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=8, joinstyle="miter")
            x0 = self.MARGIN
            y0 = self.MARGIN + i * self.SIDE
            x1 = self.WIDTH - self.MARGIN
            y1 = self.MARGIN + i * self.SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=8, joinstyle="miter")

    def __draw_puzzle(self):
        self.show_score.grid(row=3, column=0, columnspan=3)
        self.show_score.config(text='score = {}'.format(self.game.score))
        self.canvas.delete("numbers")

        for i in range(self.n):
            for j in range(self.n):
                answer = self.game.Map[i][j]
                if answer != 0:
                    x = self.MARGIN + j * self.SIDE + self.SIDE / 2
                    y = self.MARGIN + i * self.SIDE + self.SIDE / 2
                    if len(str(answer)) < 5:
                        self.canvas.create_text(x, y, text=answer, tags="numbers", fill="black", font=("Verdana", int(self.SIDE/3), "bold"))
                    else:
                        self.canvas.create_text(x, y, text=answer, tags="numbers", fill="black", font=("Verdana", int(self.SIDE/2.4)-int(self.SIDE/len(str(answer))*1.2), "bold"))

        # highlight effect
        if self.game.highlight_flag:
            i, j = self.game.highlight_index
            self.highlight_main(i, j)
            self.game.highlight_flag = False

        # GAME OVER
        if self.game.result == 'full':
            self.canvas.delete("numbers")
            for i in range(self.n):
                for j in range(self.n):
                    answer = self.game.Map[i][j]
                    if answer != 0:
                        x = self.MARGIN + j * self.SIDE + self.SIDE / 2
                        y = self.MARGIN + i * self.SIDE + self.SIDE / 2
                        self.canvas.create_text(x, y, text='game over', tags="numbers", fill="black",
                                                font=("Arial", 7, "bold"))
        # WIN
        if self.game.result == 'win':
            self.title.config(text='2048 WIN!')
            self.game.result = 'playing'

    # random 으로 생성되는 곳 highlight
    def highlight_main(self, i, j):
        x0 = (self.MARGIN + j * self.SIDE)
        y0 = (self.MARGIN + i * self.SIDE)
        x1 = x0 + self.SIDE
        y1 = y0 + self.SIDE
        init_size = self.SIDE//7     # 원래 Cell 크기에서 얼마자 작게 시작할 것인지에 대한 변수.
        self.id = self.canvas.create_rectangle(x0 + init_size, y0 + init_size, x1 - init_size, y1 - init_size,
                                               outline='red', tags="hl", width=5)
        self.parent.after(0, self.animation_hl)

    # highlight 효과를 위한 sub 함수 1
    def size_up(self):
        k = 1                                       # k : size 변경되는 폭
        x0, y0, x1, y1 = self.canvas.bbox(self.id)
        x0, y0 = x0 - k, y0 - k
        x1, y1 = x1 + k, y1 + k
        self.canvas.coords(self.id, x0, y0, x1, y1)

    # highlight 효과를 위한 sub 함수 2
    def animation_hl(self):
        if (self.canvas.bbox(self.id)) is not None:
            x0, y0, x1, y1 = self.canvas.bbox(self.id)
            if abs(x0 - x1) < self.SIDE:
                self.size_up()
                self.parent.after(80, self.animation_hl)
            else:
                self.canvas.delete("hl")
