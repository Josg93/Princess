"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for game objects.
"""

from typing import Any, Dict

import settings


def _pickup_heart(player, obj) -> None:
    player.heal(2)
    settings.SOUNDS["heart-taken"].play()


GAME_OBJECT_DEFS: Dict[str, Dict[str, Any]] = {
    "switch": {
        "type": "switch",
        "texture": "switches",
        "frame": 2,
        "width": 16,
        "height": 16,
        "solid": False,
        "default_state": "unpressed",
        "states": {
            "unpressed": {"frame": 2},
            "pressed": {"frame": 1},
        },
    },
    "pot": {
        "type": "pot",
        "texture": "tiles",
        "frame": 16,
        "width": 16,
        "height": 16,
        "solid": True,
        "consumable": False,
        "default_state": "default",
        "takeable": True,
        "states": {
            "default": {"frame": 16},
        },
    },
    # Definition of heart as a consumable object type.
    "heart": {
        "type": "heart",
        "texture": "hearts",
        "frame": 5,
        "width": 16,
        "height": 16,
        "solid": False,
        "consumable": True,
        "default_state": "default",
        "states": {
            "default": {"frame": 5},
        },
        "on_consume": _pickup_heart,
    },
    "chest": {
        "type": "chest",
        "texture": "tiles",
        "frames": [36, 37],
        "width": 32,
        "height": 16,
        "solid": True,
        "consumable": False,
        "default_state": "default",
        "takeable": False,
        "states": {
            "default": {"frames": [36, 37]},
            "open": {"frames": [55, 56]},
        },
    },
    "arrow": {
        "type": "arrow",
        "texture": "arrows",
        "frame": 1,
        "width": 32,
        "height": 32,
        "solid": False,
        "consumable": True,
        "default_state": "down",
        "states": {
            "down": {"frame": 1},
            "right": {"frame": 2},
            "up": {"frame": 3},
            "left": {"frame": 4},
        },
        "on_consume": _pickup_heart,
    },
    "fireball": {
        "type": "fireball",
        "texture": "fireball",
        "frame": 1,
        "width": 32,
        "height": 32,
        "solid": False,
        "consumable": False,
        "default_state": "down",
        "states": {
            "down": {"frame": 1},
        },
    },
}
