import pygame

# 초기 설정
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# 색깔 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 패들 설정
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
paddle_speed = 6
ball_speed_x, ball_speed_y = 5, 5

# 패들 위치
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

# 점수
left_score, right_score = 0, 0
font = pygame.font.Font(None, 36)

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed

    # 공 이동
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 공 충돌 처리
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1  # 상하 벽 반사
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1  # 패들과 충돌 시 반사

    # 점수 업데이트
    if ball.left <= 0:
        right_score += 1
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2  # 중앙 초기화
        ball_speed_x *= -1  # 방향 반전
    if ball.right >= WIDTH:
        left_score += 1
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1

    # 화면에 그리기
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # 점수 표시
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH//4, 20))
    screen.blit(right_text, (WIDTH*3//4, 20))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
