from __future__ import unicode_literals
import youtube_dl
from youtube_search import YoutubeSearch as yts
import sys, os 
import glob
import threading


def blockPrint():
    sys.stdout = open(os.devnull, 'w')
    
blockPrint()

import pygame.mixer as mixer
mixer.init(47100)

def clear(): 
    if os.name == 'nt': 
        os.system('cls')  
    else: 
        os.system('clear') 


class Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.run
		
	def run(self):
		mixer.music.load(song)
		mixer.music.play()
		
	def die(self):
		mixer.music.stop()
		
	def pause(self):
		mixer.music.pause()
		
	def cont(self):
		mixer.music.unpause()

	def replay(self):
		mixer.music.rewind()
		mixer.music.play()

def enablePrint():
    sys.stdout = sys.__stdout__
    
enablePrint()
    
search = "" 
for i in sys.argv[1:]:
	search += str(i) + " "

def download(search):
	global song, playing
	results = yts(f"{search}", max_results=1).to_dict()

	sn = results[0]["title"]
	sn = sn.replace("|", "_")
	sn = sn.replace(":", " -")

	link = f"http://www.youtube.com/watch?v={results[0]['id']}"

	print("loading...")
	blockPrint()

	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	done = False
	while not done:
		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([link])
			done = True
		except:
			done = False

	song = glob.glob(f"{sn[:-1]}*.mp3")[0]
	
	
	enablePrint()
	clear()
	print(results[0]["title"])

	playing = Thread()
	playing.start()

download(search)

inp = None
paused = False
end = ["x", "X", "exit", "Exit", "end", "End"]
while inp not in end:
	inp = input(">> ")
	
	if inp == "stop":
		if playing:
			playing.die()
			playing.join()
			
	elif inp == "pause":
		if playing and not paused:
			playing.pause()
			playing.join()
			paused = True
		elif paused:
			print("It is already paused...")
		else:
			print("Nothing is playing...")	
	elif inp == "resume":
		if not paused:
			print("Nothing is paused")
		else:
			playing.cont()
			playing.join()
			paused = False
	elif inp == "replay":
		playing.replay()
	elif inp[:4] == "play" and len(inp) >= 5:
		playing.die()
		download(inp[5:])
			
	elif inp == "help":
		print("")
		print("Hey there, champ!")
		print("Let me give you a little introduction")
		print("")
		print("If no song is playing at the moment you can write...")
		print("		play name of the song")
		print("		for example: play Rosenrot")
		print("")
		print("For controls you can write...")
		print("		stop 			-- this ends the song")
		print("		pause/resume 		-- to, well, pause and resume")
		print("		replay 			-- to play the song again")
		print("		x/exit/end 		-- to end the program")
		print("")
	elif inp not in end:
		print("Command not recognized")
			

trash = glob.glob("*.mp3")
for file in trash:
	os.remove(file)
