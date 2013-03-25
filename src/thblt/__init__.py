from weakref import ref

class TwoWayDict(dict):
	"""
	Code borrowed from http://stackoverflow.com/questions/1456373/two-way-reverse-map
	"""
	def __len__(self):
		#@FIXME: This won't work if key=value 
		return dict.__len__(self) / 2
	
	def __setitem__(self, key, value):
		dict.__setitem__(self, key, value)
		dict.__setitem__(self, value, key)

class TwoWayWeakDict(TwoWayDict):
	

	def __setitem__(self, key, value):
		dict.__setitem__(self, ref(key), ref(value))
		dict.__setitem__(self, ref(value), ref(key))


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
		for k, v in t._items():
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
		
