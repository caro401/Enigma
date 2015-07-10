print("Hello! Welcome to Enigma")

class Scrambler:
    def make_table(self):
        # take in the mapping, return a dictionary representing all orientations
        # do this with a while loop and a counter representing length of mapping? slices?
        pass

    def __init__(self, mapping, name="new"):
        self.name = name  # give the thing some meaningful name for use later (also for file?)
        self.m = mapping  # list specifying what each of letters maps to, in order

    def who(self):
        print("I'm a scrambler called", self.name)



class Machine:
    def __init__(self, scrambler1):
        self.s1 = scrambler1


    def who(self):
        print("I'm the machine")





a = ["b", "c", "d", "e", "f", "a"]
y = Scrambler(a, "Fred")
x = Machine(y)  # this is class instantiation!
x.who()
y.who()
print(y.m, y.name)
