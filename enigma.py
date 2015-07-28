# TODO make reflector class, as a subclass of something a bit more abstract than a scrambler
# TODO make a check: length of machine alphabet and scrambler mapping is the same, or make alphabet available globally


class Scrambler:
    def __init__(self, mapping, orientation=0, name="new"):
        self.name = name  # give the thing some meaningful name for use later
        self.m = mapping  # list of numbers specifying how to map from input to output characters
        self.orientation = orientation

    def encrypt_char(self, integer):  # passes a single character, represented as integer, through the scrambler
        wiring = self.m[self.orientation:] + self.m[:self.orientation]
        new_int = (integer + wiring[integer]) % len(self.m)
        return new_int


class Machine:
    def __init__(self, scrambler1, scrambler2=[0]*26,
                 scrambler3=[0]*26, alphabet="abcdef"):
        self.s1 = scrambler1
        self.s2 = scrambler2
        self.s3 = scrambler3
        self.alphabet = alphabet

    def increment_scramblers(self):
        # this is run once each time a single character is encrypted
        self.s1.orientation = (self.s1.orientation + 1) % len(self.alphabet)

        # step scrambler 2 on for each full rotation of the first, and scrambler 3 for each full rotation of the second
        # this will always happen (atm) together - 3 cannot increment without 2 incrementing too
        if self.s2.orientation == len(self.alphabet) - 1 and self.s1.orientation == 0:
            self.s2.orientation = (self.s2.orientation + 1) % len(self.alphabet)
            self.s3.orientation = (self.s3.orientation + 1) % len(self.alphabet)
            # print("incrementing all")

        # steps the second scrambler on for each full rotation of the first
        elif self.s1.orientation == 0:
            self.s2.orientation = (self.s2.orientation + 1) % len(self.alphabet)
            # print("incrementing 1 and 2")

    def encrypt(self):
        plaintext = input("Enter plaintext: ")
        ciphertext = ""
        for c in plaintext:
            # check that c is valid
            if c not in self.alphabet:
                print("invalid character", c)
                break
            else:
                initial_no = n0 = self.alphabet.find(c)  # map the letter to its equivalent integer in the alphabet
                n1 = self.s1.encrypt_char(initial_no)  # pass through first scrambler
                n2 = self.s2.encrypt_char(n1)  # pass through second scrambler
                n3 = self.s3.encrypt_char(n2)  # pass through third scrambler
                ciphertext += self.alphabet[n3]  # map from integer back to letter using alphabet, add to ciphertext str
                self.increment_scramblers()
        return ciphertext


a = "bcdefghijklmnopqrstuvwxyza"
b = [3, 1, 3, 1, 2, 2]
blank = [0] * 6
y = Scrambler(b)
z = Scrambler(blank)
w = Scrambler(blank)
x = Machine(y, z, w)
m = Machine(y, z, w)
# print(x.encrypt_basic(2))
print(x.encrypt())

