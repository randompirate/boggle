import random as rng

rng.seed(123)
# Todo:
  # Evolutionary board
  # Animate solutions

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def memoize(f):
  """
  Some basic memoizer
  """
  memory = dict()
  def memoized(*args):
    key = args
    if key not in memory:
      memory[key] = f(*args)
    return memory[key]
  return memoized

class PrefixTree():
  def __init__(self):
    self.members = dict() # New PrefixTree
    self.is_word = False
    pass

  def add_word(self, word):
    self[word] = True


  def load_from_file(self, file_path):
    with open(file_path, 'r') as f:
      wordlist = set(f.read().split('\n')) # Simpler than readlines(), because of line breaks

    for w in wordlist:
      self.add_word(w)

  def __getitem__(self, key):
    if len(key) == 1:
      if key not in self.members:
        return False, dict()
      return self.members[key].is_word, self.members[key]
    else:
      key, rest = key[0], key[1:]
      return self.members[key][rest]

  def __setitem__(self, key, value):
    if len(key) == 1:
      if key not in self.members:
        self.members[key] = PrefixTree()
      self.members[key].is_word = value
    else:
      key, rest = key[0], key[1:]
      if key not in self.members:
        self.members[key] = PrefixTree()
      self.members[key][rest] = value

  def __repr__(self):
    return str(self.is_word) + ' - ' + str([k for k in self.members])

  def __len__(self):
    return len(self.members)


class Board():
  """
  Board class to contain a grid of letters
  Filled by the Dice class
  """
  def __init__(self, width = 4, height = 4, content = ''):
    self.width, self.height = width, height
    # Lettergrid. Acces with letters[x][y]
    content = [c for c in content if c in alphabet]
    content = content + [rng.choice(alphabet) for x in range(self.width*self.height - len(content))]
    self.letters = self.read_content_string(content)

    self.neighbours = {(x,y) : self.get_neighbours(x,y) for x in range(self.width) for y in range(self.height)}

  def read_content_string(self, content):
    letters = [content[i : i+self.width] for i in range(0,self.height*self.width,self.width )]
    # letters =
    return letters


  def get_neighbours(self, x, y):
    """Neighbours of a square.
       Cartesian, non diagonal, no wraparound
    """
    neighbours = [(x + dx, y+dy) for dx in [-1,0,1] for dy in [-1,0,1]
                   if  0 <= x+dx < self.width # Borders x
                   and 0 <= y+dy < self.height# Borders y
                   # and dx * dy == 0           # Not diagonal
                   and not (dx == 0 and dy == 0) # Not itself
                   ]
    neighbouring_letters = [self[x,y] for x, y in neighbours]
    return neighbours#, neighbouring_letters

  def __getitem__(self, key):
    x,y = key
    return self.letters[y][x]


  def __setitem__(self, key, value):
    x,y = key
    self.letters[y][x] = value

  def __str__(self):
    retstr  = '\n ┏'+(2*self.width-1)*'━'+'┓\n ┃'
    retstr += '\n ┃'.join([' '.join(row) +'┃' for row in self.letters])
    retstr += '\n ┗'+(2*self.width-1)*'━'+'┛\n'
    return retstr



class Solver():
  def __init__(self, dict_path):
    self.dictionary = PrefixTree()
    self.load_dict(dict_path)
    pass

  def solve(self, board):
    """Start the solver from every square"""
    sol_set = set()
    for x in range(board.width):
      for y in range(board.height):
        for s in self.solve_from(board, (x,y), prefix = '', visited = []):
          if s not in sol_set:
            sol_set.add(s)
            yield s

  def solve_from(self, board, fromsquare = (0,0), prefix = '', visited = [], ptree = None ):
    newletter = board[fromsquare]
    word = prefix + newletter
    visited += [fromsquare]

    if not ptree:
      is_word, ptree = self.dictionary[word]
    else: # Optimise: Reuse the previous ptree
      is_word, ptree = ptree[newletter]


    if is_word:
      yield word
    if len(ptree) == 0:
      # Stop recursing
      return None

    for nb in board.neighbours[fromsquare]: #Optimise: Refactor list-comprehension
      if nb not in visited:
        yield from self.solve_from(board, nb, word, visited, ptree)

  def load_dict(self, dict_path):
    with open(dict_path, 'r') as f:
      wordlist= dictionary = set(f.read().split('\n')) # Simpler than readlines(), because of line breaks

    for word in wordlist:
      self.dictionary.add_word(word)


def profile_me():
  S = Solver('english.txt')
  for i in range(1000):
    B = Board(4,4, content = '')
    sols = S.solve(B)
    list(sols)


if __name__ == "__main__":

  S = Solver('english.txt')

  B = Board(4,4, content = 'iled vrdv oery nlsa')
  # B = Board(4,4, content = 'iled vrdv nlsa')

  print(B)
  print(sorted(list(S.solve(B))))
  # print(B)

  # print('wordcount: {}\nscore    : {}'.format(len(solutions), S.score))