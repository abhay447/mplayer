import pygame
from mutagen.mp3 import MP3
pygame.mixer.init()

def play_song(name,status):
	if status=='Start':
		pygame.mixer.music.load(name)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
		    continue
	if status=='Stop':
		pygame.mixer.music.stop()
	return

def pause(status):
	if status=='Pause':
		pygame.mixer.music.pause()
		status='Resume'
	else:
		pygame.mixer.music.unpause()
		status='Pause'
	return status

def song_len(name):
	audio=MP3(name)
	a=audio.info.length
	return a
