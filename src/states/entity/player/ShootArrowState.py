"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

This file contains the class ShootArrowState.
"""

from typing import TypeVar

import pygame

from gale.input_handler import InputData
from gale.state import StateMachine

import settings
from src.states.entity.BaseEntityState import BaseEntityState


class ShootArrowState(BaseEntityState):
    """
    State for when the player shoots an arrow using the bow.
    """
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon
        self.fired = False

        # Render offset for spaced character sprite.
        self.entity.offset_y = 5
        self.entity.offset_x = 8

        direction = self.entity.direction
        # Use shoot animation matching the direction
        self.entity.change_animation(f"shoot-{direction}")

    def enter(self) -> None:
        self.fired = False
        # Restart animation.
        self.entity.current_animation.reset()

        # Fire arrow using player's bow if owned and not already fired in this action.
        if self.entity.has_bow and self.entity.bow and not self.fired:
            self.entity.bow.fire(self.entity, self.dungeon.current_room)
            self.fired = True

    def update(self, dt: float) -> None:
        # Return to idle state once the shooting animation finishes.
        if self.entity.current_animation.times_played > 0:
            self.entity.current_animation.times_played = 0
            self.entity.change_state("idle")

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "sword" and input_data.pressed:
            self.entity.change_state("swing-sword")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
