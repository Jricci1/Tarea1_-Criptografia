


class Parser():

  def __init__(self, file=''):
    self.file = file
    self.levels = []
    self.levels_dic = {}
    self.parse_file()

  def get_levels(self, line):
    discs = line[:line.find(';')-1]
    discs = discs.strip('[')
    discs = discs.strip(']')
    discs = discs.split(',')
    return discs

  def parse_line(self, line):
    discs, plain, cipher = line.split(';')
    discs = discs.strip('[')
    discs = discs.strip(']')
    discs = discs.split(',')
    return discs, plain, cipher
  
  def parse_file(self):
    if not self.file:
      print('Missing file name to parse')
    f=open(self.file, "r")
    line = f.readline()
    while line != '':
      discs, plain, cipher = self.parse_line(line)
      # discs = self.get_levels(line)
      # print(discs)
      if self.levels_dic.get(tuple(discs), False):
      # if discs not in self.levels:
        self.levels_dic[tuple(discs)].append((plain, cipher))
        # self.levels.append(discs)
      else:
        self.levels.append(discs)
        self.levels_dic[tuple(discs)] = [(plain, cipher)]
      line = f.readline()
    f.close()


# f=open("quijote_misma_llave.txt", "r")

# line = f.readline()

# levels = []
# levels_dic = {}

#  while line:
#    discs, plain, cipher = parse_line(line)



# for i in range(1):
#   print(parse_line(f.readline()))

# f.close()