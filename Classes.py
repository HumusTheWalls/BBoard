

class Player:
  
  
  def __init__(record):
    if type(record[0]) is not str:
      raise InitError(str(name)+" is not a valid name.")
    self.name = record[0]
    self.matches = record[1] if len(record)>1 else [] # matches are tuples of [opponent_rating, result]
    self.calculate_standing()
  
  def calculate_standing():
    self.wins = 0
    self.losses = 0
    self.ties = 0
    self.total_opponent_rating = 0
    for match in self.matches:
      self.total_opponent_rating += match[0]
      if match[1] is True:
        self.wins += 1
      elif match[1] is False:
        self.losses += 1
      else:
        self.ties += 1
    if len(self.matches):
      self.rating = (self.total_opponent_rating + 400(self.wins-self.losses))/len(self.matches)
    else:
      self.rating = 1000
  
  def add_match(self, opponent_rating, outcome):
    if type(opponent_rating) is not int or type(outcome) is not bool:
      raise ChessError("Invalid match passed: "+str(outcome)+": "+str(opponent_rating))
    self.matches.append([opponent_rating, outcome])
    self.calculate_standing()
  
  def report(self, requested="name"):
    string = ""
    if requested == "name":
      string += self.name
    elif requested == "rating":
      return self.rating
    elif requested == "matches":
      for match in self.matches:
        string += str(match[0])+" "+str(match[1])+","
        string = string[:-1] # remove final ","
    elif requested == "wins":
      return self.wins
    elif requested == "losses":
      return self.losses
    elif requested == "ties":
      return self.ties
    elif requested == "file":
      string += self.report("name")+";"
      string += self.report("matches")
    return string

class Match:
  
  
  @staticmethod
  def check_players(player_list):
    if type(player_list) is not list:
      raise InitError(str(player_list)+" is not a valid list of players.")
    if len(player_list) is not 2:
      raise InitError(str(player_list)+" is "+("not long enough." if len(player_list)<2 else "too long."))
  
  @staticmethod
  def set_ratings(players, outcome):
    # 2-player game, standard outcome resolution per ELO
    player[0].add_match(player[1].report("rating"), outcome)
    player[1].add_match(player[0].report("rating"), outcome)
  
  def __init__(player_list, outcome="Nope"):
    check_players(player_list)
    self.players = player_list
    self.result = outcome
    if type(self.result) is bool:
      self.resolve(self.result)
  
  def resolve(self, outcome):
    if type(outcome) is not bool:
      raise ChessError("No valid result was passed.")
    self.result = outcome
      ##############################
     # Tell players what happened #
    ##############################
    self.set_ratings(self.players, self.result)
  
  def report(self, requested="name"):
    string = ""
    if requested == "name":
      for player in self.players:
        string += player.report("name")+", "
      string = string[:-2] # remove last ", "
    elif requested == "result":
      return self.result
    elif requested == "file":
      string += self.report("name")+";"
      string += str(self.report("result"))
    return string


class ChessError(Warning):
  def __init__(self, string="An unidentified Chess Error has occurred!"):
    self.strerror = string

class InitError(ChessError):
  def __init__(self, string=""):
    self.strerror = "Initilization failed: "+string