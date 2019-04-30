from enigma import Enigma, Rotor
from parser import Parser
import string
from sys import argv, exit

# discos_ejemplo = [
# [16,5,23,24,17,14,1,22,21,12,3,6,15,18,4,13,19,25,0,10,27,11,9,20,8,7,2,26],
# [17,6,19,11,23,2,21,13,27,9,18,24,0,4,8,26,12,5,14,1,16,7,3,22,15,10,25,20],
# [23,22,3,25,16,6,24,4,11,8,20,10,7,26,14,2,15,12,17,21,19,13,0,9,5,18,1,27],
# [4,22,26,16,19,0,9,2,14,3,24,13,1,15,18,12,21,17,23,7,11,6,20,27,8,10,5,25],
# [18,26,20,14,2,23,16,17,25,3,15,21,1,7,10,19,22,8,5,13,24,11,4,6,9,0,12,27],
# [5,21,27,24,17,8,19,3,6,23,2,12,13,14,25,1,0,4,26,7,9,10,22,20,11,18,15,16],
# [5,21,27,24,17,8,19,3,6,23,2,12,13,14,25,1,0,4,26,7,9,10,22,20,11,18,15,16]
# ]

# reflector = [1,0,3,2,5,4,7,6,9,8,11,10,13,12,15,14,17,16,19,18,21,20,23,22,25,24,27,26]

# plain = "hola ha sido muy grato poder encriptar esta cuestion, aunque no estoy muy seguro que funcione"
# print("antes de encriptar:", plain)
# enigma = Enigma(reflector, discos_ejemplo)
# cipher = enigma.cipher_text(plain, [0,1,2,3,4,5])
# print("texto cifrado:", cipher)
# plain2 = enigma.cipher_text(cipher, [0,1,2,3,4,5])
# print("después de desencriptar:", plain2)

if len(argv) < 2:
  print('Falta ingresar el nombre del archivo a parsear como argumento')
  exit()

alphabet = list(string.ascii_lowercase) + [' ', ',']
alphabet_r = {}
for index, val in enumerate(alphabet):
    alphabet_r[val] = index

discs = [
[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
]

discs_dic = [
  dict(alphabet_r),
  dict(alphabet_r),
  dict(alphabet_r),
  dict(alphabet_r),
  dict(alphabet_r),
  dict(alphabet_r),
]

levels = []

reflector = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,0]

enigma = Enigma(reflector, discs)

parser = Parser(argv[1])

def try_level(level):
  disc = int(level[0]) -1 
  # disc = discs_dic[disc]
  backtrack(level, disc, alphabet)

def backtrack(level, disc, letters, actual=0):
  discs_order = []
  for l in level:
    discs_order.append(int(l)-1)
  discs_order.reverse()
  to_change = False
  if len(letters) > 1:
    for index, letter in enumerate(letters):
      last = enigma.rotors[disc].inv_disc[alphabet_r[letter]]
      discs[disc][actual] = alphabet_r[letter]
      if type(to_change) != type(True):
        if to_change[0] == actual:
          discs[disc][last] = alphabet_r[letters[index-1]]
          enigma.set_rotor(discs[disc], disc)
          c = enigma.cipher_letter(to_change[1], to_change[2], discs_order)
          if c != to_change[3] and to_change[4]:
            if letter != letters[-1]:
              continue
            else: 
              return False

      to_change = backtrack(level, disc, letters[:letters.index(letter)] + letters[letters.index(letter)+1:], actual+1)
      if type(to_change) != type(True) and actual > to_change[0]:
        return to_change
    return False
  discs[disc][actual] = alphabet_r[letters[0]]
  enigma.set_rotor(discs[disc], disc)
  to_change = test_configuration(level)
  return to_change

def test_configuration(level):
  discs = []
  for l in level:
    discs.append(int(l)-1)
  discs.reverse()
  count = 0
  for plain, cipher in parser.levels_dic[tuple(level)]:
    f= open("./discos.txt","w+")
    for disco in enigma.rotors:
     f.write(str(disco.disc))
     f.write('\n')
    f.close()
    count +=1
    for index, letter in enumerate((plain)):
      c = enigma.cipher_letter(letter, index, discs) 
      if c != cipher[index]:
        let = enigma.rotors[discs[0]].encrypt_forward(alphabet_r[letter], index)
        disc = discs.pop()
        for i in discs:
          let = enigma.rotors[discs[i]].encrypt_forward(alphabet_r[letter], index)
        let = enigma.reflect(let)
        for i in reversed(discs):
          let = enigma.rotors[discs[i]].encrypt_backwards(alphabet_r[letter], index)
        let = enigma.rotors[disc].inv_disc[let]
        boolean = False
        if let >= alphabet_r[cipher[index]]:
          boolean = True
        let = min(let, alphabet_r[cipher[index]])
        to_change = max(alphabet_r[letter], let)
        return to_change, letter, index, cipher[index], boolean
  return True

  




def main():
  try_level(parser.levels[0])


if __name__ == '__main__':
  main()
    