import os, platform,math

def user_locale(fallback=(None, None)):
	""" Attempts at all costs to return a locale for the current user. """
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
	
	return fallback

def is_macosx(minVer=0, maxVer=1000):
	
	osx = platform.mac_ver()[0].split('.')
	if not (osx and int(osx[0]) == 10): return False 
	
	sysMajor = int(osx[1])
	sysMinor = int(osx[2])
	
	versions = {
			"cheetah":0,
			"puma":1,
			"jaguar":2,
			"panther":3,
			"tiger":4,
			"leopard":5,
			"snow Leopard":6,
			"snowleopard":6,
			"sl":6,
			"lion":7,
			"mountain lion":8,
			"mountainlion":8,
			"ml":8,
			"lynx":8}
	
	range_ = []
	for v in (minVer, maxVer):
		try:
			major = int(v)
			minor = int(v*10 % 10)
		except ValueError as e:
			v = v.lower()
			if v in versions.keys():
				major = versions[v]
				minor = 0
			else: raise e
		range_.append([major, minor])
	
	if not(range_[1][1]): range_[1][1] = 1000
	
	if range_[0][0] <= sysMajor <= range_[1][0]:
		return  range_[0][1] <= sysMinor <= range_[1][1]

	return False
	
