import random as rng

rng.seed(1)


class Dice():
  """
  Dice class for random letter gnereation
  Iterable for multiple casts
  """
  def __init__(self):
    self.letterset = 'abcdefghijklmnopqrstuvwxyz'
    pass

  def cast(self):
    return rng.choice(self.letterset)

  def __iter__(self):
    return self

  def __next__(self):
    return self.cast()



class Board():
  """
  Board class to contain a grid of letters
  Filled by the Dice class
  """
  def __init__(self, width = 4, height = 4):
    self.width, self.height = width, height
    # Lettergrid. Acces with letters[x][y]
    self.letters = self.assign_letters()
    pass

  def assign_letters(self, dice = None):
    if not dice:
      dice = Dice()

    letters = [[next(dice) for y in range(self.height)] for x in range(self.width)]
    return letters

  def neighbours(self, x, y):
    """Neighbours of a field.
       Cartesian, non diagonal, no wraparound
    """
    neighbours = [[x + dx, y+dy] for dx in [-1,0,1] for dy in [-1,0,1]
                   if  0 <= x+dx < self.width # Borders x
                   and 0 <= y+dy < self.height# Borders y
                   and dx * dy == 0           # Not diagonal
                   and not (dx == 0 and dy == 0) # Not itself
                   ]
    neighbouring_letters = [self.letters[x][y] for x, y in neighbours]
    return neighbours, neighbouring_letters


class Solver():
  def __init__(self, board, dictionary):
    self.board = board
    self.dictionary = dictionary
    pass

  def solve(self):
    pass



if __name__ == "__main__":
  B = Board()
  B.assign_letters()

  print(B.neighbours(2,2))


