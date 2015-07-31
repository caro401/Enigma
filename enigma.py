# TODO can generalise Machine.encrypt() further?
# TODO add the other real scramblers and reflectors
# TODO (eventually) be able to set up plugboard from user input?

# alphabet = "abcdef"
alphabet = "abcdefghijklmnopqrstuvwxyz"


class Scrambler():
    def __init__(self, mapping, step_orientation=[0], orientation=0):
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
        # check that it is a valid plugboard, ie swaps pairs of chars or leaves char unchanged
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
            # check that c is valid
            if c not in alphabet:
                print("invalid character", c)
                break
            else:
                self.increment_scramblers()
                print("orientations:", self.s[0].orientation, self.s[1].orientation, self.s[2].orientation)
                initial_no = alphabet.find(c)  # map the letter to its equivalent integer in the alphabet
                num = self.plug.encrypt_char(initial_no)  # plugboard forward
                num = self.loop_scramblers_f(num)  # scrambler(s) forward
                num = self.ref.encrypt_char(num)  # reflector
                num = self.loops_scramblers_b(num)  # scramblers backward
                num = self.plug.encrypt_char(num)  # plugboard backward
                ciphertext += alphabet[num]  # map from integer back to letter using alphabet, add to ciphertext str
        return ciphertext

si = Scrambler([4, 9, 10, 2, 7, 1, 23, 9, 13, 16, 3, 8, 2, 9, 10, 18, 7, 3, 0, 22, 6, 13, 5, 20, 4, 10], [18])
sii = Scrambler([0, 8, 1, 7, 14, 3, 11, 13, 15, 18, 1, 22, 10, 6, 24, 13, 0, 15, 7, 20, 21, 3, 9, 24, 16, 5], [6])
siii = Scrambler([1, 2, 3, 4, 5, 6, 22, 8, 9, 10, 13, 10, 13, 0, 10, 15, 18, 5, 14, 7, 16, 17, 24, 21, 18, 15], [23])
main_scrambler_list = [si, sii, siii]
# test_list = [Scrambler([3,1,3,1,2,2], [1,4]), Scrambler([3,1,3,1,2,2], [3]), Scrambler([0]*6)]

ra = Reflector([4, 8, 10, 22, 22, 6, 18, 16, 13, 18, 12, 20, 16, 4, 2, 5, 24, 22, 1, 25, 21, 13, 14, 10, 8, 4])
p = Plugboard([0] * 26)
# default_machine = Machine(main_scrambler_list,  ra, p)

# test_machine = Machine(test_list, Reflector([3]*6))
# print(test_machine.encrypt("aaaaaaaaaaaaaaaaaaaa"))
# print(default_machine.encrypt("dfghklmnbbgjftuklj"))
