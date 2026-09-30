"""
GameEngine: owns the player and all coins.

Starter version: one coin type, no obstacles, no timer yet. Coin
collection also has a known bug (see how `update` uses check_collection
below) that Task 1 asks you to fix - collected coins are never removed,
so standing on one keeps awarding points every frame.
"""
ROUND_DURATION = 30
NUM_LIVES = 3
import random
import pygame
from game.obstacle import Obstacle

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
COIN_TYPES = [
    (1, (205, 127, 50)),   # Bronze
    (3, (192, 192, 192)),  # Silver
    (5, (255, 215, 0)),    # Gold
]


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [
            self._random_coin(COIN_TYPES[i % len(COIN_TYPES)])
            for i in range(NUM_COINS)
            ]
        self.obstacles=[
            Obstacle(100, 100, 120, 25),
            Obstacle(400, 150, 25, 120),
            Obstacle(250, 350, 150, 25),
        ]
        self.lives=NUM_LIVES
        self.score = 0
        self.round_active = True
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = ROUND_DURATION

    def _random_coin(self, coin_type):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        value, color=coin_type
        return Coin(x=x, y=y, radius=12, value=value,color=color)

    def handle_input(self, keys_pressed):
        if not self.round_active:
            return
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        if not self.round_active:
            return
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        self.time_remaining = max(0, ROUND_DURATION - elapsed)

        if self.time_remaining == 0 or self.lives == 0:
            self.round_active = False
            return

        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
            self.coins.remove(coin)

        for obstacle in self.obstacles:
            if self.player.get_rect().colliderect(obstacle.rect):
                self.lives=max(0,self.lives-1)
                self.player.x = WIDTH / 2
                self.player.y = HEIGHT / 2
                break
        if self.lives==0:
            self.round_active=False

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles)
        renderer.draw_text(surface, font, f"Score: {self.score}   Lives:{self.lives} Time:{self.time_remaining}", (10, 10))
        if not self.round_active:
            renderer.draw_banner(surface,font,f"Round Over! Final Score: {self.score}-Press R to restart")

    def reset_round(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [
            self._random_coin(COIN_TYPES[i % len(COIN_TYPES)])
            for i in range(NUM_COINS)
    ]
        self.lives = NUM_LIVES
        self.score = 0
        self.time_remaining = ROUND_DURATION
        self.start_time = pygame.time.get_ticks()
        self.round_active = True