# TODO tidy up encrypt_basic now scrambler makes its own table
# TODO Move bits of encryption function to the scramblers
# TODO make reflector class, as a subclass of something a bit more abstract than a scrambler



class Scrambler:
    def __init__(self, mapping, name="new"):
        self.name = name  # give the thing some meaningful name for use later
        self.m = mapping  # list of numbers specifying how to map from input to output characters
        self.table = self.make_table()

    def make_table(self):
        # take in the mapping, return a dictionary representing all orientations of scrambler
        tab = {}
        for i in range(0, len(self.m)):
            newalpha = self.m[i:]
            newalpha.extend(self.m[:i])
            tab[i] = newalpha
        return tab


class Machine:
    # TODO make s2, s3, o2, o3 optional? there must be a cleaner way to do this!
    def __init__(self, scrambler1, scrambler2=[0]*26,
                 scrambler3=[0]*26,
                 orientation1=0, orientation2=0, orientation3=0, alphabet="abcdef"):
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

    def encrypt_numbers(self):
        plaintext = input("Enter plaintext: ")
        ciphertext = ""
        table1 = Scrambler.make_table(self.s1)  # build the mapping for the scramblers
        table2 = Scrambler.make_table(self.s2)  # build the mapping for the scramblers
        table3 = Scrambler.make_table(self.s3)  # build the mapping for the scramblers

        for c in plaintext:
            # check that c is valid
            if c not in self.alphabet:
                print("invalid character", c)
                break
            else:
                map1 = table1[self.o1]  # select the correct mapping for current orientation of s1
                map2 = table2[self.o2]
                map3 = table3[self.o3]
                n0 = self.alphabet.find(c)  # first find unmodified index N of plaintext character
                n1 = (map1[n0] + n0) % len(self.alphabet)  # pass through first scrambler, modify N according to mapping
                # print("after first scrambler:", n1, self.alphabet[n1])
                n2 = (map2[n1] + n1) % len(self.alphabet)
                # print("after second scrambler:", n2, self.alphabet[n2])
                n3 = (map3[n2] + n2) % len(self.alphabet)
                # print("after third scrambler:", n3, self.alphabet[n3])
                ciphertext += self.alphabet[n3]
                self.increment_scramblers()
        return ciphertext


a = "bcdefghijklmnopqrstuvwxyza"
b = [3, 1, 3, 1, 2, 2]
blank=[0]*6
y = Scrambler(b, "basicTest")
print(y.table)
z = Scrambler(blank, "basicTest2")
w = Scrambler(blank, "basicTest3")
x = Machine(y, z, w)
m = Machine(y, z, w)
#print(x.encrypt_basic(2))
print(x.encrypt_numbers())
#print()
