from datetime import datetime
import json
import random


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
def champ_mastery_string(player_dict):
    champ = find_champ(player_dict["championId"])
    champ_level = player_dict["championLevel"]
    champ_points = player_dict["championPoints"]
    last_played = change_to_timestamp((player_dict["lastPlayTime"])/1000.0)
    champ_points_til_next_level = player_dict["championPointsUntilNextLevel"]
    chest_granted = player_dict["chestGranted"]
    champ_string = "Champion: " + champ + " | " + "Champion Level: " + str(champ_level) + " | " \
                   "Champion Points: " + str(champ_points) + " | " + "Last Played: " + str(last_played)
    return champ_string


def summoner_string(player_dict):
    queue_type = player_dict["queueType"]
    tier = player_dict["tier"]
    rank = player_dict["rank"]
    my_string = queue_type + ": " + tier + " " + rank
    return my_string

def match_history_string(match_dict, summoner):
    game_mode = match_dict["info"]["gameMode"]
    for i in range(len(match_dict["info"]["participants"])):
        match = match_dict["info"]["participants"][i]["summonerName"].replace(" ", "")
        if match.lower() == summoner.lower():
            summonerName = match_dict["info"]["participants"][i]

    kills = summonerName["kills"]
    deaths = summonerName["deaths"]
    assists = summonerName["assists"]
    kda = str(kills) + "/" + str(deaths) + "/" + str(assists)
    if summonerName["win"]:
        result = "Win"
    else:
        result = "Loss"
    my_string = "Game Mode: " + game_mode + ", KDA: " + kda + ", Result: " + result
    return my_string


def sus_check():
    count = random.randint(1,10)
    if count == 3:
        return True


