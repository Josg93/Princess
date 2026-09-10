"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Projectile.
"""

from typing import Any, Optional

import pygame

import settings

_SPEED = 150
_MAX_TILES = 4


class Projectile:
    def __init__(
        self,
        obj: Any,
        direction: str,
        speed: float = _SPEED,
        vx: float = 0.0,
        vy: float = 0.0,
        max_tiles: Optional[float] = _MAX_TILES,
    ) -> None:
        self.obj = obj
        self.direction = direction
        self.speed = speed
        self.vx = vx
        self.vy = vy
        self.max_tiles = max_tiles
        self.distance = 0.0
        self.dead = False

    def get_collision_rect(self) -> pygame.Rect:
        return self.obj.get_collision_rect()

    def update(self, dt: float) -> None:
        if self.dead:
            return

        d = self.speed * dt

        if self.vx != 0.0 or self.vy != 0.0:
            self.obj.x += self.vx * d
            self.obj.y += self.vy * d

            top_limit = settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE - self.obj.height / 2
            bottom_edge = (
                settings.MAP_HEIGHT * settings.TILE_SIZE
                + settings.MAP_RENDER_OFFSET_Y
                - settings.TILE_SIZE
            )
            left_limit = settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE
            right_limit = settings.VIRTUAL_WIDTH - settings.TILE_SIZE * 2

            if (
                self.obj.y <= top_limit
                or self.obj.y + self.obj.height >= bottom_edge
                or self.obj.x <= left_limit
                or self.obj.x + self.obj.width >= right_limit
            ):
                self.dead = True
        else:
            if self.direction == "up":
                self.obj.y -= d
                limit = settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE - self.obj.height / 2
                if self.obj.y <= limit:
                    self.obj.y = limit
                    self.dead = True
            elif self.direction == "down":
                self.obj.y += d
                bottom_edge = (
                    settings.MAP_HEIGHT * settings.TILE_SIZE
                    + settings.MAP_RENDER_OFFSET_Y
                    - settings.TILE_SIZE
                )
                if self.obj.y + self.obj.height >= bottom_edge:
                    self.obj.y = bottom_edge - self.obj.height
                    self.dead = True
            elif self.direction == "left":
                self.obj.x -= d
                limit = settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE
                if self.obj.x <= limit:
                    self.obj.x = limit
                    self.dead = True
            elif self.direction == "right":
                self.obj.x += d
                limit = settings.VIRTUAL_WIDTH - settings.TILE_SIZE * 2
                if self.obj.x + self.obj.width >= limit:
                    self.obj.x = limit - self.obj.width
                    self.dead = True

        if self.dead:
            settings.SOUNDS["pot-wall"].play()
            return

        self.distance += d

        if self.max_tiles is not None and self.distance > self.max_tiles * settings.TILE_SIZE:
            self.dead = True

    def render(
        self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0
    ) -> None:
        self.obj.render(surface, offset_x, offset_y)

    def collides(self, target: Any) -> bool:
        return self.get_collision_rect().colliderect(target.get_collision_rect())
