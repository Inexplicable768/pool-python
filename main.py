import math, pygame, random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CUE_COLOR = (200, 200, 200)
RADIUS = 12
FRICTION = 0.98
IMPULSE = 0.7
NUMBALLS = 15
MAX_FORCE = 20

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pool Game with Sphere Collision")

class Pocket():
    def __init__(self, x, y, color):
        pass
class Ball():
    def __init__(self, x, y, color):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.color = color

    def move(self):
        self.pos += self.vel
        self.vel *= FRICTION
        if self.vel.length() < 0.1:
            self.vel = pygame.Vector2(0, 0)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), RADIUS)

def generate_random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

def ball_collision(ball_a, ball_b):
    delta = ball_b.pos - ball_a.pos
    dist = delta.length()
    if dist < RADIUS * 2 and dist != 0:
        overlap = (RADIUS * 2 - dist) / 2
        normal = delta.normalize()
        ball_a.pos -= normal * overlap
        ball_b.pos += normal * overlap
        rel_vel = ball_b.vel - ball_a.vel
        vel_along_normal = rel_vel.dot(normal)
        if vel_along_normal > 0:
            return
        impulse = normal * vel_along_normal * -IMPULSE
        ball_a.vel -= impulse
        ball_b.vel += impulse
def border_collision():
    pass

def init():
    running = True
    cue_ball = Ball(50, SCREEN_HEIGHT / 2, CUE_COLOR)
    rack = [cue_ball]
    pockets = []
    rows = 5
    force = 0
    cue_angle = 0
    cuestick_moving = False
    fired = False

    padding_x = RADIUS * 2
    padding_y = RADIUS * math.sqrt(3)
    start_x, start_y = (SCREEN_WIDTH // 2) + 10, SCREEN_HEIGHT // 2

    for row in range(rows):
        for i in range(row + 1):
            x = start_x + (row * padding_x)
            y = start_y + ((i - row / 2) * padding_y)
            rack.append(Ball(x, y, generate_random_color()))

    while running:
        screen.fill(WHITE)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if not cuestick_moving:
                    cuestick_moving = True
                    force = min(force + 3, MAX_FORCE)
            if e.type == pygame.MOUSEBUTTONUP:
                    cuestick_moving = False
                    cue_ball.vel = pygame.Vector2(math.cos(cue_angle), math.sin(cue_angle)) * force

        if not fired:
            mx, my = pygame.mouse.get_pos()
            dy, dx = cue_ball.pos.y - my, cue_ball.pos.x - mx
            pygame.draw.line(screen, CUE_COLOR, (cue_ball.pos.x, cue_ball.pos.y), (mx, my), 8)
            cue_angle = math.atan2(dy, dx)
        for i in pockets:
            i.draw()
        for i, ball in enumerate(rack):
            ball.move()
            for j in range(i + 1, len(rack)):
                ball_collision(ball, rack[j])
            ball.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    init()
