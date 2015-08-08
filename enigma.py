alphabet = "abcdefghijklmnopqrstuvwxyz"


class Scrambler():
    def __init__(self, mapping, step_orientation=[0], orientation=0):
        self.orientation = orientation  # integer representing orientation of scrambler
        self.m = mapping  # list of numbers specifying how to map from input to output characters
        self.inverse_m = self.calculate_inverse_m()  # list representing base mapping of scrambler in reverse direction
        self.step_orientation = step_orientation  # tuple of orientations AFTER has caused next rotor to step on

    def calculate_inverse_m(self):  # from the original mapping, work out what the mapping is in other direction
        inverse_m = [0]*len(alphabet)
        for i in range(len(alphabet)):
            result = self.m[i]
            new_map = len(alphabet) - result
            inverse_m[(result+i) % len(alphabet)] = new_map
        return inverse_m

    def encrypt_char_forward(self, integer):  # passes a single character, represented as integer, through the scrambler
        current_wiring_f = self.m[self.orientation:] + self.m[:self.orientation]
        new_int = (integer + current_wiring_f[integer]) % len(alphabet)
        return new_int

    def encrypt_char_backward(self, integer):  # passes single char represented as integer through s in reverse
        current_wiring_b = self.inverse_m[self.orientation:] + self.inverse_m[:self.orientation]
        new_int = (integer + current_wiring_b[integer]) % len(alphabet)
        return new_int

    def display_mapping(self):  # prints out the alphabetic mapping
        cipher = ""
        for i in range(len(alphabet)):
            cipher += alphabet[self.encrypt_char_forward(i)]
        print(alphabet)
        print(cipher)


class PairMap:
    def __init__(self, mapping):
        self.m = mapping

    def encrypt_char(self, integer):  # passes a single character, represented as integer, through the reflector
        new_int = (integer + self.m[integer]) % len(alphabet)
        return new_int

    def display_mapping(self):  # prints out the alphabetic mapping
        cipher = ""
        for i in range(len(alphabet)):
            cipher += alphabet[self.encrypt_char(i)]
        print(alphabet)
        print(cipher)


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
        check = True
        for i in range(len(self.m)):
            if self.m[i] != 0:
                maps_to = (i + self.m[i]) % len(self.m)
                if (maps_to + self.m[maps_to]) % len(self.m) != i:
                    check = False
        return check


class Machine:
    def __init__(self, scrambler_list, reflector=Reflector([0]*26), plugboard=Plugboard([0]*26)):
        self.s = scrambler_list
        self.ref = reflector
        self.plug = plugboard

    def increment_scramblers(self):
        for i in range(len(self.s)):
            self.s[i].orientation = (self.s[i].orientation + 1) % len(alphabet)  # increment orientation of s[i]
            if self.s[i].orientation not in self.s[i].step_orientation:  # unless this means moving past push point
                break  # break out of loop

    def loop_scramblers_f(self, num):  # pass a character forward through however many scramblers there are
        for i in range(len(self.s)):
            num = self.s[i].encrypt_char_forward(num)
        return num

    def loops_scramblers_b(self, num):  # pass a character back through however many scramblers there are
        for i in range(len(self.s)):
            num = self.s[len(self.s)-1 - i].encrypt_char_backward(num)
        return num

    def encrypt(self, plaintext):
        ciphertext = ""
        for c in plaintext:
            self.increment_scramblers()
            initial_no = alphabet.find(c)  # map the letter to its equivalent integer in the alphabet
            num = self.plug.encrypt_char(initial_no)  # plugboard forward
            num = self.loop_scramblers_f(num)  # scrambler(s) forward
            if self.ref.m != [0]*len(alphabet):
                num = self.ref.encrypt_char(num)  # reflector
                num = self.loops_scramblers_b(num)  # scramblers backward
                num = self.plug.encrypt_char(num)  # plugboard backward
                ciphertext += alphabet[num]  # map from integer back to letter using alphabet, add to ciphertext str
            else:
                ciphertext += alphabet[num]  # map from integer back to letter using alphabet, add to ciphertext str
        return ciphertext


# saved examples of real wartime scramblers, reflectors
si = Scrambler([4, 9, 10, 2, 7, 1, 23, 9, 13, 16, 3, 8, 2, 9, 10, 18, 7, 3, 0, 22, 6, 13, 5, 20, 4, 10], [18])
sii = Scrambler([0, 8, 1, 7, 14, 3, 11, 13, 15, 18, 1, 22, 10, 6, 24, 13, 0, 15, 7, 20, 21, 3, 9, 24, 16, 5], [6])
siii = Scrambler([1, 2, 3, 4, 5, 6, 22, 8, 9, 10, 13, 10, 13, 0, 10, 15, 18, 5, 14, 7, 16, 17, 24, 21, 18, 15], [23])
siv = Scrambler([4, 17, 12, 18, 11, 20, 3, 19, 16, 7, 10, 23, 5, 20, 9, 22, 23, 14, 1, 13, 16, 8, 6, 15, 24, 2], [10])
sv = Scrambler([21, 24, 25, 14, 2, 3, 13, 17, 12, 6, 8, 18, 1, 20, 23, 8, 10, 5, 20, 16, 22, 19, 9, 7, 4, 11], [0])
svi = Scrambler([9, 14, 4, 18, 10, 15, 6, 24, 16, 7, 17, 19, 1, 20, 11, 2, 13, 19, 8, 25, 3, 16, 12, 5, 21, 23],
                [0, 14])
svii = Scrambler([13, 24, 7, 4, 2, 12, 22, 16, 4, 15, 8, 11, 15, 1, 6, 16, 10, 17, 3, 18, 21, 9, 14, 19, 5, 20],
                 [0, 14])
sviii = Scrambler([5, 9, 14, 4, 15, 6, 17, 7, 20, 18, 25, 7, 3, 16, 11, 2, 10, 21, 12, 3, 19, 13, 24, 1, 8, 22],
                  [0, 14])

ra = Reflector([4, 8, 10, 22, 22, 6, 18, 16, 13, 18, 12, 20, 16, 4, 2, 5, 24, 22, 1, 25, 21, 13, 14, 10, 8, 4])
rb = Reflector([24, 16, 18, 4, 12, 13, 5, 22, 7, 14, 3, 21, 2, 23, 24, 19, 14, 10, 13, 6, 8, 1, 25, 12, 2, 20])
rc = Reflector([5, 20, 13, 6, 4, 21, 8, 17, 22, 20, 7, 14, 11, 9, 18, 13, 3, 19, 2, 23, 24, 6, 17, 15, 9, 12])
rbt = Reflector([4, 12, 8, 13, 22, 15, 18, 15, 1, 25, 18, 3, 3, 14, 23, 23, 13, 6, 7, 2, 11, 24, 11, 20, 8, 19])
rct = Reflector([17, 2, 12, 24, 5, 8, 13, 3, 13, 21, 23, 1, 25, 18, 14, 7, 9, 9, 5, 13, 4, 13, 19, 21, 22, 17])

sx = Scrambler([0] * 26)
rx = Reflector([0] * 26)
rt = Reflector([13] * 26)
px = Plugboard([0] * 26)

possible_scramblers = [si, sii, siii, siv, sv, svi, svii, sviii, sx]
possible_reflectors = [ra, rb, rc, rbt, rct, rx, rt]


# stuff needed for enigmaGUIbasic
main_scrambler_list = [si, sii, siii]
default_machine = Machine(main_scrambler_list,  ra, px)