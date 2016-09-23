# Bug-Board Official Automated Rating Database
import sys
import random


    ########
   # ToDo #
  ########
# Oh god so much

# Flags
flag = {"simulate" : False,
        "loud"     : False}
from Classes import *

def do_things():
  if flag["simulate"]:
    matches = run_games(create_players(20), 1000)
    display_results(matches)
    pass
  pass

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
    playing = random.sample(players, 2)
    playing.sort()
    if flag["loud"]:
      print(playing[0].report("name")+" vs "+playing[1].report("name"))
    win_chance = .5+(playing[0].report("strength")-playing[1].report("strength"))
    outcome = True if random.random() < win_chance else False
    if flag["loud"]:
      print("   - "+playing[0].report("name")+" "+("wins!" if outcome else "tied!" if outcome is None else "loses!"))
      print("     ({0:.2f}-{1:.2f}) = {2:.2f}".format(playing[0].report("strength"),playing[1].report("strength"),win_chance))
      print("  - Match Summary:")
    match = Match(playing, outcome)
    match_list.append(match)
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
  if not flag["loud"]:
    total_points = 0
    for player in player_list:
      total_points += player.report("rating")
      print(player.report())
    print("Points per player: {0:.0f}".format(total_points/len(player_list)))


if __name__ == "__main__":
  try:
    commands = sys.argv[1:]
    command_count = 0
    for command in commands:
      if command in flag:
        flag[command] = True
        command_count += 1
      else:
        raise ChessError("Invalid command sent: "+command)
    do_things()
  except KeyboardInterupt as KI:
    print("~~~~~~~~~~~~~~~~~~~~~~Ok Bye!~~~~~~~~~~~~~~~~~~~")