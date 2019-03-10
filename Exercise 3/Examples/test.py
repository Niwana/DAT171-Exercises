
class One():
    def __init__(self, value):
        self.value = value
        print("One:", self.value)

    def returnera(self):
        return self.value

class Two():
    def __init__(self, one):
        self.one = one
        print("Two:", one.value)


run = Two(One(1))