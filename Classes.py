import random

from bookie import flag

class Player:
  def __init__(self, record):
    if type(record[0]) is not str:
      raise InitError(str(name)+" is not a valid name.")
    self.name = record[0]
    self.matches = record[1] if len(record)>1 else [] # matches are tuples of [opponent[s]_rating, result]
    self.strength = random.random() # in simulations, estimates chances of winning
    self.rating = 1000
    self.calculate_standing()
  
  # Allows class to be sorted by rating
  def __lt__(self, other):
    return other.rating < self.rating
  
  def calculate_standing(self):
    # Calculates a player's total standing
    # from scratch every time
    # based on player's self.matches record
    self.wins = 0
    self.losses = 0
    self.ties = 0
    for match in self.matches:
      # ELO rating system
      self.adjust_rating(match)
  
  def adjust_rating(self, match=None):
    # adjusts rating according to individual match
    # using a 'match' in form of [rating, outcome]
    if match is None:
      match = self.matches[-1]
    # for bug chess:
    # [ratings[], outcome[]]
    # where outcome=[team#, result]
    # result is for team 1
    if flag["bug"]:
      team_averages = []
      team_averages.append(int((match[0][0]+match[0][1])/2)) # Team 1 is team_averages[0]
      team_averages.append(int((match[0][2]+match[0][3])/2)) # Team 2 is team_averages[1]
      average_difference = abs(team_averages[0] - team_averages[1])
      win_probability = 1/(pow(10,average_difference/400)+1)
      point_exchange = 0
      # using %2 to change team without knowing current team
      if((team_averages[0] <= team_averages[1] and match[1][1]) or
        (team_averages[0] >= team_averages[1] and not match[1][1])):
        # Underdog team won
        # or Expected team loses
        point_exchange = 2*int(32*(1-win_probability)) # 2x because 2 players split points
      elif((team_averages[0] >= team_averages[1] and match[1][1]) or
        (team_averages[0] <= team_averages[1] and not match[1][1])):
        # Underdog team loses
        # or Expected team wins
        point_exchange = 2*int(32*win_probability)
      else: #Ties should not happen in Bug Chess
        raise ChessError("Tie game in bug chess. Something went wrong.")
        #########################
       # Modify ELO value here #
      #########################
      ## Bug Rating Theory
      # R1: self     R2: teammate
      # R3: 1st opp  R4: 2nd opp
      # avg : calculated from avg team ratings
      #       as seen above
      # (R2+R4)*(R2)*2(ELO[avg])
      # -------------------
      # (R1+R3)*(R1+R2)
      #
      # validity = (R2+R4)/(R1+R3)
      # carry_weight = (R2)/(R1+R2)
      validity = (match[0][1]+match[0][3])/(match[0][0]+match[0][2])
      # Determining R2
      #                            V if self rating is first player on team, use other rating
      R2 = match[0][2*match[1][0]+(1 if self.rating == match[0][2*match[1][0]] else 0)]
      team_average = match[0][2*match[1][0]]+match[0][2*match[1][0]+1]
      carry_weight = (2*R2/(2*team_average))
      points = int(round(int(round(validity*point_exchange))*carry_weight)) # int() truncates by default
      if flag["loud"]:
        print("    {0}pts: {1:.2f}*{2:4}/{3:4}*{4:.0f}".format(points, validity, R2, team_average, point_exchange))
      if(match[1][0] is 0 and match[1][1] or
        match[1][0] is 1 and not match[1][1]):
        # Player wins
        self.rating += points
        self.wins += 1
      else: # No ties possible, only outcome is loss
        self.rating -= points
        self.losses += 1
    else:
      win_probability = 1/(pow(10,(abs(match[0]-self.rating)/400))+1)
      point_exchange = 0
      if (self.rating <= match[0] and match[1] is True) or (self.rating >= match[0] and match[1] is False):
        # Underdog and wins
        # or Expected and loses
        point_exchange = int(32*(1 - win_probability)) # PE(u)
      elif (self.rating >= match[0] and match[1] is True) or (self.rating <= match[0] and match[1] is False):
        ######### "or equal" because tied ratings work with either equation
        # Underdog/Even and loses
        # or Expected/Even and wins
        point_exchange = int(32*win_probability) # PE(e)
      else: # should only occur for match[1] is None: a tie
        point_exchange = int(16*(1-2*win_probability)) # simplification of (PE(u) - PE(e))/2
      if flag["loud"]:
        print("    {0}pts ({1} vs {2})-{3:.0f}%".format(point_exchange,self.rating,match[0],100*win_probability))
      if match[1] is True: # Won
        self.rating += point_exchange
        self.wins += 1
      elif match[1] is False: # Lost
        self.rating -= point_exchange
        self.losses += 1
      else: # Tied
        # points are either gained or lost depending on difference between self and opponent ratings
        self.rating = (self.rating + point_exchange) if self.rating < match[0] else (self.rating - point_exchange)
        self.ties += 1
  
  def add_match(self, opponent_rating, outcome):
    self.matches.append([opponent_rating, outcome])
  
  def report(self, requested="summary"):
    string = ""
    if requested == "name":
      string += self.name
    elif requested == "summary":
      string += "({0:4}:{1:2.0f})  {2:20}".format(self.rating, 100*self.strength, self.name)
      string += "  W-{0:4}  L-{1:4}  T-{2:4}".format(self.wins, self.losses, self.ties)
    elif requested == "rating":
      return int(self.rating)
    elif requested == "matches":
      for match in self.matches:
        string += str(match[0])+" "+str(match[1])+","
      string = string[:-1] # remove final ","
    elif requested == "strength":
      return float(self.strength)
    elif requested == "wins":
      return int(self.wins)
    elif requested == "losses":
      return int(self.losses)
    elif requested == "ties":
      return int(self.ties)
    elif requested == "file":
      string += self.report("name")+";"
      string += self.report("matches")
    else:
      string += "ARG AN ERROR KILL IT WITH FIRE!"
    return string

class Match:
  def check_players(self):
    if type(self.players) is not list:
      raise InitError(str(self.players)+" is not a valid list of players.")
    if len(self.players) is not 2:
      raise InitError(str(self.players)+" is "+("not long enough." if len(self.players)<2 else "too long."))
  
  @staticmethod
  def set_ratings(players, outcome):
    # 2-player game, standard outcome resolution per ELO
    players[0].add_match(players[1].report("rating"), outcome)
    players[1].add_match(players[0].report("rating"), (not outcome) if outcome is not None else outcome)
    players[0].adjust_rating()
    players[1].adjust_rating()
  
  def __init__(self, player_list, outcome="Nope"):
    self.players = player_list
    self.check_players()
    self.result = outcome
    if type(self.result) is bool or self.result is None:
      self.resolve(self.result)
  
  def resolve(self, outcome):
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
    elif requested == "players":
      return self.players
    elif requested == "result":
      return self.result
    elif requested == "file":
      string += self.report("name")+";"
      string += str(self.report("result"))
    else:
      string += "ARG AN ERROR KILL IT WITH FIRE!"
    return string

class BBMatch(Match):
  def check_players(self):
    if type(self.players) is not list:
      raise InitError(str(self.players)+" is not a valid list of players.")
    if len(self.players) is not 4:
      raise InitError(str(self.players)+" is "+("not long enough." if len(self.players)<4 else "too long."))
  
  @staticmethod
  def set_ratings(players, outcome):
    # 4-player 'bug-out' chess match
    # Players rated against average opponent
    # players should be in known sorted form
    # as per check_players() sorting
    ratings = []
    ratings.extend(list(player.report("rating") for player in players))
    for player in players:
      player.add_match(ratings, [(0 if player in players[:2] else 1), outcome])
    for player in players:
      player.adjust_rating()

class ChessError(Warning):
  def __init__(self, string="An unidentified Chess Error has occurred!"):
    self.strerror = string

class InitError(ChessError):
  def __init__(self, string=""):
    self.strerror = "Initilization failed: "+string

   #################
  # Silly Things  #
 # Because Bored #
#################
player_name_list = [
  "Bobbie McGee",
  "Kelso Feltso",
  "Samwise Gainsee",
  "The One",
  "Uncle Bruster",
  "DaGirl NextDoor",
  "Chez Prodijay",
  "Notta Bot",
  "Nerdy Boi",
  "My Roommate",
  "George Washington",
  "John Adams",
  "Alexander Hamilton",
  "Napoleon Bonaparte",
  "Julius Caesar",
  "AppleBottom Jeans",
  "Boots WitDaFur",
  "Gandalf Greatname",
  "Unworthy Opponent",
  "Smart Squirrel",
  "Poor Loser",
  "Deep Blue",
  "Arlet Sarsonel",
  "Valley Girl",
  "Earl Bootlicker",
  "Jack Aronda",
  "Thum Bollina"]