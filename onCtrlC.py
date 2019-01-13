from pynput import keyboard
import pyperclip
import json

ctrl=False
cKey=False
def listen(handler):
	#load settings
	f = open("settings.json", "r")
	settings=json.loads(f.read())
	start=settings['start']
	end=settings['end']
	
	def parseAttributes(str):
		#starts with
		if not str.startswith(start):
			return False
			
		#endWith
		if not str.endswith(end):
			return False
			
		return True
	
	def setClipboardData(d):
		pyperclip.copy(d)
		
	def getClipData():
		return pyperclip.paste()
	
	prevData=""
	
	def on_press(key):
		keyStr=""
		try:
			keyStr=key.char
		except AttributeError:
			keyStr=key.name
		
		global ctrl
		global cKey
		if "ctrl" in keyStr:
			ctrl=True
		elif keyStr=="c":
			cKey=True
			
	def on_release(key):
		keyStr=""
		try:
			keyStr=key.char
		except AttributeError:
			keyStr=key.name
		
		global ctrl
		global cKey
		data=getClipData()
		if ctrl and cKey and "ctrl" in keyStr or keyStr=="c" and data!=prevData:
			#CTRL+C event
			attrStr=parseAttributes(data)
			if attrStr:
				res=handler(data)
				if res:
					print(res)
					setClipboardData(res)
			
			
		if "ctrl" in keyStr:
			ctrl=False
		elif keyStr=="c":
			cKey=False


	#Set event listeners
	with keyboard.Listener(
		on_press=on_press,
		on_release=on_release) as listener:
		listener.join()
