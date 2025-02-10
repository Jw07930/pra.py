import pygame
import random

# 게임 설정
GRID_SIZE = 10  # 10x10 그리드
CELL_SIZE = 40  # 한 칸 크기
MINES_COUNT = 15  # 지뢰 개수
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# 색상 설정
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# pygame 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("지뢰찾기")
font = pygame.font.Font(None, 30)


# 지뢰 필드 생성
def create_minefield():
    field = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = set()

    # 랜덤한 위치에 지뢰 배치
    while len(mines) < MINES_COUNT:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            field[y][x] = -1  # 지뢰 위치

    # 주변 지뢰 개수 계산
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if field[y][x] == -1:
                continue
            count = sum((ny, nx) in mines for ny in range(y - 1, y + 2) for nx in range(x - 1, x + 2) if
                        0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE)
            field[y][x] = count

    return field, mines


# 게임 초기화
minefield, mines = create_minefield()
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
flags = set()
game_over = False


# 주변 빈 칸 열기
def reveal_cells(x, y):
    if (x, y) in flags or revealed[y][x]:
        return
    revealed[y][x] = True

    # 빈 칸이면 주변 자동 확장
    if minefield[y][x] == 0:
        for ny in range(y - 1, y + 2):
            for nx in range(x - 1, x + 2):
                if 0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE:
                    reveal_cells(nx, ny)


# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = event.pos
            x, y = mx // CELL_SIZE, my // CELL_SIZE

            if event.button == 1:  # 왼쪽 클릭
                if minefield[y][x] == -1:  # 지뢰 클릭
                    game_over = True
                else:
                    reveal_cells(x, y)

            elif event.button == 3:  # 오른쪽 클릭 (깃발)
                if (x, y) in flags:
                    flags.remove((x, y))
                else:
                    flags.add((x, y))

    # 셀 그리기
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if revealed[y][x]:  # 열린 셀
                pygame.draw.rect(screen, GRAY, rect)
                if minefield[y][x] > 0:
                    text = font.render(str(minefield[y][x]), True, BLACK)
                    screen.blit(text, (x * CELL_SIZE + 15, y * CELL_SIZE + 10))
            elif (x, y) in flags:  # 깃발
                pygame.draw.rect(screen, GREEN, rect)
            else:  # 닫힌 셀
                pygame.draw.rect(screen, DARK_GRAY, rect)

            pygame.draw.rect(screen, BLACK, rect, 2)

    # 지뢰가 터졌을 때 게임 오버 화면 표시
    if game_over:
        for (x, y) in mines:
            pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()

pygame.quit()
