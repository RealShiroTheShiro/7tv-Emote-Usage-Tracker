#
# Code related to data processing.
#


# imports
import json
import re
import gzip
import os
from datetime import datetime
from datetime import date
import time


# Decelerations
livestreamID = 1
EmoteSetID = "63897e65bf900727661286f2"


# Counts appearances of sub string in string.
def betterCount(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count += 1
        else:
            return count


# Reads logged chat messages and outputs them in a list of dicts with separated entries for time, channel, username and message.
def readLog(file):
    data = []

    # Reads logged messaged.
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n')

        # Parsing and reformatting.
        for line in lines:
            try:

                time_logged = line.split('—')[0].strip()
                time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')

                username_message = line.split('—')[1:]
                username_message = '—'.join(username_message).strip()

                matches = re.findall( ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #([^:]*) :(.*)', username_message)
                for match in matches:
                    username, channel, message = match
                    d = {
                        'dt': time_logged,
                        'channel': channel,
                        'username': username,
                        'message': message
                    }
                    data.append(d)

            except Exception:
                print("execption raised")
                pass

    return data


#  Main function, emote usage analysis handler.
def emoteUsageHandler():
    #
    # Decelerations And Set-Up
    #

    # Decelerations
    global livestreamID


    # Gets enabled 7tv emote list using 7tv api.
    while True:
        response = requests.get("https://7tv.io/v3/emote-sets/" + EmoteSetID)
        try:
            emoteList = [item["name"] for item in response.json()["emotes"]]
            break
        except:
            time.sleep(5)


    # Loads previous data.
    with open("Emote Stats.txt", 'r', encoding='utf-8') as f:
        emoteStats = json.load(f)
    data = get_chat_dataframe("chat.log")


    #
    # Main Handler
    #


    # New/Removed emote management.
    for emote in emoteList:
        if emote not in emoteStats.keys():
            emoteStats[emote] = [0, 0]

    tempList = []
    for emote in emoteStats.keys():
        if emote not in emoteList:
            tempList.append(emote)

    for emote in tempList:
        emoteStats.pop(emote)


    # Process new data for emote usage.
    for item in data:
        for emote in emoteList:
            if " " + emote + " " in item["message"] or item["message"].startswith(emote + " ") or item["message"].endswith(" " + emote) or item["message"] == emote:
                emoteStats[emote][0] += 1
                if item["message"] == emote:
                    emoteStats[emote][1] += 1
                else:
                    emoteStats[emote][1] += betterCount(item["message"], " " + emote + " ")
                    if item["message"].startswith(emote + " "):
                        emoteStats[emote][1] += 1
                    if item["message"].endswith(" " + emote):
                        emoteStats[emote][1] += 1


    # Outputs updated data and creates a compressed log of chat.
    location = os.getcwd() + '/Emote Stats History/Stream ' + str(livestreamID) + ' - ' + str(date.today())
    os.makedirs(location)

    with open('chat.log', 'rb') as f_in, gzip.open(location + '/chat.log.gz', 'wb') as f_out:
        f_out.writelines(f_in)
    with open('Emote Stats.txt', 'rb') as f_in, gzip.open(location + '/Pre Stream Stats.txt.gz', 'wb') as f_out:
        f_out.writelines(f_in)

    open('chat.log', 'w').close()

    with open("Emote Stats.txt", 'w', encoding='utf-8') as f:
        json.dump(emoteStats, f)

    livestreamID += 1
