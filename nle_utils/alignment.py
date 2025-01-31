import enum
import re


class Alignment(enum.Enum):
    UNKNOWN = -1
    CHAOTIC = 0
    NEUTRAL = 1
    LAWFUL = 2
    UNALIGNED = 3

    _name_to_alignment = {
        "chaotic": CHAOTIC,
        "neutral": NEUTRAL,
        "lawful": LAWFUL,
        "unaligned": UNALIGNED,
    }

    @classmethod
    def from_str(cls, string):
        for key in cls._name_to_alignment.value.keys():
            if string == key[:3]:
                return Alignment(cls._name_to_alignment.value[key])
        raise ValueError()

    @classmethod
    def parse(cls, description):
        pattern = rf'\b({"|".join(cls._name_to_alignment.value.keys())})\b'
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            key = match.group(1).lower()
            return Alignment(cls._name_to_alignment.value[key])
        assert False
