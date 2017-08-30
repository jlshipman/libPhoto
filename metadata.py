import sys
sys.path.append('lib')
sys.path.append('libPhoto')
import funcReturn
import comWrap

#exiftool must be installed for this to run

def getTag( filePath, tag ):
	#exiftool "-*resolution*" image.jpg
	if filePath == "":
		retObj = funcReturn.funcReturn('getTag')
		retObj.setError("filePath field not set")
		return retObj

	if tag == "":
		retObj = funcReturn.funcReturn('getTag')
		retObj.setError("tag field not set")
		return retObj

	retObjWhich=comWrap.which("exiftool")
	retVal=retObjWhich.getRetVal()
		
	if retVal == 0:
		command = 'exiftool "-' + tag + '" ' + filePath
		retObj = comWrap.comWrapString(command)
		stdOut=retObj.getStdout()
		if stdOut != "":
			result = stdOut.split(":")
			retObj.setResult(result[1].lstrip())
		retObj.setCommand(command)
		retObj.setName('getTag')
		return retObj
	else:
		retObj = funcReturn.funcReturn('getTag')
		retObj.setError("exiftool is not installed")
		return retObj

def clearTag( filePath, tag ):
	#exiftool -artist= a.jpg
	retObj = funcReturn.funcReturn('clearTag')
	if filePath == "":
		retObj = funcReturn.funcReturn('clearTag')
		retObj.setError("filePath field not set")
		return retObj
		
	if tag == "":
		retObj = funcReturn.funcReturn('clearTag')
		retObj.setError("filePath tag not set")
		return retObj
	
	retObjWhich=comWrap.which("exiftool")
	retVal=retObjWhich.getRetVal()
	if retVal == 0:
		command = 'exiftool -' + tag + '= ' + filePath
		retObj = comWrap.comWrapString(command)
		stdOut=retObj.getStdout()
		retObj.setCommand(command)
		retObj.setName('clearTag')
		retObjGet = getTag( filePath, tag )
		getResultVal = retObjGet.getResult()
		if getResultVal == "":
			retObj.setRetVal(0)
		else:
			retObj.setRetVal(1)
			retObj.setError("tag:  " +  tag + " is not cleared")
		return retObj
	else:
		retObj = funcReturn.funcReturn('getTag')
		retObj.setError("exiftool is not installed")
		return retObj

def setDescriptionTag( filePath, data ):
	#exiftool -Caption-Abstract+=me a.jpg	
	tag = "Description"
	retObj = funcReturn.funcReturn('setDescriptionTag')
	if filePath == "":
		retObj = funcReturn.funcReturn('setDescriptionTag')
		retObj.setError("filePath field not set")
		return retObj
						
	if data == "":
		retObj = funcReturn.funcReturn('setDescriptionTag')
		retObj.setError("data field not set")
		return retObj
						
	retObjWhich=comWrap.which("exiftool")
	retVal=retObjWhich.getRetVal()
	if retVal == 0:		
		command = 'exiftool -' + tag + '="' + data + '" ' + filePath
		retObj = comWrap.comWrapString(command)
		retObj.setCommand(command)
		retObj = funcReturn.funcReturn('setDescriptionTag')
		if retObj.getRetVal() == 0:
			print "\t\t\tafter retObj.getRetVal() == 0"
			if retObj.getStderr() != "":
				err = retObj.getStderr()
				resultFind = err.find("exceeds length limit")
				if resultFind != -1:
					retObj.setError("to much information trying to be added to _" + tag + "_ tag")
					retObj.setRetVal(1)
					return retObj
		if retObj.getRetVal() == 1:
			std=retObj.getStderr()
			resultFind = std.find("Warning: Can't convert")
			if resultFind != -1:
				retObj.setError("Can't find _" + tag + "_ tag")
				retObj.setName('setDescriptionTag')
				return retObj
		retObjGet = getTag( filePath, tag )		
		getResultVal = retObjGet.getResult()
		retObj.setResult(getResultVal)
		
		data2 = retObjGet.getResult()
# 		if data == data2:
# 			retObj.setRetVal(0)
		retObj.setRetVal(0)
		return retObj
	else:
		retObj = funcReturn.funcReturn('setDescriptionTag')
		retObj.setError("exiftool is not installed")
		return retObj	
				
def setKeywordTag( filePath, data ):
	#exiftool -Keywords+=me a.jpg	
	tag = "Keywords"
	retObj = funcReturn.funcReturn('setKeywordTag')
	if filePath == "":
		retObj = funcReturn.funcReturn('setKeywordTag')
		retObj.setError("filePath field not set")
		return retObj
						
	if data == "":
		retObj = funcReturn.funcReturn('setKeywordTag')
		retObj.setError("data field not set")
		return retObj
	else:
		data = data.replace(',', '')
		lengthData = len(data)
		dataList =data.split()
		lengthDataList = len(dataList)
					
	retObjWhich=comWrap.which("exiftool")
	retVal=retObjWhich.getRetVal()
	if retVal == 0:
		lengthPush = 0 
		stringPush = ""
		for d in dataList:
			#print "d           :  " + d
			command = 'exiftool -overwrite_original -' + tag + '+="' + d + '" ' + filePath
			retObj = comWrap.comWrapString(command)
			retObj.setCommand(command)
			retObj = funcReturn.funcReturn('setKeywordTag')
			retObjGet = getTag( filePath, tag )		
			if retObj.getRetVal() == 0:
				if retObj.getStderr() != "":
					err = retObj.getStderr()
					resultFind = err.find("exceeds length limit")
					if resultFind != -1:
						retObj.setError("to much information trying to be added to _" + tag + "_ tag")
						retObj.setRetVal(1)
						return retObj
			if retObj.getRetVal() == 1:
				std=retObj.getStderr()
				resultFind = std.find("Warning: Can't convert")
				if resultFind != -1:
					retObj.setError("Can't find _" + tag + "_ tag")
					retObj.setName('setKeywordTag')
					return retObj
					
		retObjGet = getTag( filePath, tag )		
		getResultVal = retObjGet.getResult()
		print "\t\tgetResultVal  :  _" + str(getResultVal)  + "_"
		retObj.setResult(getResultVal)
		
		data = ', '.join(dataList)
		data2 = retObjGet.getResult()
# 		if data == data2:
# 			retObj.setRetVal(0)
		retObj.setRetVal(0)
		return retObj
	else:
		retObj = funcReturn.funcReturn('setKeywordTag')
		retObj.setError("exiftool is not installed")
		return retObj	
	
def getAllTags( filePath ):
	#exiftool -a -u -g1 a.jpg
	if filePath == "":
		retObj = funcReturn.funcReturn('getAllTags')
		retObj.setError("filePath field not set")
		return retObj
		
	retObjWhich=comWrap.which("exiftool")
	retVal=retObjWhich.getRetVal()
	if retVal == 0:
		command = 'exiftool -a -u -g1 ' + filePath
		retObj = comWrap.comWrapString(command)
		retObj.setCommand(command)
		retObj.setName('getAllTags')
		stdOut=retObj.getStdout()
		out = stdOut.split("\n")
		keyDict = {}
		for line in out:
			res = line.split(":")
			if len(res) == 2:
				keyDict[res[0]] = res[1]
		retObj.setResult(keyDict)
	else:
		retObj = funcReturn.funcReturn('getAllTags')
		retObj.setError("exiftool is not installed")
	
	
	return retObj
