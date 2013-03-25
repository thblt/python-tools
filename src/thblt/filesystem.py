# -*- coding: UTF-8 -*-

import os, time, stat
from threading import Thread

def splitPath(path):
	""" Splits a path in individual components. (Difference with os.path.split is that the 
	latter only separates path and filename. """
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

class FSWatcher(Thread):

	_creationCallback = None
	_modificationCallback = None
	_deletionCallback = None
	
	_sleepInterval = 0
	
	_baseFileList = None
	_paused = False
	_stop_ = False  # Trailing underscore to avoid conflicts with Thread methods

	def pause(self, pause = True):
		self._paused = pause
		
	def unpause(self):
		self.pause(False)
		
	def stop(self):
		self._stop_ = True
	
	def listFS(self, root):
		# @FIXME Critical ! This will break and kill the thread 
		# if a file gets deleted or renamed between the 
		# os.listdir() and the os.path.getmtime
		ret = {}
		for f in os.listdir(root):
			fPath = os.path.join(root, f)
			# @FIXME Test this on Windows : If ST_INO doesn't return a unique,
			# path and filename-independant identifier, then find some other way to 
			# achieve the same result --- or else everything will break.
			ret[os.stat(fPath)[stat.ST_INO]] = [ fPath, os.path.getmtime(fPath) ]
			if os.path.isdir(fPath):
				ret.update(self.listFS(fPath))
				 
		return ret
	
	def reportChange(self, reportIds, fullList, method, dirsFirst=True):
		if not reportIds: return
		# By sorting, we guarantee not that every directory will come first, but that
		# every file in a directory will come after this directory.
		reportIds = sorted(reportIds, key=lambda x: len(fullList[x][0]))
		if not dirsFirst: reportIds.reverse() 
		for i in reportIds:
			method(i, fullList[i][0])
	
	def run(self):
		root = self._fss._root
		before = dict()  # Starting clean, ie reporting everything as added on first run.
		i = 0
		while not self._stop_:
			if not self._paused:
				i += 1
				try:
					after = self.listFS(root)
				except Exception:
					return  # see FIXME in listFS()
				
				set_current, set_past = set(after.keys()), set(before.keys())
				intersect = set_current.intersection(set_past)
				
				deleted = set(before.keys() - after.keys())
				added = set(after.keys() - before.keys())
				changed = set(o for o in intersect if before[o] != after[o]) 

				self.reportChange(deleted, before, self._deletionCallback, False)
				self.reportChange(added, after, self._creationCallback)
				self.reportChange(changed, after, self._modificationCallback)
				
				before = after  # Metaphysics!
			
			time.sleep(self._sleepInterval)
			
	def __init__(self, creationCallback, modificationCallback, deletionCallback, sleepInterval=.1):
		Thread.__init__(self)
		self.daemon = True
		self._creationCallback = creationCallback
		self._modificationCallback = modificationCallback
		self._deletionCallback = deletionCallback
		
		self._sleepInterval = float(sleepInterval)