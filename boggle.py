import random as rng


# Todo:
  # Dictionary tree
  # Evolutionary board

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
    pass

  def read_content_string(self, content):
    letters = [content[i : i+self.width] for i in range(0,self.height*self.width,self.width )]
    # letters =
    return letters

  @memoize
  def neighbours(self, x, y):
    """Neighbours of a square.
       Cartesian, non diagonal, no wraparound
    """
    neighbours = [(x + dx, y+dy) for dx in [-1,0,1] for dy in [-1,0,1]
                   if  0 <= x+dx < self.width # Borders x
                   and 0 <= y+dy < self.height# Borders y
                   # and dx * dy == 0           # Not diagonal
                   and not (dx == 0 and dy == 0) # Not itself
                   ]
    # neighbouring_letters = [self[x,y] for x, y in neighbours]
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
    self.solution_set = set()
    self.score = 0
    for x in range(board.width):
      for y in range(board.height):
        for s in self.solve_from(board, (x,y), prefix = '', visited = []):
          if s not in self.solution_set:
            self.solution_set.add(s)
            self.score += self.score_word(s)
            yield s

  def score_word(self, word):
    length = len(word)
    if length>= 8: return 11
    return [0,0,0,1,1,2,3,5][length]

  def solve_from(self, board, fromsquare = (0,0), prefix = '', visited = [] ):
    newletter = board[fromsquare]
    word = prefix + newletter
    visited += [fromsquare]


    is_word, PTree = self.dictionary[word]

    if is_word:
      yield word
    if len(PTree) == 0:
      # Stop recursing
      return None

    neighbours = [nb for nb in board.neighbours(*fromsquare)
                  if nb not in visited]
    for nb in neighbours:
      yield from self.solve_from(board, nb, word, visited)

  def load_dict(self, dict_path):
    with open(dict_path, 'r') as f:
      wordlist= dictionary = set(f.read().split('\n')) # Simpler than readlines(), because of line breaks

    for word in wordlist:
      self.dictionary.add_word(word)


if __name__ == "__main__":

  S = Solver('english.txt')


  B = Board(4,4, content = '')
  print(B)

  solutions = sorted(S.solve(B), key = lambda x : -len(x))
  print('wordcount: {}\nscore    : {}'.format(len(solutions), S.score))
  print(' '.join(solutions))