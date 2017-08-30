#!/usr/bin/python	
import unittest
import os, sys
import glob

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
print "curDir:  " + curDir


libPhotoPath=os.path.dirname(curDir)
print "libPhotoPath:  " + libPhotoPath
sys.path.append(libPhotoPath)

libPath=os.path.dirname(libPhotoPath) + "/lib"
print "libPath:  " + libPath
sys.path.append(libPath)

ret=curDir.split("/")
scriptTest1=ret.pop()
scriptTest2=ret.pop()
if scriptTest2 == "scripts":
	scriptDir = scriptTest1
else:
	scriptDir = scriptTest2
print "scriptDir:  " + scriptDir

threeDecimalFile = curDir+"/TEMP/threeDecimal.txt"
threeDecimalItem=curDir+"/TEMP/1981-L-12345.000.tif"
testFile=curDir+"/TEMP/1981-L-12345.000.tif"
testFile2=curDir+"/TEMP/1981-L-12345.000.jpg"
repositorySearchListFile=curDir+"/TEMP/repositorySearchListFile.txt"
amountTif=5	
#testAmount=amountTif+1
testAmount=16
amountJpg=7	
print "repositorySearchListFile:  " + repositorySearchListFile
repositoryImageListFile=curDir+"/TEMP/repositoryImageListFile.txt"
TEMP=curDir + "/TEMP"
import photoFunctions
from log import *
import fileFunctions
import funcReturn
import listFunctions
import directory

os.putenv("MSSUSER", "jshipman")
os.putenv("MSSHOST", "css-10g")
	
class TestPhotoFunc(unittest.TestCase):
 	print "Tests for `TestPhotoFunc.py`."
 	
	def setUp(self):
		print "#############################################"
		print "setUp" 

# 	def testPhotoUpdateObj(self):
# 		print "\ttestPhotoUpdateObj"
# 		name =  "LRC-1911-B701_P_F001-19297.tif"
# 		noSuffix =  "LRC-1911-B701_P_F001-19297"
# 		cd = ""
# 		stage = "development"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.photoUpdateObj (conn, name, cd, noSuffix)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 
# 
# 	def testPhotoInsertObj(self):
# 		print "\ttestPhotoInsertObj"
# 		name =  "LRC-1911-B701_P_F001-19297.tif"
# 		noSuffix =  "LRC-1911-B701_P_F001-19297"
# 		cd = ""
# 		stage = "development"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.photoInsertObj (conn, name, cd, noSuffix)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 

# 
# 	def testPhotoParts(self):
# 		print "\tTestPhotoPartsWithF"
# 		fileName = "LRC-1942-B701_P_F001-19297.tif"
#  		retObj = photoFunctions.photoParts(fileName)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
	def testPhotoExistObj2Exist(self):
		print "\ttestPhotoExistObj2Exist"
		stage = "production"
 		retObjConn = photoFunctions.photoConnectMysql2(stage)
 		conn = retObjConn.getResult()
		webname = "LRC-1999-B701_P-02479.jpg"
		retObj = photoFunctions.photoExistObj2(conn, webname)
		
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		command = retObj.getCommand()
		error = retObj.getError()
 		print "\t\tresult:   _" + str(result)  + "_"
		print "\t\tretVal:   _" + str(retVal)  + "_"
		print "\t\tcomment:  _" + comment + "_"
		print "\t\tstdout:   _" + stdout + "_"
		print "\t\tstderr:   _" + stderr + "_"
		print "\t\tremed:    _" + remed + "_"
		print "\t\tfound:    _" + str(found) + "_"	
		print "\t\terror:    _" + error + "_"	
		print "\t\tcommand:  _" + str(command)  + "_"

	def testPhotoExistObj2DoesNotExist(self):
		print "\ttestPhotoExistObj2DoesNotExist"
		stage = "production"
 		retObjConn = photoFunctions.photoConnectMysql2(stage)
 		conn = retObjConn.getResult()
		webname = "LRC-1933-B701_P-16185.jpg"
		retObj = photoFunctions.photoExistObj2(conn, webname)	
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		command = retObj.getCommand()
		error = retObj.getError()
 		print "\t\tresult:   _" + str(result)  + "_"
		print "\t\tretVal:   _" + str(retVal)  + "_"
		print "\t\tcomment:  _" + comment + "_"
		print "\t\tstdout:   _" + stdout + "_"
		print "\t\tstderr:   _" + stderr + "_"
		print "\t\tremed:    _" + remed + "_"
		print "\t\tfound:    _" + str(found) + "_"	
		print "\t\terror:    _" + error + "_"	
		print "\t\tcommand:  _" + str(command)  + "_"
		
# 	def testCreateAssetChksumList(self):
# 		print "\ttestCreateAssetChksumList"
# 		dirPath = "/Volumes/photoRepository/source/"
# 		retObj=directory.listFilesSuffixSortCreate( dirPath, "tif" )
# 		result = retObj.getResult()
# 		retObj = photoFunctions.createAssetChksumList(result)
# 		
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
#  		for r in result:
#  			print r
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 

# 	def testPhotoArchiveObj(self):
# 		print "\tPhotoArchiveObj"
# 		stage = "production"
# 		searchList = ['/Volumes/photoRepository/testingOne ']
# 		dirContentsList = []
# 		dirContentsFile = '/scripts/photoProcess/libPhoto/unitTests/dirContentsFile.txt'
# 		for s in searchList:
# 			term = s.rstrip()
# 			dirContentsList = glob.glob(term + "/*" ) + dirContentsList
# 		fileFunctions.listToFile(dirContentsList, dirContentsFile)
# 		chksumDir = '/scripts/photoProcess/libPhoto/unitTests/chksumDir/'
# 		baseError = '/scripts/photoProcess/libPhoto/unitTests/ERROR/'
# 		archiveFile = '/scripts/photoProcess/libPhoto/unitTests/archive.txt'
# 		retObj = photoFunctions.photoArchiveObj(dirContentsFile, archiveFile, baseError, chksumDir, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 
# 	def testPhotoSortObj(self):
# 		print "\tPhotoSortObj"
# 		stage = "production"
# 		searchList = ['/Volumes/photoRepository/testingOne ']
# 		dirContentsList = []
# 		dirContentsFile = '/scripts/photoProcess/libPhoto/unitTests/dirContentsFile.txt'
# 		for s in searchList:
# 			term = s.rstrip()
# 			dirContentsList = glob.glob(term + "/*" ) + dirContentsList
# 		fileFunctions.listToFile(dirContentsList, dirContentsFile)
# 		resposDict={}
# 		resposDict['repoProcess'] = "/Volumes/photoRepository/mastered/"
# 		resposDict['repoRaw']  = "/Volumes/photoRepository/source/"
# 		chksumDir = '/scripts/photoProcess/libPhoto/chksumDir/'
# 		retObj = photoFunctions.photoSortObj (dirContentsFile, resposDict, chksumDir, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
#  	 		
# 	def testPhotoMysql2(self):
# 		print "\tTestphotoMysql2"
# 		stage = "developmentMarvin"
# 		cdNameFile = "cdNameFile.txt"
#  		dirContentsFileJpg = curDir +"/jpgList.txt"
#  		repositorylist = "repositorylist.txt"
# 		retObj = photoFunctions.photoMysql2(dirContentsFileJpg, stage, cdNameFile, repositorylist)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
#  		print "\t\tdirContentsFileJpg:  _" + str(dirContentsFileJpg)  + "_"
#  	
# 	def testPhotoPrefix2(self):
# 		print "\tTestphotoPrefix2"
# 		stage = "developmentMarvin"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		hostName = retObjConn.getComment()
# 		retObj = photoFunctions.photoPrefix2(conn)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\thostName:   _" + str(hostName)  + "_"
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 
# 	def testPhotoEmails2(self):
# 		print "\tTestphotoEmails2"
# 		stage = "developmentMarvin"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		hostName = retObjConn.getComment()
# 		retObj = photoFunctions.photoEmails2(conn)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\thostName:   _" + str(hostName)  + "_"
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 		
# 	def testPhotoYearRecordsExport(self):
# 		print "\tTestPhotoYearRecordsExport"
# 		stage = "developmentMarvin"
# 		year = 1923
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.photoYearRecordsExport(conn, year)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"

# 	def testPhotoFileConvertObj(self):
# 		print "\tTestPhotoFileConvertObj"
# 		dirPath = "/Volumes/photoRepository/jeffTest"
# 		dirContentsFile ="/scripts/photoProcess/TEMP/dirContentsFile.txt"	
# 		dirContentsFileJpg = "/scripts/photoProcess/TEMP/dirContentsFileJpg.txt"
# 		baseTemp = "/scripts/photoProcess/TEMP/"
# 		badName ="/Volumes/repository3/badName"
# 		badTif = "/Volumes/repository3/badTif"
# 		retObj=directory.listFilesSuffixNoDups2( dirPath, "tif" )
# 		searchList = retObj.getResult()
# 		print ("\t\tsearchList:  " + str(searchList))
# 		fileFunctions.listToFile(searchList, dirContentsFile)
# 		retObj = photoFunctions.photoFileConvertObj (dirContentsFile, dirContentsFileJpg, baseTemp, badName, badTif, False )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		assestList = result[0]
# 		badTiffList = result[1]
# 		badNameList = result[2]
# 		print "\t\tassestList:   _" + str(assestList)  + "_"
# 		print "\t\tbadTiffList:   _" + str(badTiffList)  + "_"		
# 		print "\t\tbadNameList:   _" + str(badNameList)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"

# 	def testSetImageMetaData(self):
# 		print "\tTestSetImageMetaData"
# 		print "\ttest if LRC-2015-B701_P-00001.jpg can have metadata set"
# 		asset = "LRC-2015-B701_P-00001.tif"
# 		stage = "developmentMarvin"
# 		metaDataFile = "exif.txt"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.setImageMetaData (conn, asset, metaDataFile)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 		
# 	
# 	def testGetImageMetaDataDatabase(self):
# 		print "\tTestGetImageMetaDataDatabase"
# 		print "\ttest if LRC-2015-B701_P-00215 returns metadata"
# 		image = "LRC-2015-B701_P-00215.jpg"
# 		stage = "developmentMarvin"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.getImageMetaDataDatabase (conn, image)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 		
# 	def testPhotoDelete_Exists(self):
# 		print "\tTestPhotoDelete_Exists"
# 		print "\ttest if 1957-L-00027.jpg -  does  exist"
# 		image = "1957-L-00027.jpg"
# 		stage = "developmentMarvin"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.photoDelete (conn, stage, image)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 
# 	def testPhotoDelete_DoesNotExists(self):
# 		print "\tTestPhotoDelete_DoesNotExists"
# 		print "\ttest if 1901-L-00027.jpg -  does  exist"
# 		image = "1901-L-00027.jpg"
# 		stage = "developmentMarvin"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.photoDelete (conn, stage, image)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"	
# 		
# 	def testPhotoExistObj_Exists(self):
# 		print "\tTestPhotoExistObj_Exists"
# 		print "\ttest if LRC-1942-B701_P-27064.jpg -  does  exist"
# 		image = "LRC-1942-B701_P-27064.jpg"
# 		stage = "developmentMarvin"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.photoExistObj (conn, image)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"
# 
# 	def testPhotoExistObj_DoesNotExists(self):
# 		print "\tTestPhotoExistObj_DoesNotExists"
# 		print "\ttest if 1901-L-00027.jpg -  does  exist"
# 		image = "1901-L-00027.jpg"
# 		stage = "developmentMarvin"
# 		retObjConn = photoFunctions.photoConnectMysql2(stage)
# 		conn = retObjConn.getResult()
# 		retObj = photoFunctions.photoExistObj (conn, image)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 
# 		print "\t\tresult:   _" + str(result)  + "_"
# 		print "\t\tretVal:   _" + str(retVal)  + "_"
# 		print "\t\tcomment:  _" + comment + "_"
# 		print "\t\tstdout:   _" + stdout + "_"
# 		print "\t\tstderr:   _" + stderr + "_"
# 		print "\t\tremed:    _" + remed + "_"
# 		print "\t\tfound:    _" + str(found) + "_"	
# 		print "\t\terror:    _" + error + "_"	
# 		print "\t\tcommand:  _" + str(command)  + "_"		
# 
# 	def testConvertNoYearNewNameToNewNameYearCheckMastered(self):
# 		print "\ttestConvertNoYearNewNameToNewNameYearCheckMastered"
# 		#LRC-B701_P-00060.tif to LRC-1921-B701_P00060.tif
# 		YearFile="years.txt"
# 		fileName = "LRC-B701_P-00060.tif"
# 		correct = "LRC-1921-B701_P00060.tif"
# 		retObj = photoFunctions.convertNoYearNewNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 
# 	def testConvertNoYearNewNameToNewNameYearCheckSource(self):
# 		print "\ttestConvertNoYearNewNameToNewNameYearCheckSource"
# 		#LRC-B701_P-00060.tif to LRC-1921-B701_P00060.tif
# 		YearFile="years.txt"
# 		fileName = "R-LRC-B701_P-00060.tif"
# 		correct = "R-LRC-1921-B701_P00060.tif"
# 		retObj = photoFunctions.convertNoYearNewNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"			
# 
#  	def testRepoCheck2NotMasterNotSource(self):
# 		print "\tTestRepoCheck2NotMasterNotSource"
# 		print "\ttest if LRC-1942-B701_P-27064.tif does not exist"
# 		image = "LRC-1942-B701_P-27064.tif"
# 		repositorylist = "repositorylist.txt"
# 		retObj = photoFunctions.repoCheck2(image, repositorylist)
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
# 		print "\t\terror:   _" + error + "_"	
# 
# 
# 
# 	def testRepoCheck2FoundMasterNotSource(self):
# 		print "\tTestRepoCheck2FoundMasterNotSource"
# 		print "\ttest if LRC-1930-B701_P_F003-03925.tif exists in mastered"
# 		image = "LRC-1930-B701_P_F003-03925.tif"
# 		repositorylist = "repositorylist.txt"
# 		retObj = photoFunctions.repoCheck2(image, repositorylist)
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
# 		print "\t\terror:   _" + error + "_"	
# 
# 	def testRepoCheck2NotMasterFoundSource(self):
# 		print "\tTestRepoCheck2NotMasterFoundSource"
# 		print "\ttest if R-LRC-1922-B701_P-00183.tif exists in source"
# 		image = "R-LRC-1922-B701_P-00183.tif"
# 		repositorylist = "repositorylist.txt"
# 		retObj = photoFunctions.repoCheck2(image, repositorylist)
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
# 		print "\t\terror:   _" + error + "_"			
# 
# 	def testPhotoPartsOld_NoYearProcessWithDecimalsRaw(self):
# 		print "\tTestPhotoPartsOld_NoYearProcessWithDecimalsRaw"
# 		fileName = "R-L-15645_1231234.tif"
# 		retObj = photoFunctions.photoPartsOld2(fileName)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
# 	def testPhotoPartsOld_ProcessWithDecimalsRaw(self):
# 		print "\tTestPhotoPartsOld_ProcessWithDecimalsRaw"
# 		fileName = "R-1995-L-15645_1231234.tif"
# 		retObj = photoFunctions.photoPartsOld2(fileName)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
# 	def testPhotoPartsOld_NoYearProcessWithDecimals(self):
# 		print "\tTestPhotoPartsOld_NoYearProcessWithDecimals"
# 		fileName = "L-15645_1231234.tif"
# 		retObj = photoFunctions.photoPartsOld2(fileName)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
# 	def testPhotoPartsOld_ProcessWithDecimals(self):
# 		print "\tTestPhotoPartsOld_ProcessWithDecimals"
# 		fileName = "1995-L-15645_1231234.tif"
# 		retObj = photoFunctions.photoPartsOld2(fileName)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
# 
# 	def testImageProperlyNamedOld2_NoYearProcessWithDecimals(self):
# 		print "\tTestImageProperlyNamedOld2_NoYearProcessWithDecimals"
# 		fileName = "L-15645_1231234.tif"
# 		retObj = photoFunctions.imageProperlyNamedOld2( fileName )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
# 	def testImageProperlyNamedOld2_processNoYearWithDecimalsTooManySeq(self):
# 		print "\tTestImageProperlyNamedOld2_processNoYearWithDecimalsTooManySeq#"
# 		fileName = "L-156455_1231234.tif"
# 		retObj = photoFunctions.imageProperlyNamedOld2( fileName )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
# 	def testImageProperlyNamedOld2_processWithDecimalsTooManySeq(self):
# 		print "\tTestImageProperlyNamedOld2_processWithDecimalsTooManySeq#"
# 		fileName = "1988-L-156455_1231234.tif"
# 		retObj = photoFunctions.imageProperlyNamedOld2( fileName )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
# 	def testImageProperlyNamedOld2_processWithDecimals(self):
# 		print "\tTestImageProperlyNamedOld2_processWithDecimals"
# 		fileName = "1988-L-15645_1231234.tif"
# 		retObj = photoFunctions.imageProperlyNamedOld2( fileName )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
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
# 			
# 	def testProperNumberingGoodFileName(self):
# 		print "\tTestProperNumbering"
# 		fileName = ""
# 		stage = "development"
# 		retDict=photoFunctions.properNumbering(fileName, stage)
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
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		
# 	def testPhotoYearsNOTGivenYear(self):
# 		print "\tTestPhotoYearsNOTGivenYear"
# 		year = ""
# 		knowStart = 1
# 		knowEnd = 97253
# 		stage = "development"
# 		retDict=photoFunctions.photoConnectMysqlDict(stage)
# 		conn = retDict['conn']	
# 		retObj = photoFunctions.photoYears(conn, year)
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
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		
# 	def testPhotoYearsGivenYear(self):
# 		print "\tTestPhotoYearsGivenYear"
# 		year = 1957
# 		knowStart = 1
# 		knowEnd = 5658
# 		stage = "development"
# 		retDict=photoFunctions.photoConnectMysqlDict(stage)
# 		conn = retDict['conn']	
# 		retObj = photoFunctions.photoYears(conn, year)
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
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 	
# 
# 
# 	def testconvertOldNameToNewNameYearCheckYear1930(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckYearUnderScore"
# 		#L-03925_3.tif to LRC-1930-B701_P_F003-03925.tif
# 		YearFile="years.txt"
# 		fileName = "L-03925_3.tif"
# 		correct = "LRC-1930-B701_P_F003-03925.tif"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 	
# 	def testconvertOldNameToNewNameYearCheckYearRaw(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckYearRaw"
# 		#R_1988-L-00809.tiff to R-LRC-1988-B701_P-00809.tif
# 		YearFile="years.txt"
# 		fileName = "R_1988-L-00809.tif"
# 		correct = "R-LRC-1988-B701_P-00809.tif"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 
# 	def testconvertOldNameToNewNameYearCheckNoYearTwoDecRaw(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckNoYearTwoDecRaw"
# 		#R-L-156345_1231234.tif to R-LRC-B701_P_L-F1231234-156345.tif
# 		fileName = "R-L-156345_1231234.tif"
# 		correct = "R-LRC-B701_P_F1231234-156345.tif"
# 		YearFile="years.txt"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
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
# 	def testconvertOldNameToNewNameYearCheckNoYear1931(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckNoYear1931"
# 		#L-6038.tif to LRC-1931-B701_P-6038.tif
# 		fileName = "L-6038.tif"
# 		correct = "LRC-1931-B701_P-6038.tif"
# 		YearFile="years.txt"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 			
# 	def testconvertOldNameToNewNameYearCheckRawNoYear(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckRawNoYear"
# 		#R-L-03683.tif to R-LRC-B701_P-03683.tif
# 		fileName = "R-L-00148.tif"
# 		correct = "R-LRC-1921-B701_P-00148.tif"
# 		YearFile="years.txt"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 			
# 	def testconvertOldNameToNewNameYearCheckRawYear(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckRawYear"
# 		#R-1987-L-12115-11.tif to R-LRC-1987-B701_P_F11-12115.tif
# 		fileName = "R-1987-L-12115-11.tif"
# 		correct = "R-LRC-1987-B701_P_F011-12115.tif"
# 		YearFile="years.txt"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 
# 	def testconvertOldNameToNewNameYearCheckNoYear(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckNoYear"
# 		#L-156345.tif to LRC-B701_P-156345.tif
# 		fileName = "L-156345.tif"
# 		correct = "LRC-B701_P-156345.tif"
# 		YearFile="years.txt"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 			
# 	def testconvertOldNameToNewNameYearCheckNoYearTwoDec(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckNoYearTwoDec"
# 		#L-156345_1231234.tif to LRC-B701_P_L-F1231234-156345.tif
# 		fileName = "L-156345_1231234.tif"
# 		correct = "LRC-B701_P_F1231234-156345.tif"
# 		YearFile="years.txt"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
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
# 
# 	def testconvertOldNameToNewNameYearCheckYear(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckYear"
# 		#L-156345_1231234.tif to LRC-B701_P_L-F1231234-156345.tif
# 		fileName = "1988-L-156345.tif"
# 		correct = "LRC-1988-B701_P-156345.tif"
# 		YearFile="years.txt"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result['newName']:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 	
# 	def testconvertOldNameToNewNameYearCheckYearTwoDec(self):
# 		print "\tTestconvertOldNameToNewNameYearCheckYearTwoDec"
# 		#L-156345_1231234.tif to LRC-B701_P_L-F1231234-156345.tif
# 		fileName = "1988-L-156345_1231234.tif"
# 		correct = "LRC-1988-B701_P_F1231234-156345.tif"
# 		YearFile="years.txt"
# 		retObj = photoFunctions.convertOldNameToNewNameYearCheck( fileName, YearFile )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(fileName)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
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
# 					
# 	
# 	def testRemoveBadCharsSpaces(self):
# 		print "\ttestRemoveBadCharsSpaces"
# 		#L-156345.1231234.tif to L-156345_1231234.tif
# 		filePath = "L-156345_1231234.tif  "
# 		correct = "L-156345_1231234.tif"
# 		retObj = photoFunctions.removeBadChars( filePath )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(filePath)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 					
# 	def testRemoveBadCharsDoubleHypen(self):
# 		print "\ttestRemoveBadCharsDoubleHypen"
# 		#L-156345.1231234.tif to L-156345_1231234.tif
# 		filePath = "L--156345_1231234.tif"
# 		correct = "L-156345_1231234.tif"
# 		retObj = photoFunctions.removeBadChars( filePath )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(filePath)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 
#  	def testRemoveBadCharsDecimal(self):
# 		print "\ttestRemoveBadCharsDecimal"
# 		#L-156345.1231234.tif to L-156345_1231234.tif
# 		filePath = "L-156345.1231234.tif"
# 		correct = "L-156345_1231234.tif"
# 		retObj = photoFunctions.removeBadChars( filePath )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		error = retObj.getError()
# 		print "\t\tfilePath  :  _" + str(filePath)  + "_"
# 		print "\t\tcorrect   :  _" + str(correct)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tcommand: _" + command + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		if correct == result:
# 			print "\t\t\tsuccess"
# 		else:
# 			print "\t\t\tfailure"
# 
#   	def testPrefix(self):
#   		print "testPhotoPrefix"
# 		retDict = photoFunctions.photoConnectMysqlDict("production")
# 		conn = retDict['conn']
# 		retObj = photoFunctions.prefix (conn)
# 		result = retObj.getResult()
# 		print result['L']
# 		print result['LV']
# 			
#   	def testUpdateWebserverImage(self):
# 		print "testUpdateWebserverImage"
# 		image = "/scripts/photoProcess/TEMP/Full/1959-L-00057.jpg"
# 		repositorylist="/scripts/photoProcess/LIST/repositorylist.txt"
# 		retDict = photoFunctions.updateWebserverImage(image, repositorylist)
# 		print retDict
# 		
# 		
#  	def testIsRawTrue(self):
# 		print "testIsRawTrue"
# 
#  	def testPhotoPartsDicOrigNoYear(self):
# 		print "\ttestPhotoPartsDicOrigNoYear"
# 		testVal = "R-L-44556.tif"
# 		retDict = photoFunctions.photoPartsDict(testVal)
# 		year = retDict['year']
# 		type = retDict['type']
# 		if year == "":
# 			year = 0
# 		else:
# 			year = int(retDict['year'])
# 		print "\t\tyear:  " + str(year)
# 		print "\t\ttype:  " + type
# 		self.assertEqual( year , 0 )	
# 		
#  	def testPhotoPartsDicOrigYear(self):
# 		print "\ttestPhotoPartsDicOrigYear"
# 		testVal = "R-1984-L-12310.tif"
# 		retDict = photoFunctions.photoPartsDict(testVal)
# 		year = retDict['year']
# 		type = retDict['type']
# 		if year == "":
# 			year = 0
# 		else:
# 			year = int(retDict['year'])
# 		print "\t\tyear:  " + str(year)
# 		print "\t\ttype:  " + type
# 		self.assertEqual( year , 1984 )	
# 
#  	def testPhotoPartsDicModNoYear(self):
# 		print "\ttestPhotoPartsDicModNoYear"
# 		testVal = "L-5555.tif"
# 		retDict = photoFunctions.photoPartsDict(testVal)
# 		year = retDict['year']
# 		type = retDict['type']
# 		if year == "":
# 			year = 0
# 		else:
# 			year = int(retDict['year'])
# 		print "\t\tyear:  " + str(year)
# 		print "\t\ttype:  " + type
# 		self.assertEqual( year , 0 )
# 		
#  	def testPhotoPartsDicModYear(self):
# 		print "\ttestPhotoPartsDicOrigYear"
# 		testVal = "1981-L-12310.tif"
# 		retDict = photoFunctions.photoPartsDict(testVal)
# 		year = retDict['year']
# 		type = retDict['type']
# 		if year == "":
# 			year = 0
# 		else:
# 			year = int(retDict['year'])
# 		print "\t\tyear:  " + str(year)
# 		print "\t\ttype:  " + type
# 		self.assertEqual( year , 1981 )
# 				
#   	def testUpdateWebserverModifiedImage(self):
# 		print "\ttestUpdateWebserverImage"
# 		image = "/scripts/photoProcess/TEMP/Full/1964-L-00711.tif"
# 		repositorylist="/scripts/photoProcess/LIST/repositorylist.txt"
# 		retDict = photoFunctions.updateWebserverImage(image, repositorylist)
# 		result = retDict['result']
# 		print "\t\tresult:  " + str(result)
# 		
#  	def testUpdateWebserverOriginalImage(self):
# 		print "\ttestUpdateWebserverOriginalImage"
# 		image = "/scripts/photoProcess/TEMP/Full/R-1993-L-00002.tif"
# 		repositorylist="/scripts/photoProcess/LIST/repositorylist.txt"
# 		retDict = photoFunctions.updateWebserverImage(image, repositorylist)
# 		result = retDict['result']
# 		print "\t\tresult:  " + str(result)
# 		
#  	def testIsRawTrue(self):
# 		print "\ttestIsRawTrue"
# 		testVal = "R-1981-L-1231"
# 		if photoFunctions.isRaw(testVal):
# 			retVal = 0
# 		else:
# 			retVal = 1
# 		self.assertEqual( retVal , 0 )	
# 		
#  	def testPhotoImagesRepos(self):
# 		print "testPhotoImagesRepos"
#  		suffix="tif"
#  		dict=photoFunctions.photoImagesRepos(repositorySearchListFile, repositoryImageListFile, suffix)
#  		self.assertEqual( dict['count'] , testAmount )
#  		print dict['comment']
#  		
# 	def testPhotoFileModReturn(self):
# 		l=log()
# 		prefix="test"
# 		l.setData(prefix, "myLogger")
# 		knownAnswer="1981-L-12345_000.tif"
# 		retDic=photoFunctions.photoFileModReturn (l, threeDecimalFile)
# 		newTIFF=retDic['newTIFF']
#  		print "_"+newTIFF+"_"
# 		error=retDic['error']	
# 		print "_"+error+"_"
# 		self.assertEqual( newTIFF , knownAnswer )
# 
#  	def testPhotoPartsDicModNoYear(self):
# 		print "\ttestPhotoPartsDicModNoYear"
# 		testVal = "L-5555.tif"
# 		retDict = photoFunctions.photoPartsDict(testVal)
# 		year = retDict['year']
# 		type = retDict['type']
# 		if year == "":
# 			year = 0
# 		else:
# 			year = int(retDict['year'])
# 		print "\t\tyear:  " + str(year)
# 		print "\t\ttype:  " + type
# 		self.assertEqual( year , 0 )
# 		
#  	def testPhotoPartsDicModYear(self):
# 		print "\ttestPhotoPartsDicOrigYear"
# 		testVal = "1981-L-12310.tif"
# 		retDict = photoFunctions.photoPartsDict(testVal)
# 		year = retDict['year']
# 		type = retDict['type']
# 		if year == "":
# 			year = 0
# 		else:
# 			year = int(retDict['year'])
# 		print "\t\tyear:  " + str(year)
# 		print "\t\ttype:  " + type
# 		self.assertEqual( year , 1981 )
# 				
#   	def testUpdateWebserverModifiedImage(self):
# 		print "\ttestUpdateWebserverImage"
# 		image = "/scripts/photoProcess/TEMP/Full/1964-L-00711.tif"
# 		repositorylist="/scripts/photoProcess/LIST/repositorylist.txt"
# 		retDict = photoFunctions.updateWebserverImage(image, repositorylist)
# 		result = retDict['result']
# 		print "\t\tresult:  " + str(result)
# 		
#  	def testUpdateWebserverOriginalImage(self):
# 		print "\ttestUpdateWebserverOriginalImage"
# 		image = "/scripts/photoProcess/TEMP/Full/R-1993-L-00002.tif"
# 		repositorylist="/scripts/photoProcess/LIST/repositorylist.txt"
# 		retDict = photoFunctions.updateWebserverImage(image, repositorylist)
# 		result = retDict['result']
# 		print "\t\tresult:  " + str(result)
# 		
#  	def testIsRawTrue(self):
# 		print "\ttestIsRawTrue"
# 		testVal = "R-1981-L-1231"
# 		if photoFunctions.isRaw(testVal):
# 			retVal = 0
# 		else:
# 			retVal = 1
# 		self.assertEqual( retVal , 0 )	
# 		
#  	def testPhotoImagesRepos(self):
# 		print "testPhotoImagesRepos"
#  		suffix="tif"
#  		dict=photoFunctions.photoImagesRepos(repositorySearchListFile, repositoryImageListFile, suffix)
#  		self.assertEqual( dict['count'] , testAmount )
#  		print dict['comment']
#  		
# 	def testPhotoFileModReturn(self):
# 		l=log()
# 		prefix="test"
# 		l.setData(prefix, "myLogger")
# 		knownAnswer="1981-L-12345_000.tif"
# 		retDic=photoFunctions.photoFileModReturn (l, threeDecimalFile)
# 		newTIFF=retDic['newTIFF']
#  		print "_"+newTIFF+"_"
# 		error=retDic['error']	
# 		print "_"+error+"_"
# 		self.assertEqual( newTIFF , knownAnswer )
# 		

		
	def tearDown(self):
		print "tearDown" 
		print "#############################################"
		print ""
		
if __name__ == '__main__':
    unittest.main()
 