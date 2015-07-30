# TODO URGENT tidy up Machine.encrypt() like Carl said
# TODO check i got the mappings of the real rotors right! zzzzz
# TODO (eventually) be able to set up plugboard from user input?

# alphabet = "abcdef"
alphabet = "abcdefghijklmnopqrstuvwxyz"


class Scrambler():
    def __init__(self, mapping, orientation=0, step_orientation=[0]):
        self.orientation = orientation  # integer representing orientation of scrambler
        self.m = mapping  # list of numbers specifying how to map from input to output characters
        self.inverse_m = self.calculate_inverse_m()  # list representing base mapping of scrambler in reverse direction
        self.step_orientation = step_orientation  # tuple of orientation AFTER has caused next rotor to step on

    def calculate_inverse_m(self):  # from the original mapping, work out what the mapping is in other direction
        reversed_inverse_m = []
        for i in range(len(alphabet)):
            new_map = (len(alphabet) - self.m[i]) % len(alphabet)
            reversed_inverse_m.append(new_map)  # this gives the right numbers in reversed order.
        inverse_m = reversed_inverse_m[::-1]  # reverse the list
        return inverse_m

    def encrypt_char_forward(self, integer):  # passes a single character, represented as integer, through the scrambler
        current_wiring_f = self.m[self.orientation:] + self.m[:self.orientation]
        # print("wiring forwards: ", current_wiring_f)  # for debugging
        new_int = (integer + current_wiring_f[integer]) % len(alphabet)
        return new_int

    def encrypt_char_backward(self, integer):  # passes single char represented as integer through s in reverse
        current_wiring_b = self.inverse_m[self.orientation:] + self.inverse_m[:self.orientation]
        # print("wiring backwards: ", current_wiring_b)  # for debugging
        new_int = (integer + current_wiring_b[integer]) % len(alphabet)
        return new_int


class PairMap:
    def __init__(self, mapping):
        self.m = mapping

    def encrypt_char(self, integer):  # passes a single character, represented as integer, through the reflector
        new_int = (integer + self.m[integer]) % len(alphabet)
        return new_int


class Reflector(PairMap):
    def __init__(self, mapping):
        PairMap.__init__(self, mapping)
        self.check = self.check_mapping()

    def check_mapping(self):
        # check that it is a valid reflector, ie swaps pairs of characters
        check = True
        for i in range(len(self.m)):
            maps_to = (i + self.m[i]) % len(self.m)
            if (maps_to + self.m[maps_to]) % len(self.m) != i:
                check = False
        return check


class Plugboard(PairMap):  # note directionality is irrelevant for plugboard!
    def __init__(self, mapping):
        PairMap.__init__(self, mapping)
        self.check = self.check_mapping()

    def check_mapping(self):
        # check that it is a valid plugboard, ie swaps pairs of chars or leaves char unchanged
        check = True
        for i in range(len(self.m)):
            if self.m[i] != 0:
                maps_to = (i + self.m[i]) % len(self.m)
                if (maps_to + self.m[maps_to]) % len(self.m) != i:
                    check = False
        return check


class Machine:
    def __init__(self, scrambler1, scrambler2=Scrambler([0]*26),
                 scrambler3=Scrambler([0]*26), reflector=Reflector([0]*26), plugboard=Plugboard([0]*26)):
        # would it be better to do this with everything except s1 as *args? worried as never used before
        # and also there isn't really an arbitrary number of arguments, just 0-4
        self.s1 = scrambler1
        self.s2 = scrambler2
        self.s3 = scrambler3
        self.ref = reflector
        self.plug = plugboard

    def increment_scramblers(self):  # steps on when orientation of s1, s2 returns to 0
        length = len(alphabet)
        # this is run once each time a single character is encrypted
        self.s1.orientation = (self.s1.orientation + 1) % length

        # step scrambler 2 on for each full rotation of the first, and scrambler 3 for each full rotation of the second
        # this will always happen (atm) together - 3 cannot increment without 2 incrementing too
        if self.s1.orientation in self.s1.step_orientation:
            self.s2.orientation = (self.s2.orientation + 1) % length
            if self.s2.orientation in self.s2.step_orientation:
                self.s3.orientation = (self.s3.orientation + 1) % length

    def encrypt(self, plaintext):
        # concerned this is really redundant and messy, esp if most of the bits of Machine don't do anything
        # also not very general, but fixing this depends on how deal with Machine's parameters?

        self.plaintext = plaintext
        ciphertext = ""
        for c in self.plaintext:
            # check that c is validz
            if c not in alphabet:
                print("invalid character", c)
                break
            else:
                self.increment_scramblers()
                # print(self.s1.orientation, self.s2.orientation, self.s3.orientation)  # for debugging
                initial_no = alphabet.find(c)  # map the letter to its equivalent integer in the alphabet
                n0 = self.plug.encrypt_char(initial_no)  # plugboard forward
                n1 = self.s1.encrypt_char_forward(n0)  # pass through first scrambler
                n2 = self.s2.encrypt_char_forward(n1)  # pass through second scrambler
                n3 = self.s3.encrypt_char_forward(n2)  # pass through third scrambler
                n4 = self.ref.encrypt_char(n3)  # reflector
                n5 = self.s3.encrypt_char_backward(n4)  # through third scrambler in reverse
                n6 = self.s2.encrypt_char_backward(n5)  # through second scrambler in reverse
                n7 = self.s1.encrypt_char_backward(n6)  # through first scrambler in reverse
                n8 = self.plug.encrypt_char(n7)  # plugboard backward
                ciphertext += alphabet[n8]  # map from integer back to letter using alphabet, add to ciphertext str
                # print(initial_no, n0, n1, n2, n3, n4, n5, n6, n7, n8)  # so i can see what it's doing!
        return ciphertext


si = Scrambler([5, 9, 10, 2, 7, 1, 23, 9, 13, 16, 3, 8, 2, 9, 10, 18, 7, 3, 0, 22, 6, 13, 5, 20, 4, 10], 0, [18])
sii = Scrambler([0, 8, 1, 7, 14, 3, 11, 13, 15, 18, 1, 22, 10, 6, 24, 13, 0, 15, 7, 20, 21, 3, 8, 24, 16, 5], 0, [6])
siii = Scrambler([1, 2, 2, 4, 5, 6, 22, 8, 9, 10, 13, 10, 13, 0, 10, 15, 18, 5, 14, 7, 16, 17, 22, 21, 18, 15], 0, [23])
ra = Reflector([4, 8, 10, 22, 22, 6, 18, 16, 13, 18, 12, 20, 16, 4, 2, 5, 24, 22, 1, 25, 21, 13, 14, 10, 8, 4])
p = Plugboard([0] * 26)
default_machine = Machine(si, Scrambler([0]*26), Scrambler([0]*26), ra, p)