import enum
import re


class Gender(enum.Enum):
    UNKNOWN = -1
    MALE = 0
    FEMALE = 1

    _name_to_gender = {
        "male": MALE,
        "female": FEMALE,
    }

    @classmethod
    def parse(cls, description):
        pattern = rf'\b({"|".join(cls._name_to_gender.value.keys())})\b'
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            key = match.group(1).lower()
            return Gender(cls._name_to_gender.value[key])
        else:
            if "Priest" in description or "Caveman" in description:
                return Gender.MALE
            elif "Priestess" in description or "Cavewoman" in description or "Valkyrie" in description:
                return Gender.FEMALE
        assert False
