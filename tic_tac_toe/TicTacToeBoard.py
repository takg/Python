
class TicTacToeBoard:
    def __init__(self):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.win_combinations = []
        self.next_player = 1
        self.moves = []
        self.game_over = False

        # row
        for x in range(3):
            self.win_combinations.append([3*x, 3*x + 1, 3*x + 2])
        # col
        for x in range(3):
            self.win_combinations.append([x, x + 3, x + 6])
        # diagonal
        self.win_combinations.append([0, 4, 8])
        self.win_combinations.append([2, 4, 6])

    def check_game_over(self):
        return self.game_over

    def save_game_and_reset(self):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.next_player = 1
        self.moves = []
        self.game_over = False

    def check_more_slots_available(self):
        flag = False

        if self.game_over:
            flag = False
        else:
            for index in range(9):
                if self.check_position_empty(index):
                    flag = True

        if not flag:
            self.game_over = True

        return flag

    def take(self, index):
        flag = False

        if not self.game_over and self.check_position_empty(index):
            self.board[index] = self.next_player
            self.moves.append(index)
            self.next_player = -1 * self.next_player
            flag = True
            self.check_more_slots_available()

        return flag

    def check_position_empty(self, index):
        return self.board[index] == 0

    def check_position_taken_by_first_player(self, index):
        return self.board[index] == 1

    def check_win(self):
        flag = False
        for [x, y, z] in self.win_combinations:
            sum = self.board[x] + self.board[y] + self.board[z]
            if sum == 3 or sum == -3:
                flag = True
                self.game_over = True
                break
        return flag