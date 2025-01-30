import enum

import numpy as np

from nle_utils.role import Role


class P_SKILLS(enum.Enum):
    # Code to denote that no skill is applicable
    P_NONE = 0

    # Weapon Skills -- Stephen White
    # Order matters and are used in macros.
    # Positive values denote hand-to-hand weapons or launchers.
    # Negative values denote ammunition or missiles.
    # Update weapon.c if you amend any skills.
    # Also used for oc_subtyp.
    P_DAGGER = 1
    P_KNIFE = 2
    P_AXE = 3
    P_PICK_AXE = 4
    P_SHORT_SWORD = 5
    P_BROAD_SWORD = 6
    P_LONG_SWORD = 7
    P_TWO_HANDED_SWORD = 8
    P_SCIMITAR = 9
    P_SABER = 10
    P_CLUB = 11  # Heavy-shafted bludgeon
    P_MACE = 12
    P_MORNING_STAR = 13  # Spiked bludgeon
    P_FLAIL = 14  # Two pieces hinged or chained together
    P_HAMMER = 15  # Heavy head on the end
    P_QUARTERSTAFF = 16  # Long-shafted bludgeon
    P_POLEARMS = 17  # attack two or three steps away
    P_SPEAR = 18  # includes javelin
    P_TRIDENT = 19
    P_LANCE = 20
    P_BOW = 21  # launchers
    P_SLING = 22
    P_CROSSBOW = 23
    P_DART = 24  # hand-thrown missiles
    P_SHURIKEN = 25
    P_BOOMERANG = 26
    P_WHIP = 27  # flexible, one-handed
    P_UNICORN_HORN = 28  # last weapon, two-handed

    # Spell Skills added by Larry Stewart-Zerba
    P_ATTACK_SPELL = 29
    P_HEALING_SPELL = 30
    P_DIVINATION_SPELL = 31
    P_ENCHANTMENT_SPELL = 32
    P_CLERIC_SPELL = 33
    P_ESCAPE_SPELL = 34
    P_MATTER_SPELL = 35

    # Other types of combat
    P_BARE_HANDED_COMBAT = 36  # actually weaponless; gloves are ok
    P_TWO_WEAPON_COMBAT = 37  # pair of weapons, one in each hand
    P_RIDING = 38  # How well you control your steed

    P_NUM_SKILLS = 39

    @property
    def P_FIRST_WEAPON(self):
        return P_SKILLS.P_DAGGER

    @property
    def P_LAST_WEAPON(self):
        return P_SKILLS.P_UNICORN_HORN

    @property
    def P_FIRST_SPELL(self):
        return P_SKILLS.P_ATTACK_SPELL

    @property
    def P_LAST_SPELL(self):
        return P_SKILLS.P_MATTER_SPELL

    @property
    def P_LAST_H_TO_H(self):
        return P_SKILLS.P_RIDING

    @property
    def P_FIRST_H_TO_H(self):
        return P_SKILLS.P_BARE_HANDED_COMBAT


Skill_A = [
    (P_SKILLS.P_DAGGER, "Basic"),
    (P_SKILLS.P_KNIFE, "Basic"),
    (P_SKILLS.P_PICK_AXE, "Expert"),
    (P_SKILLS.P_SHORT_SWORD, "Basic"),
    (P_SKILLS.P_SCIMITAR, "Skilled"),
    (P_SKILLS.P_SABER, "Expert"),
    (P_SKILLS.P_CLUB, "Skilled"),
    (P_SKILLS.P_QUARTERSTAFF, "Skilled"),
    (P_SKILLS.P_SLING, "Skilled"),
    (P_SKILLS.P_DART, "Basic"),
    (P_SKILLS.P_BOOMERANG, "Expert"),
    (P_SKILLS.P_WHIP, "Expert"),
    (P_SKILLS.P_UNICORN_HORN, "Skilled"),
    (P_SKILLS.P_ATTACK_SPELL, "Basic"),
    (P_SKILLS.P_HEALING_SPELL, "Basic"),
    (P_SKILLS.P_DIVINATION_SPELL, "Expert"),
    (P_SKILLS.P_MATTER_SPELL, "Basic"),
    (P_SKILLS.P_RIDING, "Basic"),
    (P_SKILLS.P_TWO_WEAPON_COMBAT, "Basic"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Expert"),
]

Skill_B = [
    (P_SKILLS.P_DAGGER, "Basic"),
    (P_SKILLS.P_AXE, "Expert"),
    (P_SKILLS.P_PICK_AXE, "Skilled"),
    (P_SKILLS.P_SHORT_SWORD, "Expert"),
    (P_SKILLS.P_BROAD_SWORD, "Skilled"),
    (P_SKILLS.P_LONG_SWORD, "Skilled"),
    (P_SKILLS.P_TWO_HANDED_SWORD, "Expert"),
    (P_SKILLS.P_SCIMITAR, "Skilled"),
    (P_SKILLS.P_SABER, "Basic"),
    (P_SKILLS.P_CLUB, "Skilled"),
    (P_SKILLS.P_MACE, "Skilled"),
    (P_SKILLS.P_MORNING_STAR, "Skilled"),
    (P_SKILLS.P_FLAIL, "Basic"),
    (P_SKILLS.P_HAMMER, "Expert"),
    (P_SKILLS.P_QUARTERSTAFF, "Basic"),
    (P_SKILLS.P_SPEAR, "Skilled"),
    (P_SKILLS.P_TRIDENT, "Skilled"),
    (P_SKILLS.P_BOW, "Basic"),
    (P_SKILLS.P_ATTACK_SPELL, "Basic"),
    (P_SKILLS.P_ESCAPE_SPELL, "Basic"),
    (P_SKILLS.P_RIDING, "Basic"),
    (P_SKILLS.P_TWO_WEAPON_COMBAT, "Basic"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Master"),
]

Skill_C = [
    (P_SKILLS.P_DAGGER, "Basic"),
    (P_SKILLS.P_KNIFE, "Skilled"),
    (P_SKILLS.P_AXE, "Skilled"),
    (P_SKILLS.P_PICK_AXE, "Basic"),
    (P_SKILLS.P_CLUB, "Expert"),
    (P_SKILLS.P_MACE, "Expert"),
    (P_SKILLS.P_MORNING_STAR, "Basic"),
    (P_SKILLS.P_FLAIL, "Skilled"),
    (P_SKILLS.P_HAMMER, "Skilled"),
    (P_SKILLS.P_QUARTERSTAFF, "Expert"),
    (P_SKILLS.P_POLEARMS, "Skilled"),
    (P_SKILLS.P_SPEAR, "Expert"),
    (P_SKILLS.P_TRIDENT, "Skilled"),
    (P_SKILLS.P_BOW, "Skilled"),
    (P_SKILLS.P_SLING, "Expert"),
    (P_SKILLS.P_ATTACK_SPELL, "Basic"),
    (P_SKILLS.P_MATTER_SPELL, "Skilled"),
    (P_SKILLS.P_BOOMERANG, "Expert"),
    (P_SKILLS.P_UNICORN_HORN, "Basic"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Master"),
]

Skill_H = [
    (P_SKILLS.P_DAGGER, "Skilled"),
    (P_SKILLS.P_KNIFE, "Expert"),
    (P_SKILLS.P_SHORT_SWORD, "Skilled"),
    (P_SKILLS.P_SCIMITAR, "Basic"),
    (P_SKILLS.P_SABER, "Basic"),
    (P_SKILLS.P_CLUB, "Skilled"),
    (P_SKILLS.P_MACE, "Basic"),
    (P_SKILLS.P_QUARTERSTAFF, "Expert"),
    (P_SKILLS.P_POLEARMS, "Basic"),
    (P_SKILLS.P_SPEAR, "Basic"),
    (P_SKILLS.P_TRIDENT, "Basic"),
    (P_SKILLS.P_SLING, "Skilled"),
    (P_SKILLS.P_DART, "Expert"),
    (P_SKILLS.P_SHURIKEN, "Skilled"),
    (P_SKILLS.P_UNICORN_HORN, "Expert"),
    (P_SKILLS.P_HEALING_SPELL, "Expert"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Basic"),
]

Skill_K = [
    (P_SKILLS.P_DAGGER, "Basic"),
    (P_SKILLS.P_KNIFE, "Basic"),
    (P_SKILLS.P_AXE, "Skilled"),
    (P_SKILLS.P_PICK_AXE, "Basic"),
    (P_SKILLS.P_SHORT_SWORD, "Skilled"),
    (P_SKILLS.P_BROAD_SWORD, "Skilled"),
    (P_SKILLS.P_LONG_SWORD, "Expert"),
    (P_SKILLS.P_TWO_HANDED_SWORD, "Skilled"),
    (P_SKILLS.P_SCIMITAR, "Basic"),
    (P_SKILLS.P_SABER, "Skilled"),
    (P_SKILLS.P_CLUB, "Basic"),
    (P_SKILLS.P_MACE, "Skilled"),
    (P_SKILLS.P_MORNING_STAR, "Skilled"),
    (P_SKILLS.P_FLAIL, "Basic"),
    (P_SKILLS.P_HAMMER, "Basic"),
    (P_SKILLS.P_POLEARMS, "Skilled"),
    (P_SKILLS.P_SPEAR, "Skilled"),
    (P_SKILLS.P_TRIDENT, "Basic"),
    (P_SKILLS.P_LANCE, "Expert"),
    (P_SKILLS.P_BOW, "Basic"),
    (P_SKILLS.P_CROSSBOW, "Skilled"),
    (P_SKILLS.P_ATTACK_SPELL, "Skilled"),
    (P_SKILLS.P_HEALING_SPELL, "Skilled"),
    (P_SKILLS.P_CLERIC_SPELL, "Skilled"),
    (P_SKILLS.P_RIDING, "Expert"),
    (P_SKILLS.P_TWO_WEAPON_COMBAT, "Skilled"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Expert"),
]

Skill_Mon = [
    (P_SKILLS.P_QUARTERSTAFF, "Basic"),
    (P_SKILLS.P_SPEAR, "Basic"),
    (P_SKILLS.P_CROSSBOW, "Basic"),
    (P_SKILLS.P_SHURIKEN, "Basic"),
    (P_SKILLS.P_ATTACK_SPELL, "Basic"),
    (P_SKILLS.P_HEALING_SPELL, "Expert"),
    (P_SKILLS.P_DIVINATION_SPELL, "Basic"),
    (P_SKILLS.P_ENCHANTMENT_SPELL, "Basic"),
    (P_SKILLS.P_CLERIC_SPELL, "Skilled"),
    (P_SKILLS.P_ESCAPE_SPELL, "Skilled"),
    (P_SKILLS.P_MATTER_SPELL, "Basic"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Grand Master"),
]

Skill_P = [
    (P_SKILLS.P_CLUB, "Expert"),
    (P_SKILLS.P_MACE, "Expert"),
    (P_SKILLS.P_MORNING_STAR, "Expert"),
    (P_SKILLS.P_FLAIL, "Expert"),
    (P_SKILLS.P_HAMMER, "Expert"),
    (P_SKILLS.P_QUARTERSTAFF, "Expert"),
    (P_SKILLS.P_POLEARMS, "Skilled"),
    (P_SKILLS.P_SPEAR, "Skilled"),
    (P_SKILLS.P_TRIDENT, "Skilled"),
    (P_SKILLS.P_LANCE, "Basic"),
    (P_SKILLS.P_BOW, "Basic"),
    (P_SKILLS.P_SLING, "Basic"),
    (P_SKILLS.P_CROSSBOW, "Basic"),
    (P_SKILLS.P_DART, "Basic"),
    (P_SKILLS.P_SHURIKEN, "Basic"),
    (P_SKILLS.P_BOOMERANG, "Basic"),
    (P_SKILLS.P_UNICORN_HORN, "Skilled"),
    (P_SKILLS.P_HEALING_SPELL, "Expert"),
    (P_SKILLS.P_DIVINATION_SPELL, "Expert"),
    (P_SKILLS.P_CLERIC_SPELL, "Expert"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Basic"),
]

Skill_R = [
    (P_SKILLS.P_DAGGER, "Expert"),
    (P_SKILLS.P_KNIFE, "Expert"),
    (P_SKILLS.P_SHORT_SWORD, "Expert"),
    (P_SKILLS.P_BROAD_SWORD, "Skilled"),
    (P_SKILLS.P_LONG_SWORD, "Skilled"),
    (P_SKILLS.P_TWO_HANDED_SWORD, "Basic"),
    (P_SKILLS.P_SCIMITAR, "Skilled"),
    (P_SKILLS.P_SABER, "Skilled"),
    (P_SKILLS.P_CLUB, "Skilled"),
    (P_SKILLS.P_MACE, "Skilled"),
    (P_SKILLS.P_MORNING_STAR, "Basic"),
    (P_SKILLS.P_FLAIL, "Basic"),
    (P_SKILLS.P_HAMMER, "Basic"),
    (P_SKILLS.P_POLEARMS, "Basic"),
    (P_SKILLS.P_SPEAR, "Basic"),
    (P_SKILLS.P_CROSSBOW, "Expert"),
    (P_SKILLS.P_DART, "Expert"),
    (P_SKILLS.P_SHURIKEN, "Skilled"),
    (P_SKILLS.P_DIVINATION_SPELL, "Skilled"),
    (P_SKILLS.P_ESCAPE_SPELL, "Skilled"),
    (P_SKILLS.P_MATTER_SPELL, "Skilled"),
    (P_SKILLS.P_RIDING, "Basic"),
    (P_SKILLS.P_TWO_WEAPON_COMBAT, "Expert"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Expert"),
]

Skill_Ran = [
    (P_SKILLS.P_DAGGER, "Expert"),
    (P_SKILLS.P_KNIFE, "Skilled"),
    (P_SKILLS.P_AXE, "Skilled"),
    (P_SKILLS.P_PICK_AXE, "Basic"),
    (P_SKILLS.P_SHORT_SWORD, "Basic"),
    (P_SKILLS.P_MORNING_STAR, "Basic"),
    (P_SKILLS.P_FLAIL, "Skilled"),
    (P_SKILLS.P_HAMMER, "Basic"),
    (P_SKILLS.P_QUARTERSTAFF, "Basic"),
    (P_SKILLS.P_POLEARMS, "Skilled"),
    (P_SKILLS.P_SPEAR, "Expert"),
    (P_SKILLS.P_TRIDENT, "Basic"),
    (P_SKILLS.P_BOW, "Expert"),
    (P_SKILLS.P_SLING, "Expert"),
    (P_SKILLS.P_CROSSBOW, "Expert"),
    (P_SKILLS.P_DART, "Expert"),
    (P_SKILLS.P_SHURIKEN, "Skilled"),
    (P_SKILLS.P_BOOMERANG, "Expert"),
    (P_SKILLS.P_WHIP, "Basic"),
    (P_SKILLS.P_HEALING_SPELL, "Basic"),
    (P_SKILLS.P_DIVINATION_SPELL, "Expert"),
    (P_SKILLS.P_ESCAPE_SPELL, "Basic"),
    (P_SKILLS.P_RIDING, "Basic"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Basic"),
]

Skill_S = [
    (P_SKILLS.P_DAGGER, "Basic"),
    (P_SKILLS.P_KNIFE, "Skilled"),
    (P_SKILLS.P_SHORT_SWORD, "Expert"),
    (P_SKILLS.P_BROAD_SWORD, "Skilled"),
    (P_SKILLS.P_LONG_SWORD, "Expert"),
    (P_SKILLS.P_TWO_HANDED_SWORD, "Expert"),
    (P_SKILLS.P_SCIMITAR, "Basic"),
    (P_SKILLS.P_SABER, "Basic"),
    (P_SKILLS.P_FLAIL, "Skilled"),
    (P_SKILLS.P_QUARTERSTAFF, "Basic"),
    (P_SKILLS.P_POLEARMS, "Skilled"),
    (P_SKILLS.P_SPEAR, "Skilled"),
    (P_SKILLS.P_LANCE, "Skilled"),
    (P_SKILLS.P_BOW, "Expert"),
    (P_SKILLS.P_SHURIKEN, "Expert"),
    (P_SKILLS.P_ATTACK_SPELL, "Basic"),
    (P_SKILLS.P_DIVINATION_SPELL, "Basic"),
    (P_SKILLS.P_CLERIC_SPELL, "Skilled"),
    (P_SKILLS.P_RIDING, "Skilled"),
    (P_SKILLS.P_TWO_WEAPON_COMBAT, "Expert"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Master"),
]

Skill_T = [
    (P_SKILLS.P_DAGGER, "Expert"),
    (P_SKILLS.P_KNIFE, "Skilled"),
    (P_SKILLS.P_AXE, "Basic"),
    (P_SKILLS.P_PICK_AXE, "Basic"),
    (P_SKILLS.P_SHORT_SWORD, "Expert"),
    (P_SKILLS.P_BROAD_SWORD, "Basic"),
    (P_SKILLS.P_LONG_SWORD, "Basic"),
    (P_SKILLS.P_TWO_HANDED_SWORD, "Basic"),
    (P_SKILLS.P_SCIMITAR, "Skilled"),
    (P_SKILLS.P_SABER, "Skilled"),
    (P_SKILLS.P_MACE, "Basic"),
    (P_SKILLS.P_MORNING_STAR, "Basic"),
    (P_SKILLS.P_FLAIL, "Basic"),
    (P_SKILLS.P_HAMMER, "Basic"),
    (P_SKILLS.P_QUARTERSTAFF, "Basic"),
    (P_SKILLS.P_POLEARMS, "Basic"),
    (P_SKILLS.P_SPEAR, "Basic"),
    (P_SKILLS.P_TRIDENT, "Basic"),
    (P_SKILLS.P_LANCE, "Basic"),
    (P_SKILLS.P_BOW, "Basic"),
    (P_SKILLS.P_SLING, "Basic"),
    (P_SKILLS.P_CROSSBOW, "Basic"),
    (P_SKILLS.P_DART, "Expert"),
    (P_SKILLS.P_SHURIKEN, "Basic"),
    (P_SKILLS.P_BOOMERANG, "Basic"),
    (P_SKILLS.P_WHIP, "Basic"),
    (P_SKILLS.P_UNICORN_HORN, "Skilled"),
    (P_SKILLS.P_DIVINATION_SPELL, "Basic"),
    (P_SKILLS.P_ENCHANTMENT_SPELL, "Basic"),
    (P_SKILLS.P_ESCAPE_SPELL, "Skilled"),
    (P_SKILLS.P_RIDING, "Basic"),
    (P_SKILLS.P_TWO_WEAPON_COMBAT, "Skilled"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Skilled"),
]

Skill_V = [
    (P_SKILLS.P_DAGGER, "Expert"),
    (P_SKILLS.P_AXE, "Expert"),
    (P_SKILLS.P_PICK_AXE, "Skilled"),
    (P_SKILLS.P_SHORT_SWORD, "Skilled"),
    (P_SKILLS.P_BROAD_SWORD, "Skilled"),
    (P_SKILLS.P_LONG_SWORD, "Expert"),
    (P_SKILLS.P_TWO_HANDED_SWORD, "Expert"),
    (P_SKILLS.P_SCIMITAR, "Basic"),
    (P_SKILLS.P_SABER, "Basic"),
    (P_SKILLS.P_HAMMER, "Expert"),
    (P_SKILLS.P_QUARTERSTAFF, "Basic"),
    (P_SKILLS.P_POLEARMS, "Skilled"),
    (P_SKILLS.P_SPEAR, "Skilled"),
    (P_SKILLS.P_TRIDENT, "Basic"),
    (P_SKILLS.P_LANCE, "Skilled"),
    (P_SKILLS.P_SLING, "Basic"),
    (P_SKILLS.P_ATTACK_SPELL, "Basic"),
    (P_SKILLS.P_ESCAPE_SPELL, "Basic"),
    (P_SKILLS.P_RIDING, "Skilled"),
    (P_SKILLS.P_TWO_WEAPON_COMBAT, "Skilled"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Expert"),
]

Skill_W = [
    (P_SKILLS.P_DAGGER, "Expert"),
    (P_SKILLS.P_KNIFE, "Skilled"),
    (P_SKILLS.P_AXE, "Skilled"),
    (P_SKILLS.P_SHORT_SWORD, "Basic"),
    (P_SKILLS.P_CLUB, "Skilled"),
    (P_SKILLS.P_MACE, "Basic"),
    (P_SKILLS.P_QUARTERSTAFF, "Expert"),
    (P_SKILLS.P_POLEARMS, "Skilled"),
    (P_SKILLS.P_SPEAR, "Basic"),
    (P_SKILLS.P_TRIDENT, "Basic"),
    (P_SKILLS.P_SLING, "Skilled"),
    (P_SKILLS.P_DART, "Expert"),
    (P_SKILLS.P_SHURIKEN, "Basic"),
    (P_SKILLS.P_ATTACK_SPELL, "Expert"),
    (P_SKILLS.P_HEALING_SPELL, "Skilled"),
    (P_SKILLS.P_DIVINATION_SPELL, "Expert"),
    (P_SKILLS.P_ENCHANTMENT_SPELL, "Skilled"),
    (P_SKILLS.P_CLERIC_SPELL, "Skilled"),
    (P_SKILLS.P_ESCAPE_SPELL, "Expert"),
    (P_SKILLS.P_MATTER_SPELL, "Expert"),
    (P_SKILLS.P_RIDING, "Basic"),
    (P_SKILLS.P_BARE_HANDED_COMBAT, "Basic"),
]


class Skill:
    possible_skill_types = ["Fighting Skills", "Weapon Skills", "Spellcasting Skills"]
    possible_skill_levels = ["UnSkilled", "Basic", "Skilled", "Expert", "Master", "Grand Master"]

    SKILL_LEVEL_RESTRICTED = 0
    SKILL_LEVEL_UNSKILLED = 1
    SKILL_LEVEL_BASIC = 2
    SKILL_LEVEL_SKILLED = 3
    SKILL_LEVEL_EXPERT = 4
    SKILL_LEVEL_MASTER = 5
    SKILL_LEVEL_GRAND_MASTER = 6

    weapon_bonus = {
        SKILL_LEVEL_RESTRICTED: (-4, 2),
        SKILL_LEVEL_UNSKILLED: (-4, 2),
        SKILL_LEVEL_BASIC: (0, 0),
        SKILL_LEVEL_SKILLED: (2, 1),
        SKILL_LEVEL_EXPERT: (3, 2),
    }
    two_weapon_bonus = {
        SKILL_LEVEL_RESTRICTED: (-9, -3),
        SKILL_LEVEL_UNSKILLED: (-9, -3),
        SKILL_LEVEL_BASIC: (-7, -1),
        SKILL_LEVEL_SKILLED: (-5, 0),
        SKILL_LEVEL_EXPERT: (-3, 1),
    }
    riding_bonus = {
        SKILL_LEVEL_RESTRICTED: (-2, 0),
        SKILL_LEVEL_UNSKILLED: (-2, 0),
        SKILL_LEVEL_BASIC: (-1, 0),
        SKILL_LEVEL_SKILLED: (0, 1),
        SKILL_LEVEL_EXPERT: (0, 2),
    }
    unarmed_bonus = {
        SKILL_LEVEL_RESTRICTED: (1, 0),
        SKILL_LEVEL_UNSKILLED: (1, 0),
        SKILL_LEVEL_BASIC: (1, 1),
        SKILL_LEVEL_SKILLED: (2, 1),
        SKILL_LEVEL_EXPERT: (2, 2),
        SKILL_LEVEL_MASTER: (3, 2),
        SKILL_LEVEL_GRAND_MASTER: (3, 3),
    }
    martial_bonus = {
        SKILL_LEVEL_RESTRICTED: (1, 0),  # no one has it restricted
        SKILL_LEVEL_UNSKILLED: (2, 1),
        SKILL_LEVEL_BASIC: (3, 3),
        SKILL_LEVEL_SKILLED: (4, 4),
        SKILL_LEVEL_EXPERT: (5, 6),
        SKILL_LEVEL_MASTER: (6, 7),
        SKILL_LEVEL_GRAND_MASTER: (7, 9),
    }

    name_to_skill_level = {
        k: v
        for k, v in zip(
            ["Restricted"] + possible_skill_levels,
            [
                SKILL_LEVEL_RESTRICTED,
                SKILL_LEVEL_UNSKILLED,
                SKILL_LEVEL_BASIC,
                SKILL_LEVEL_SKILLED,
                SKILL_LEVEL_EXPERT,
                SKILL_LEVEL_MASTER,
                SKILL_LEVEL_GRAND_MASTER,
            ],
        )
    }

    name_to_skill_type = {
        # "": P_SKILLS.P_NONE,
        "dagger": P_SKILLS.P_DAGGER,
        "knife": P_SKILLS.P_KNIFE,
        "axe": P_SKILLS.P_AXE,
        "pick-axe": P_SKILLS.P_PICK_AXE,
        "short sword": P_SKILLS.P_SHORT_SWORD,
        "broadsword": P_SKILLS.P_BROAD_SWORD,
        "long sword": P_SKILLS.P_LONG_SWORD,
        "two-handed sword": P_SKILLS.P_TWO_HANDED_SWORD,
        "scimitar": P_SKILLS.P_SCIMITAR,
        "saber": P_SKILLS.P_SABER,
        "club": P_SKILLS.P_CLUB,
        "mace": P_SKILLS.P_MACE,
        "morning star": P_SKILLS.P_MORNING_STAR,
        "flail": P_SKILLS.P_FLAIL,
        "hammer": P_SKILLS.P_HAMMER,
        "quarterstaff": P_SKILLS.P_QUARTERSTAFF,
        "polearms": P_SKILLS.P_POLEARMS,
        "spear": P_SKILLS.P_SPEAR,
        "trident": P_SKILLS.P_TRIDENT,
        "lance": P_SKILLS.P_LANCE,
        "bow": P_SKILLS.P_BOW,
        "sling": P_SKILLS.P_SLING,
        "crossbow": P_SKILLS.P_CROSSBOW,
        "dart": P_SKILLS.P_DART,
        "shuriken": P_SKILLS.P_SHURIKEN,
        "boomerang": P_SKILLS.P_BOOMERANG,
        "whip": P_SKILLS.P_WHIP,
        "unicorn horn": P_SKILLS.P_UNICORN_HORN,
        "attack spells": P_SKILLS.P_ATTACK_SPELL,
        "healing spells": P_SKILLS.P_HEALING_SPELL,
        "divination spells": P_SKILLS.P_DIVINATION_SPELL,
        "enchantment spells": P_SKILLS.P_ENCHANTMENT_SPELL,
        "clerical spells": P_SKILLS.P_CLERIC_SPELL,
        "escape spells": P_SKILLS.P_ESCAPE_SPELL,
        "matter spells": P_SKILLS.P_MATTER_SPELL,
        "bare handed combat": P_SKILLS.P_BARE_HANDED_COMBAT,
        "martial arts": P_SKILLS.P_BARE_HANDED_COMBAT,
        "two weapon combat": P_SKILLS.P_TWO_WEAPON_COMBAT,
        "riding": P_SKILLS.P_RIDING,
    }

    def __init__(self, predefined_skill):
        self.skill_levels = np.zeros(max([v.value for v in self.name_to_skill_type.values()]) + 1, dtype=int)

        # Parse the skill array and set the skill levels
        for skill_entry in predefined_skill:
            skill_type: P_SKILLS = skill_entry[0]  # P_DAGGER, P_KNIFE, etc.
            skill_level = skill_entry[1]  # Basic, Skilled, etc.
            self.skill_levels[skill_type.value] = self.name_to_skill_level[skill_level]

    @staticmethod
    def from_role(role: Role):
        role_to_skill = {
            Role.ARCHEOLOGIST: Skill_A,
            Role.BARBARIAN: Skill_B,
            Role.CAVEMAN: Skill_C,
            Role.HEALER: Skill_H,
            Role.KNIGHT: Skill_K,
            Role.MONK: Skill_Mon,
            Role.PRIEST: Skill_P,
            Role.RANGER: Skill_Ran,
            Role.ROGUE: Skill_R,
            Role.SAMURAI: Skill_S,
            Role.TOURIST: Skill_T,
            Role.VALKYRIE: Skill_V,
            Role.WIZARD: Skill_W,
        }
        skill = role_to_skill[role]
        return Skill(skill)

    def get_skill_str_list(self):
        inv_skill_type = {v: k for k, v in self.name_to_skill_type.items()}
        inv_skill_level = {v: k for k, v in self.name_to_skill_level.items()}
        return list(
            inv_skill_type[P_SKILLS(skill_type)] + "-" + inv_skill_level[level]
            for skill_type, level in enumerate(self.skill_levels)
            if level in inv_skill_level and P_SKILLS(skill_type) in inv_skill_type and level != 0
        )
