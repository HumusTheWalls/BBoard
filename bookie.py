# Bug-Board Official Automated Rating Database
import sys
import random
import time


    ########
   # ToDo #
  ########
# Oh god so much

# Flags
flag = {"loud"     : False,
        "bug"      : False,
        "players"  : 10,
        "games"    : 100}
from Classes import *

def do_things():
  if flag["loud"] and flag["games"] > 100:
    response = ""
    while response != ("y" or "yes" or "n" or "no"):
      response = input("Warning: Games take .5 secs each. The {0} games selected will take {1} seconds. Continue?".format(flag["games"],flag["games"]/2))
      if response == ("n" or "no"):
        raise ChessError("Please choose a smaller batch of games, or turn off 'loud' flag.")
  matches = run_games(create_players(flag["players"]), flag["games"])
  display_results(matches)

def create_players(count):
  player_list = []
  if flag["loud"]:
    print("Players:")
  for i in range(count):
    player_list.append(Player([str("Player "+str(i))]))
    if flag["loud"]:
      print("{0} at strength {1:.2f}".format(player_list[-1].report("name"),player_list[-1].report("strength")))
  return player_list

def run_games(players, game_count):
  match_list = []
  if flag["loud"]:
    print("") # separating line for clarity
  for i in range(game_count):
    if not flag["loud"]:
      print("Match {0}".format(i), end="\r") # placeswrite-point at beginning of line
    else:
      print("Match {0}".format(i))
    match = None
    if flag["bug"]:
      playing = random.sample(players, 4)
      team_one = playing[:2]
      team_one.sort()
      team_two = playing[2:]
      team_two.sort()
      playing.clear()
      playing.extend(team_one)
      playing.extend(team_two)
      if flag["loud"]:
        string = ""
        for player in team_one:
          string += player.report("name")+","
        string = string[:-1]
        string += " vs "
        for player in team_two:
          string += player.report("name")+","
        string= string[:-1]
        print(string)
      team_one_strength = (team_one[0].report("strength")+team_one[1].report("strength"))/2
      team_two_strength = (team_two[0].report("strength")+team_two[1].report("strength"))/2
      win_chance = .5+2*(team_one_strength - team_two_strength)
      outcome = True if random.random() < win_chance else False #True = team one wins
      if flag["loud"]:
        print("   - Team "+("One" if outcome else "None" if outcome is None else "Two")+" wins!")
        print("     {0:.2f}-{1:.2f} = {2:.2f}".format(team_one_strength, team_two_strength, win_chance))
        print("  - Match Summary:")
      match = BBMatch(playing, outcome)
    else:
      playing = random.sample(players, 2)
      playing.sort()
      if flag["loud"]:
        print(playing[0].report("name")+" vs "+playing[1].report("name"))
      win_chance = .5+2*(playing[0].report("strength")-playing[1].report("strength"))
      outcome = True if random.random() < win_chance else False
      if flag["loud"]:
        print("   - "+playing[0].report("name")+" "+("wins!" if outcome else "tied!" if outcome is None else "loses!"))
        print("     ({0:.2f}-{1:.2f}) = {2:.2f}".format(playing[0].report("strength"),playing[1].report("strength"),win_chance))
        print("  - Match Summary:")
      match = Match(playing, outcome)
    match_list.append(match)
    if flag["loud"]:
      time.sleep(.5) # artificial pacing to remove server lag
    else:
      time.sleep(.1)
  return match_list

def display_results(match_list):
  player_list = []
  for match in match_list:
    players = match.report("players")
    for player in players:
      try:
        player_list.index(player)
      except ValueError:
        player_list.append(player)
  player_list.sort()
  #if not flag["loud"]:
  total_points = 0
  for player in player_list:
    total_points += player.report("rating")
    print(player.report())
  print("Points per player: {0:.0f}".format(total_points/len(player_list)))


if __name__ == "__main__":
  try:
    commands = sys.argv[1:]
    i = 0
    while(i < len(commands)):
      if commands[i] in flag:
        if type(flag[commands[i]]) is bool:
          flag[commands[i]] = True
        if type(flag[commands[i]]) is int: # some flags can take arguments
          flag[commands[i]] = int(commands[i+1])
          i += 1
      else:
        raise ChessError("Invalid command sent: "+commands[i])
      i += 1
    do_things()
  except KeyboardInterrupt as KI:
    print("~~~~~~~~~~~~~~~~~~~~~~Ok Bye!~~~~~~~~~~~~~~~~~~~")