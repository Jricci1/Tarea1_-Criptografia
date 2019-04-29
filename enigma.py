# { 
#   a: [forward_output, backward_output],
#   b: a: [forward_output, backward_output],
#   ....
# }

import string


alphabet = list(string.ascii_lowercase) + [' ', ',']
alphabet_r = {}
for index, val in enumerate(alphabet):
    alphabet_r[val] = index


class Rotor():
    '''
    Rotor class intend to represent a disc in the enigma machine
    '''
    def __init__(self, disc):
        self.disc = disc
        self.inv_disc = []
        self.set_disc(disc)

    def set_disc(self, disc):
        self.validate_disc(disc)
        self.disc = disc
        self.inv_disc = [0] * len(alphabet)
        for index, value in enumerate(disc):
            self.inv_disc[value] = index

    def validate_disc(self, disc):
        if len(disc) != len(alphabet):
            raise Exception('El largo del disco es menor al del alfabeto')
        validation_array = [0] * len(alphabet)
        for i in disc:
            validation_array[i] = 1
        if sum(validation_array) != len(alphabet):
            raise Exception('La configuración del disco es incorrecta')
    
    def encrypt_forward(self, letter, offset):
        ''' Encrypt letter forward in the disc'''
        return (self.disc[(letter + offset) % len(alphabet)] - offset) % len(alphabet)

    def encrypt_backward(self, letter, offset):
        ''' Encrypt letter forward in the disc'''
        return (self.inv_disc[(letter + offset) % len(alphabet)] - offset) % len(alphabet)


class Enigma():

    def __init__(self, reflector, discs):
        self.rotors = []
        self.reverse_rotors = []
        self.reflector = reflector
        self.divs = []
        self.offsets = []
        self.set_rotors(discs)

    def set_rotor(self, disc, position=-1):
        rotor = Rotor(disc)
        if position != -1:
            self.rotors[position] = rotor
            self.reverse_rotors[len(self.rotors)-1-position] = rotor
            return
        self.rotors.append(rotor)
        self.reverse_rotors.insert(0, rotor)
        self.set_divs()

    def set_divs(self):
        self.divs = [0] * len(self.rotors)
        for i in range(len(self.divs)):
            self.divs[i] = len(alphabet) ** i
    
    def set_offsets(self, x):
        self.offsets = [0] * len(self.divs)
        for i in range(len(self.divs)):
            self.offsets[i] = x // self.divs[i]

    def set_rotors(self, discs):
        self.rotors = []
        self.reverse_rotors = []
        for disc in discs:
            self.set_rotor(disc)
    
    def reflect(self, c):
        return self.reflector[c]
    
    def encrypt_forward(self, c, discs=False):
        if discs:
            rotors = []
            for i in discs:
                rotors.append(self.rotors[i])
            rotors.reverse()
        else:
            rotors = self.reverse_rotors
        offsets = self.offsets[:len(rotors)]
        for index, rotor in enumerate(rotors):
            offset = offsets[index]
            c = rotor.encrypt_forward(c, offset)
        return c

    def encrypt_backward(self, c, discs=False):
        if discs:
            rotors = []
            for i in discs:
                rotors.append(self.rotors[i])
        else:
            rotors = self.rotors
        offsets = self.offsets[:len(rotors)]
        for index, rotor in enumerate(rotors):
            offset = offsets[len(offsets) - index - 1]
            c = rotor.encrypt_backward(c, offset)
        return c

    def encrypt(self, c, discs):
        c = self.encrypt_forward(c, discs)
        c = self.reflect(c)
        return self.encrypt_backward(c, discs)

    def cipher_letter(self, c, i, discs=None):
        self.set_offsets(i)
        c = alphabet_r[c]
        c = self.encrypt(c, discs)
        return alphabet[c]

    def cipher_text(self, text, discs=None):
        text = list(text)
        cypher = ''
        for index, letter in enumerate(text):
            if letter not in alphabet:
                raise Exception("Caracter no soportado: "+letter)
            cypher += self.cipher_letter(letter, index, discs)
        return cypher

