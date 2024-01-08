#
# Code related to tracking twitch chat.
#


# Imports
import requests
import socket
import logging
import time


# Decelerations
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'ShiroTheShiro'
token = ''
channel = '#avast'
channelName = 'avast'
sock = None
liveFlag = False
liveFlagLock = threading.Lock()


# Sets up the logger.
def loggerSetup():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s — %(message)s',
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        handlers=[logging.FileHandler('chat.log', encoding='utf-8')])


# Starts and sets up a socket.
def socketSetup():
    global sock
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))


# Checks user status using Twitch api.
def checkIfUserIsStreaming(username):
    url = "https://gql.twitch.tv/gql"
    query = "query {\n  user(login: \""+username+"\") {\n    stream {\n      id\n    }\n  }\n}"
    return True if requests.request("POST", url, json={"query": query, "variables": {}}, headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}).json()["data"]["user"]["stream"] else False


# Updates live flag.
def updateLiveFlag():
    global liveFlag
    counter = 0


    # Checks livestream status.
    # Updates from offline to online on first signal, updates from online to offline after continuous offline signal for 60 seconds.
    while True:
        if checkIfUserIsStreaming(channelName):
            counter = 0
            liveFlag = True
            time.sleep(10)
        else:
            if liveFlag == True:
                counter += 1
                time.sleep(10)
            if counter == 6:
                counter = 0
                liveFlag = False
                emoteUsageHandler()
            time.sleep(1)


# Main function, chat listener handler.
def chatListenerHandler():
    # Decelerations
    global liveFlag
    global sock


    # Looped socket response reader and handler.
    while True:
        resp = sock.recv(2048).decode('utf-8')


        # Message handler.
        if resp is None:
            sock = socket.socket()
            sock.connect((server, port))
            sock.send(f"PASS {token}\n".encode('utf-8'))
            sock.send(f"NICK {nickname}\n".encode('utf-8'))
            sock.send(f"JOIN {channel}\n".encode('utf-8'))

        elif resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0 and liveFlag:
            logging.info(resp)
