from __future__ import annotations

import re
from enum import Enum
from typing import Optional

from nle import nethack


class ArmorType(Enum):
    SUIT = 0
    SHIELD = 1  # needed for special wear function
    HELM = 2
    GLOVES = 3
    BOOTS = 4
    CLOAK = 5
    SHIRT = 6


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
    AMULET = nethack.AMULET_CLASS
    WEAPON = nethack.WEAPON_CLASS
    ARMOR = nethack.ARMOR_CLASS
    COMPESTIBLES = nethack.FOOD_CLASS
    SCROLL = nethack.SCROLL_CLASS
    SPELLBOOK = nethack.SPBOOK_CLASS
    POTION = nethack.POTION_CLASS
    RING = nethack.RING_CLASS
    WAND = nethack.WAND_CLASS
    TOOL = nethack.TOOL_CLASS
    GEM = nethack.GEM_CLASS
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
        # Look for a plus or minus followed by one or more digits
        match = re.search(r"[+\-]\d+", full_name)
        if match:
            # match.group(0) returns the entire matched string, e.g. "+3" or "-2"
            ench = int(match.group(0))
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
