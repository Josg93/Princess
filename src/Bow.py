"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class Bow and Arrow.
"""

from typing import Any
from gale.factory import Factory
from src.GameObject import GameObject
from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.Projectile import Projectile


class Arrow(GameObject):
    """
    Arrow game object instantiated by the Bow factory.
    """
    def __init__(self, x: float, y: float, direction: str = "down") -> None:
        super().__init__(GAME_OBJECT_DEFS["arrow"], x, y)
        self.state = direction


class Bow:
    """
    Bow weapon class responsible for managing arrow creation using Gale's Factory pattern
    and firing projectiles into the room.
    """
    def __init__(self) -> None:
        # Initialize Gale factory for Arrow objects
        self.arrow_factory = Factory(Arrow)

    def fire(self, player: Any, room: Any) -> None:
        """
        Calculates spawn position based on player's direction, creates an arrow
        using the factory, wraps it in a Projectile, and adds it to the room's projectiles.
        """
        x = player.x
        y = player.y

        # Adjust arrow spawn offset depending on player facing direction
        if player.direction == "right":
            x += player.width
            y += player.height / 2 - 8
        elif player.direction == "left":
            x -= 16
            y += player.height / 2 - 8
        elif player.direction == "up":
            y -= 16
            x += player.width / 2 - 8
        elif player.direction == "down":
            y += player.height
            x += player.width / 2 - 8

        # Create arrow using factory, passing player direction to set its state/sprite frame
        arrow_obj = self.arrow_factory.create(x - 8  , y - 8, {"direction": player.direction})
        # Wrap in Projectile and add to room
        projectile = Projectile(arrow_obj, player.direction)
        room.projectiles.append(projectile)
