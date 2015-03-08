import play,os,time
from gi.repository import Gtk,GObject
from threading import Thread
from KThread import *		#the KThread module is used to kill a thread,By:C. Barnes connellybarnes at yahoo.com

songlist=[]					#STORES CURRENT PLAYLIST
counter=1					#KEEPS A TRACK OF SONG WHICH IS TO BE PLAYED
nstatus=''					#CHECKS STATUS FOR PAUSE/PLAY

def aisehi():				#DOES NOTHING...IT IS USED FOR TIMEOUT
	return

#TO HIGHLIGHT THE CURRENT SONG PLAYING IN THE PLAYLIST
def highlight_song(counter):
	global builder
	mybuffer=builder.get_object('tvplaylist').get_buffer()
	iter0=mybuffer.get_iter_at_line(0)
	iterall=mybuffer.get_iter_at_line(mybuffer.get_line_count())
	iter1=mybuffer.get_iter_at_line(counter-1)
	iter2=mybuffer.get_iter_at_line(counter)
	mybuffer.remove_all_tags(iter0,iterall)
	mybuffer.create_tag("highlighted",  background = "green")
	mybuffer.apply_tag_by_name("highlighted", iter1, iter2)

#TO CHECK IF MUSIC PLAYER IS PAUSED/PLAYING
def pause_checker():
	while True:
		global nstatus
		if nstatus=='Resume':
			time.sleep(0.3)
			continue
		break
	return

#TO GET THE NAME OF THE SONG WHICH IS TO PLAYED
def currentSong():
	global counter
	highlight_song(counter)
	return songlist[counter-1]

#TO SWITCH SONG TO NEXT OR PREVIOUS SONG
def changeSong(action):
	global counter
	if action=='Next':
		counter+=1
		if counter>len(songlist):
			counter=1			

	elif action=='Previous':
		counter-=1
		if counter==-1:
			counter=len(songlist)
	currentSong()
	return

#TO MANAGE THE COUNTDOWNTIMER AND THE PROGRESS BAR
def count_down(timex):
	global builder
	totaltime=builder.get_object('totaltime')
	timex=int(timex)
	mint=timex/60
	secs=timex%60
	s1= "%0.2d:%0.2d" % (mint,secs)
	totaltime.set_label(s1)
	for t in range(1,int(timex)+1):
		pause_checker()
		minutes = t / 60
		seconds = t % 60
		s= "%0.2d:%0.2d" % (minutes,seconds)
		time.sleep(1.0)
		base.update_time(builder,s)
		base.progress(builder,t/float(timex))
	base.reset(builder)				#TO RESET THE GUI WHEN THE SONG FINISHES
	return

class Handler:
	
	#TO EXIT THE PLAYER
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	#TO PLAY/PAUSE THE SONG
	def onToggle(self,button):		
		global nstatus
		self.toggle=builder.get_object('tpause')
		status=self.toggle.get_label()
		nstatus=play.pause(status)
		self.toggle.set_label(nstatus)

	#TO START/STOP THE SONG
	def onStart(self, button):		
		self.bstart=builder.get_object('bplay')
		status=self.bstart.get_label()
		name=os.path.dirname(os.path.realpath('mplayer.py'))+"/nish_playlist/"+currentSong() #PATH TO THE PLAYLIST FOLDER
		timex=play.song_len(name)
		t=Thread(target=play.play_song,args=(name,status,))
		t.daemon=True
		if status=='Start':
			self.bstart.set_label('Stop')
			global timer
			timer=KThread(target=count_down,args=(timex,))
			timer.daemon=True
			timer.start()

		else:
			timer.kill()
			self.bstart.set_label('Start')
			base.progress(builder,0.0)	
			base.reset_time(builder)
		t.start()

	#TO GO TO NEXT SONG
	def on_bnext_pressed(self,button):
		self.bstart=builder.get_object('bplay')
		self.bstart.set_label('Start')
		changeSong('Next')
		timer.kill()
		self.onStart(self.bstart)

	#TO GO TO PREVIOUS SONG
	def on_bprevious_pressed(self,button):
		self.bstart=builder.get_object('bplay')
		self.bstart.set_label('Start')
		changeSong('Previous')
		timer.kill()
		self.onStart(self.bstart)

class Base:
	def __init__(self):	
		global builder
		builder = Gtk.Builder()
		builder.add_from_file("mplayer.glade")
		builder.connect_signals(Handler())
		window = builder.get_object("window1")
		#window.set_size_request(200,360)
		window.show_all()
		GObject.timeout_add(10,aisehi)
		self.prep(builder)

	def main(self):
		Gtk.main()
	
	#TO UPDATE THE PROGRESS BAR	
	def progress(self,builder,num=0.5):
		self.progress_bar=builder.get_object('progbar')
		self.progress_bar.set_fraction(num)
	
	#TO PREPARE THE PLAYLIST AND THE LOGO	
	def prep(self,builder):
		self.load_list(builder)
		self.load_pic(builder)
	
	#TO LOAD THE SONGS PLACED IN THE nish_playlist FOLDER AS THE CURRENT PLAYLIST
	def load_list(self,builder):
		global songlist
		self.playlist=builder.get_object('tvplaylist')
		self.bufferlist=self.playlist.get_buffer()
		for r in os.listdir(os.path.dirname(os.path.realpath('mplayer.py'))+"/nish_playlist/"):
			self.bufferlist.insert(self.bufferlist.get_end_iter(),r+"\n")
			songlist.append(r)
	
	#TO PUT THE LOGO INTO THE GUI
	def load_pic(self,builder):
		self.image=builder.get_object('imart')
		self.image.set_from_file('nish.jpeg')
	
	#TO UPDATE THE TEXT IN THE COUNTDOWN TIMER
	def update_time(self,builder,s):
		self.timenow=builder.get_object('timenow')
		self.timenow.set_label(s)

	#TO RESET THE TIMER
	def reset_time(self,builder):
		self.timenow=builder.get_object('timenow')
		self.timenow.set_label('00:00')
		self.totaltime=builder.get_object('totaltime')
		self.totaltime.set_label('00:00')
		
	#TO RESET THE WHOLE GRAPHICAL USER INTERFACE
	def reset(self,builder):
		self.starter=builder.get_object('bplay')
		self.starter.set_label('Start')
		self.toggler=builder.get_object('tpause')
		self.toggler.set_label('Pause')
		self.timenow=builder.get_object('timenow')
		self.timenow.set_label('00:00')
		self.totaltime=builder.get_object('totaltime')
		self.totaltime.set_label('00:00')
		
base=Base()

if __name__=='__main__':
	main_thread=Thread(target=base.main)
	main_thread.start()
