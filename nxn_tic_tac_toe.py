class TicTacToe:

    def __init__(self, n = 3):

        if not isinstance(n, int) or n < 1:
            raise ValueError("Board size must be an Integer of atleast size 1...")


        self.board = [["." for i in range(n)] for j in range(n)]
        self.valid_states = {(i,j) for i in range(1,n+1) for j in range(1,n+1)}
        
        self.winning_states = [[(i,j) for j in range(n)] for i in range(n)] + [[(i,j) for i in range(n)] for j in range(n)] + [[(i,i) for i in range(n)]] + [[(n - 1 - i,i) for i in range(n)]]

        self.current_player = 1
        self.game_over = False


    def display_board(self):

        for i in self.board:
            print("|".join(i))
    
    def get_move(self):

        while True:
            try:
                row = int(input("Enter row: "))
                column = int(input("Enter column: "))

                if (row, column) in self.valid_states:
                    return row, column
                    
                print("Please enter a Valid move.")
            
            except ValueError:
                print("Please enter an Integer...")
    
    def make_move(self, row, column):

        if self.current_player == 1:
            self.board[row - 1][column - 1] = "X"
        else:
            self.board[row - 1][column - 1] = "O"
        
        self.valid_states.remove((row, column))
        self.current_player = 1 - self.current_player

    def check_game_over(self):

        for line in self.winning_states:
            values = [self.board[r][c] for r,c in line]
            if values[0] != "." and len(set(values)) == 1:
                print(f"Player {values[0]} has won, Congrats!")
                self.game_over = True
                break
    
        
        if not self.valid_states and not self.game_over:
            print("The game has ended in a Draw!")
            self.game_over = True
    
    def play(self):

        print("Welcome to TicTacToe!")
        self.display_board()

        while not self.game_over:

            row, column = self.get_move()
            self.make_move(row, column)
            self.display_board()
            self.check_game_over()


if __name__ == "__main__":

    game = TicTacToe()
    game.play()
