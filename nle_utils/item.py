from enum import Enum
from typing import Optional

from nle import nethack


class ItemBeatitude(Enum):
    # beatitude
    UNKNOWN = 0
    CURSED = 1
    UNCURSED = 2
    BLESSED = 3


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
