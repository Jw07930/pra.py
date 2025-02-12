import pygame
import numpy as np

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
GRAY = (169, 169, 169)

# 게임 설정
BOARD_SIZE = 24
CELL_SIZE = 30
WIDTH = BOARD_SIZE * CELL_SIZE + 200  # 점수 표시 공간 포함
HEIGHT = BOARD_SIZE * CELL_SIZE
FPS = 60

# 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello 24x24")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()


# 오델로 보드 초기화
def initialize_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    mid = BOARD_SIZE // 2
    board[mid - 1][mid - 1], board[mid][mid] = 1, 1  # 흰 돌
    board[mid - 1][mid], board[mid][mid - 1] = -1, -1  # 검은 돌
    return board


def draw_board(board):
    screen.fill(GREEN)

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if board[y][x] == 1:
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE // 2 - 2)
            elif board[y][x] == -1:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 2 - 2)

    # 점수 표시
    white_score = np.sum(board == 1)
    black_score = np.sum(board == -1)
    text_white = font.render(f"White: {white_score}", True, WHITE)
    text_black = font.render(f"Black: {black_score}", True, BLACK)
    screen.blit(text_white, (BOARD_SIZE * CELL_SIZE + 20, 50))
    screen.blit(text_black, (BOARD_SIZE * CELL_SIZE + 20, 100))


def is_valid_move(board, x, y, player):
    if board[y][x] != 0:
        return False
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    valid = False

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board[ny][nx] == -player:
                found_opponent = True
            elif board[ny][nx] == player:
                if found_opponent:
                    return True
                break
            else:
                break
            nx += dx
            ny += dy
    return valid


def apply_move(board, x, y, player):
    board[y][x] = player
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        to_flip = []
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board[ny][nx] == -player:
                to_flip.append((nx, ny))
            elif board[ny][nx] == player:
                for fx, fy in to_flip:
                    board[fy][fx] = player
                break
            else:
                break
            nx += dx
            ny += dy


def get_valid_moves(board, player):
    return [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if is_valid_move(board, x, y, player)]


def is_game_over(board):
    return not get_valid_moves(board, 1) and not get_valid_moves(board, -1)


def get_winner(board):
    white_score = np.sum(board == 1)
    black_score = np.sum(board == -1)
    if white_score > black_score:
        return "White Wins!"
    elif black_score > white_score:
        return "Black Wins!"
    else:
        return "Draw!"


def main():
    board = initialize_board()
    running = True
    player = -1  # Black starts

    while running:
        screen.fill(GREEN)
        draw_board(board)
        pygame.display.flip()

        if is_game_over(board):
            winner_text = font.render(get_winner(board), True, WHITE)
            screen.blit(winner_text, (BOARD_SIZE * CELL_SIZE + 20, 200))
            pygame.display.flip()
            pygame.time.delay(3000)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if (x, y) in get_valid_moves(board, player):
                    apply_move(board, x, y, player)
                    player *= -1

        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()