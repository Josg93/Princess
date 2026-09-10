"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class Boss.
"""

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
        )
        self.max_health = 6
        self.health = 6
        self.attack_cooldown = 2.0  # Segundos entre cada disparo
        self.attack_timer = 0.0
        # Guardamos la posición última conocida del jugador (al entrar a la sala)
        self.player_spawn_pos: Tuple[float, float] = (player.x, player.y)

        # Factory de Gale para crear fireballs automáticamente
        self.fireball_factory = Factory(GameObject)

    def update(self, dt: float, room: Any) -> None:
        self.attack_timer -= dt

        if self.attack_timer <= 0:
            # Calculamos la dirección hacia la posición guardada del jugador
            dx = self.player_spawn_pos[0] - self.x
            dy = self.player_spawn_pos[1] - self.y

            
            if abs(dx) > abs(dy):
                fireball_dir = "right" if dx > 0 else "left"
            else:
                fireball_dir = "down" if dy > 0 else "up"

            # Creamos la fireball usando el Factory de Gale
            fireball_obj = self.fireball_factory.create(GAME_OBJECT_DEFS["fireball"], self.x, self.y)
            # Instanciamos el Projectile con la dirección calculada y velocidad lenta (50)
            fireball = Projectile(fireball_obj, fireball_dir, speed=50)
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