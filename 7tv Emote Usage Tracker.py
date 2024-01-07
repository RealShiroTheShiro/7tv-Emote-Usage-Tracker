# Counting 7tv emote usage bot.

# Imports
#import socket
#import logging
#import requests
from multiprocessing import Process
#import time
'''
from datetime import date
from datetime import datetime
import json
import re
import gzip
import os
'''
import threading

# Declarations
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'ShiroTheShiro'
token = 'oauth:lktxd96xj4qu2g6fl2zi5pavq5m3l7'
channel = '#avast'
channelName = 'avast'
avastTwitchID = 32905366
#avastEmoteSetID = "63897e65bf900727661286f2"
liveFlag = False
liveFlagLock = threading.Lock()
#livestreamID = 1

"""
# Socket Set-up
sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

# Logger Set-up
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])
"""
"""
def checkIfUserIsStreaming(username):
    url = "https://gql.twitch.tv/gql"
    query = "query {\n  user(login: \""+username+"\") {\n    stream {\n      id\n    }\n  }\n}"
    return True if requests.request("POST", url, json={"query": query, "variables": {}}, headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}).json()["data"]["user"]["stream"] else False
"""

'''
def betterCount(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count += 1
        else:
            return count


def get_chat_dataframe(file):
    data = []

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n')

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
*/
'''

"""
def UpdateLiveFlag():
    global liveFlag
    counter = 0

    # Check Livestream Status.
    while True:
        if checkIfUserIsStreaming(channelName):
            counter = 0
            liveFlag = True
            time.sleep(10)
        else:
            if liveFlag == True:
                counter += 1
                time.sleep(10)
            if counter == 5:
                counter = 0
                liveFlag = False
                EmoteStatsHandler()
            time.sleep(1)
"""


"""
# Logger Loop Wrapper Function.
def LoggerFunction():
    global liveFlag
    global sock

    while True:
        resp = sock.recv(2048).decode('utf-8')

        # Messsage Handler.
        if resp == 0:
            sock = socket.socket()
            sock.connect((server, port))
            sock.send(f"PASS {token}\n".encode('utf-8'))
            sock.send(f"NICK {nickname}\n".encode('utf-8'))
            sock.send(f"JOIN {channel}\n".encode('utf-8'))

        elif resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0 and liveFlag:
            logging.info(resp)
"""

'''
# Emote Statistical Analysis
def EmoteStatsHandler():
    # Decelerations And Set-Up
    global livestreamID

    while True:
        response = requests.get("https://7tv.io/v3/emote-sets/" + avastEmoteSetID)
        try:
            emoteList = [item["name"] for item in response.json()["emotes"]]
            break
        except:
            time.sleep(5)

    with open("Emote Stats.txt", 'r', encoding='utf-8') as f:
        emoteStats = json.load(f)
    data = get_chat_dataframe("chat.log")

    #
    # Main Handler
    #

    # New/Removed Emote Managements
    for emote in emoteList:
        if emote not in emoteStats.keys():
            emoteStats[emote] = [0, 0]

    tempList = []
    for emote in emoteStats.keys():
         if emote not in emoteList:
             tempList.append(emote)

    for emote in tempList:
        emoteStats.pop(emote)

    # Process Emote Usage
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


    # Output Stats
    location = os.getcwd() + '/Emote Stats History/Stream '+ str(livestreamID) + ' - ' + str(date.today())
    os.makedirs(location)

    with open('chat.log', 'rb') as f_in, gzip.open(location + '/chat.log.gz', 'wb') as f_out:
        f_out.writelines(f_in)
    with open('Emote Stats.txt', 'rb') as f_in, gzip.open(location + '/Pre Stream Stats.txt.gz', 'wb') as f_out:
        f_out.writelines(f_in)

    open('chat.log', 'w').close()

    with open("Emote Stats.txt", 'w', encoding='utf-8') as f:
        json.dump(emoteStats, f)

    livestreamID += 1
'''

# Concurrenting Parts
if __name__ == '__main__':
    try:
        streaming_thread = threading.Thread(target=UpdateLiveFlag)
        streaming_thread.start()

        LoggerFunction()
    except Exception:
        print("Exception Raised")
        try:
            sock.close()
        except:
            print("Socket Close Exception")


