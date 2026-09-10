"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class Boss.
"""

import math
from typing import Any, Dict, Optional, Tuple

import pygame

from gale.factory import Factory
from gale.input_handler import InputData
from gale.state import StateMachine

import settings
from src.Entity import Entity
from src.GameObject import GameObject
from src.definitions.entity import ENTITY_DEFS
from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.Projectile import Projectile
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState


class Fireball(GameObject):
    """
    Fireball game object instantiated by the Boss factory.
    """
    def __init__(self, x: float, y: float, direction: str = "down") -> None:
        super().__init__(GAME_OBJECT_DEFS["fireball"], x, y)
        self.state = direction


class Boss(Entity):
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        animation_defs: Dict[str, Dict[str, Any]],
        states: Dict[str, Any],
        player: Entity,
        default_texture: str = "boss",
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            walk_speed=25,
            health=6,
            animation_defs=animation_defs,
            states=states,
            default_texture=default_texture,
        )
        self.max_health = 6
        self.health = 6
        self.attack_cooldown = 2.0  # Segundos entre cada disparo
        self.attack_timer = 0.0
        self.player = player

        self.vulnerable = False
        self.vulnerable_timer = 0.0
        self.vulnerable_duration = 5.0

        self.state_machine.states = {
            "walk": lambda sm, e=self: EntityWalkState(e, sm),
            "idle": lambda sm, e=self: EntityIdleState(e, sm),
        }
        self.change_state("walk")

        # Factory de Gale para crear fireballs automáticamente
        self.fireball_factory = Factory(Fireball)

    def update(self, dt: float) -> None:
        super().update(dt)

        if self.vulnerable:
            self.vulnerable_timer += dt
            if self.vulnerable_timer > self.vulnerable_duration:
                self.vulnerable = False
                self.vulnerable_timer = 0.0

    def process_ai(self, room: Any, dt: float) -> None:
        super().process_ai(room, dt)
        self.attack_timer -= dt

        if self.attack_timer <= 0:
            # Calculamos la dirección real hacia la posición actual del jugador
            dx = self.player.x - self.x
            dy = self.player.y - self.y

            length = math.hypot(dx, dy)
            if length == 0:
                vx, vy = 1.0, 0.0
            else:
                vx, vy = dx / length, dy / length

            if abs(dx) > abs(dy):
                fireball_dir = "right" if dx > 0 else "left"
            else:
                fireball_dir = "down" if dy > 0 else "up"

            # Creamos la fireball usando el Factory de Gale
            fireball_obj = self.fireball_factory.create(self.x, self.y, {"direction": fireball_dir})
            # Instanciamos el Projectile con vectores y sin límite de distancia (max_tiles=None)
            fireball = Projectile(fireball_obj, fireball_dir, speed=60, vx=vx, vy=vy, max_tiles=None)
            # Añadimos la fireball a la habitación
            room.projectiles.append(fireball)

            # Reiniciamos el timer
            self.attack_timer = self.attack_cooldown

    def take_damage(self, amount: int) -> None:
        """
        Recibe daño. Reduce la salud. Si llega a 0, marca al boss como muerto.
        """
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.dead = True