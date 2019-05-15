import numpy as np
import random as rd

class MapClass:
    n = 0
    Map = None
    Map_prev = None
    input_ = None
    flag = True
    win_flag = False
    score = 0
    score_prev = 0
    highlight_flag = False
    result = 'playing'

    def __init__(self, n):
        self.n = n
        self.Map = np.full((n, n), 0)
        self.AddNew(2)
        self.Map_prev = self.Map.copy()  # save previous state
        self.score = 0
        self.score_prev = 0
        self.highlight_index = tuple()


    #  0 인곳 중 랜덤인 곳에 랜덤으로 2 or 4 생성.
    def AddNew(self, block=1):
        zero_list = np.argwhere(self.Map == 0)                           # 0 인곳 좌표 찾고 리스트(zero_list)에 좌표 넣기.
        rd_list = list()                                                 # highlight effect 를 위해 위치 받기.

        for _ in range(block):
            i, j = rd.choice(zero_list)
            self.Map[i, j] = rd.choice([2] * 10 + [4])                   # 0인곳 중 한 곳에 2 or 4 넣기. (10 : 1 비율로 2 or 4 출력.)
            zero_list = zero_list[~np.all(zero_list == [i, j], axis=1)]  # zero_list 에서 위의 좌표 제거.
            rd_list.append((i, j))
        return rd_list[0]


    def step(self, detail):
        inputs = str(detail.keysym)[0]

        temp_score = self.score
        temp_prev = self.Map.copy()

        if inputs == 'U':
            self.Up()

        elif inputs == 'D':
            self.Down()

        elif inputs == 'L':
            self.Left()

        elif inputs == 'R':
            self.Right()

        else:
            print("잘못된 입력\n")
            return

        if np.array_equal(temp_prev, self.Map) is True:
            return

        self.Map_prev = temp_prev.copy()
        self.score_prev = temp_score

        # 후처리
        if self.iswin():
            self.result = 'win'

        if not self.isfull():
            """highlight_flag :: on/off highlight effect"""
            self.highlight_flag = True
            """highlight_index :: index that you want to see highlight effect on matrix"""
            self.highlight_index = self.AddNew()


        if self.isfull():
            if self.islose():
                self.result = 'full'
        return


    # 빈 공간 제거
    def move_Up(self):
        for i in range(len(self.Map)):
            tmp_list = self.Map[:, i]
            tmp_zeros = tmp_list[tmp_list == 0]
            tmp_values = tmp_list[tmp_list != 0]
            self.Map[:, i] = np.concatenate([tmp_values, tmp_zeros])

    def move_Down(self):
        for i in range(len(self.Map)):
            tmp_list = self.Map[:, i]
            tmp_zeros = tmp_list[tmp_list == 0]
            tmp_values = tmp_list[tmp_list != 0]
            self.Map[:, i] = np.concatenate([tmp_zeros, tmp_values])

    # 같은 숫자 merge
    def merge_UpDown(self, line1, line2):
        for i in range(len(self.Map)):
            if self.Map[line1, i] == self.Map[line2, i]:
                self.Map[line1, i] = 0
                self.Map[line2, i] = self.Map[line2, i] * 2
                self.score += self.Map[line2, i]

    # 빈 공간 제거
    def move_Left(self):
        for i in range(len(self.Map)):
            tmp_list = self.Map[i, :]
            tmp_zeros = tmp_list[tmp_list == 0]
            tmp_values = tmp_list[tmp_list != 0]
            self.Map[i, :] = np.concatenate([tmp_values, tmp_zeros])

    def move_Right(self):
        for i in range(len(self.Map)):
            tmp_list = self.Map[i, :]
            tmp_zeros = tmp_list[tmp_list == 0]
            tmp_values = tmp_list[tmp_list != 0]
            self.Map[i, :] = np.concatenate([tmp_zeros, tmp_values])

    # 같은 숫자 merge
    def merge_LeftRight(self, line1, line2):
        for i in range(len(self.Map)):
            if self.Map[i, line1] == self.Map[i, line2]:
                self.Map[i, line1] = 0
                self.Map[i, line2] = self.Map[i, line2] * 2
                self.score += self.Map[i, line2]

    # 1
    def Up(self):
        # print('input : 위\n')
        for i in range(1, len(self.Map)):  # if 4*4    ==>    1,0    2,1    3,2
            self.move_Up()
            self.merge_UpDown(i, i - 1)

    # 2
    def Down(self):
        # print('input : 아래\n')
        for i in range(len(self.Map) - 1, 0, -1):  # if 4*4    ==>    2,3     1,2     0,1
            self.move_Down()
            self.merge_UpDown(i - 1, i)

    # 3
    def Left(self):
        # print('input : 좌\n')
        for i in range(1, len(self.Map)):  # if 4*4    ==>    1,0    2,1    3,2
            self.move_Left()
            self.merge_LeftRight(i, i - 1)

    # 4
    def Right(self):
        # print('input : 우\n')
        for i in range(len(self.Map) - 1, 0, -1):  # if 4*4    ==>    2,3     1,2     0,1
            self.move_Right()
            self.merge_LeftRight(i - 1, i)

    # return boolean
    def iswin(self):
        if 2048 in self.Map and self.win_flag is False:
            self.win_flag = True
            return True

    def isfull(self):
        if len(self.Map[self.Map == 0]) == 0:
            return True
        return False

    def islose(self):
        for i in range(0, len(self.Map)):
            for j in range(0, len(self.Map)):
                if j != len(self.Map) - 1 and self.Map[i][j] == self.Map[i][j + 1]:
                    return False
                if i != len(self.Map) - 1 and self.Map[i][j] == self.Map[i + 1][j]:
                    return False
        self.flag = False
        return True
