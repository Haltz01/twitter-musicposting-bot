#!/usr/bin/python3
import tweepy
from dotenv import load_dotenv
import os
import requests
import random

# import logging

# logger = logging.getLogger()

# https://realpython.com/twitter-bot-python-tweepy/
# http://docs.tweepy.org/en/latest/getting_started.html

# https://spinditty.com/genres/100-Best-Metalcore-Bands

# import PyV8
# ctx = PyV8.JSContext()
# ctx.enter()

# js = """
# <script type="text/javascript" src="http://tracking.musixmatch.com/t1.0/AMa6hJCIEzn1v8RuOP">
# """

# print ctx.eval(js.replace("document.write", "return "))

def getRandomArtist(): # gets random artist from artists_list.txt file and returns artist ID in the API
    print("\n======= getRandomArtist() =======")
    
    artists_list = open('artists_list.txt', 'r') 
    fileLines = artists_list.readlines() 

    randArtistIndex = random.randint(0, len(fileLines)-1)

    selectedArtist = fileLines[randArtistIndex]

    if (selectedArtist[-1] == '\n'): # removing '\n' if there's one in string
        selectedArtist = selectedArtist[:-1]


    artistSearchURL = "artist.search?page_size=1&q_artist=" + selectedArtist + "&apikey=" + MUSIXMATCH_API_KEY

    print("[*] Getting " + selectedArtist + " ID...")
    response = requests.get(rootUrlAPI + artistSearchURL)

    if (response.status_code != 200):
        print("[!] Something went wrong! Status code = " + response.status_code)
        return -1
        
    response = response.json()

    print("[*] JSON response:", response["message"]["body"]["artist_list"][0])

    artistID = response["message"]["body"]["artist_list"][0]["artist"]["artist_id"]
    print("[*] OK - Artist ID = ", artistID)

    return artistID

def getRandomAlbum(artistID): # gets a random album from the selected artist and returns the album ID
    print("\n======= getRandomAlbum() =======")

    albumSearchURL = "artist.albums.get?page_size=100&g_album_name=1&artist_id=" + str(artistID) + "&s_release_date=desc&apikey=" + MUSIXMATCH_API_KEY

    response = requests.get(rootUrlAPI + albumSearchURL)

    if (response.status_code != 200):
        print("[!] Something went wrong! Status code = " + response.status_code)
        return -1
    
    response = response.json()

    albumList = response["message"]["body"]["album_list"]

    selectedIndex = random.randint(0, len(albumList)-1)

    print("[*] Selected album JSON:", albumList[selectedIndex]["album"])

    albumID = albumList[selectedIndex]["album"]["album_id"]

    print("[*] OK - album ID = ", albumID)

    return albumID

def getRandomSong(albumID): # gets a random song from an album (popular song is prefered) and returns its ID
    print("\n======= getRandomSong() =======")

    albumTracksURL = "album.tracks.get?page_size=50&album_id=" + str(albumID) + "&apikey=" + MUSIXMATCH_API_KEY

    response = requests.get(rootUrlAPI + albumTracksURL)

    if (response.status_code != 200):
        print("[!] Something went wrong! Status code = " + response.status_code)
        return (-1, "")
    
    response = response.json()

    tracksList = response["message"]["body"]["track_list"]

    selectedIndex = random.randint(0, len(tracksList)-1)

    print("[*] Selected track JSON:", tracksList[selectedIndex]["track"])

    trackID = tracksList[selectedIndex]["track"]["track_id"]
    trackName = tracksList[selectedIndex]["track"]["track_name"]

    print("[*] OK - track ID = " + str(trackID) + " - track name = " + trackName)

    return (trackID, trackName)

def getLyrics(trackID): # gets the lirycs of a song
    print("\n======= getLyrics() =======")

    trackLyricsURL = "track.lyrics.get?track_id=" + str(trackID) + "&apikey=" + MUSIXMATCH_API_KEY

    response = requests.get(rootUrlAPI + trackLyricsURL)

    if (response.status_code != 200):
        print("[!] Something went wrong! Status code = " + response.status_code)
        return -1

    print(response.json())

# Getting environment variables
load_dotenv(verbose=True)
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
MUSIXMATCH_API_KEY = os.getenv("MUSIXMATCH_API_KEY")

print("== .ENV VARIABLES ==")
print("API_KEY:", API_KEY)
print("API_SECRET_KEY: ", API_SECRET_KEY)
print("BEARER_TOKEN: ", BEARER_TOKEN)
print("ACCESS_TOKEN: ", ACCESS_TOKEN)
print("ACCESS_TOKEN_SECRET: ", ACCESS_TOKEN_SECRET)
print("MUSIXMATCH_API_KEY: ", MUSIXMATCH_API_KEY)

# Authenticating to Twitter
# print("[*] Authenticating to Twitter...")
# auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY) 
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Creating API object
# api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) # when rate limit is exceed, it notifies and waits

# Verifying credentials
# try:
#     api.verify_credentials()
#     print("[*] Authentication OK")
# except:
#     print("[!] Error during authentication")

# Testing song APIs
# https://www.last.fm/api/show/track.search
# https://api.vagalume.com.br/
# https://github.com/canarado/node-lyrics

# https://developer.musixmatch.com/ -> I'll probably use this one
rootUrlAPI = "https://api.musixmatch.com/ws/1.1/"

artistID = getRandomArtist()
if (artistID == -1):
    exit(1)
albumID = getRandomAlbum(artistID)
if (albumID == -1):
    exit(1)
trackID, trackName = getRandomSong(albumID)
if (trackID == -1):
    exit(1)
getLyrics(trackID)
