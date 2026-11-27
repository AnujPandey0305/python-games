class ConnectFour:
     
    def __init__(self):
          
        self.board = [["." for i in range(7)] for j in range(6)]
        self.current_player = 1
        self.valid_moves = {}
        for i in range(7):
            self.valid_moves[i] = 5

        self.winning_states = []

        directions = [(0,1), (1,0), (1,1), (-1, 1)]

        for r in range(6):
            for c in range(7):
                for dr, dc in directions:

                    end_r = r + 3*dr
                    end_c = c + 3*dc

                    if 0 <= end_r < 6 and 0 <= end_c < 7:

                        positions = []

                        for k in range(4):
                            positions.append((r + k*dr, c+ k*dc))
                        
                        self.winning_states.append(positions)
    
    def display_board(self):

        blue = "\033[44m"
        reset = "\033[0m"

        symbols = {
            "X": "🔴",
            "O": "🟡",
            ".": "⚫"
        }

        print("1   2   3   4   5   6   7")

        print(blue + " " * 28 + reset)

        for row in self.board:

            print(blue + " " + "  ".join(
                symbols[value] for value in row
            ) + " " + reset)

            print(blue + " " * 28 + reset)

        print()

    
    def validate_move(self):

        player = "🔴 Red" if self.current_player == 1 else "🟡 Yellow"

        while True:

            try:

                column = int(input(f"{player}, which column would you like to play? ")) - 1

                if column in self.valid_moves and self.valid_moves[column] != -1:      
                    return column

                print("Move Invalid, Please try again...")

            except ValueError:
                print("Please enter an Integer...")

    def make_move(self, column):

        if self.current_player == 1:
            self.board[self.valid_moves[column]][column] = "X"
        else:
            self.board[self.valid_moves[column]][column] = "O"

        self.current_player = 1 - self.current_player
        self.valid_moves[column] -= 1
    
    def check_game_over(self):

        for values in self.winning_states:

            state = {self.board[r][c] for r,c in values}
        
            if len(state) == 1 and "." not in state:

                winner = state.pop()
                colours = {"X": "🔴 Red", "O": "🟡 Yellow"}

                print(f"Player {colours[winner]} has Won, Congrats!")
                return True

        if all(row == -1 for row in self.valid_moves.values()):
            print("The game has ended in a Draw!")
            return True
        
        return False
    
    def play(self):

        self.display_board()

        while not self.check_game_over():

            column = self.validate_move()
            self.make_move(column)
            self.display_board()


if __name__ == "__main__":
    game = ConnectFour()
    game.play()
