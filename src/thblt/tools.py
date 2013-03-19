import os, platform

def userLocale():
	import locale, json
	from subprocess import Popen, PIPE

	loc = locale.getdefaultlocale()
	if loc[0]:
		return loc
	
	ver = platform.mac_ver()
	if (ver):
		ver = ver[0].split(".")
		# No plutil before 10.2 (manpage). Sorry 10.1 users, but please.
		# @TODO Should check when the file we dig appeared, and if it still exists in 10.8 and above.
		if int(ver[0]) == 10 and int(ver[1]) >= 2: 
			# Let's dig
			try:
				args = ["plutil", "-convert", "json", "-o", "-", os.path.expanduser("~/Library/Preferences/.GlobalPreferences.plist")]
				p = Popen(args, stdout=PIPE)
				out = p.communicate()
				loc = (json.loads(str(out, "UTF-8"))['AppleLocale'])
				loc = loc.split("_")
				if len(loc) == 2: return loc
			except Exception:
				pass
	
	return {None, None} 

def li(list_, c):
	""" Returns an item of a list_, or false if this element doesn't exist. """
	if len(list_) > c: return list_[c]
	return False;

def dumpTree(t, depth=0):
	if isinstance(t, list):
		for v in t:
			if len(v):
				print (' ' * depth + '[')
				dumpTree(v, depth + 1)
				print (' ' * depth + ']')
			else:
				print (' ' * depth + '=[]')
	elif isinstance(t, dict):
		for k, v in t.items():
			if (isinstance(v, dict) or isinstance(v, list)):
				if len(v):
					print (' ' * depth + k + '={')
					dumpTree(v, depth + 1)
					print (' ' * depth + '} # ' + k)
				else:
					print (' ' * depth + k + '={}')
			else:
				print(' ' * depth + str(k) + '=' + str(v))
	else:
		print(' ' * depth + str(t))
		
def splitPath(path):
	ret = []
	head, tail = os.path.split(path)
	while 1: 
		head, tail = os.path.split(path) 

		if tail == '': 
			if head != '': ret.insert(0, head) 
			break 
		else: 
			ret.insert(0, tail) 
			path = head
			
	return ret 
