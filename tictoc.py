class TicToc:
    def __init__(self, n):
        self.n = n
        self.rows = [0]*n
        self.cols = [0]*n
        self.diagonal = 0
        self.anti_diagonal = 0

    def move(self, row, col, player):
        value = 1 if player==1 else -1
        self.rows[row] += value
        self.cols[col] += value
        if row==col:
            self.diagonal += value
        
        if row + col == self.n - 1:
            self.anti_diagonal += value

        if (abs(self.rows[row]) == self.n or
            abs(self.cols[col]) == self.n or
            abs(self.anti_diagonal) == self.n or
            abs(self.diagonal) == self.n):
            return player

        return 0

