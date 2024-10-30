import random

BOARD_HEIGHT = 8
BOARD_WIDTH = 6
BITS = 10


def run():
    # GENERATE BOARD
    board = [[0] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]
    # FILL WITH RANDOM BITS
    for i in range(BITS):
        ry = random.randint(0, BOARD_HEIGHT - 1)
        rx = random.randint(0, BOARD_WIDTH - 1)
        board[ry][rx] = random.choice([1, 2, 3])
    pg(board)
    shift_down(board)


def shift_down(board):
    for x in range(BOARD_WIDTH):
        moved = 1
        while moved > 0:
            moved = 0
            for y in range(BOARD_HEIGHT - 1, 0, -1):
                if board[y][x] == 0 and board[y - 1][x] != 0:
                    board[y][x], board[y - 1][x] = board[y - 1][x], board[y][x]
                    moved += 1

    pg(board)


def pg(board):
    print("########################")
    for y in range(BOARD_HEIGHT):
        print(board[y])


if __name__ == "__main__":
    run()
