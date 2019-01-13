import json
import glob
import re
#load settings
f = open("settings.json", "r")
settings=json.loads(f.read())
start=settings['start']
end=settings['end']

class Snippet:
	def __init__(self,str,justAttr):
		attrStr=""
		if not justAttr:
			#content
			self.content=str[str.find('\n'):]
			#process attributes
			attrStr=str[:str.find('\n')]
		else:
			attrStr=str
		attrStr=attrStr[len(start):len(attrStr)-len(end)]
		#in case some attribute is also an argument
		argList=list()
		self.attr=set()
		self.arg=dict()
		#create set of attributes
		regex="([A-Za-z_-]+([=]([1-9][0-9]*|[a-z]*|[\"][^\"]*[\"]))*(\s+|$))"
		for a in re.findall(regex,attrStr):
			#collect arguments
			a=a[0]
			if '=' in a:
				argList.append(a)
				self.attr.add(a.split('=',1)[0])
			else:
				self.attr.add(a)
			
		#arguments found, collect them
		if len(argList):
			for arg in argList:
				splitted=arg.split('=',1)
				self.arg[splitted[0]]=splitted[1]
	
#load snippets			
pathList=glob.glob('snippets\*')#all file from snippets folder
snippetList=[]
for p in pathList:
	f = open(p, "r")
	snippetList.append(Snippet(f.read(),False))

def prepareContent(cont,args):
	print(cont)
	return cont


def handler(data):
	res=""
	inputSnip=Snippet(data,True)
	#find snippet
	for snip in snippetList:
		if inputSnip.attr.issubset(snip.attr):
			if len(inputSnip.arg)>=len(snip.arg):
				res=prepareContent(snip.content,inputSnip.arg)
			else:
				for key,val in snip.arg.items():
					if key not in inputSnip.arg:
						inputSnip.arg[key]=val
				res=prepareContent(snip.content,inputSnip.arg)
			break
	
	return res
