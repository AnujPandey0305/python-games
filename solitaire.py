#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:15:13 2024

@author: anujpandey

# Import the random module to later shuffle cards in the initial_state function.
import random 

def display_state(s, *, clear=False):
    """
    Display the state s

    If 'clear' is set to True, erase previous displayed states
   """
    def colored(r, g, b, text):
        rb,gb,bb=(r+2)/3,(g+2)/3,(b+2)/3
        rd,gd,bd=(r)/1.5,(g)/1.5,(b)/1.5
        return f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m"

    def inverse(text):
        rb,gb,bb=.2,.2,.2
        rd,gd,bd=.8,.8,.8
        return f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m"

    colours = [(1.0, 0.349, 0.369),
               (1.0, 0.573, 0.298),
               (1.0, 0.792, 0.227),
               (0.773, 0.792, 0.188),
               (0.541, 0.788, 0.149),
               (0.322, 0.651, 0.459),
               (0.098, 0.509, 0.769),
               (0.259, 0.404, 0.675),
               (0.416, 0.298, 0.576)]

    n_columns = len(s['stacks'])
    if clear:
        print(chr(27) + "[2J")

    print('\n')
    row = 0
    numrows = max(len(stack) for stack in s['stacks'])
    for row in range(numrows-1,-1,-1):
        for i in range(n_columns):
            num_in_col = len(s['stacks'][i])
            if num_in_col > row:
                val = s['stacks'][i][row]
                if num_in_col == row+1 and s['blocked'][i]:
                    print(inverse(' '+str(val)+' '),end=' ')
                else:
                    if s['complete'][i]:
                        print(colored(*colours[val-1],'   '),end=' ')
                    else:
                        print(colored(*colours[val-1],' '+str(val)+' '),end=' ')
            else:
                print('    ',end='')
        print()
    print(' A   B   C   D   E   F')


# Q1
def initial_state():
    # Create a list holding all the cards (numbers) required.
    cards = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9]
    # Shuffle the cards
    random.shuffle(cards)
    # Let the first 6 elements of cards become stack A and so on... 
    # At the start, all stacks should not be blocked or completed.
    initial_state = {"blocked": [False,False,False,False,False,False], 
                     "complete": [False,False,False,False,False,False],
                     "stacks": [cards[0:6],cards[6:12],cards[12:18],
                     cards[18:24],cards[24:30],cards[30:36]]}
    # Finally, return this intial_state
    return initial_state


# Q2
def parse_move(input_str):
    # If the user enters "ab3", treat it as "AB3"
    input_str = input_str.upper()
    # For Q8, if input_str == "U" or "u", return the integer -1
    if input_str == "U" or input_str == "u":
        return -1
    # For Q7, if input_str == "R" or 'r' return the integer 0.
    if input_str == "R" or input_str == "r":
        return 0
    # For Q6, raise a ValueError if the string is not of the form of 2 letters,
    # optionally followed by a positive integer.
    # We have already taken into account the cases where input_str is a restart or undo 
    # move, so input_str must be atleast two letters.
    if len(input_str) < 2:
        raise ValueError
    # input_str[0] and input_str[1] should be letters:
    if not input_str[0].isascii() or not input_str[1].isascii():
        raise ValueError
    # If the input_str has a number, it must be a positive integer.
    if len(input_str) > 2:
        # isdigit() rules out decimals and int(input_str[2]) > 0 rules out 0.
        if not input_str[2].isdigit() or int(input_str[2]) == 0:
            raise ValueError
    # Create a dictionary to easily convert between stacks in terms of letters and numbers.
    # Raise ValueError if the two letters are outside the range A-F.
    stacks = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}
    if input_str[0] not in stacks or input_str[1] not in stacks:
        raise ValueError
    # Q2
    # input_str will be a string e.g "AB3"
    # parse_move("AB3") should return the tuple (0, 1, 3)
    # Using the dictionary, turn the input_str into a tuple representing the move.
    # Add a condition so if no number is given e.g "AB" (hence len(input_str) == 2),
    # then Number of cards moved = 1
    if len(input_str) == 2:
        move_tuple = (stacks[input_str[0]], stacks[input_str[1]], 1)
    else:
        move_tuple = (stacks[input_str[0]], stacks[input_str[1]], int(input_str[2]))
    # Finally, return the move as a tuple
    return move_tuple 
    

# Q3
def validate_move(state, move):
    # Determine if a certain move is allowed (True) or not (False)
    # Example move (0, 1, 3) meaning move 3 cards from stack A to stack B.
    # Assign 3 variables initial, destination and number_of_cards from the move tuple
    # to simplify code.
    initial, destination, number_of_cards = move
    # Make sure the initial stack has enough cards for this move.
    # The initial stack and destination stack must be numbers between 0-5.
    if (initial < 0 or initial > 5) or (destination < 0 or destination > 5):
        return False
    if number_of_cards > len(state["stacks"][initial]):
        return False
    # Make sure the destination stack (e.g. B) isn't "blocked" else invalid move.
    if state["blocked"][destination]:
        return False
    # Make sure BOTH the initial and destination stacks aren't "complete" else invalid move.
    if state["complete"][initial] or state["complete"][destination]:
        return False
    # A 9 on it's own can move to any stack but if you are moving multiple cards and the
    # bottom card is 9, then it must move to an empty stack.
    # Assign a variable to the bottom moving card:
    bottom_moving_card = state["stacks"][initial][-number_of_cards]
    if bottom_moving_card == 9 and number_of_cards > 1:
        # Multiple moving cards with a bottom_moving_card = 9 must go onto an empty stack.
        if len(state["stacks"][destination]) != 0:
            return False
    # For the following logic, we can ignore the case where the bottom_moving_card == 9,
    # because we have already considered it in the lines above. If we are moving 
    # multiple cards, we cannot play a blocking move hence the bottom_moving_card must
    # be 1 less than the top card in the destination stack or the destination stack must be empty.
    # First assign a variable to the top card in the destination stack.
    # We need this if statement to make sure the destination stack isn't empty otherwise
    # we will get a list index error.
    if len(state["stacks"][destination]) != 0:
        top_destination_card = state["stacks"][destination][-1]
    else:
        # We also have to state what the top_destination_card is when the stack is empty
        # for our following code.
        top_destination_card = None
    if (number_of_cards > 1) and (bottom_moving_card != 9):
        # Check bottom_moving_card is one less than the top_destination_card
        if (top_destination_card is not None) and (bottom_moving_card + 1 != top_destination_card):
            return False
    # If the initial stack is blocked then the card can only go to a valid stack,
    # i.e It can't go and block another stack.
    if state["blocked"][initial]:
        # If a stack is blocked, only one card can be moved from it.
        if number_of_cards > 1:
            return False
        # If the blocking card was 9, it must move to an empty stack.
        if (bottom_moving_card == 9) and (len(state["stacks"][destination]) != 0):
            return False  
        # (e.g. If the blocking card == 2, it must move to an empty stack or on top of a 3.)
        # This logic follows for all blocking cards != 9.
        if (bottom_moving_card != 9):
            if (top_destination_card is not None) and (bottom_moving_card + 1 != top_destination_card):
                return False
    # If multiple cards are being moved, they must be adjacent values
    if number_of_cards > 1:
        for i in range(1, number_of_cards):
            if state["stacks"][initial][-i] + 1 != state["stacks"][initial][(-(i+1))]:
                return False
    # If the move passes (or can skip) all of these conditions then we know the move is valid.
    return True


# Q4
def apply_move(state, move):
    # This function should update the state and modify it in place to what the state
    # becomes after the move is played. We can assume the states and moves inputted are valid.
    # Unpack the move tuple to simplify further code.
    initial, destination, number_of_cards = move
    # We need to remove number_of_cards from the initial stack and put it 
    # onto the destination stack. Assign a variable to both of these stacks.
    # Both of these variables will be a list of numbers representing the cards in the stack.
    initial_stack = state["stacks"][initial]
    destination_stack = state["stacks"][destination]
    # We can assign variables for the bottom moving card on the initial stack and the top card 
    # on the destination_stack to simplify code later on. When assigning a variable for the
    # top_card, we have to make sure if the stack is empty then top_card is None
    moving_card = initial_stack[-number_of_cards]
    if len(state["stacks"][destination]) != 0:
        top_card = state["stacks"][destination][-1]
    else:
        # We also have to state what the top_card is when the stack is empty
        # for our following code.
        top_card = None
    # We can add the required cards into the destination_stack using the following for
    # loop, the -1 at the end is required to make sure the bottom_moving_card moves first.
    for i in range(number_of_cards, 0, -1):
        destination_stack.append(initial_stack[-i])
    # Next we have to remove these cards form the initial_stack.
    initial_stack[-number_of_cards:] = []
    # Now we have modified both the initial_stack and destination_stack.
    # We can now focus on modifying the blocked and complete lists.
    # First with blocked, a stack only becomes blocked if we move one card onto it
    # and this one card is not 1 less than the top card on this stack.
    # We only have to consider number_of_cards == 1 as if it was > 1, 
    # the move would be invalid and our validate_move function takes care of this.
    if number_of_cards == 1:
        # Here we have to state moving_card != 9 as our logic for 9 will be different.
        if moving_card != 9:
            if (top_card is not None) and (moving_card + 1 != top_card):
                # We have to mark the destination_stack as Blocked.
                state["blocked"][destination] = True
        else: 
            # If the moving_card is 9, the destination_stack must now look like
            # [9] after the move is played, otherwise we are playing a blocking move. 
            if destination_stack == [9]:
                state["blocked"][destination] = False
            else:
                state["blocked"][destination] = True
            
    # We have to also consider the case where the initial_stack was blocked, but we moved
    # the blocking card onto another stack, i.e. freeing the initial_stack.
    if state["blocked"][initial]:
        # After any valid move starting at this stack, this stack would be unblocked.
        state["blocked"][initial] = False
    # Finally, we have to update the complete list.
    if destination_stack == [9,8,7,6,5,4,3,2,1]:
        state["complete"][destination] = True

# Q5
def game_won(state):
    # We can keep the code concise by checking in one line if the number of complete stacks 
    # in our state dictionary == 4 (which would mean the game has been won).
    return sum(state["complete"]) == 4

# For questions 1-5, DO NOT edit the play_game function.
# For the tasks in questions 1-5 initial_state, parse_move,
# validate_move, apply_move, and game_won must work with the
# the unmodified play_game function.

# For questions 6, 7 and 8, you should modify the play_game
# function

# Import the copy module so we can do a deep copy
import copy

def play_game():
    # When we start the game,
    board = initial_state()
    # Keep a list of all the previous board states, incase you want to undo.
    history_board_states = [copy.deepcopy(board)]
    # Assign a variable to keep track of which state you are in, in the history list.
    # To start you are in the 0 state:
    current_state_index = 0
    try:
        while True:
            # Display the current game state
            display_state(board, clear=False)
            # Parse the text typed by the user and convert it to a move
            # If users text raised ValueError in the parse_move function, 
            # re-prompt the User for another move
            while True:
                try:
                    # Read input from the user.
                    # (Do not alter this line, even in questions 6, 7, 8.)
                    move_str = input()
                    move = parse_move(move_str)
                    break
                except ValueError:
                    pass
            
            # For Q7, if parse_move returns 0, reset the game.
            if move == 0:
                board = initial_state()
                # If we reset the game, we have to reset the history_board_states 
                # and the current_state_index for the undo functionality, Q8.
                history_board_states = [copy.deepcopy(board)]
                current_state_index = 0
                continue
            
            # For Q8, if parse_move returns -1, undo a move. (i.e. go to the last
            # board state in history_board_states)
            if move == -1:
                # Current_state_index must be > 0 to make sure we aren't at our initial state.
                if current_state_index > 0:
                    current_state_index -= 1
                    board = history_board_states[current_state_index]       
                    # We have to remove our last state in the history_board_states list,
                    # if we undo a move.
                    history_board_states = history_board_states[:current_state_index + 1]
                # Display the previous board state after the undo, or the same board state
                # if we are already at the initial state (i.e. current_state_index == 0)
                display_state(board, clear = False)
                continue

            # If the move was valid...
            if validate_move(board,move):
                apply_move(board, move) # ... alter the board
                # After applying the move, we have a new board state, so we need to 
                # modify the history_board_states and the current_state_index.
                history_board_states.append(copy.deepcopy(board))
                # Add one to current_state_index to keep it on track.
                current_state_index += 1

            # If we've won, end the game
            if game_won(board):
                # If the game is won, display a final winning board state.
                display_state(board, clear = False)
                break

    except KeyboardInterrupt: # If the user presses Ctrl-C, quit
        pass


if __name__ == "__main__":
    play_game()
