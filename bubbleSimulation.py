import pygame
import random
import math

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("비눗방울 시뮬레이션")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 비눗방울 클래스
class Bubble:
    def __init__(self):
        self.radius = random.randint(40, 55)
        self.x = random.randint(self.radius * 2, WIDTH - self.radius * 2)  # 최소 두 배 반지름만큼 떨어지도록 수정
        self.y = random.randint(self.radius * 2, HEIGHT - self.radius * 2)  # 최소 두 배 반지름만큼 떨어지도록 수정
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 1.7)  # 비눗방울의 속도를 무작위로 설정
        self.dx = speed * math.cos(angle)
        self.dy = speed * math.sin(angle)
        self.color = (
            random.randint(60, 255),  # R: 50~200 범위
            random.randint(60, 255),  # G: 50~200 범위
            random.randint(60, 255)   # B: 50~200 범위
        )
        self.pop_chance = random.random() < 0.6  # 60% 확률로 터질 수 있도록 설정

    def move(self):
        """비눗방울을 움직임"""
        self.x += self.dx
        self.y += self.dy

        # 벽과의 충돌 체크
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.dx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.dy *= -1

    def draw(self, screen):
        """비눗방울을 화면에 그림"""
        bubble_surface = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        
        for r in range(self.radius):
            if r < self.radius * 0.4:
                # 반지름의 20% 부분에서 그라데이션 적용
                alpha = int(255 * math.exp(-r / (self.radius * 0.15)))

            elif r < self.radius:
                # 20% 이상부터는 알파값 0
                alpha = 0
            else:
                # 반지름 바깥 영역에서는 알파값 0
                alpha = 0
            
            # 색상 적용: 알파값을 적용해서 그라데이션을 그림
            color = (self.color[0], self.color[1], self.color[2], alpha)
            pygame.draw.circle(bubble_surface, color, (self.radius, self.radius), self.radius - r)

        screen.blit(bubble_surface, (int(self.x) - self.radius, int(self.y) - self.radius))









    def check_collision(self, other):
        """다른 비눗방울과의 충돌을 체크하고, 터지거나 반발함"""
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        if distance < self.radius + other.radius:
            if self.pop_chance and other.pop_chance:
                return True
            else:
                self.resolve_overlap(other)
        return False

    def resolve_overlap(self, other):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        if distance == 0:
            return  # 두 비눗방울의 위치가 동일한 경우 무한루프 방지
        overlap = self.radius + other.radius - distance
        nx = (other.x - self.x) / distance
        ny = (other.y - self.y) / distance
        self.x -= nx * overlap / 2
        self.y -= ny * overlap / 2
        other.x += nx * overlap / 2
        other.y += ny * overlap / 2

        # 속도를 서로 반발시키기
        self.dx, self.dy = self.reflect_velocity(self.dx, self.dy, nx, ny)
        other.dx, other.dy = other.reflect_velocity(other.dx, other.dy, -nx, -ny)

    def reflect_velocity(self, vx, vy, nx, ny):
        dot_product = vx * nx + vy * ny
        vx -= 2 * dot_product * nx
        vy -= 2 * dot_product * ny
        return vx, vy

import random
import pygame

# 파티클 클래스
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 6)
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)
        self.life = random.randint(30, 60)  # 파티클의 수명 (프레임 단위)
        self.color = color
        self.gravity = 0.1  # 중력 가속도
        self.friction = 0.99  # 마찰 계수 (0.99는 1%의 마찰을 의미, 값이 작을수록 마찰이 강해짐)
        
    def move(self):
        self.dy += self.gravity  # 중력 적용
        self.dx *= self.friction  # 마찰력 적용 (수평 속도 감소)
        self.dy *= self.friction  # 마찰력 적용 (수직 속도 감소)
        
        self.x += self.dx
        self.y += self.dy
        self.life -= 1
        if self.life > 0:
            self.radius *= 0.95  # 파티클이 작아지면서 사라짐

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), max(1, int(self.radius)))


# 비눗방울 여러 개 생성
num_bubbles = 15  # 비눗방울 개수
bubbles = [Bubble() for _ in range(num_bubbles)]
particles = []  # 파티클들을 저장할 리스트

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # FPS = 60
    screen.fill(BLACK)  # 배경색 설정
            
    # 비눗방울 이동 및 그리기
    for bubble in bubbles:
        bubble.move()
        bubble.draw(screen)
    
    # 파티클 이동 및 그리기
    for particle in particles[:]:
        particle.move()
        particle.draw(screen)
        if particle.life <= 0:  # 파티클이 소멸하면 제거
            particles.remove(particle)
    
    # 비눗방울 간 충돌 체크
    popped_indices = set()  # pop될 비눗방울 인덱스를 기록
    for i in range(len(bubbles) - 1, -1, -1):  # 인덱스를 뒤에서부터 접근
        if i in popped_indices:  # 이미 터진 비눗방울이면 스킵
            continue
        for j in range(i - 1, -1, -1):
            if j in popped_indices:  # 이미 터진 비눗방울이면 스킵
                continue
            if bubbles[i].check_collision(bubbles[j]):
                # 파티클 효과 생성
                x = (bubbles[i].x + bubbles[j].x) / 2
                y = (bubbles[i].y + bubbles[j].y) / 2
                color1 = bubbles[i].color
                color2 = bubbles[j].color

                # 두 색상을 파티클에 적용
                for _ in range(20):  # 20개의 파티클 생성
                    particles.append(Particle(x, y, random.choice([color1, color2])))

                # 터진 비눗방울의 인덱스를 기록
                popped_indices.add(i)
                popped_indices.add(j)
                break  # 내부 루프 탈출, 이미 비눗방울이 제거됨

    # 터진 비눗방울을 제거
    for idx in sorted(popped_indices, reverse=True):
        if idx < len(bubbles):
            bubbles.pop(idx)
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
