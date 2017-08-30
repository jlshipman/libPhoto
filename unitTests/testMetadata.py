#!/usr/bin/python
import unittest, inspect, os, sys
curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
dirName2 = os.path.dirname(dirName)
libPath = dirName2 + "/lib"
sys.path.append(libPath)
import unittest
import metadata
 
class TestMetadata(unittest.TestCase):
 	print "Test Metadata Fucntion"
 	
	def setUp(self):
		print "#############################################"
		print "setUp" 
# 
# 	def testGetTag(self):
# 		print "\tGetTag"
# 		filePath = "R-LRC-1937-B701_P-12915.tif"
# 		tag = "Format"
# 		retObj = metadata.getTag( filePath, tag )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand:   _" + command + "_"	
# 		print "\t\terror:   _" + error + "_"
# 		
# 	def testClearTag(self):
# 		print "\ttestClearTag"
# 		filePath = "R-LRC-1937-B701_P-12915.tif"
# 		tag = "keywords"
# 		retObj = metadata.clearTag( filePath, tag )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand:   _" + command + "_"
# 		print "\t\terror:   _" + error + "_"
# 				
# 	def testGetTagBadTag(self):
# 		print "\ttestGetTagBadTag"
# 		filePath = "R-LRC-1937-B701_P-12915.tif"
# 		tag = "key"
# 		retObj = metadata.getTag( filePath, tag )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand:   _" + command + "_"	
# 		print "\t\terror:   _" + error + "_"

# 	def testSetTag(self):
# 		print "\ttestSetTag"
# 		filePath = "R-LRC-1937-B701_P-12915.tif"
# 		tag = "keywords"
# 		data = "testing"
# 		retObj = metadata.setTag( filePath, tag, data )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand:   _" + command + "_"
# 		print "\t\terror:   _" + error + "_"
# 		
# 	def testSetTagBadKeyWord(self):
# 		print "\ttestSetTagBadKeyWord"
# 		filePath = "R-LRC-1937-B701_P-12915.tif"
# 		tag = "key"
# 		data = "testing"
# 		retObj = metadata.setTag( filePath, tag, data )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand:   _" + command + "_"
# 		print "\t\terror:   _" + error + "_"
# 
# 	def testGetAllTags(self):
# 		print "\ttestGetAllTags"
# 		filePath = "R-LRC-1937-B701_P-12915.tif"
# 		retObj = metadata.getAllTags( filePath )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:"
# 		for key, value in result.iteritems():
# 			print "\t\t\tkey:  " + key + "  value  "  + value
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"
# 
 	def testSetTagDescription(self):
		print "\ttestSetTagDescription"
		filePath = "R-LRC-1937-B701_P-12915.tif"
		tag = "Description"
		data="What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye"
		#data="What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye in the morning! [Chorus:] Way hay and up she rises Way hay and up she rises Way hay and up she rises Earl-eye in the morning Shave his belly with a rusty razor, Shave his belly with a rusty razor, Shave his belly with a rusty razor, Earl-eye in the morning! [Chorus] Put him in the hold with the Captain's daughter, Put him in the hold with the Captain's daughter, Put him in the hold with the Captain's daughter, Earl-eye in the morning! [Chorus] What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye in the morning! [Chorus] Put him the back of the paddy wagon, Put him the back of the paddy wagon, Put him the back of the paddy wagon, Earl-eye in the morning! [Chorus] Throw him in the lock-up 'til he's sober, Throw him in the lock-up 'til he's sober, Throw him in the lock-up 'til he's sober, Earl-eye in the morning! [Chorus] What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye in the morning! [Chorus] What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye in the morning! [Chorus]"
		retObjClear = metadata.clearTag( filePath, tag )
		retObj = metadata.setDescriptionTag( filePath, data )
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		command = retObj.getCommand()
		error = retObj.getError()
		print "\t\tdata  :  _" + str(data)  + "_"
		print "\t\tresult:  _" + str(result)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
		print "\t\tcommand: _" + command + "_"
		print "\t\terror:   _" + error + "_"	
				
# 	def testSetTagKeywordLong(self):
# 		print "\ttestSetTagKeywordLong"
# 		filePath = "R-LRC-1937-B701_P-12915.tif"
# 		tag = "Keywords"
# 		data="What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye"
# 		#data="What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye in the morning! [Chorus:] Way hay and up she rises Way hay and up she rises Way hay and up she rises Earl-eye in the morning Shave his belly with a rusty razor, Shave his belly with a rusty razor, Shave his belly with a rusty razor, Earl-eye in the morning! [Chorus] Put him in the hold with the Captain's daughter, Put him in the hold with the Captain's daughter, Put him in the hold with the Captain's daughter, Earl-eye in the morning! [Chorus] What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye in the morning! [Chorus] Put him the back of the paddy wagon, Put him the back of the paddy wagon, Put him the back of the paddy wagon, Earl-eye in the morning! [Chorus] Throw him in the lock-up 'til he's sober, Throw him in the lock-up 'til he's sober, Throw him in the lock-up 'til he's sober, Earl-eye in the morning! [Chorus] What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye in the morning! [Chorus] What do you do with a drunken sailor, What do you do with a drunken sailor, What do you do with a drunken sailor, Earl-eye in the morning! [Chorus]"
# 		retObjClear = metadata.clearTag( filePath, tag )
# 		retObj = metadata.setKeywordTag( filePath, data )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		data = data.replace(',', '')
# 		dataList =data.split()
# 		data = ', '.join(dataList)
# 		print "\t\tdata  :  _" + str(data)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 			
	def tearDown(self):
		print "tearDown" 
		print "#############################################"
		print ""
 
      
if __name__ == '__main__':
    unittest.main()