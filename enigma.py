# TODO implement error handling for plaintext
# TODO make Scrambler automatically build its own table, so can tidy up encrypt_basic

class Scrambler:
    def __init__(self, mapping, name="new"):
        self.name = name  # give the thing some meaningful name for use later (also for file?)
        self.m = mapping  # string specifying what each of letters maps to, in order

    def make_table(self):
        # take in the mapping, return a dictionary representing all orientations of scrambler
        tab = {}
        for i in range(0, len(self.m)):
            newalpha = self.m[i:] + self.m[:i]
            tab[i] = newalpha
        return tab


class Machine:
    # make s2, s3, o2, o3 optional
    def __init__(self, scrambler1, scrambler2, scrambler3, orientation1=0, orientation2=0, orientation3=0, alphabet="abcdefghijklmnopqrstuvwxyz"):
        self.s1 = scrambler1
        self.s2 = scrambler2
        self.s3 = scrambler3
        self.o1 = orientation1
        self.o2 = orientation2
        self.o3 = orientation3
        self.alphabet = alphabet

    def increment_scramblers(self):
        # this is run each time a single character is encrypted
        orientation1 = self.o1 + 1
        self.o1 = orientation1 % len(self.s1.m)
        orientation2 = self.o2

        # step scrambler 2 on for each full rotation of the first, and scrambler 3 for each full rotation of the second
        # this will always happen (atm) together - 3 cannot increment without 2 incrementing too
        if orientation2 == len(self.s1.m) - 1 and orientation1 == len(self.s1.m):
            orientation2 += 1
            self.o2 = orientation2 % len(self.s2.m)
            orientation3 = self.o3 + 1
            self.o3 = orientation3 % len(self.s2.m)

        # steps the second scrambler on for each full rotation of the first
        elif orientation1 == len(self.s2.m):
            orientation2 = self.o2 + 1
            self.o2 = orientation2 % len(self.s2.m)

    def encrypt_basic(self, number_of_scramblers=3):   #TODO error handling for number of scramblers
        plaintext = input("Enter plaintext: ")
        ciphertext = ""
        table1 = Scrambler.make_table(self.s1)  # build the mapping for the scramblers
        for c in plaintext:
            sub_alpha1 = table1[self.o1]
            initial_index = self.alphabet.find(c)
            char_after_first = sub_alpha1[initial_index]

            if number_of_scramblers == 1:
                ciphertext += char_after_first
                self.increment_scramblers()

            else:  # ie more than one scrambler
                table2 = Scrambler.make_table(self.s2)
                sub_alpha2 = table2[self.o2]
                index_after_first = self.alphabet.find(char_after_first)  # find index of result
                char_after_second = sub_alpha2[index_after_first]  # pass this new character through second scrambler
                if number_of_scramblers == 2:
                    ciphertext += char_after_second
                    self.increment_scramblers()

                else:  # currently can't do anything different for more than 3
                    table3 = Scrambler.make_table(self.s3)
                    sub_alpha3 = table3[self.o3]
                    index_after_second = self.alphabet.find(char_after_second)  # find index of result
                    char_after_third = sub_alpha3[index_after_second]  # pass new character through third scrambler
                    ciphertext += char_after_third
                    self.increment_scramblers()
        return ciphertext



a = "bcdefghijklmnopqrstuvwxyza"
y = Scrambler(a, "basicTest")
z = Scrambler(a, "basicTest2")
w = Scrambler(a, "basicTest3")
x = Machine(y, z, w)
m = Machine(y, z, w)
print(x.encrypt_basic())
print(x.o1, x.o2, x.o3)
