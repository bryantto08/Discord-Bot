from datetime import datetime
import json
import random
from discord.ext import commands


def change_to_timestamp(time):
    timestamp = datetime.fromtimestamp(time)
    return timestamp


# finds the champion that corresponds to the key in the data_dragon.json file
def find_champ(key):
    json_file = open("data_dragon.json", "r", encoding="utf-8")
    data_dragon = json.load(json_file)
    for i in data_dragon["data"]:
        if data_dragon["data"][i]["key"] == str(key):
            return i


# Turns champ_mastery dictionary into readable and easy to add string
def champ_mastery_string(player_dict, embed):
    champ = find_champ(player_dict["championId"])
    champ_level = player_dict["championLevel"]
    champ_points = player_dict["championPoints"]
    last_played = change_to_timestamp((player_dict["lastPlayTime"])/1000.0)
    champ_points_til_next_level = player_dict["championPointsUntilNextLevel"]
    chest_granted = player_dict["chestGranted"]
    embed.add_field(
        name=champ + " (Level " + str(champ_level) + ")",
        value="Champion Points: " + str(champ_points) + " | " + "Last Played: " + str(last_played),
        inline=False
    )


def summoner_string(player_dict):
    queue_type = player_dict["queueType"]
    tier = player_dict["tier"]
    rank = player_dict["rank"]
    my_string = queue_type + ": " + tier + " " + rank
    return my_string


# Takes the multikill int and converts it to proper string
def multikill_converter(num):
    if num == 0:
        return "No Kills"
    if num == 1:
        return "Single Kill"
    if num == 2:
        return "Double Kill"
    if num == 3:
        return "Triple Kill"
    if num == 4:
        return "Quadra Kill"
    if num == 5:
        return "Penta Kill"
    else:
        return "wtf"


def match_history_string(match_dict, summoner, embed):
    game_mode = match_dict["info"]["gameMode"]
    for i in range(len(match_dict["info"]["participants"])):
        match = match_dict["info"]["participants"][i]["summonerName"].replace(" ", "")
        if match.lower() == summoner.lower():
            summonerName = match_dict["info"]["participants"][i]

    kills = summonerName["kills"]
    deaths = summonerName["deaths"]
    assists = summonerName["assists"]
    champion = summonerName["championName"]
    position = summonerName["teamPosition"]

    # Changing the name of utility to support
    if position == "UTILITY":
        position == "SUPPORT"

    largest_multi_kill = multikill_converter(summonerName["largestMultiKill"])
    kda = str(kills) + "/" + str(deaths) + "/" + str(assists)
    if summonerName["win"]:
        result = "Win"
    else:
        result = "Loss"
    points = point_tracker(deaths, largest_multi_kill, result, position)
    # ARAM doesn't contain Role
    if game_mode == "ARAM":
        embed.add_field(
            name="Game Mode: " + game_mode + ", Result: " + result + ", Points: " + str(points),
            value="Champion: " + champion + ", KDA: " + kda + ", Multikill: " + largest_multi_kill,
            inline=False
        )
    else:
        embed.add_field(
            name="Game Mode: " + game_mode + ", Result: " + result + ", Points: " + str(points),
            value="Role: " + position + ", Champion: " + champion + ", KDA: " + kda + ", Multikill: " + largest_multi_kill,
            inline=False
        )


# Calculates the number of points gained from the specific league game
def point_tracker(deaths, largest_multi_kill, win, is_support):
    points = 0
    if win == "Win" and is_support == "SUPPORT":
        points += 100
    elif win == "Win":
        points += 10

    if largest_multi_kill == "Double Kill":
        points += 50
    elif largest_multi_kill == "Triple Kill":
        points += 200
    elif largest_multi_kill == "Quadra Kill":
        points += 1000
    elif largest_multi_kill == "Penta Kill":
        points += 15000
    if deaths == 0 and is_support == "SUPPORT":
        points += 5000
    elif deaths == 0:
        points += 500
    if (deaths - 10) > 0:
        d = deaths - 10
        points -= 100
        for i in range(d):
            points -= 10

    return points


def sus_check():
    count = random.randint(1, 10)
    if count == 3:
        return True


