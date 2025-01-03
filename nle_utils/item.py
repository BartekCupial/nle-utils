from __future__ import annotations

import re
from enum import Enum
from typing import Optional

from nle import nethack


class ItemBeatitude(Enum):
    # beatitude
    UNKNOWN = 0
    CURSED = 1
    UNCURSED = 2
    BLESSED = 3

    @staticmethod
    def from_name(full_name: str) -> ItemBeatitude:
        """
        Determine beatitude from item name

        Args:
            full_name (str): The full name of the item

        Returns:
            ItemBeatitude: The corresponding beatitude enum value
        """
        if "blessed" in full_name.lower():
            return ItemBeatitude.BLESSED
        elif "uncursed" in full_name.lower():
            return ItemBeatitude.UNCURSED
        elif "cursed" in full_name.lower():
            return ItemBeatitude.CURSED
        else:
            return ItemBeatitude.UNKNOWN


class ItemClasses(Enum):
    RANDOM = nethack.RANDOM_CLASS  # used for generating random objects
    COINS = nethack.COIN_CLASS
    AMULETS = nethack.AMULET_CLASS
    WEAPONS = nethack.WEAPON_CLASS
    ARMOR = nethack.ARMOR_CLASS
    COMPESTIBLES = nethack.FOOD_CLASS
    SCROLLS = nethack.SCROLL_CLASS
    SPELLBOOKS = nethack.SPBOOK_CLASS
    POTIONS = nethack.POTION_CLASS
    RINGS = nethack.RING_CLASS
    WANDS = nethack.WAND_CLASS
    TOOLS = nethack.TOOL_CLASS
    GEMS = nethack.GEM_CLASS
    ROCKS = nethack.ROCK_CLASS
    BALL = nethack.BALL_CLASS
    CHAIN = nethack.CHAIN_CLASS
    VENOM = nethack.VENOM_CLASS
    MAXOCLASSES = nethack.MAXOCLASSES

    @staticmethod
    def from_oclass(oclass: int) -> ItemClasses:
        """
        Determine item class from object
        """
        return ItemClasses(oclass)


class ItemShopStatus(Enum):
    NOT_SHOP = 0
    FOR_SALE = 1
    UNPAID = 2


class ItemEnchantment:
    class EnchantmentState(Enum):
        UNKNOWN = "UNKNOWN"

    def __init__(self, value: Optional[int] = None):
        self._value = value

    @property
    def value(self) -> Optional[int]:
        """Get the enchantment value."""
        return self._value

    @value.setter
    def value(self, new_value: Optional[int]) -> None:
        """Set the enchantment value."""
        if new_value is not None and not isinstance(new_value, int):
            raise ValueError("Enchantment value must be an integer or None")
        self._value = new_value

    @property
    def is_unknown(self) -> bool:
        """Check if the enchantment state is unknown."""
        return self._value is None

    def __str__(self) -> str:
        return str(self.EnchantmentState.UNKNOWN.value if self.is_unknown else self._value)

    def __repr__(self) -> str:
        return f"ItemEnchantment({self._value})"

    def __eq__(self, other) -> bool:
        if isinstance(other, ItemEnchantment):
            return self._value == other._value
        return False

    @staticmethod
    def from_name(full_name):
        if "+" in full_name:
            ench = int(full_name.split("+")[1].split(" ")[0])
        elif "-" in full_name:
            ench = int(full_name.split("-")[1].split(" ")[0])
        else:
            ench = None
        return ItemEnchantment(ench)


class ItemErosion(Enum):
    NONE = 0  # No erosion
    BASIC = 1  # Basic damage (no prefix)
    HEAVY = 2  # Heavy damage (prefix: 'very')
    SEVERE = 3  # Severe damage (prefix: 'thoroughly')

    @staticmethod
    def from_name(full_name):
        # rusty, very rusty, thoroughly rusty
        # corroded, very corroded, thoroughly corroded
        # burnt, very burnt, thoroughly burnt
        # rotten, very rotten, thoroughly rotten
        damage_pattern = re.compile(r"(?:(very|thoroughly)\s+)?(rusty|burnt|corroded|rotted)(?:\s+|$)")

        # Find all matches in the text
        matches = damage_pattern.finditer(full_name)

        intensity_map = {None: 1, "very": 2, "thoroughly": 3}  # Basic damage  # Heavy damage  # Severe damage

        damages = []
        for match in matches:
            intensity_word, damage_type = match.groups()
            damages.append(intensity_map[intensity_word])
        erosion = max(damages) if damages else 0

        return ItemErosion(erosion)
