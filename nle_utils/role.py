import enum
import re


class Role(enum.Enum):
    UNKNOWN = -1
    ARCHEOLOGIST = 0
    BARBARIAN = 1
    CAVEMAN = 2
    HEALER = 3
    KNIGHT = 4
    MONK = 5
    PRIEST = 6
    RANGER = 7
    ROGUE = 8
    SAMURAI = 9
    TOURIST = 10
    VALKYRIE = 11
    WIZARD = 12

    _name_to_role = {
        "archeologist": ARCHEOLOGIST,
        "barbarian": BARBARIAN,
        "caveman": CAVEMAN,
        "cavewoman": CAVEMAN,
        "healer": HEALER,
        "knight": KNIGHT,
        "monk": MONK,
        "priest": PRIEST,
        "priestess": PRIEST,
        "ranger": RANGER,
        "rogue": ROGUE,
        "samurai": SAMURAI,
        "tourist": TOURIST,
        "valkyrie": VALKYRIE,
        "wizard": WIZARD,
    }

    @classmethod
    def from_str(cls, string):
        for key in cls._name_to_role.value.keys():
            if string == key[:3]:
                return Role(cls._name_to_role.value[key])
        raise ValueError()

    @classmethod
    def parse(cls, description):
        pattern = rf'\b({"|".join(cls._name_to_role.value.keys())})\b'
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            key = match.group(1).lower()
            return Role(cls._name_to_role.value[key])
        else:
            # TODO: this is nle bug
            # for _ in range(1000):
            #     # Get past initial phase of game. This should make sure
            #     # all the observations are present.
            #     if self._in_moveloop(self.last_observation):
            #         break
            #     # This fails if the agent picks up a scroll of scare
            #     # monster at the 0th turn and gets asked to name it.
            #     # Hence the defensive iteration above.
            #     # TODO: Detect this 'in_getlin' situation and handle it.
            #     self.last_observation, done = self.nethack.step(ASCII_SPACE)
            #     assert not done, "Game ended unexpectedly"
            # message `Hello %name, welcome to NetHack! You are a neutral female gnomish\nArcheologist.`
            # is two lines long self._in_moveloop(self.last_observation) returns false
            # fortunately this only happens for archeologist
            return Role.ARCHEOLOGIST
