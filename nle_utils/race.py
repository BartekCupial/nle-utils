import enum
import re


class Race(enum.Enum):
    UNKNOWN = -1
    HUMAN = 0
    DWARF = 1
    ELF = 2
    GNOME = 3
    ORC = 4

    _name_to_race = {
        "human": HUMAN,
        "dwarf": DWARF,
        "dwarven": DWARF,
        "elf": ELF,
        "elven": ELF,
        "gnome": GNOME,
        "gnomish": GNOME,
        "orc": ORC,
        "orcish": ORC,
    }

    @classmethod
    def from_str(cls, string):
        for key in cls._name_to_race.value.keys():
            if string == key[:3]:
                return Race(cls._name_to_race.value[key])
        raise ValueError()

    @classmethod
    def parse(cls, description):
        pattern = rf'\b({"|".join(cls._name_to_race.value.keys())})\b'
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            key = match.group(1).lower()
            return Race(cls._name_to_race.value[key])
        assert False
