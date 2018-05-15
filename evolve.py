from boggle import Board, Solver, alphabet, rng


pop_size = 2000
iter_count = 3000

elite_size      = 30*pop_size // 100 # Elite top that gets to stay
lucky_size      =  5*pop_size // 100 # Lucky remainder that also gets to stay
crossover_size  = 20*pop_size // 100 # Number of bred agents



SIZE = (4,4)

S = Solver('english.txt')


class Agent():
  def __init__(self, board = None):

    if not board:
      # Iniate random
      self.ftype = Board(*SIZE) #Fenotype
    else:
      self.ftype = board

    self.gtype = ''.join([''.join(line) for line in self.ftype.letters]) #Genotype
    self.score = self.calc_score() #Fitness

  def crossover_with(self, other, swap_prob = .4):
    content = ''
    swapper = 0
    for c1, c2 in zip(self.gtype, other.gtype):
      c = [c1,c2][swapper]
      content += c
      swapper = 1-swapper if rng.random()<swap_prob else swapper
    b = Board(*SIZE, content = content)
    return Agent(board = b)
    # return new agent

  def mutate(self, probability = .3):
    content = ''
    for c in self.gtype:
      if rng.random()<probability:
        c = rng.choice(alphabet)
      content += c
    b = Board(*SIZE, content= content)
    return Agent(board = b)

  def calc_score(self):
    def score(word):
      # return 1 # emphasis on number of results
      # return 3**len(word) # heavy emphasis on word length
      length = len(word)
      if length>= 8: return 11
      # return [0,0,0,1,1,2,3,5][length] # Original scoring
      return [0,0,0,0,1,2,5,7][length] # Emphasis on longer words

    total_score = 0
    solution_set = set()
    for word in S.solve(self.ftype):
      if word not in solution_set:
        solution_set.add(word)
        total_score += score(word)
    # self.score = total_score
    return total_score


def diversify(population, remove_duplicate_prob = .5):
  gtype_set = set()
  remove_index = set()
  for i,p in enumerate(population):
    if p.gtype in gtype_set:
      if rng.random()<=remove_duplicate_prob:
        remove_index.add(i)
    else:
      gtype_set.add(p.gtype)
  return [p for i,p in enumerate(population) if i not in remove_index], len(gtype_set)




if __name__ == "__main__":

  population = [Agent() for i in range(pop_size//2)]
  population += [Agent(Board(*SIZE, content = 'iledversofylcerp')).mutate() for i in range(pop_size//2)]
  unique = pop_size
  for i in range(iter_count):
    # Sort new pop, trim or append to pop_size
    population = sorted(population, key = lambda p: -p.score)

    # Diversify by killing off some duplicates
    population, unique = diversify(population, remove_duplicate_prob = 0.33)
    # Complete or trim to pop size
    population += [Agent() for i in range(pop_size - len(population))]
    population = population[:pop_size]
    assert len(population) == pop_size

    # Report stats
    print(i, unique, [p.score for p in population[:5]])

    #Get elites and luckies
    elites = population[:elite_size]
    lucky = [rng.choice(population[elite_size:]) for i in range(lucky_size)]
    population = elites + lucky

    # Mutate all elites and lucky remainder once.
    population += [a.mutate() for a in elites]
    population += [a.mutate() for a in lucky]

    # Crossover (elites and lucky twice)
    newly_breds = []
    while len(newly_breds) < crossover_size:
      a1 = rng.choice(elites + lucky + lucky)
      a2 = rng.choice(elites + lucky + lucky)
      if a1.gtype != a2.gtype: # only if diverse
        newly_breds.append(a1.crossover_with(a2))
    population += newly_breds

    if i%100==0:
      print(population[0].ftype)


  population, unique = diversify(population, remove_duplicate_prob = 1)
  winner = population[0].ftype
  print(winner, population[0].score)
  print(sorted(list(S.solve(winner)), key = lambda w : -len(w)))

  winner = population[1].ftype
  print(winner, population[1].score)
  print(sorted(list(S.solve(winner)), key = lambda w : -len(w)))