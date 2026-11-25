#!/usr/bin/env python3
"""
Number Solitaire
================

36 cards (four each of 1-9) are shuffled and dealt into six stacks, A-F.
The goal is to build four complete stacks running 9 down to 1.

Rules
-----
- A card can go onto a card exactly one higher (e.g. a 4 onto a 5) or onto
  an empty stack.
- A single card may also be placed on any other card, but that BLOCKS the
  destination stack: nothing can be placed on it until the blocking card is
  moved off again, and a blocking card may only be moved to a legal spot.
- A run of consecutive cards (e.g. 6-5-4) can be moved together, but only
  onto a card one higher than its bottom card, or onto an empty stack.
  A run starting with 9 can only go onto an empty stack.
- A stack holding exactly 9, 8, ..., 1 is complete and locked.

Controls
--------
  AB    move one card from stack A to stack B
  AB3   move three cards from stack A to stack B
  U     undo the last move
  R     restart with a new deal
  Q     quit (Ctrl-C also works)
"""

import copy
import random

STACK_LETTERS = "ABCDEF"
N_STACKS = len(STACK_LETTERS)
COMPLETE_STACK = [9, 8, 7, 6, 5, 4, 3, 2, 1]
STACKS_TO_WIN = 4

UNDO, RESTART, QUIT = "undo", "restart", "quit"


def display_state(s, *, clear=False):
    """Print the game state. If clear is True, clear the terminal first."""

    def colored(r, g, b, text):
        rb, gb, bb = (r + 2) / 3, (g + 2) / 3, (b + 2) / 3
        rd, gd, bd = r / 1.5, g / 1.5, b / 1.5
        return (f"\033[38;2;{int(rb*255)};{int(gb*255)};{int(bb*255)}m"
                f"\033[48;2;{int(rd*255)};{int(gd*255)};{int(bd*255)}m{text}\033[0m")

    def inverse(text):
        return f"\033[38;2;51;51;51m\033[48;2;204;204;204m{text}\033[0m"

    colours = [(1.0, 0.349, 0.369),
               (1.0, 0.573, 0.298),
               (1.0, 0.792, 0.227),
               (0.773, 0.792, 0.188),
               (0.541, 0.788, 0.149),
               (0.322, 0.651, 0.459),
               (0.098, 0.509, 0.769),
               (0.259, 0.404, 0.675),
               (0.416, 0.298, 0.576)]

    if clear:
        print("\033[2J\033[H", end="")

    print("\n")
    numrows = max((len(stack) for stack in s["stacks"]), default=0)
    for row in range(numrows - 1, -1, -1):
        for i, stack in enumerate(s["stacks"]):
            if len(stack) > row:
                val = stack[row]
                if len(stack) == row + 1 and s["blocked"][i]:
                    print(inverse(f" {val} "), end=" ")
                elif s["complete"][i]:
                    print(colored(*colours[val - 1], "   "), end=" ")
                else:
                    print(colored(*colours[val - 1], f" {val} "), end=" ")
            else:
                print("    ", end="")
        print()
    print("  ".join(f" {c}" for c in STACK_LETTERS))


def initial_state():
    """Shuffle four copies of 1-9 and deal them into six stacks of six."""
    cards = [value for value in range(1, 10) for _ in range(4)]
    random.shuffle(cards)
    size = len(cards) // N_STACKS
    return {
        "blocked": [False] * N_STACKS,
        "complete": [False] * N_STACKS,
        "stacks": [cards[i * size:(i + 1) * size] for i in range(N_STACKS)],
    }


def parse_move(input_str):
    """
    Turn user input into a command.

    Returns UNDO, RESTART or QUIT for those commands, otherwise a tuple
    (from_stack, to_stack, n_cards), e.g. "AB3" -> (0, 1, 3).
    Raises ValueError for anything else.
    """
    text = input_str.strip().upper()

    if text == "U":
        return UNDO
    if text == "R":
        return RESTART
    if text == "Q":
        return QUIT

    if len(text) < 2 or text[0] not in STACK_LETTERS or text[1] not in STACK_LETTERS:
        raise ValueError(f"Not a valid move: {input_str!r}")

    count_str = text[2:]
    if count_str == "":
        n_cards = 1
    elif count_str.isdigit() and int(count_str) > 0:
        n_cards = int(count_str)
    else:
        raise ValueError(f"Card count must be a positive integer: {input_str!r}")

    return STACK_LETTERS.index(text[0]), STACK_LETTERS.index(text[1]), n_cards


def validate_move(state, move):
    """Return True if the move is legal in the given state."""
    source, dest, n_cards = move
    stacks = state["stacks"]

    if not (0 <= source < N_STACKS and 0 <= dest < N_STACKS):
        return False
    if source == dest:
        return False
    if n_cards < 1 or n_cards > len(stacks[source]):
        return False
    if state["blocked"][dest]:
        return False
    if state["complete"][source] or state["complete"][dest]:
        return False

    # The moving cards must form a descending run, e.g. 6-5-4.
    moving = stacks[source][-n_cards:]
    if any(moving[k] != moving[k + 1] + 1 for k in range(n_cards - 1)):
        return False

    bottom = moving[0]
    top_dest = stacks[dest][-1] if stacks[dest] else None
    lands_legally = top_dest is None or bottom + 1 == top_dest

    # Only the single blocking card can be moved off a blocked stack.
    if state["blocked"][source] and n_cards > 1:
        return False

    # A run, or the card blocking a stack, can't create a new block.
    if n_cards > 1 or state["blocked"][source]:
        return lands_legally

    # A single unblocked card can go anywhere (possibly blocking the destination).
    return True


def apply_move(state, move):
    """Apply a valid move to the state, modifying it in place."""
    source, dest, n_cards = move
    source_stack = state["stacks"][source]
    dest_stack = state["stacks"][dest]

    bottom = source_stack[-n_cards]
    top_dest = dest_stack[-1] if dest_stack else None

    dest_stack.extend(source_stack[-n_cards:])
    del source_stack[-n_cards:]

    # Moving cards off a blocked stack always frees it.
    state["blocked"][source] = False

    # A single card that doesn't land on (card + 1) or an empty stack blocks it.
    if n_cards == 1 and top_dest is not None and bottom + 1 != top_dest:
        state["blocked"][dest] = True

    if dest_stack == COMPLETE_STACK:
        state["complete"][dest] = True


def game_won(state):
    return sum(state["complete"]) == STACKS_TO_WIN


def play_game():
    board = initial_state()
    history = [copy.deepcopy(board)]

    try:
        while True:
            display_state(board)

            try:
                command = parse_move(input("Move: "))
            except ValueError as err:
                print(err)
                continue

            if command == QUIT:
                break

            if command == RESTART:
                board = initial_state()
                history = [copy.deepcopy(board)]
                continue

            if command == UNDO:
                if len(history) > 1:
                    history.pop()
                    # Copy, so later moves don't modify the saved state.
                    board = copy.deepcopy(history[-1])
                else:
                    print("Nothing to undo.")
                continue

            if not validate_move(board, command):
                print("Illegal move.")
                continue

            apply_move(board, command)
            history.append(copy.deepcopy(board))

            if game_won(board):
                display_state(board)
                print(f"You won in {len(history) - 1} moves!")
                break

    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    play_game()
