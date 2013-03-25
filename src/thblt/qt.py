from PyQt4 import QtCore

def loadResource(path):
	file = QtCore.QFile(path)
	if file.open(QtCore.QIODevice.ReadOnly):
		return file.readAll().data()
	return None 
		
def loadResourceText(path, encoding="utf-8"):
	raw = loadResource(path)
	if raw:
		return raw.decode(encoding)
