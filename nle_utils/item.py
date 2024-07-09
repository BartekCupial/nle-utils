from enum import Enum

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
