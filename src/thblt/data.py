
class SimpleTree(object):
	parent = None
	role = None
	children = None
	value = None
	parent = None
	
	def __init__(self, value=None):
		self.value = value
		self.children = []
	
	def getChildrenCount(self):
		return len(self.children)
	
	def getChild(self, row):
		if 0 <= row < self.getChildrenCount():
			return self.children[row]
		return None
	
	def getValue(self):
		return self.value
		
	def addChild(self, c):
		""" Deprecated """
		self.addChildren(c)	
		
	def addChildren(self, child):
		try:
			for c in child:
				c.parent = self;
				self.children.append(c)
		except TypeError:
			child.parent = self
			self.children.append(child)
		
	def removeChildren(self, child):
		try:
			for c in child:
				self.children.remove(c)
		except TypeError:
			self.children.remove(child)
		
	def clearChildren(self):
		self.children = []
		
	def getChildIndex(self, child):
		return self.children.index(child)
		
	def getIndexInParent(self):
		return self.parent.getChildIndex(self)