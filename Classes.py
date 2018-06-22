
class Sim():
    def __init__(self, first: object, last: object, age: object, gender: object, career: object) -> object:
        # Characteristics
        self.first = first
        self.last = last
        self.age = age
        self.gender = gender
        self.career = career
        # "Behaviors"


class Player(Sim):
    def __init__(self, first, last, age, gender, career, clothing, ambition):
        super().__init__(first, last, age, gender, career)
        self.ambition = ambition
        self.clothing = clothing
        self.befriendable = True
        self.romanceable = True
        self.seduceable = True


class NPC(Sim):
    def __init__(self,first, last, age, gender, career, f, r, fwb):
        super().__init__(first, last, age, gender, career)
        self.befriendable = f
        if int(age) < 18:
            self.romanceable = False
            self.seduceable = False
        else:
            self.romanceable = r
            self.seduceable = fwb

