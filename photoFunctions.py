import sys
sys.path.append('lib')
sys.path.append('libPhoto')
#from datetime import datetime, date, time
import datetime
from time import *
from log import *
from simpleMail import *
from listFunctions import *
from fileFunctions import *
import socket
from stringFunctions import *
import shutil
from directory import *
from mysqlFunctions import *
from pprint import pprint
from paramiko import SSHClient
from scp import SCPClient
import paramiko
from comWrap import *
import string 
import funcReturn
import imageFunc
import dictFunc
import pprint
import re

def photoExistObj3 (conn, name):
	print "photoExistObj3"
	print "\tname:  " + name
	retObj = funcReturn.funcReturn('photoExistObj3')
	retObjPart=photoParts(name, "jpg")
			
	if (retObjPart.getRetVal() == 0):
		result = retObjPart.getResult()
		raw=result['raw']
	
	print "\traw:  " + str(raw)
	year=result['year']
	letter=result['letter']
	seq=result['seq']
	extra=result['extra']
	if extra != "":
		seq = seq + "." + extra

	type=result['type']
	noSuffix=result['noSuffix']
	webname=result['webname']
	
	print "year:  " + str(year)
	print "seq:   " + str(seq)
	statement = """SELECT *
			FROM P_L
			WHERE lYear = %s
			AND lSequence = %s""";
	stringArray = ["%s", "%s"]
	searchArray = [year, seq]				
# 	statement = """SELECT *
# 				FROM P_L
# 				WHERE fileName = %s""";
# 	stringArray = ["%s"]
# 	searchArray = [name]			
	retObjShow= showQuery ( statement, stringArray, searchArray)
	result = retObjShow.getResult()
	retObj.setCommand(result)
	c = conn.cursor()	
	c.execute (statement, searchArray)
	rows = c.fetchall()
	
	try:
		numberOfRows = len (rows)
		print "\tnumberOfRows:  "	+  	str(numberOfRows)
	except Exception:
		comment = "no records found for:  " + name
		retObj.setRetVal(0)
		retObj.setFound(1)
		numberOfRows = 0
			
	if numberOfRows == 1:
		print "numberOfRows = 1"
		retObj.setRetVal(0)
		retObj.setFound(0)
		retDic = {}
		rowList = list(rows)
		r = rowList[0]
		print "\tr:  " + str(r)
		retList = [numberOfRows]
		retObjRow = photoRowTodict(r)
		retDic = retObjRow.getRetDic()
		retList.append(retDic)
		print "\tretDic:  " + str(retDic)
		result = dict([('numberOfRows', numberOfRows), ('retDic', retDic)])
		retObj.setResult(result)
		comment = "numberOfRows:  " + str(numberOfRows) + " - " + name
		retObj.setRetDic(retDic)
	elif numberOfRows == 0:
		print "numberOfRows = 0"
		retObj.setRetVal(0)
		retObj.setFound(1)
		comment = "numberOfRows:  " + str(numberOfRows) + " - " + name
	else:
		print "numberOfRows > 1"
		error = "numberOfRows:  more than 1:  " + str(numberOfRows) + " - " + name
		retDic = {}
		retList = [numberOfRows]
		rowList = list(rows)
		for r in rowList:
			retObjRow = photoRowTodict(r)
			retDic = retObjRow.getResult()
			retList.append(retDic)
		retObj.setError(error)
		retObj.setFound(0)
		retObj.setResult(retList)
		retObj.setRetVal(0)
		return retObj
	
	retObj.setComment(comment)
	return retObj	
				
def photoUpdatePixel2 (conn, fileName, xsize, ysize):
	retObj = funcReturn.funcReturn('photoUpdatePixel')
	photo={}
	photoObj=photoParts(fileName, "jpg")
	retObjPart2=photoPartsOld3(fileName, "jpg")	

	if (photoObj.getRetVal() == 1) and (retObjPart2.getRetVal()  == 1):
		retObj.setError("photoUpdatePixel2: photoParts3 and photoParst2 failed")
		print "photoUpdatePixel2: photoParts3 and photoParst2 failed"
		return 	retObj		
		
	if (photoObj.getRetVal() == 0):
		photoResult = photoObj.getResult()
	
	if (retObjPart2.getRetVal() == 0):	
		photoResult = retObjPart2.getResult()

	type=photoResult['type'].strip()
	raw=photoResult['raw']
	alpha=photoResult['letter']
	retObj = prefix (conn)
	result = retObj.getResult()
	letter=result[alpha]
	year=photoResult['year']	
	if year == "":
		year = "noYear"
	seq=photoResult['seq']
	type=photoResult['type']
	noSuffix=photoResult['noSuffix']
	webname=photoResult['webname']
	if type == "raw":
		rawStr = "on"
	else:
		rawStr = "off"

	searchArray = [xsize, ysize, fileName]
	
	statement = """UPDATE P_L 
		SET timeModifiy =  CURRENT_TIMESTAMP, 
			xSize = %s,
			ySize = %s
		WHERE fileName = %s""";
	stringArray = ["%s" , "%s", "%s"]	
	
	retObjState = showQuery( statement, stringArray, searchArray)
	if retObjState.getRetVal() == 1:
		error = "photoUpdatePixel2:  problem with function showQuery - " + fileName
		er = retObjState.getError()
		print "\t\t" + error + "\n" + er
		retObj.setError(error)
		return retObj
	result = retObjState.getResult()
	print("\t\tinsert statement:  " + str(result))
	retObj.setComment("\t\tinsert statement:  " + str(result))
	c = conn.cursor()	
	c.execute (statement, searchArray)	
	retObj.setRetVal(0)
	return retObj

def photoUpdateRaw (conn, fileName, rawStr):
	retObj = funcReturn.funcReturn('photoUpdateRaw')
	photo={}
	
	searchArray = [rawStr, fileName]
	
	statement = """UPDATE P_L 
		SET timeModifiy =  CURRENT_TIMESTAMP, raw = %s
		WHERE fileName = %s"""
	stringArray = ["%s" , "%s"]	
	
	retObjState = showQuery( statement, stringArray, searchArray)
	if retObjState.getRetVal() == 1:
		error = "photoUpdateRaw:  problem with function showQuery - " + name
		er = retObjState.getError()
		print "\t\t" + error + "\n" + er
		retObj.setError(error)
		return retObj
	result = retObjState.getResult()
	print("\t\tinsert statement:  " + str(result))
	retObj.setComment("\t\tinsert statement:  " + str(result))
	c = conn.cursor()	
	c.execute (statement, searchArray)	
	retObj.setRetVal(0)
	return retObj

def photoParts2(fileName, type = "tif"):
	retObj = funcReturn.funcReturn('photoParts')
	if type == "tif":
		retObj2 = imageProperlyNamed(fileName)
		funcRun = "imageProperlyNamed - tif"
	else:
		retObj2 = imageProperlyNamedJpg(fileName)
		funcRun = "imageProperlyNamedJpg"
	retVal = retObj2.getRetVal()
	#R-LRC-1942-B701_P-27063.tif
	#print "retVal:  " + str(retVal)
	if retVal == 0:
		splitDot=fileName.split('.')
			
		splitHyphen=splitDot[0].split('-')
	
		result=isRaw(fileName)
	
		raw=""
		year=""	
		letter=""	
		seq=""
		type=""
		center = ""
		meta = ""
		extra = "" 
		#print "fileName:  " + fileName
		#print "isRaw:  " + str(isRaw(fileName))
		if isRaw(fileName):
			#print "sourced"
			center = splitHyphen[1]
			year = int(splitHyphen[2])
			hold = splitHyphen[3]
			splitF=hold.split('F')
			if len(splitF) == 2:
				meta = splitF[0]
				extra = splitF[1]
			else:
				meta = hold
			seq = splitHyphen[4]
			webname = fileName
			core = fileName
		else:
			#print "mastered"
			if splitHyphen[0] == "LRC":    #LRC test
				center = splitHyphen[0]
				year = int(splitHyphen[1])
				hold = splitHyphen[2]
				splitF=hold.split('F')
				if len(splitF) == 2:
					meta = splitF[0]
					extra = splitF[1]
				else:
					meta = hold
				seq = splitHyphen[3]
			webname = fileName
			core = splitDot[0]
		if isRaw(fileName):
			type = "source"
		else:
			type ="mastered"
		result = dict([('raw', result), ('center', center), ('meta', meta), ('extra', extra), ('year', year), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname), ('core', core)])	
		retObj.setResult(result)
		retObj.setRetVal(0)
	else:
		error = retObj2.getError()
		error = error + "\nfuncRun:  " + funcRun + "\n" + fileName + " is improperly named" + " - type:  " + type
		retObj.setError(error)
	return retObj

def photoPartsOld3(fileName, type = "tif"):
	retObj = funcReturn.funcReturn('photoPartsOld')
	print "photoPartsOld3"
	print "\tfileName:  " + fileName
	if type != "tif":
		fileNameNew = fileName.replace(type, "tif")
		fileName = fileNameNew
		print fileName
	webname = fileName.replace("tif", "jpg")
	
	
	retObj2 = imageProperlyNamedOld2(fileName)
	retVal = retObj2.getRetVal()

	#print "retVal:  " + str(retVal)
	if retVal == 0:
		splitDot=fileName.split('.')
			
		splitHyphen=splitDot[0].split('-')
	
		result=isRaw(fileName)
		print "\traw:  " + str(result)
		raw=""
		year=""	
		letter=""	
		seq=""
		type=""
		extra=""
		if isRaw(fileName):
			#year test
			if isNumber(splitHyphen[1]):
				year = splitHyphen[1]
				letter = splitHyphen[2]
				seq = splitHyphen[3]
			else:
				letter = splitHyphen[1]
				seq = splitHyphen[2]
		else:
			#year test
			if isNumber(splitHyphen[0]):
				year = splitHyphen[0]
				letter = splitHyphen[1]
				seq = splitHyphen[2]
			else:
				letter = splitHyphen[0]
				seq = splitHyphen[1]

		if isRaw(fileName):
			type = "source"
		else:
			type ="mastered"
		result = dict([('raw', result), ('year', year), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname), ('extra', extra)])	
		retObj.setResult(result)
		retObj.setRetVal(0)
	return retObj

#create list of asset and checksum; requires assets
def createAssetChksumList(assetList):
	resultList = []
	retObj=funcReturn.funcReturn('createAssetChksumList')
	for a in assetList:
		base = os.path.basename(a)
		newBase = base.replace("tif", "ck")
		dirPath = os.path.dirname(a) 
		yearDirPath =  os.path.dirname(dirPath)
		newFullPath = yearDirPath + "/ck/" + newBase
		entry = a + "\t" + newFullPath
		resultList.append(entry)
	retObj.setResult(resultList)
	retObj.setRetVal(0)
	return retObj
	
def photoFileConvertObj (dirContentsFile, dirContentsFileJpg, temp, badName, badTif, checkName = True ):
	retObj = funcReturn.funcReturn('photoFileConvertObj')
	print "\tphotoFileConvertObj"
	dirContentsList = listFromFile(dirContentsFile)
	newDirContentsList = []
	jpdDirFull=temp + "Full"
	makeDirectory(jpdDirFull)
	jpdDirThumb=temp + "Thumb"
	makeDirectory(jpdDirThumb)
	jpgList = []
	badNameList = []
	badTifList = []
	error = ""
	#change privilege and correct names
	sizeDir=len(dirContentsList)
	count=0
	comments = ""
	comment = "\tdirContentsFile:  "+ dirContentsFile
	print comment 
	comments = comments + comment + "\n"
	comment = "\tsizeDir:  "+ str(sizeDir)
	print comment 
	comments = comments + comment + "\n"
	for t in dirContentsList:
		t=t.rstrip()
		comment = "\t\tt:  "+ t
		print comment 
		comments = comments + comment + "\n"
		count+=1
		comment = "\t\t" + str(count) + " of " + str(sizeDir)
		base = os.path.basename(t) 
		comment = "\t\tbase:  "+ base 
		print comment 
		comments = comments + comment + "\n"
		comment = "\t\tcheckName:  "+ str(checkName)
		print comment 
		comments = comments + comment + "\n"
		if checkName == True:
			retObjNamed = imageProperlyNamed(base)		
			retVal = retObjNamed.getRetVal()
			checkVal = retVal
			comment = "\t\t\tif checkVal:  "+ str(checkVal)
			print comment 
			comments = comments + comment + "\n"
		else:
			checkVal = 0 
			comment = "\t\t\telse checkVal:  "+ str(checkVal)
			print comment 
			comments = comments + comment + "\n"
		if checkVal == 0:
			comment = "\t\t\tphoto is properly named:  "
			print comment 
			comments = comments + comment + "\n"			
			jpgBase = base.replace(".tif", ".jpg")
			jpgFull= jpdDirFull + "/" + jpgBase
			jpgThumb= jpdDirThumb + "/" + jpgBase
			comment = "\t\t\tjpgFull:  "+ jpgFull 
			print comment 
			comments = comments + comment + "\n"
			comment = "\t\t\tjpgThumb:  "+ jpgThumb
			print comment 
			comments = comments + comment + "\n"
			retObjBig = comWrapConvertTiff2JpgObj( t, jpgFull)
			retValBig =retObjBig.getRetVal()
			commandBig =retObjBig.getCommand()
			comment = "\t\t\tcommandBig:  "+ str(commandBig)
			print comment 
			comments = comments + comment + "\n"
			comment = "\t\t\tretValBig:  "+ str(retValBig) 
			print comment 
			comments = comments + comment + "\n"
			retObjThumb = comWrapConvertTiff2JpgThumbObj( t, jpgThumb)
			retValThumb =retObjThumb.getRetVal()
			commandThumb =retObjThumb.getCommand()
			comment = "\t\t\tcommandThumb:  "+ str(commandThumb)
			print comment 
			comments = comments + comment + "\n"
			comment = "\t\t\tretValThumb:  "+ str(retValThumb)
			print comment 
			comments = comments + comment + "\n"
			commandThumb=retObjThumb.getCommand()
			commandFull=retObjBig.getCommand()
			#test to see that tif file was able to convert to jpg
			#change test to testing existence of file before going forward
			if (retObjThumb == 1 or retObjThumb == 1):
				badTifList.append(t)
				comment = "\t\tcommandThumb:  tif is badly constructed and can't be converted:  " + t
				print comment 
				comments = comments + comment + "\n"
				comment = "\t\tcommandThumb:  "+ commandFull + "\n"
				print comment 
				comments = comments + comment + "\n"
				comment = "\t\tcommandThumb:  "+ commandThumb
				print comment 
				comments = comments + comment + "\n"
				src = t
				dst = badTif + "/" + base
				retDict = fileMove2 (src, dst)
				result=retDict['retVal']
				if result == 1:
					errorInst = retDict['error']
					errorInst = "unable to move badly constructed tif file:  " + src + " - " + errorInst + "\n"
					error = error + errorInst
					retObj.setError(error)
					retObj.setCommand(command)
					return retObj
			else:
				#create new list for next function
				newDirContentsList.append(t)
				jpgList.append(jpgBase)		
		else:
			badNameList.append(t)
			comment = "\t\tphoto is not properly named:  " + base + "\n"
			src = t
			dst = badName + "/" + base
			retDict = fileMove2 (src, dst)
			result=retDict['retVal']
			if result == 1:
				errorInst = retDict['error']
				errorInst = "unable to move badly constructed tif file:  " + src + " - " + errorInst + "\n"
				error = error + errorInst
				retObj.setError(error)
				retObj.setCommand(command)
				return retObj
				
	listToFile(jpgList, dirContentsFileJpg)
	#create new dirContentsList
	listToFile(newDirContentsList, dirContentsFile)
		
	resultList = [newDirContentsList, badNameList, badTifList]
	retObj.setResult(resultList)
	retObj.setComment(comments)
	retObj.setRetVal(0)	
	return retObj

def photoTransferObj(stage, temp, outputFile, repositorylist):
	retObj = funcReturn.funcReturn('photoTransferObj')
	now = datetime.datetime.now()
	dirBaseName= now.strftime("%Y%m%d%H%M%S")
	curDir=os.getcwd()
	user="msbwcup"
	public_key = '/Users/admin/.ssh/.ssh/id_rsa.pub'
	private_key = '/Users/admin/.ssh/.ssh/id_rsa'
	comments = ""
	comment = "\tstage:  " + stage 
	print comment 
 	comments = comments + comment + "\n"
	comment = "\ttemp:  " + temp 
	print comment 
 	comments = comments + comment + "\n"
	if stage == "production":
		sshConnect="msbwcup@lamp.larc.nasa.gov"	
		dstDir="/usr/local/web/htdocs/msbwc/photo/"
		server="lamp.larc.nasa.gov"
	else:
		sshConnect="msbwcup@lamp-d.larc.nasa.gov"	
		dstDir="/usr/local/web/htdocs/msbwc-d/photo/"
		server="lamp-d.larc.nasa.gov"

	######################### create big images - begin ########################
	dst = dstDir + "images"
	jpdDirFull=temp + "Full"
	#Create list of files with the Full directory within the temp directory
	dirContentsList = glob.glob(jpdDirFull + "/*" )
	sizeDir=len(dirContentsList)
	comment = "\t==================Big Image - Begin ================" 
	print comment 
 	comments = comments + comment + "\n"
	comment = "\t\tjpdDirFull:  "+ jpdDirFull 
	print comment 
 	comments = comments + comment + "\n"
	os.chdir(jpdDirFull)
	count=0
	#iterate through created list 
	#remove the R- 
	#push to lamps
 	comments = comments + comment + "\n"
	for t in dirContentsList:
		t=t.rstrip()
		comment = "\t\tt:  " + t 
		print comment 
		comments = comments + comment + "\n"
		retDict = repoCheck(t, repositorylist) 
		#if file does not exist or is modified image
		comment = "\t\trepoCheck comment"
		print comment 
		commentList = retDict['comment'].split("\n")
		for r in commentList:
			if r != "\n":
				comment = "\t\t\t" + r
				print comment 
 				comments = comments + comment + "\n"
	
		if (retDict['result'] == "update"):
			comment = "\t\tfile did not exist on repository or is a modified image"
			src = t.replace("R-", "")
			os.rename(t, src)
			comment = "\t\timage - full:  "+ t
			print comment 
 			comments = comments + comment + "\n"
			comment = "\t\tsrc:  "+ src	 
			print comment 
 			comments = comments + comment + "\n"
			if fileExist(outputFile):
				fileDelete (outputFile)
			fileCreate(outputFile)
			os.chmod(outputFile, 0777)
			resultDict=comWrapSSH(src, sshConnect, dst, "ladmin", outputFile)
			errorCheck = resultDict['errorCheck']
			comment = "\t\tcomWrapSSH"
			print comment
			comment = "\t\t\terrorCheck:  " + str(errorCheck) 
			print comment 
 			comments = comments + comment + "\n"
			command = resultDict['command']
			comment = "\t\t\tcommand:  " + command 
			print comment 
 			comments = comments + comment + "\n"
			output = resultDict['output']
			comment = "\t\t\toutput:  "  
			print comment 
			outputList = output.split("\n")
			for o in outputList:
				comment = "\t\t\t"  + o
				print comment
 				comments = comments + comment + "\n"
			result =  resultDict['retVal']
			comment = "\t\t\tresult:  " + str(result)  
			print comment 
 			comments = comments + comment + "\n"
			if result == 0:
				fileDelete(src)
				comment = "\t\t\tdeleted image - full:  "+ t
				print comment 
				comments = comments + comment + "\n"
			else:
				error = "unable to transfer big image file:  " + t  
				retObj.setError(error)
				command = resultDict['command']
				retObj.setCommand(command)
				return retObj
		else:
			comment = "\t\tfile did exist on repository"  
			print comment 
 			comments = comments + comment + "\n"
			fileDelete(t)
	comment = "\t==================Big Image - End ================" 
	print comment 
 	comments = comments + comment + "\n"
	######################### create big images - end ########################

	######################### create thumb images - begin ########################
	comment = "\t================Thumbs -  Begin ========================"
	print comment 
	comments = comments + comment + "\n"
	jpdDirThumb=temp + "Thumb"	
	dirContentsList = glob.glob(jpdDirThumb + "/*" )
	sizeDir=len(dirContentsList)
	comment = "\t\tjpdDirThumb:  "+ jpdDirThumb	
	print comment 
	comments = comments + comment + "\n"
	os.chdir(jpdDirThumb)
	count=0
	dst = dstDir + "thumbs"
	for t in dirContentsList:
		t=t.rstrip()
		retDict = repoCheck(t, repositorylist) 
		#if file does not exist or is modified image
		if (retDict['result'] == "update"):
			src = t.replace("R-", "")
			os.rename(t, src)
			if fileExist(outputFile):
				fileDelete (outputFile)
			fileCreate(outputFile)
			os.chmod(outputFile, 0777)
			resultDict=comWrapSSH(src, sshConnect, dst, "ladmin", outputFile)
			errorCheck = resultDict['errorCheck']
			comment = "\t\terrorCheck:  " + str(errorCheck) 
			print comment 
			comments = comments + comment + "\n"
			command = resultDict['command']
			comment = "\t\tcommand:  " + command 
			print comment 
			comments = comments + comment + "\n"
			output = resultDict['output']
			comment = "\t\t\toutput:  "  
			print comment 
			outputList = output.split("\n")
			for o in outputList:
				comment = "\t\t\t"  + o
				print comment
				comments = comments + comment + "\n"
			result =  resultDict['retVal']
			comment = "\t\t\tresult:  " + str(result) 
			print comment 
			comments = comments + comment + "\n"
			if result == 0:
				fileDelete(src)
				comment = "\t\t\tdeleted image - thumb:  "+ t
				print comment 
				comments = comments + comment + "\n"	
			else:
				error = "unable to transfer thumbnail image file:  " + t
				retObj.setError(error)
				command = resultDict['command'] 
				comments = comments + command
				retObj.setComment(comments)
				return retObj
		else:
			comment = "\t\tfile did exist on repository"
			print comment 
			comments = comments + comment + "\n"
			fileDelete(t)


	comment = "\t================Thumbs -  End ========================"
	print comment 
	comments = comments + comment + "\n"	
	
	num=countFiles(jpdDirFull)
	comment = "\tfiles left in " + jpdDirFull + ":  " + str(num)
	print comment 
	comments = comments + comment + "\n"	
	num=countFiles(jpdDirThumb)
	comment = "\tfiles left in " + jpdDirThumb + ":  " + str(num)
	print comment 
	comments = comments + comment + "\n"
	######################### create thumb images - begin ########################	
	
	os.chdir(curDir)
	retObj.setRetVal(0)
	retObj.setComment(comments)
	return retObj
	
def photoMysqlObj(dirContentsFileJpg, stage, cdNameFile, repositorylist):
	retObj = funcReturn.funcReturn('photoMysqlObj')
	comments = ""
	if fileExist(cdNameFile) == False:
		cdName = ""
	else:
		cdName=readFirstLineFile(cdNameFile)
	comment = "\tcdName:  " + cdName 
 	comments = comments + comment + "\n" 
	if stage == "production":
		webDir = "msbwc"
	else:
		webDir = "msbwc-d"
	comment = "\twebDir:  " + webDir 
 	comments = comments + comment + "\n"
		
	pathFin ="/usr/local/web/htdocs/" + webDir + "/photo/images"
	pathThumb ="/usr/local/web/htdocs/" + webDir + "/photo/thumbs"
	comment = "\tpathFin:  " + pathFin
	comments = comments + comment + "\n"
	comment = "\tpathThumb:  " + pathThumb 
 	comments = comments + comment + "\n"
	
	retObjConn = photoConnectMysql2(stage)
	if retObjConn.getRetVal() == 1:
		retObj.setError("photoConnectMysql2:  problem with mysql connection")
		errorFunc = retObjConn.getError()
		error = error + "\n" + errorFunc
		retObj.setError(error)
		retObj.setComment(comments)
		return retObj
	else:
		conn = retObjConn.getResult()
		
	retObjEmail=photoEmails2 (conn)
	photoEmail=retObjEmail.getResult()
	comment = "\tphotoEmail:  " + photoEmail 
	comments = comments + comment + "\n"
	
  	retObjPrefix=photoPrefix2 (conn)
  	result=retObjPrefix.getResult()
  	for key, value in result.items(): # returns the dictionary as a list of value pairs -- a tuple.
		comment = "\t\tkey:  " + key 
		comments = comments + comment + "\n"
		comment = "\t\tvalue:  " + str(value)
		comments = comments + comment + "\n"
		
	jpgList = listFromFile(dirContentsFileJpg)
	for j in jpgList:
		j=j.rstrip()
		comment = "\tj:  " + j 
		retObjName = imageProperlyNamedJpg(j)
		result = retObjName.getRetVal()
		if result == 0 :
			comment = "\t\tphoto is properly named" 
 			comments = comments + comment + "\n"
			retObjPart=photoParts(j, "jpg")
			
			if retObjPart.getRetVal() == 1:
				error = "photoConnectMysql2:  problem with function photoParts - " + j
				errorFunc = retObjPart.getError()
				error = error + "\n" + errorFunc
				retObj.setError(error)
				retObj.setComment(comments)
				return retObj
				
			result = retObjPart.getResult()
			raw=result['raw']
			year=result['year']
			if year == "":
				year = "noYear"
			letter=result['letter']
			seq=result['seq']
			type=result['type']
			noSuffix=result['noSuffix']
			webname=result['webname']
			core=result['core']
			comment = "\t\traw:  " + str(raw) 
 			comments = comments + comment + "\n"
			comment = "\t\tyear:  " + str(year) 
 			comments = comments + comment + "\n"
			comment = "\t\ttype:  " + type 
 			comments = comments + comment + "\n"
			comment = "\t\tseq:  " + seq 
 			comments = comments + comment + "\n"
			comment = "\t\tnoSuffix:  " + noSuffix 
 			comments = comments + comment + "\n"
			comment = "\t\twebname:  " + webname 
 			comments = comments + comment + "\n"
			comment = "\t\tcoreasfd:  " + core 
 			comments = comments + comment + "\n"
 			
 			
 			retObjExist = photoExistObj3(conn, webname)
			retValExist = retObjExist.getRetVal()
 			comment = "\t\tretValExist:  " + str(retValExist) 
 			print comment
 			comments = comments + comment + "\n"
 			
			if retValExist == 0:
				found = retObjExist.getFound() 
				comment = "\t\tfound:  " + str(found)
				comments = comments + comment + "\n"
				if found == 0:
					comment = "\t\texistInDatabase" 
					print comment
					comments = comments + comment + "\n"
					comment = "\t\tupdate database" 
					comments = comments + comment + "\n"
					
					retObjUpdate = photoUpdateObj (conn, webname, cdName, noSuffix)
					if retObjUpdate.getRetVal() == 1:
						error = "photoConnectMysql2:  problem with function photoUpdateObj - " + j
						retObj.setError(error)
						print error
						retObj.setComment(comments)
						return retObj
					else:
						sqlState = retObjUpdate.getComment()
						print sqlState
						comment = comments + sqlState + "\n"
				else:
					comment = "insert database" 
					print comment
 					comments = comments + comment + "\n"
					comment = "\t\tcomments  " + comment 
					comments = comments + comment + "\n"			
					comment = "\t\tj:  " + j 
					comments = comments + comment + "\n"
					comment = "\t\tcdName:  " + cdName
					comments = comments + comment + "\n"
					retObjInsert = photoInsertObj (conn, webname, cdName, noSuffix)
					if retObjInsert.getRetVal() == 1:
						error = "photoConnectMysql2:  problem with function photoInsertObj - " + j
						retObj.setError(error)
						print error
						retObj.setComment(comments)
						return retObj
					else:
						sqlState = retObjInsert.getComment()
						print sqlState
						comment = comments + sqlState + "\n"

			else:
				error = "photoConnectMysql2:  problem with function existInDatabase - " + j
				errorFunc = retObjExist.getError()
				error = error + "\n" + errorFunc
				retObj.setError(error)
				retObj.setComment(comment)
				return retObj	
		else:
			error = "photoConnectMysql2:  problem with function imageProperlyNamedJpg - " + j
			errorFunc = retObjName.getError()
			error = error + "\n" + errorFunc
			retObj.setError(error)
			retObj.setComment(comment)
			return retObj
	
   	c = conn.cursor()
  	c.close()
   	retObj.setResult(jpgList)
   	retObj.setComment(comment)
	retObj.setRetVal(0)
  	return retObj  	

def photoArchiveObj (dirContentsFile, archiveFile, baseError, chksumDir, stage):
	retObj = funcReturn.funcReturn('photoArchiveObj')
	dirContentsList = listFromFile(dirContentsFile)
	lenCheck = int(len(dirContentsList))
	comments = ""
	if lenCheck > 0:
		cssErrorMkdir=baseError + "cssErrorMkdir.txt"
		cssErrorCopyPic=baseError + "cssErrorCopyPic.txt"
		cssErrorCopyCK=baseError + "cssErrorCopyCK.txt"
		dirObj=makeDirectoryObj(chksumDir)
		retValDir= dirObj.getRetVal()
		if retValDir == 1:
			error = "makeDirectoryObj:  could not create directory:   ---" + dirPath
			retObj.setError(error)
			retObj.setComment(comments)
			return retObj
		
		hostName=socket.gethostname()		
		comment = "\thostName:  "+ hostName 
		print comment 
		comments = comments + comment + "\n"
				
		archiveList = []
		archiveList = listFromFile(archiveFile)
	
		#remove old chksum
		chksumList = glob.glob(chksumDir + "/*" )
		for c in chksumList:
			result=comWrapDelete(c)
			if result == 1:
				error = "comWrapDelete:  unable to delete file:  " + c
				retObj.setError(error)
				retObj.setComment(comments)
				return retObj
		try:
			curPath = os.getcwd()
		except Exception:
			error = "unable to get current direcotry"
			retObj.setError(error)
			retObj.setComment(comments)
			return retObj
			
		dirContentsList = listFromFile(dirContentsFile)
		sizeDir=len(dirContentsList)
		count=0
		for t in dirContentsList:
			t=t.rstrip()
			comment = "\tt:  "+ t
			print comment 
			comments = comments + comment + "\n"
			
			count+=1
			
			comment = "\t\t" + str(count) +" of "+ str(sizeDir)
			print comment 
			comments = comments + comment + "\n"
			
			base = os.path.basename(t) 
			comment = "\t\t\tbase:  " + base
			print comment 
			comments = comments + comment + "\n"
			
			dirPath = os.path.dirname(t) 
			comment = "\t\t\tdirPath:  "+ dirPath
			print comment 
			comments = comments + comment + "\n"
			
			retObjNamed = imageProperlyNamed(base)		
			retVal = retObjNamed.getRetVal()
			if retVal == 0:		
				comment = "\t\t\tphoto is properly named"
				print comment 
				comments = comments + comment + "\n"
				
				photo={}
				retObjPhoto=photoParts(base)
			
				if retObjPhoto.getRetVal() == 1:
					error = "photoParts:  problem with file:  " + base
					retObj.setError(error)
					retObj.setComment(comments)
					return retObj
				
				result = retObjPhoto.getResult()
				raw=result['raw']
				year=result['year']	
				if year == "":
					year = "noYear"
				letter=result['letter']	
				seq=result['seq']
				type=result['type']
				noSuffix=result['noSuffix']
							
				#create checksums and copy record to CSS
				for a in archiveList:
					archive=a.strip()	
					#cssDirCk=archive + "/" + hostName + "/" + type + "/" + str(year) + "/ck" 
					cssDirCk=archive + "/" + type + "/" + str(year) + "/ck" 

					comment =  "\t\t\t\tcssDirCk: " + cssDirCk
					print comment 
					comments = comments + comment + "\n"
					
					#cssDirPic=archive + "/" + hostName + "/" + type + "/" + str(year) + "/pic"
					cssDirPic=archive + "/" + type + "/" + str(year) + "/pic"

					comment =  "\t\t\t\tcssDirPic: " + cssDirPic
					print comment 
					comments = comments + comment + "\n"
					
					#create checkSum File
					#change directory to unprocessed folder
					try:
						os.chdir(dirPath)
					except Exception:
						os.chdir(curPath)	
						retObj.setError("unable to to change direcotry to: " + dirPath)
						retObj.setComment(comments)
						return retObj

					comment =  "\t\t\tchanged directory to: " + dirPath
					print comment 
					comments = comments + comment + "\n"

					chksumFilePath=chksumDir + noSuffix + ".ck"
					comment =  "\t\t\tchksumFilePath: " + chksumFilePath
					print comment 
					comments = comments + comment + "\n"
					
					result = comWrapCheckSum(base, chksumFilePath)
					if result != 0:
						os.chdir(curPath)	
						retObj.setError("unable to create checksum for " + base)
						retObj.setComment(comments)
						return retObj
					else:
						comment =  "\t\t\tcheck sum created"
						print comment 
						comments = comments + comment + "\n"
						
					comment =  "\t\t\tstage: " + stage
					print comment 
					comments = comments + comment + "\n"
					
					if stage == "production":
						#copy to CSS
						comment =  "\t\t\tlocal full path: " + t
						print comment 
						comments = comments + comment + "\n"
						comment =  "\t\t\tcssDirPic: " + cssDirPic
						print comment 
						comments = comments + comment + "\n"
						
						resultDict = comWrapMasmkdir(cssDirPic, cssErrorMkdir)
						command = resultDict[ 'command']
						
						comment =  "\t\t\tcomWrapMasmkdir command: " + command
						print comment 
						comments = comments + comment + "\n"
						
						result = resultDict[ 'retVal']
						if result != 0:		
							comment =  "\t\t\tstage: " + stage
							print comment 
							comments = comments + comment + "\n"									
							function = resultDict[ 'function']
							command = resultDict[ 'command']
							error = resultDict[ 'error']						
							function2 = resultDict[ 'function2']
							command2 = resultDict[ 'function2Command']
						
							errorMessage = "unable to mkdir pic for CSS: " + cssDirPic
							errorMessage = errorMessage + "function:  " + function + "\n"
							errorMessage = errorMessage + "command:  " + command + "\n"
							errorMessage = errorMessage + "error:  " + error + "\n"
							errorMessage = errorMessage + "function2:  " + function2 + "\n"
							errorMessage = errorMessage + "command2:  " + command2 + "\n"
							retObj.setError(errorMessage)
							retObj.setComment(comments)
							return retObj
						
						
						comment =  "\t\t\tcomWrapMasputDelay2:"
						print comment 
						comments = comments + comment + "\n"
						
						cssFullPath = cssDirPic + "/" + noSuffix + ".tif"
						comment =  "\t\t\t\tcssFullPath: " + cssFullPath
						print comment 
						comments = comments + comment + "\n"
						
						comment =  "\t\t\t\tcssErrorCopyPic: " + cssErrorCopyPic
						print comment 
						comments = comments + comment + "\n"
						
						resultDict = comWrapMasputDelay2(t, cssFullPath, cssErrorCopyPic)	
						command = resultDict[ 'command']
						comment =  "\t\t\tcomWrapMasputDelay2 command: " + command
						print comment 
						comments = comments + comment + "\n"
						
						commentList = resultDict[ 'comment']
						for c in commentList:
							comment =  "\t\t\t" + c 
							print comment 
							comments = comments + comment + "\n"
						result = resultDict[ 'retVal']
						if result != 0:												
							function = resultDict[ 'function']
							command = resultDict[ 'command']
							error = resultDict[ 'error']
							function2 = resultDict[ 'function2']
							command2 = resultDict[ 'function2Command']
						
							errorMessage = "unable to copy file to CSS: " + t
							errorMessage = errorMessage + "function:  " + function + "\n"
							errorMessage = errorMessage + "command:  " + command + "\n"
							errorMessage = errorMessage + "error:  " + error + "\n"
							errorMessage = errorMessage + "function2:  " + function2 + "\n"
							errorMessage = errorMessage + "command2:  " + command2 + "\n"
							retObj.setError(errorMessage)
							retObj.setComment(comments)
							return retObj
						
						comment =  "\t\t\tcssFullPath: " + cssFullPath
						print comment 
						comments = comments + comment + "\n"
						comment =  "\t\t\tcssDirCk: " + cssDirCk
						print comment 
						comments = comments + comment + "\n"
							
						resultDict = comWrapMasmkdir(cssDirCk, cssErrorMkdir)
						command = resultDict[ 'command']
						comment =  "\t\t\tcomWrapMasmkdir  command: " + command
						print comment 
						comments = comments + comment
						
						result = resultDict[ 'retVal']
						if result != 0:						
							function = resultDict[ 'function']
							command = resultDict[ 'command']
							error = resultDict[ 'error']
							function2 = resultDict[ 'function2']
							command2 = resultDict[ 'function2Command']
												
							errorMessage = "unable to mkdir checksum for CSS: " + cssDirCk
							errorMessage = errorMessage + "function:  " + function + "\n"
							errorMessage = errorMessage + "command:  " + command + "\n"
							errorMessage = errorMessage + "error:  " + error + "\n"
							errorMessage = errorMessage + "function2:  " + function2 + "\n"
							errorMessage = errorMessage + "command2:  " + command2 + "\n"
							retObj.setError(errorMessage)
							retObj.setComment(comments)
							return retObj
							
						cssCkFullPath = cssDirCk + "/" + noSuffix + ".ck"
						comment =  "\t\t\tcssCkFullPath: " + cssCkFullPath
						print comment 
						comments = comments + comment + "\n"
						
						resultDict = comWrapMasputDelay2(chksumFilePath, cssCkFullPath, cssErrorCopyCK)	
						command = resultDict[ 'command']
						result = resultDict[ 'retVal']
						comment =  "\t\t\tcomWrapMasputDelay2 command: " + command
						print comment 
						comments = comments + comment + "\n"
						
						commentList = resultDict[ 'comment']
						for c in commentList:
							comment =  "\t\t\t" + c 
							print comment 
							comments = comments + comment + "\n"
							
						comment =  "\t\t\tresult: " + str(result)
						print comment 
						comments = comments + comment + "\n"
						
						if result != 0:
							function = resultDict[ 'function']
							command = resultDict[ 'command']
							error = resultDict[ 'error']
							function2 = resultDict[ 'function2']
							command2 = resultDict[ 'function2Command']
							
							errorMessage = "unable to copy file to CSS: " + chksumFilePath						
							errorMessage = errorMessage + "function:  " + function + "\n"
							errorMessage = errorMessage + "command:  " + command + "\n"
							errorMessage = errorMessage + "error:  " + error + "\n"
							errorMessage = errorMessage + "function2:  " + function2 + "\n"
							errorMessage = errorMessage + "command2:  " + command2 + "\n"
							
							retObj.setError(errorMessage)
							retObj.setComment(comments)
							return retObj

			else:
				errorMessage = "photo is not properly named:  "
				retObj.setError(errorMessage)
				retObj.setComment(comments)
				return retObj	
		os.chdir(curPath)	
	else:
		comment =  "\t\t\tno records in list"
		print comment 
		comments = comments + comment + "\n"
			
	retObj.setComment(comments)
	retObj.setRetVal(0)
	return retObj						

def photoSortObj (dirContentsFile, resposDict, chksumDir, stage):
	retObj = funcReturn.funcReturn('photoSortObj')
	dirContentsList = listFromFile(dirContentsFile)
	sizeDir=len(dirContentsList)
	comments = ""
	comment = "\tsizeDir:  "+ str(sizeDir)
	print comment 
	comments = comments + comment + "\n"
	if int(sizeDir) > 0:
		count=0
		for t in dirContentsList:
			t=t.rstrip()
			
			comment = "\tt:  "+ t
			print comment  + "\n"
			comments = comments + comment
			count+=1
		
			comment = "\t"+ str(count) +" of "+ str(sizeDir)
			print comment 
			comments = comments + comment + "\n"
			
			base = os.path.basename(t) 
			comment = "\t\tbase:  "+ base
			print comment 
			comments = comments + comment + "\n"
			
			dirPath = os.path.dirname(t) 
			comment = "\t\tdirPath:  "+ dirPath
			print comment 
			comments = comments + comment + "\n"
			
			result=isRaw(base)
			comment = "\t\tisRaw:  " + str(result)
			print comment 
			comments = comments + comment + "\n"
			
			retObjNamed = imageProperlyNamed(base)		
			retVal = retObjNamed.getRetVal()
			if retVal == 0:

				comment = "\t\tphoto is properly named:"
				print comment 
				comments = comments + comment + "\n"
				
				retObjParts=photoParts(base)
				if retObjParts.getRetVal() == 1:
					error = "problem with function photoParts in function photoSort"
					retObj.setError("photoParts:  " + base)
					retObj.setComment(comments)
					return retObj
				
				result = retObjParts.getResult()
				raw=result['raw']
				year=result['year']	
				if year == "":
					year = "noYear"
				letter=result['letter']	
				seq=result['seq']
				type=result['type']
				noSuffix=result['noSuffix']
			
				repositoryProcess = resposDict['repoProcess']
				repositoryRaw = resposDict['repoRaw']
				newLocalFullPath=""
				
				if raw == True:					
					#go to raw repository
					comment = "\t\traw"
					print comment 
					comments = comments + comment + "\n"
					if year!="":
						comment = "\t\tyear:  " + str(year)
						print comment 
						comments = comments + comment + " \n"

						newLocalFullPath=repositoryRaw  + str(year) + "/pic/" + base
						newLocalFullPathck=repositoryRaw  + str(year) + "/ck/" + noSuffix + ".ck"
				else:
					comment = "\t\tprocessed"
					print comment 
					comments = comments + comment + " \n"

					newLocalFullPath=repositoryProcess  +  str(year) + "/pic/" + base
					newLocalFullPathck=repositoryProcess  +  str(year) + "/ck/" + noSuffix + ".ck"

				comment = "\t\tfor base:  " + base + " newPath:  " + newLocalFullPath
				print comment 
				comments = comments + comment + "\n"
	
				src = t
				dst = newLocalFullPath
				src2 = chksumFilePath=chksumDir + noSuffix + ".ck"
				comment = "\t\tnewLocalFullPathck:  " + newLocalFullPathck
				print comment 
				comments = comments + comment + "\n"
				
				dst2 = newLocalFullPathck
				comment = "\t\tstage:  " + stage
				print comment 
				comments = comments + comment + "\n"
				
				if stage == "production":
					comment = "\t\tsrc:  " + src
					print comment 
					comments = comments + comment + "\n"
				
					comment = "\t\tdst:  " + dst
					print comment 
					comments = comments + comment + "\n"
					
					retDict = fileMove2(src, dst)
					result=retDict['retVal']
					print  "\t\tresult:  " + str(result) 
					if result == 1:
						error = retDict['error']
						if error == "destination directory does not exist":
							print  "\t\t" + error + "   " + src
							dstDir = os.path.dirname(dst)
							os.makedirs(dstDir)
							print  "\t\tdstDir:  " + dstDir
							retDict = fileMove2(src, dst)
							result=retDict['retVal']
							if result == 1:
								errorMessage = "unable to move picture file - created directory:  " + src + "\n"
								print  "\t\t\t" + errorMessage
								errorMessage = "error:  " + error + "\n"
								retObj.setError(errorMessage)
								retObj.setComment(comments)
								return retObj
# 							else:
# 								errorMessage = "unable to move picture file:  " + src + "\n"
# 								errorMessage = "error:  " + error + "\n"
# 								retObj.setError(errorMessage)
# 								retObj.setComment(comments)
# 								return retObj
				
					retDict = fileMove2(src2, dst2)	
					result=retDict['retVal']
					if result == 1:
						error = retDict['error']
						if error == "destination directory does not exist":
							print  "\t\t" + error + "   " + src2
							dstDir = os.path.dirname(dst2)
							print  "\t\tdstDir:  " + dstDir
							os.makedirs(dstDir)
							retDict = fileMove2(src2, dst2)
							result=retDict['retVal']
							if result == 1:
								errorMessage = "unable to move checkSum file - created directory:  " + src + "\n"
								print  "\t\t\t" + errorMessage
								errorMessage = "error:  " + error + "\n"
								retObj.setError(errorMessage)
								retObj.setComment(comments)
								return retObj
# 						else:
# 							errorMessage = "unable to move checkSum file:  " + src + "\n"
# 							errorMessage = "error:  " + error + "\n"
# 							retObj.setError(errorMessage)
# 							retObj.setComment(comments)
# 							return retObj

			else:
				errorMessage = "photo is not properly named:  " + base + "\n"
				retObj.setError(errorMessage)
				retObj.setComment(comments)
				return retObj
				
	retObj.setComment(comments)
	retObj.setRetVal(0)
	return retObj

def photoUpdatePixel (conn, noSuffixName, xsize, ysize):
	retObj = funcReturn.funcReturn('photoUpdatePixel')
	name = noSuffixName + ".jpg"
	photo={}
	photoObj=photoParts(name, "jpg")
	
	if photoObj.getRetVal() == 1:
		e = photoObj.setError(error)
		error = "photoUpdatePixel:  problem with function photoParts - " + name + "\n\t\t" + e
		print "\t\t" + error
		retObj.setError(error)
		return retObj
	
	photoResult = photoObj.getResult()
	type=photoResult['type'].strip()
	raw=photoResult['raw']
	alpha=photoResult['letter']
	retObj = prefix (conn)
	result = retObj.getResult()
	letter=result[alpha]
	year=photoResult['year']	
	if year == "":
		year = "noYear"
	seq=photoResult['seq']
	type=photoResult['type']
	noSuffix=photoResult['noSuffix']
	webname=photoResult['webname']
	if type == "raw":
		rawStr = "on"
	else:
		rawStr = "off"

	searchArray = [rawStr, webname, xsize, ysize, year, seq]
	
	statement = """UPDATE P_L 
		SET timeModifiy =  CURRENT_TIMESTAMP, raw = %s, fileName = %s, 
			xSize = %s,
			ySize = %s
		WHERE lYear = %s
		AND lSequence  = %s""";
	stringArray = ["%s" , "%s" , "%s" , "%s", "%s", "%s"]	
	
	retObjState = showQuery( statement, stringArray, searchArray)
	if retObjState.getRetVal() == 1:
		error = "photoUpdatePixel:  problem with function showQuery - " + name
		er = retObjState.getError()
		print "\t\t" + error + "\n" + er
		retObj.setError(error)
		return retObj
	result = retObjState.getResult()
	print("\t\tinsert statement:  " + str(result))
	retObj.setComment("\t\tinsert statement:  " + str(result))
	c = conn.cursor()	
	c.execute (statement, searchArray)	
	retObj.setRetVal(0)
	return retObj

def photoInsertPixel (conn, noSuffixName, xsize, ysize):
	retObj = funcReturn.funcReturn('photoInsertPixel')
	name = noSuffixName + ".jpg"
	photo={}
	photoObj=photoParts(name, "jpg")
	
	if photoObj.getRetVal() == 1:
		e = photoObj.setError(error)
		error = "photoInsertPixel:  problem with function photoParts - " + name + "\n\t\t" + e
		print "\t\t" + error
		retObj.setError(error)
		return retObj
	
	photoResult = photoObj.getResult()
	type=photoResult['type'].strip()
	raw=photoResult['raw']
	alpha=photoResult['letter']
	retObj = prefix (conn)
	result = retObj.getResult()
	letter=result[alpha]
	year=photoResult['year']	
	if year == "":
		year = "noYear"
	seq=photoResult['seq']
	type=photoResult['type']
	noSuffix=photoResult['noSuffix']
	webname=photoResult['webname']
	if type == "raw":
		rawStr = "on"
	else:
		rawStr = "off"

	searchArray = [webname, year, seq, letter, rawStr, xsize, ysize]
	statement = """INSERT INTO P_L(fileName, lYear, lSequence, prefix,  timeModifiy, timeCreated, raw, xSize, ySize) 
		VALUES (%s , %s , %s , %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s, %s )""";	
	stringArray = ["%s" , "%s" , "%s" , "%s", "%s", "%s", "%s"]
	
	retObjState = showQuery( statement, stringArray, searchArray)
	if retObjState.getRetVal() == 1:
		error = "photoInsertObj:  problem with function showQuery - " + name
		er = retObjState.getError()
		print "\t\t" + error + "\n" + er
		retObj.setError(error)
		return retObj
	result = retObjState.getResult()
	print("\t\tinsert statement:  " + str(result))
	retObj.setComment("\t\tinsert statement:  " + str(result))
	c = conn.cursor()	
	c.execute (statement, searchArray)	
	retObj.setRetVal(0)
	return retObj

def photoInsertObj (conn, name, cd, noSuffix):
	retObj = funcReturn.funcReturn('photoInsert')
	name = noSuffix + ".jpg"
	photo={}
	photoObj=photoParts(name, "jpg")
	
	if photoObj.getRetVal() == 1:
		error = "photoInsertObj:  problem with function photoParts - " + name
		print "\t\t" + error
		retObj.setError(error)
		return retObj
	
	photoResult = photoObj.getResult()
	type=photoResult['type'].strip()
	raw=photoResult['raw']
	alpha=photoResult['letter']
	retObj = prefix (conn)
	result = retObj.getResult()
	letter=result[alpha]
	year=photoResult['year']	
	if year == "":
		year = "noYear"
	seq=photoResult['seq']
	extra=photoResult['extra']
	if extra != "":
		seq = seq + "." + extra

	type=photoResult['type']
	noSuffix=photoResult['noSuffix']
	webname=photoResult['webname']
	if type == "raw":
		rawStr = "on"
	else:
		rawStr = "off"

	searchArray = [webname, year, seq, letter, rawStr, cd]
	statement = """INSERT INTO P_L(fileName, lYear, lSequence, prefix,  timeModifiy, timeCreated, raw, rawDVD) 
		VALUES (%s , %s , %s , %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s )""";	
	stringArray = ["%s" , "%s" , "%s" , "%s", "%s", "%s"]
	retObjState = showQuery( statement, stringArray, searchArray)
	if retObjState.getRetVal() == 1:
		error = "photoInsertObj:  problem with function showQuery - " + name
		er = retObjState.getError()
		print "\t\t" + error + "\n" + er
		retObj.setError(error)
		return retObj
	result = retObjState.getResult()
	print("\t\tinsert statement:  " + str(result))
	retObj.setComment("\t\tinsert statement:  " + str(result))
	c = conn.cursor()	
	c.execute (statement, searchArray)	
	retObj.setRetVal(0)
	return retObj

def photoUpdateObj (conn, name, cd, noSuffix):
	retObj = funcReturn.funcReturn('photoUpdate')
	name = noSuffix + ".jpg"
	retObjPart= photoParts(name, "jpg")
	if retObjPart.getRetVal() == 1:
		error = "photoUpdateObj:  problem with function photoParts - " + name
		retObj.setError(error)
		return retObj
				
	result = retObjPart.getResult()
	raw=result['raw']
	year=result['year']	
	letter=result['letter']	
	seq=result['seq']
	extra=result['extra']
	if extra != "":
		seq = seq + "." + extra
	type=result['type']
	noSuffix=result['noSuffix']
	alpha=""
	webname=result['webname']
	if type == "source":
		rawStr = "on"
	else:
		rawStr = "off"
	searchArray = [rawStr, webname, letter, cd, year, seq]
	statement = """UPDATE P_L 
			SET timeModifiy =  CURRENT_TIMESTAMP, raw = %s, fileName = %s, 
				prefix = %s, rawDVD = %s	
			WHERE lYear = %s
			AND lSequence  = %s""";
	stringArray = ["%s" , "%s" , "%s" , "%s", "%s", "%s"]		
	retObjState = showQuery( statement, stringArray, searchArray)
	if retObjState.getRetVal() == 1:
		error = "photoUpdateObj:  problem with function showQuery - " + name
		er = retObjState.getError()
		error =  "\t\t" + error + "\n" + er
		retObj.setError(error)
		return retObj
	result = retObjState.getResult()
	comment = "\t\tupdate statement:  " + str(result)
	retObj.setComment(comment)
	c = conn.cursor()	
	c.execute (statement, searchArray)	
	retObj.setRetVal(0)
	return retObj

def photoRowTodict (row):
	print "photoRowTodict"
	retObj = funcReturn.funcReturn('photoRowTodict')
	r = list(row)
	retDic = {}	
	id = r[0]
	retDic['id'] = id
	fileName = r[1]
	retDic['fileName'] = fileName
	cd = r[2]
	retDic['cd'] = cd
	dvd = r[3]
	retDic['dvd'] = dvd
	lYear = r[5]
	retDic['lYear'] = lYear
	lSequnce = r[6]
	retDic['lSequnce'] = lSequnce
	EL = r[7]
	retDic['EL'] = EL
	active = r[8]
	retDic['active'] = active
	mod = r[9]
	retDic['mod'] = mod
	prefix = r[10]
	retDic['prefix'] = prefix
	created = r[11]
	retDic['created'] = created
	raw = r[12]
	retDic['raw'] = raw
	rawdvd = r[13]
	retDic['rawdvd'] = rawdvd
	keywords = r[14]
	retDic['keywords'] = keywords
	groupID = r[15]
	retDic['groupID'] = groupID
	xSize = r[16]
	retDic['xSize'] = xSize
	ySize = r[17]
	retDic['ySize'] = ySize
	retObj.setRetDic(retDic)
	return retObj


  		
def photoExistObj2 (conn, name):
	retObj = funcReturn.funcReturn('photoExistObj2')
	retObjPart=photoParts(name, "jpg")
	if retObjPart.getRetVal() == 1:
		error = "photoExistObj:  problem with function photoParts - " + name
		retObj.setError(error)
		return retObj
	
	result = retObjPart.getResult()
	raw=result['raw']
	year=result['year']
	letter=result['letter']
	seq=result['seq']
	extra=result['extra']
	if extra != "":
		seq = seq + "." + extra

	type=result['type']
	noSuffix=result['noSuffix']
	webname=result['webname']
		
	statement = """SELECT *
				FROM P_L
				WHERE lYear = %s
				AND lSequence = %s""";
	stringArray = ["%s", "%s"]
	searchArray = [year, seq]
	retObjShow= showQuery ( statement, stringArray, searchArray)
	result = retObjShow.getResult()
	retObj.setResult(result)
	c = conn.cursor()	
	c.execute (statement, (year, seq))
	rows = c.fetchall()
	
	try:
		numberOfRows = len (rows)		
	except Exception:
		comment = "no records found for:  " + name
		retObj.setRetVal(0)
		retObj.setFound(1)
		numberOfRows = 0
			
	if numberOfRows == 1:
		retObj.setRetVal(0)
		retObj.setFound(0)
		retDic = {}
		rowList = list(rows)
		r = rowList[0]
		print "r:  " + str(r)
		retObjRow = photoRowTodict(r)
		retDic = retObjRow.getRetDic()
		retObj.setResult(result)
		comment = "numberOfRows:  " + str(numberOfRows) + " - " + name
		retObj.setRetDic(retDic)
	elif numberOfRows == 0:
		retObj.setRetVal(0)
		retObj.setFound(1)
		comment = "numberOfRows:  " + str(numberOfRows) + " - " + name
	else:
		error = "numberOfRows:  more than 1:  " + str(numberOfRows) + " - " + name
		retObj.setError(error)
		retObj.setFound(0)
		retObj.setRetVal(0)
		return retObj
	
	retObj.setComment(comment)
  	return retObj	
  	
def photoEmails2 (conn):
	retObj = funcReturn.funcReturn('photoEmails2')
	#return emails
	searchValue = "photoUploadEmail";
	statement = """SELECT value
				FROM valuePair
				WHERE value2 = %s""";
	c = conn.cursor()	
	
	#My understanding is that it should follow the pattern 
	#cursor.execute( <select statement string>, <tuple>) 
	#and by putting only a single value in the tuple location 
	#it is actually just a string. To make the second argument 
	#the correct data type you need to put a comma in there
	c.execute (statement, (searchValue, ))
	
	result_set = c.fetchall()
	retObj.setResult(result_set[0][0])
	retObj.setRetVal(0)
	return retObj

def photoPrefix2 (conn):
	retObj = funcReturn.funcReturn('photoPrefix2')
	# SELECT Prefxs ##
	statement = ""
	statement = statement + "SELECT * \n";
	statement = statement + "FROM P_Prefix";
	c = conn.cursor()	
	c.execute (statement)
	result_set = c.fetchall()
	dict = {}
	for row in result_set:
		dict[row[1]] = row[0]
	retObj.setResult(dict)
	retObj.setRetVal(0)
	return retObj
	
def photoYearRecordsExport (conn, year):
	retObj = funcReturn.funcReturn('photoYearRecordsExport')
	cursor = conn.cursor()
	
	statement = """SELECT COLUMN_NAME 
					FROM INFORMATION_SCHEMA.COLUMNS 
					WHERE TABLE_SCHEMA = 'jlshipman' 
					AND TABLE_NAME = 'P_L'""";
	
	cursor.execute (statement, ())
	rowsName = cursor.fetchall()
	tableList = []
	innerList = []
	for r in rowsName:
		innerList.append(str(r[0]))
	tableList.append(innerList)
	numberOfRows = 0
	try:
		numberOfRows = len (rowsName)		
	except Exception:
		retObj.setError("Problem getting field names of P_L table")
		return retObj
		
	if year != "":
		statement = """SELECT *
					FROM P_L
					WHERE lYear =  %s""";
		#My understanding is that it should follow the pattern 
		#cursor.execute( <select statement string>, <tuple>) 
		#and by putting only a single value in the tuple location 
		#it is actually just a string. To make the second argument 
		#the correct data type you need to put a comma in there
		cursor.execute (statement, (year, ))
		rows = cursor.fetchall()
		numberOfRows = 0
		try:
			numberOfRows = len (rows)		
		except Exception:
			retObj.setError("no records found for year:  " + str(year))
			return retObj
			
		retObj.setComment("number Of Rows:  " + str(numberOfRows))

		if (numberOfRows > 0):
			retObj.setRetVal(0)

		retObj.setResult(rows)
	else:
		print "no Year"
		statement = """SELECT start 
					FROM P_L
					WHERE lYear =  0""";
		cursor.execute (statement, (year, ))
		rows = cursor.fetchall()
		numberOfRows = 0
		try:
			numberOfRows = len (rows)		
		except Exception:
			retObj.setError("no records found for blank years")
			return retObj
			
		retObj.setComment("number of rows:  " + str(numberOfRows))
	

		if (numberOfRows > 1):
			retObj.setRetVal(0)
		
		
	if retObj.getRetVal() == 0:
		print "number of rows:  " + str (numberOfRows)	
		for r in rows:
			innerList = []
			print str(r) + "\n"
			for piece in r:
				print str(piece) + "\n"
				innerList.append(str(piece))
			tableList.append(innerList)

		retObj.setResult(tableList)
	return retObj	
		
def fileConvert (dirContentsFile, dirContentsFileJpg, temp, badName, badTif ):
	retObj = funcReturn.funcReturn('fileConvert')
	dirContentsList = listFromFile(dirContentsFile)
	
	###############create dir#################
	jpdDirFull=temp + "Full"
	makeDirectory(jpdDirFull)
	jpdDirThumb=temp + "Thumb"
	makeDirectory(jpdDirThumb)
	
	###########create list############
	jpgList = []
	badNameList = []
	badTifList = []
	newDirContentsList = []
	
	#change privilege and correct names
	sizeDir=len(dirContentsList)
	count=0
	
	for t in dirContentsList:
		t=t.rstrip()
		#print ("    t:  "+ t)
		count+=1
		#print (str(count) +" of "+ str(sizeDir))
		base = os.path.basename(t) 
		#print ("    base:  "+ base)
		retObjNamed = imageProperlyNamed(base)		
		retVal = retObjNamed.getRetVal()
		if retVal == 0:
			#print ("      photo is properly named:  ")				
			jpgBase = base.replace(".tif", ".jpg")
			jpgFull= jpdDirFull + "/" + jpgBase
			jpgThumb= jpdDirThumb + "/" + jpgBase
			#print ("      jpgFull:  "+ jpgFull)
			#print ("      jpgThumb:  "+ jpgThumb)
			resultDictFull = comWrapConvertTiff2Jpg( t, jpgFull)
			resultFull = resultDictFull['retVal']
			#print ("      resultFull:  "+ str(resultFull))
			resultDictThumb = comWrapConvertTiff2JpgThumb( t, jpgThumb)
			resultThumb = resultDictThumb['retVal']
			#print ("      resultThumb:  "+ str(resultThumb))
			commandThumb=resultDictThumb['command']
			commandFull=resultDictFull['command']
			#test to see that tif file was able to convert to jpg
			#change test to testing existence of file before going forward
			if (resultFull == 1 or resultThumb == 1):
				badTifList.append(t)
				#print  ("      tif is badly constructed and can't be converted:  " + t)
				#print  (commandFull)
				#print  (commandThumb) 
				src = t
				dst = badTif + "/" + base
				retDict = fileMove2 (src, dst)
				result=retDict['retVal']
				if result == 1:
					error = retDict['error']
					error = error + "\nunable to move badly constructed tif file:  " + src
					retObj.setError(error)
					#print  ("      unable to move badly constructed tif file:  " + src )
					return retObj
			else:
				#create new list for next function
				newDirContentsList.append(t)
				jpgList.append(jpgBase)	
		else:
			badNameList.append(t)
			#print  ("      photo is not properly named:  " + base)
			src = t
			dst = badName + "/" + base
			retDict = fileMove2 (src, dst)
			result=retDict['retVal']
			if result == 1:
				error = retDict['error']
				error = retDict['error']
				error = error + "\nunable to move bad file:  " + src
				retObj.setError(error)
				return retObj

	listToFile(newDirContentsList, dirContentsFile)
	retObj.setResult(newDirContentsList)

	return retObj

def	setImageMetaData (conn, asset, metaDataFile):
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')
	retObj = funcReturn.funcReturn('setImageMetaData')
	
	retObjGet = getImageMetaDataDatabase (conn, asset)
	retValGet = retObjGet.getRetVal()
	retGetResults = retObjGet.getResult()
	command = retObjGet.getCommand()
	print "command:  " + 	command 	
	retGetResults = retObjGet.getResult()
	baseName = os.path.basename(asset) 
	baseName = re.sub('\.tif$', '', baseName)
	keyword = ""
	subject = ""
	ImageSupplierImageID = baseName
	print "ImageSupplierImageID:  " + 	baseName 	
	print "\tretValGet:  " + 	str(retValGet) 
	if int(retValGet) == 0:
		print "\t\tif" 
		#get fileName
		fileName = ""
		if  (retGetResults['fileName'] != "" and retGetResults['fileName'] is not None):
			fileName = retGetResults['fileName']
			fileName = re.sub('\.jpg$', '', fileName)
			keyword = fileName
			subject = fileName
		else:
			error = "problem with setting fileName"
			#print error
			retObj.setError(error)
			return retObj
				
		#print retGetResults
		requestor = ""
		if  (retGetResults['requestor'] != "" and retGetResults['requestor'] is not None):
			if requestor == "":
				requestor = retGetResults['requestor']
				#print "requestor:  " + 	requestor
			
		title = ""
		if  (retGetResults['title'] != "" and retGetResults['title'] is not None):
			if title == "":
				title = retGetResults['title']
				#print "title:  " + 	title
			
		other = ""
		if  (retGetResults['otherText'] != "" and retGetResults['otherText'] is not None) :	
			if other == "":
				other = retGetResults['otherText']
				subject = subject + ", " + other
				#print "subject:  " + 	subject
				
		project = ""
		if  (retGetResults['project'] != "" and retGetResults['project'] is not None):
			if project == "":
				subject = subject+ " " +retGetResults['project']	
				#print "subject:  " + 	subject
			
		#P_Groups keyword	
		key = ""	
		if  (retGetResults['keyword'] != "" and retGetResults['keyword'] is not None):
			key = retGetResults['keyword']
			keyList2 = []
			#print "\t\t\tP_Groups keywords"
			if key != "":
				#print "\t\t\t\tkey:  " + key
	# 			m = re.search('--(.+?)--', key)
	# 			if m:
	# 				found = m.group(1)
	# 				key = key.replace(found, "")
	# 				keyword = keyword + ", " + found.strip()
	# 				subject = subject + ", " + found.strip()
	# 				print "found:  " + found
			
				key = key.strip()
				key = key.replace("--", ",")	
				key = key.replace("  ", " ")
				key = key.replace(" ,", ",")
				if keyword != "":
					keyword = keyword + ", " + key 
				else:
					keyword = key
			
				if subject != "":
					subject = subject + ", " + key
				else:
					subject = key

		#P_L keywords
		key = ""
		if  (retGetResults['keywords'] != "" and retGetResults['keywords'] is not None):
			#print ""
			#print "\t\t\tP_L keywords"
			key = retGetResults['keywords']
			keyList2 = []
			if key != "":
				#print "\t\t\t\tkey:  " + key
				#print ""
	# 			m = re.search('--(.+?)--', key)
	# 			if m:
	# 				found = m.group(1)
	# 				key = key.replace(found, "")
	# 				keyword = keyword + ", " + found.strip()
	# 				subject = subject + ", " + found.strip()
	# 				print "found:  " + found
	# 			
				key = key.strip()
				key = key.replace("--", ",")	
				key = key.replace("  ", " ")
				key = key.replace(" ,", ",")
				if keyword != "":
					keyword = keyword + ", " + key 
				else:
					keyword = key
			
				if subject != "":
					subject = subject + ", " + key
				else:
					subject = key

		ELNumber = ""
		if  (retGetResults['ELNumber'] != "" and retGetResults['ELNumber'] is not None):
			ELNumber = retGetResults['ELNumber']
			if keyword != "":
				if ELNumber != "":
					ELNumber =retGetResults['ELNumber']
					#print "ELNumber:  " + 	ELNumber	
					keyword = str(ELNumber) + ", " +  keyword
					subject = str(ELNumber) + ", " +  subject
	
		photographerText = ""
		if  (retGetResults['photographerText'] != "" and retGetResults['photographerText'] is not None):
			if photographerText == "":
				photographerText = retGetResults['photographerText'] 	
				##print "photographerText:  " + 	photographerText
			
		description = ""
		if  (retGetResults['description'] != "" and retGetResults['description'] is not None):
			if description == "":
				description = retGetResults['description']		
				#print "description:  " + 	description
			
		location = ""
		if  (retGetResults['location'] != "" and retGetResults['location'] is not None):
			if location == "":
				location = retGetResults['location']		
				#print "location:  " + 	location
			
		source = ""
		if  (retGetResults['source'] != "" and retGetResults['source'] is not None):
			if source == "":
				source = retGetResults['source']		
				#print "source:  " + 	source
	
		dateVar = ""
		if  (retGetResults['datePhoto'] != "" and retGetResults['datePhoto'] is not None):
			if dateVar == "":
				dateVar = retGetResults['datePhoto']		
				#print "source:  " + 	source
	
		keyword = keyword + ", NASA, Langley, LRC, LARC"

		subject = subject + ", NASA, Langley, LRC, LARC"

		newDate =str(dateVar).replace("-", ":")
		newDate = newDate + " 00:00:00"
		#print "\t\t\tnewDate:  " + newDate
		
	else:
		#print "\t\telse" 
		fileName = baseName
		subject = baseName
		requestor = ""
		title = ""
		other = ""
		project = ""
		key = ""	
		ELNumber = ""
		photographerText = ""
		description = ""
		location = ""
		source = ""
		dateVar = ""
		keyword = keyword + ", NASA, Langley, LRC, LARC"
		subject = subject + ", NASA, Langley, LRC, LARC"
		newDate =str(dateVar).replace("-", ":")
		newDate = newDate + " 00:00:00"
		
	metaDataDict = {}
	metaDataDict.update({'ImageSupplierName': (requestor, False)})
	metaDataDict.update({'Requestor': (requestor, False)})
	metaDataDict.update({'Title': (title, False)})
	metaDataDict.update({'Subject': (subject, False)})
	metaDataDict.update({'Keywords': (keyword, True)})
	metaDataDict.update({'Creator': (photographerText, False)})
	metaDataDict.update({'Description': (description, False)})
	metaDataDict.update({'Source': (source, False)})
	metaDataDict.update({'Location': (location, False)})
	metaDataDict.update({'ImageSupplierImageID': (ImageSupplierImageID, False)})
	metaDataDict.update({'createdate': (newDate, False)})
	metaDataDict.update({'Date/Time Original': (newDate, False)})
	#print ""
	dictVar = dictFunc.fileToDict(metaDataFile, "#")
	for k, v in dictVar.items():
		v = v.rstrip()
		#print "k:   " + k
		#print "v: " + v
		metaDataDict.update({k: (v, False)})
		
	for (key, valueArray) in metaDataDict.items():
		value = valueArray[0].rstrip()
		quote = valueArray[1]
		#print "key:   _" + key + "_"
		#print "vaule: _" + value + "_"
		retObjPhoto = imageFunc.setMetadataTiff( asset, key, value, quote)
		comment=retObjPhoto.getComment()
		print "comment:  "  + comment
		retValPhoto = retObjPhoto.getRetVal()
		if retValPhoto == 1:
			retObj.setRetVal(1)
			error = retObjPhoto.getError()
			command = retObjPhoto.getCommand()
			retObj.setCommand(command)
			error = "problem with setMetadataTiff:  asset: " + asset + " key:  " + key + "\n error : " + error
			#print error
			retObj.setError(error)
			return retObj
	
	retObj.setResult(metaDataDict)
	retObj.setRetVal(0)
	return retObj


def getImageMetaDataDatabase (conn, asset):
	retObj = funcReturn.funcReturn('getImageMetaDataDatabase')
	baseName = os.path.basename(asset) 
	retObjPhoto = photoParts(baseName)
	comment = ""
	if retObjPhoto.getRetVal() == 1:
		error = retObjPhoto.getError()
		retObj.setError("problem with photoParts:  " + error)
		return retObj
	retDict = retObjPhoto.getResult()
	#print retDict
	#result = dict([('raw', result), ('year', year), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname)])	
	year = retDict['year']
	seq = retDict['seq']
	searchArray = (year, year, seq)
	c = conn.cursor()
	searchValue = asset;
	
	############### get P_LGroup fields - begin ###############
	statement = """SHOW columns 
					FROM P_LGroup""";
	retObj.setCommand(statement)
	c.execute (statement)
	rows = c.fetchall()

	try:
		numberOfRows = len (rows)
		comment = comment + "P_LGroup - number of rows:  " + str(numberOfRows) + "\n"			
	except Exception:
		comment = comment + "no colums found table P_L" + "\n"
		retObj.setComment(comment)
		retObj.setError(comment)
		return retObj
		
	keys = []	
	for r in rows:
		keys.append (r[0])
	############### get P_LGroup fields - end ###############
	
	############### get P_L fields - begin ###############	
	statement = """SHOW columns 
					FROM P_L""";
	retObj.setCommand(statement)
	c.execute (statement)
	rows = c.fetchall()

	try:
		numberOfRows = len (rows)	
		comment = comment + "P_L - number of rows:  " + str(numberOfRows) + "\n"	
	except Exception:
		comment = comment + "no columms found table P_L" + "\n"
		retObj.setComment(comment)
		retObj.setError(comment)
		return retObj
		
	for r in rows:
		keys.append (r[0])
	############### get P_L fields - end ###############		
	
	#sql for calling individual photos from collections
	# SELECT *
	# FROM P_LGroup G, P_L P
	# WHERE G.id = 00000985006
	# AND G.year = P.lYear
	# AND G.seqBegin <= P.lSequence
	# AND G.seqEnd >= P.lSequence
	#	((seqBegin = '215') OR (`seqEnd` = '215') AND ((seqBegin >= '215') AND (seqEnd <= '215') AND (seqEnd != '0') ))
	statement = """SELECT *
				FROM P_LGroup G, P_L P
				WHERE year = %s 
				AND G.id = P.group_id
				AND G.active = '0'
				AND P.lYear = %s 
				AND P.lSequence = %s """;


# 	statement = """SELECT *
# 				FROM P_LGroup
# 				WHERE year = %s 
# 				AND active = '0'
# 				AND (((seqBegin = %s) OR (seqEnd = %s )) OR ((seqBegin <= %s) AND (seqEnd >= %s) AND (seqEnd != '0')))""";
	statementTxt = statement % searchArray
	#print statementTxt
	retObj.setCommand(statementTxt)
	c.execute (statement, searchArray)
	
	
	rows = c.fetchall()
	try:
		numberOfRows = len (rows)	
		comment = comment + "inner join - number of rows:  " + str(numberOfRows) + "\n"	
	except Exception:
		comment = comment + "no records found for:  " + asset + "\n"
		retObj.setComment(comment)
		retObj.setError(comment)
		return retObj
		
	
	#print comment
	retObj.setComment(comment)
	
	if numberOfRows == 1:
		retObj.setRetVal(0)
	else:
		error = "number of rows returned:  " + str(numberOfRows)
		error = error + "\n" + statementTxt
		retObj.setError(error)
		return retObj
		
	values = list(rows[0])
# 	for r in rows:
# 		print str(r) + "\n";
	retDict = {key:value for key, value in zip(keys,values)}
	retObj.setResult(retDict)
	return retObj

def repoCheck2(image, repositorylist):
	#check for for file having copy in source or mastered
	retObj = funcReturn.funcReturn('repoCheck2')
	#print "image: " + image
	base = os.path.basename(image)
	retObjPhoto = photoParts(base)
	if retObjPhoto.getRetVal() == 1:
		error = retObjPhoto.getError()
		retObj.setError(error)
		return retObj
		
	retDict = retObjPhoto.getResult()
	#print retDict
	#result = dict([('raw', result), ('year', year), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname)])	
	year = retDict['year']
	typePhoto = retDict['type']
	noSuffix = retDict['noSuffix']
	checkOrig = 0
	checkMod = 0
	comment = ""
	if year == "":
		year = "noYear"
	else:
		year = retDict['year']	
	f = open(repositorylist)
	original = []
	modified = []
	lines = f.readlines()
	sep = "#"
	for line in lines:
		type, path = line.rstrip().split(sep)
		if type == "modified":
			modified.append(path)
		if type == "original":
			original.append(path)
	f.close()	
	#print "typePhoto:  _" + typePhoto + "_"
	if typePhoto == "source":
		comment = comment + "file is source \n"
	else:
		comment = comment + "file is mastered \n"
		
	modName = noSuffix.replace("R-", "")	
	for o in original:
		fileToCheck = o +  "/" + str(year) +  "/pic/R-" + modName + ".tif"
		comment = comment + "\t\t\tfileToCheck: " + fileToCheck + " \n"
		if fileExist(fileToCheck):
			comment = comment + "\t\t\tsource exists \n"
			checkOrig =  1
			retObj.setFound(0)
			
	for m in modified:	
		fileToCheck = m  + "/" + str(year) +  "/pic/" + modName + ".tif"
		comment = comment + "\t\t\tfileToCheck: " + fileToCheck + " \n"
		if fileExist(fileToCheck):
			comment = comment + "\t\t\tmastered exists \n"
			checkMod =  1
			retObj.setFound(0)
			
	retObj.setResult(dict([('checkOrig', checkOrig), ('checkMod', checkMod), ('type', type)]))
	
	comment = comment.rstrip()
	retObj.setComment(comment)
	retObj.setRetVal(0)
	return retObj
	
def convertNoYearNewNameToNewNameYearCheck (fileName, YearFile):
	#LRC-B701_P-00060.tif to LRC-1941-B701_P-00060.tif
	retObj = funcReturn.funcReturn('convertNoYearNewNameToNewNameYearCheck')
	dict = {}
	fileName = fileName.replace("R_", "R-")
	splitDot=fileName.split('.')	
	splitHyphen=splitDot[0].split('-')
	#print "splitHyphen:  "  + str(splitHyphen)
	result=isRaw(fileName)	
	raw=""
	year=""	
	letter=""	
	seq=""
	type=""	
	
	resultList = listFunctions.listFromFile(YearFile)
	if isRaw(fileName):
		print "Raw"	
		fileName = fileName.replace("R-", "")
		splitDot=fileName.split('.')	
		splitHyphen=splitDot[0].split('-')
		#print "Number"	
		letter = splitHyphen[0]
		org = splitHyphen[1]
		seq = splitHyphen[2]
		seqInt = int(seq)
		seqName = seq
		yearCheck = 0
		type = "source"
		for r in resultList:
			bits=r.split('\t')
			yearCheck = int(bits[0])
			begin = int(bits[1])
			end = int(bits[2])
# 				print "begin:      " + str(int(begin))
# 				print "end:        " + str(int(end))
# 				print "yearCheck:  " + str(int(yearCheck))
# 				print ""
# 				print str(begin) + "  <  " + str(seq) + " and " + str(end) + "  >  " + str(seq)
			if ((begin <= seqInt) and (end >= seqInt)):
				year = yearCheck
		newName ="R-LRC-" + str(year) + "-B701_P-" + str(seqName) + "." + splitDot[1]
	else:
		letter = splitHyphen[0]
		org = splitHyphen[1]
		seq = splitHyphen[2]
		seqInt = int(seq)
		seqName = seq
		type = "mastered"
		yearCheck = 0
		for r in resultList:
			bits=r.split('\t')
			yearCheck = int(bits[0])
			begin = int(bits[1])
			end = int(bits[2])
# 				print "begin:      " + str(int(begin))
# 				print "end:        " + str(int(end))
# 				print "yearCheck:  " + str(int(yearCheck))
# 				print ""
# 				print str(begin) + "  <  " + str(seq) + " and " + str(end) + "  >  " + str(seq)
			if ((begin <= seqInt) and (end >= seqInt)):
				year = yearCheck
		newName ="LRC-" + str(year) + "-B701_P-" + str(seqName) + "." + splitDot[1]

	noSuffix = 	newName.split('.')
	dict['year'] = year
	dict['letter'] = letter
	dict['seq'] = seq
	dict['type'] = type
	dict['noSuffix'] = noSuffix[0]
	dict['newName'] = newName
	retObj.setResult(dict)
	retObj.setRetVal(0)
	return retObj

def convertOldNameToNewNameYearCheck (fileName, YearFile):
	#L-156345_1231234.tif to LRC-B701_P_L-F1231234-156345.tif
	retObj = funcReturn.funcReturn('convertOldNameToNewNameYearCheck')
	dict = {}
	fileName = fileName.replace("R_", "R-")
	splitDot=fileName.split('.')	
	splitHyphen=splitDot[0].split('-')
	#print "splitHyphen:  "  + str(splitHyphen)
	result=isRaw(fileName)	
	raw=""
	year=""	
	letter=""	
	seq=""
	type=""	
	
	resultList = listFunctions.listFromFile(YearFile)
	if isRaw(fileName):
		#print "Raw"	
		fileName = fileName.replace("R-", "")
		#year test
		if isNumber(splitHyphen[1]):
			#print "Number"	
			if len(splitHyphen) == 5:
				year = splitHyphen[1]
				letter = splitHyphen[2]
				seq = splitHyphen[3]
				fname = splitHyphen[4]
				#print fname
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj				
				seqName="_F"+ fname+ "-"+seq
				newName ="R-LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
			else:
				#print "Not Number"	
				year = splitHyphen[1]
				letter = splitHyphen[2]
				seq = splitHyphen[3]
				seqList=seq.split('.')
				if len(seqList) == 4:
					#print "decimal"
					fname = seqList[1]
					#print str(len(fname)) 
					if len(fname) == 1:
						fname = "00" + fname
					if len(fname) == 2:
						fname = "0" + fname
					if len(fname) > 3:
						retObj.setRetVal(1)
						retObj.setError(fileName + ":  too many decimal places")
						return retObj	
					seqName="_F"+ fname + "-"+seqList[0]
				else:
					#print "no decimal"
					seqName="-" + seq
				seqList=seq.split('_')	
				#print "seq:  "  + str(seq)
				#print "seqList:  "  + str(seqList)
				if len(seqList) == 2:
					#print "decimal"
					fname = seqList[1]
					#print str(len(fname)) 
					if len(fname) == 1:
						fname = "00" + fname
					if len(fname) == 2:
						fname = "0" + fname
					if len(fname) > 3:
						retObj.setRetVal(1)
						retObj.setError(fileName + ":  too many decimal places")
						return retObj	
					seqName="_F"+ fname + "-"+seqList[0]
				newName ="R-LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
		else:
			#print "No Number"	
			letter = splitHyphen[1]
			seq = splitHyphen[2]

			seqList=seq.split('_')
			if len(seqList) == 2:
				#print "decimal"
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F"+ fname+ "-"+seqList[0]
				seqInt = int(seqList[0])
			else:
				#print "no decimal"
				seqName="-" + seq
				seqInt = int(seq)
			seqList=seq.split('_')			
			if len(seqList) == 2:
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F"+ fname + "-"+seqList[0]
			
			yearCheck = 0
			for r in resultList:
				bits=r.split('\t')
				yearCheck = int(bits[0])
				begin = int(bits[1])
				end = int(bits[2])
# 				print "begin:      " + str(int(begin))
# 				print "end:        " + str(int(end))
# 				print "yearCheck:  " + str(int(yearCheck))
# 				print ""
# 				print str(begin) + "  <  " + str(seq) + " and " + str(end) + "  >  " + str(seq)
				if ((begin <= seqInt) and (end >= seqInt)):
					year = yearCheck
			#newName ="R-LRC-B701_P" + str(seqName) + "." + splitDot[1]
			newName ="R-LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
		webname = newName.replace(".tif", ".jpg")	
		type = "raw"
	else:
		#print "Not Raw"	
		#year test
		if isNumber(splitHyphen[0]):
			#print "number"
			year = splitHyphen[0]
			letter = splitHyphen[1]
			seq = splitHyphen[2]
			seqList=seq.split('.')
			##print "year:  " + str(year)
			##print "seq:  " + str(seq)	
			if len(seqList) == 2:
				#print "decimal"
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F"+ fname + "-"+seqList[0]
			else:
				#print "no decimal"
				seqName="-" + seq
			seqList=seq.split('_')
			#print seqList
			if len(seqList) == 2:
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F" + fname + "-"+seqList[0]
			newName ="LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
		else:
			#print "no number"
			letter = splitHyphen[0]
			seq = splitHyphen[1]
			seqList=seq.split('_')
			if len(seqList) == 2:
				#print "decimal"
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj				
				seqName="_F" + fname + "-"+seqList[0]
				seqInt = int(seqList[0])
			else:
				#print "no decimal"
				seqName="-" + seq
				seqInt = int(seq)
			seqList=seq.split('_')
			if len(seqList) == 2:
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F" + fname + "-"+seqList[0]
			
			yearCheck = 0
			for r in resultList:
				bits=r.split('\t')
				yearCheck = int(bits[0])
				begin = int(bits[1])
				end = int(bits[2])
# 				print "begin:      " + str(int(begin))
# 				print "end:        " + str(int(end))
# 				print "yearCheck:  " + str(int(yearCheck))
# 				print ""
# 				print str(begin) + "  <=  " + str(seq) + " and " + str(end) + "  >=  " + str(seq)
				if ((begin <= seqInt) and (end >= seqInt)):
					year = yearCheck
			#newName ="LRC-B701_P" + str(seqName) + "." + splitDot[1]
			newName ="LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
		webname = newName.replace(".tif", ".jpg")
		type ="processed"
	noSuffix = 	newName.split('.')
	dict['raw'] = str(result)
	dict['year'] = year
	dict['letter'] = letter
	dict['seq'] = seq
	dict['type'] = type
	dict['noSuffix'] = noSuffix[0]
	dict['webname'] = webname
	dict['newName'] = newName
	retObj.setResult(dict)
	retObj.setRetVal(0)
	return retObj
	
def photoYears (conn, year):
	retObj = funcReturn.funcReturn('photoYears')
	cursor = conn.cursor()
	
	if year != "":
		statement = """SELECT start, end 
					FROM P_photoCount
					WHERE year =  %s""";
		#My understanding is that it should follow the pattern 
		#cursor.execute( <select statement string>, <tuple>) 
		#and by putting only a single value in the tuple location 
		#it is actually just a string. To make the second argument 
		#the correct data type you need to put a comma in there
		cursor.execute (statement, (year, ))
		rows = cursor.fetchall()
		numberOfRows = 0
		try:
			numberOfRows = len (rows)		
		except Exception:
			retObj.setError("      photoYears - no records found for year:  " + str(year))
		
		retObj.setComment("      photoYears - numberOfRows:  " + str(numberOfRows))

		if (numberOfRows == 1):
			retObj.setRetVal(0)
		retDict = {}
		retDict['start'] = rows[0][0]
		retDict['end'] = rows[0][1]	
		retObj.setResult(retDict)
	else:
		print "no Year"
		year = 1921
		statement = """SELECT start 
					FROM P_photoCount
					WHERE year =  %s""";
		cursor.execute (statement, (year, ))
		rows = cursor.fetchall()
		numberOfRows = 0
		try:
			numberOfRows = len (rows)		
		except Exception:
			retObj.setError("      photoYears - no records found for year:  " + str(year))
		
		retObj.setComment("      photoYears - numberOfRows:  " + str(numberOfRows))

		if (numberOfRows == 1):
			retObj.setRetVal(0)
		retDict = {}
		retDict['start'] = rows[0][0]
	
		year = 1956
		statement = """SELECT end 
					FROM P_photoCount
					WHERE year =  %s""";
		cursor.execute (statement, (year, ))
		rows = cursor.fetchall()
		numberOfRows = 0
		try:
			numberOfRows = len (rows)		
		except Exception:
			retObj.setError("      photoYears - no records found for year:  " + str(year))
		
		retObj.setComment("      photoYears - numberOfRows:  " + str(numberOfRows))

		if (numberOfRows == 1):
			retObj.setRetVal(0)
		retDict['end'] = rows[0][0]
		retObj.setResult(retDict)
	return retObj	

def properNumbering(fileName, stage):
	retObj = funcReturn.funcReturn('properNumbering')
	retObjParts=photoParts(fileName, type = "tif")
	dictPart = retObjParts.getResult()
	year = dictPart['year']
	retDict=photoConnectMysqlDict(stage)
	conn = retDict['conn']	
	retObjYears = photoYears (conn, year)
	resYears = retObjYears.getResult()
	start= resYears['start']
	end = resYears['end']
	if start >= year and end <= year :
		retObj.setRetVal(0)
	retObj.setResult(retDict)	
	return retObj
	
def convertOldNameToNewName (fileName):
	#L-156345_1231234.tif to LRC-B701_P_L-F1231234-156345.tif
	retObj = funcReturn.funcReturn('convertOldNameToNewName')
	dict = {}
	fileName = fileName.replace("R_", "R-")
	splitDot=fileName.split('.')
		
	splitHyphen=splitDot[0].split('-')
	#print "splitHyphen:  "  + str(splitHyphen)
	result=isRaw(fileName)	
	raw=""
	year=""	
	letter=""	
	seq=""
	type=""	
	if isRaw(fileName):
		#print "Raw"	
		fileName = fileName.replace("R-", "")
		#year test
		if isNumber(splitHyphen[1]):
			#print "Number"	
			if len(splitHyphen) == 5:
				year = splitHyphen[1]
				letter = splitHyphen[2]
				seq = splitHyphen[3]
				fname = splitHyphen[4]
				#print fname
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj				
				seqName="_F"+ fname+ "-"+seq
				newName ="R-LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
			else:
				#print "Not Number"	
				year = splitHyphen[1]
				letter = splitHyphen[2]
				seq = splitHyphen[3]
				seqList=seq.split('.')
				if len(seqList) == 4:
					#print "decimal"
					fname = seqList[1]
					#print str(len(fname)) 
					if len(fname) == 1:
						fname = "00" + fname
					if len(fname) == 2:
						fname = "0" + fname
					if len(fname) > 3:
						retObj.setRetVal(1)
						retObj.setError(fileName + ":  too many decimal places")
						return retObj	
					seqName="_F"+ fname + "-"+seqList[0]
				else:
					#print "no decimal"
					seqName="-" + seq
				seqList=seq.split('_')	
				#print "seq:  "  + str(seq)
				#print "seqList:  "  + str(seqList)
				if len(seqList) == 2:
					#print "decimal"
					fname = seqList[1]
					#print str(len(fname)) 
					if len(fname) == 1:
						fname = "00" + fname
					if len(fname) == 2:
						fname = "0" + fname
					if len(fname) > 3:
						retObj.setRetVal(1)
						retObj.setError(fileName + ":  too many decimal places")
						return retObj	
					seqName="_F"+ fname + "-"+seqList[0]
				newName ="R-LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
		else:
			#print "No Number"	
			letter = splitHyphen[1]
			seq = splitHyphen[2]
			seqList=seq.split('.')
			if len(seqList) == 2:
				#print "decimal"
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F"+ fname+ "-"+seqList[0]
			else:
				#print "no decimal"
				seqName="-" + seq
			seqList=seq.split('_')			
			if len(seqList) == 2:
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F"+ fname + "-"+seqList[0]
			newName ="R-LRC-B701_P" + str(seqName) + "." + splitDot[1]
		webname = newName.replace(".tif", ".jpg")	
		type = "raw"

	else:
		#print "Not Raw"	
		#year test
		if isNumber(splitHyphen[0]):
			#print "number"
			year = splitHyphen[0]
			letter = splitHyphen[1]
			seq = splitHyphen[2]
			seqList=seq.split('.')
			##print "year:  " + str(year)
			##print "seq:  " + str(seq)	
			if len(seqList) == 2:
				#print "decimal"
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F"+ fname + "-"+seqList[0]
			else:
				#print "no decimal"
				seqName="-" + seq
			seqList=seq.split('_')
			#print seqList
			if len(seqList) == 2:
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F" + fname + "-"+seqList[0]
			newName ="LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
		else:
			#print "no number"
			letter = splitHyphen[0]
			seq = splitHyphen[1]
			seqList=seq.split('.')
			if len(seqList) == 2:
				#print "decimal"
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj				
				seqName="_F" + fname + "-"+seqList[0]
			else:
				#print "no decimal"
				seqName="-" + seq
			seqList=seq.split('_')
			if len(seqList) == 2:
				fname = seqList[1]
				#print str(len(fname)) 
				if len(fname) == 1:
					fname = "00" + fname
				if len(fname) == 2:
					fname = "0" + fname
				if len(fname) > 3:
					retObj.setRetVal(1)
					retObj.setError(fileName + ":  too many decimal places")
					return retObj
				seqName="_F" + fname + "-"+seqList[0]
			newName ="LRC-B701_P" + str(seqName) + "." + splitDot[1]
			
		webname = newName.replace(".tif", ".jpg")
		type ="processed"
	noSuffix = 	newName.split('.')
	dict['raw'] = str(result)
	dict['year'] = year
	dict['letter'] = letter
	dict['seq'] = seq
	dict['type'] = type
	dict['noSuffix'] = noSuffix[0]
	dict['webname'] = webname
	dict['newName'] = newName
	retObj.setResult(dict)
	retObj.setRetVal(0)
	return retObj
	
def removeBadChars (filePath):
	#removes spaces, extra decimals, double hyphens 
	#changes privileges
	retObj = funcReturn.funcReturn('removeBadChars')	
	filePath=filePath.rstrip()

	imageTIFF = filePath
	
	#test TIFF name
	oldTIFF = os.path.basename(imageTIFF) 
	#print ("  oldTIFF:  "+ oldTIFF)
	dirPath = os.path.dirname(imageTIFF) 
	#print ("  dirPath:  "+ dirPath)
	newTIFF = oldTIFF
	newTIFF = newTIFF.replace(" ", "")
	newTIFF = newTIFF.replace("R_", "R-")
	newTIFF = newTIFF.replace("--", "-")
	#print ("newTIFF:  " + newTIFF)
	
	#replace the second to last decimal in number with underscore
	#L-156345.1231234.tif to L-156345_1231234.tif
	#print ("three decimal ")
	def numReplace(matchobj):
		test = matchobj.group(0)
		if matchobj.group(0)[0] == ".":
			test = string.replace(matchobj.group(0), ".", "_", 1)
		return test	
	newTIFF = re.sub('.\d+.tif', numReplace, newTIFF)
	#print ("\tnewTIFF:  " + newTIFF)
	#print ("hyphen ")	
	#replace the last hyphen in number when it is the symbolic decimal
	def decHyphenReplace(matchobj):
		test = matchobj.group(0)
		#print ("\ttest:  " + test)
		#print ("\tmatchobj.group(0)[0]:  " + matchobj.group(0)[0])
		second_index = test.find("-", test.find("-")+1)
		if matchobj.group(0)[second_index] == "-":
			stringList = list(test)
			stringList[second_index] = "_"
			test = "".join(stringList)
			#print ("\ttest:  " + test)
		return test	
	newTIFF = re.sub('-\d+-\d+.tif', decHyphenReplace, newTIFF)
	#print ("\toldTIFF:  " + oldTIFF)
	#print ("\tnewTIFF:  " + newTIFF)
	retObj.setRetVal(0)
	retObj.setResult(newTIFF)
	return retObj

def photoPartsOld2(fileName, type = "tif"):
	retObj = funcReturn.funcReturn('photoPartsOld2')
	if type == "tif":
		retObj2 = imageProperlyNamedOld2(fileName)
		retVal = retObj2.getRetVal()
	else:
		retVal = 1
	#print "retVal:  " + str(retVal)
	if retVal == 0:
		splitDot=fileName.split('.')
			
		splitHyphen=splitDot[0].split('-')
	
		result=isRaw(fileName)
	
		raw=""
		year=""	
		letter=""	
		seq=""
		type=""
		if isRaw(fileName):
			#year test
			if isNumber(splitHyphen[1]):
				year = splitHyphen[1]
				letter = splitHyphen[2]
				seq = splitHyphen[3]
			else:
				letter = splitHyphen[1]
				seq = splitHyphen[2]
			webname = fileName.replace("R-", "")
		else:
			#year test
			if isNumber(splitHyphen[0]):
				year = splitHyphen[0]
				letter = splitHyphen[1]
				seq = splitHyphen[2]
			else:
				letter = splitHyphen[0]
				seq = splitHyphen[1]
			webname = fileName

		if isRaw(fileName):
			type = "source"
		else:
			type ="mastered"
		result = dict([('raw', result), ('year', year), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname)])	
		retObj.setResult(result)
		retObj.setRetVal(0)
	return retObj
	
def photoParts(fileName, type = "tif"):
	retObj = funcReturn.funcReturn('photoParts')
	if type == "tif":
		retObj2 = imageProperlyNamed(fileName)
		funcRun = "imageProperlyNamed - tif"
	else:
		retObj2 = imageProperlyNamedJpg(fileName)
		funcRun = "imageProperlyNamedJpg"
	retVal = retObj2.getRetVal()
	#R-LRC-1942-B701_P-27063.tif
	#print "retVal:  " + str(retVal)
	if retVal == 0:
		splitDot=fileName.split('.')
			
		splitHyphen=splitDot[0].split('-')
	
		result=isRaw(fileName)
	
		raw=""
		year=""	
		letter=""	
		seq=""
		type=""
		center = ""
		meta = ""
		extra = "" 
		#print "fileName:  " + fileName
		#print "isRaw:  " + str(isRaw(fileName))
		if isRaw(fileName):
			#print "sourced"
			center = splitHyphen[1]
			year = int(splitHyphen[2])
			hold = splitHyphen[3]
			splitF=hold.split('F')
			if len(splitF) == 2:
				meta = splitF[0]
				extra = splitF[1]
			else:
				meta = hold
			seq = splitHyphen[4]
			webname = fileName.replace("R-", "")
			core = splitDot[0].replace("R-", "")
		else:
			#print "mastered"
			if splitHyphen[0] == "LRC":    #LRC test
				center = splitHyphen[0]
				year = int(splitHyphen[1])
				hold = splitHyphen[2]
				splitF=hold.split('F')
				if len(splitF) == 2:
					meta = splitF[0]
					extra = splitF[1]
				else:
					meta = hold
				seq = splitHyphen[3]
			webname = fileName
			core = splitDot[0]
		if isRaw(fileName):
			type = "source"
		else:
			type ="mastered"
		result = dict([('raw', result), ('center', center), ('meta', meta), ('extra', extra), ('year', year), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname), ('core', core)])	
		retObj.setResult(result)
		retObj.setRetVal(0)
	else:
		error = retObj2.getError()
		error = error + "\nfuncRun:  " + funcRun + "\n" + fileName + " is improperly named" + " - type:  " + type
		retObj.setError(error)
	return retObj

def imageProperlyNamedJpg(s):
	#print "s :  " + str(s)
	#^LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}\.tif
	retObj = funcReturn.funcReturn('imageProperlyNamedJpg')
	prog = re.compile(r"""^R-		# Raw
					  LRC-				# LRC
					  \d{4}-			# Year
					  B701_				# org
					  [PAVG]			# dept
					  [0-9a-zA-Z_]*		# metadata
					  -\d{5}			# Seq
					  \.jpg				# jpg suffix""", re.X)
	source = bool(prog.search(s))
	#print source
	prog = re.compile(r"""^LRC-			# LRC
					  \d{4}-			# Year
 					  B701_				# org
 					  [PAVG]			# dept
 					  [0-9a-zA-Z_]*		# metadata
 					  -\d{5}			# Seq
					  \.jpg				# jpg suffix""", re.X)
	mastered = bool(prog.search(s))
	#print mastered
	resultBool =  (source or mastered)
	if resultBool == True:
		result = 0
	else:
		result = 1
	retObj.setRetVal(result)
	return retObj

def photoPartsNoYear(fileName, type = "tif"):
	retObj = funcReturn.funcReturn('photoParts')
	if type == "tif":
		retObj2 = imageProperlyNamedNoYear(fileName)
	else:
		retObj2 = imageProperlyNamedJpg(fileName)
		
	retVal = retObj2.getRetVal()
	#R-LRC-1942-B701_P-27063.tif
	#print "retVal:  " + str(retVal)
	if retVal == 0:
		splitDot=fileName.split('.')
			
		splitHyphen=splitDot[0].split('-')
	
		result=isRaw(fileName)
	
		raw=""
		letter=""	
		seq=""
		type=""
		center = ""
		meta = ""
		#print "fileName:  " + fileName
		#print "isRaw:  " + str(isRaw(fileName))
		if isRaw(fileName):
			#print "sourced"
			center = splitHyphen[1]
			meta = splitHyphen[2]
			seq = splitHyphen[3]
			webname = fileName.replace("R-", "")
		else:
			#print "mastered"
			if splitHyphen[0] == "LRC":    #LRC test
				center = splitHyphen[0]
				meta = splitHyphen[1]
				seq = splitHyphen[2]
			webname = fileName

		if isRaw(fileName):
			type = "source"
		else:
			type ="mastered"
		result = dict([('raw', result), ('center', center), ('meta', meta), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname)])	
		retObj.setResult(result)
		retObj.setRetVal(0)
	return retObj
	
def imageProperlyNamedNoYear(s):
	#^LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}\.tif
	retObj = funcReturn.funcReturn('imageProperlyNamedNoYear')
	prog = re.compile(r"""^R-		# Raw
					  LRC-				# LRC
					  B701_				# org
					  [PAVG]			# dept
					  [0-9a-zA-Z_]*		# metadata
					  -\d{5}			# Seq
					  \.tif				# tif suffix""", re.X)
	source = bool(prog.search(s))
	#print source
	prog = re.compile(r"""^LRC-			# LRC
 					  B701_				# org
 					  [PAVG]			# dept
 					  [0-9a-zA-Z_]*		# metadata
 					  -\d{5}			# Seq
					  \.tif				# tif suffix""", re.X)
	mastered = bool(prog.search(s))
	#print mastered
	resultBool =  (source or mastered)
	if resultBool == True:
		result = 0
	else:
		result = 1
	retObj.setRetVal(result)
	return retObj

def imageProperlyNamed(s):
	#^LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}\.tif
	#LRC-2015-B701_P-02749.tif
	retObj = funcReturn.funcReturn('imageProperlyNamed')
	error = ""
	##################  source - begin ##################
	prog = re.compile(r"""^R-LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}\.tif""", re.X)
	source = bool(prog.search(s))
	if source == False:
		error = error + "\nsource: "
		prog = re.compile(r"""^R-""", re.X)
		test = bool(prog.search(s))
		if False == test: 
			problem = "\tRaw - not present"
			error = error + problem
		else:
			prog = re.compile(r"""^R-LRC-""", re.X)
			test = bool(prog.search(s))
			if False == test:
				error = error + "\tLRC- not present"
			else:
				prog = re.compile(r"""^R-LRC-\d{4}""", re.X)
				test = bool(prog.search(s))
				if False == test:
					error = error + "\tYear not present"
				else:
					prog = re.compile(r"""^R-LRC-\d{4}-B701_""", re.X)
					test = bool(prog.search(s))
					if False == test:
 						error = error + "\tOrg not present"
 					else:
 						prog = re.compile(r"""^R-LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*""", re.X)
 						test = bool(prog.search(s))
						if False == test:
							error = error + "\tDept not present"
						else:
							prog = re.compile(r"""^R-LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}""", re.X)
							test = bool(prog.search(s))
							if False == test:
								error = error + "\tSequence not present"
							else:
								prog = re.compile(r"""^R-LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}\.tif""", re.X)
 					  			test = bool(prog.search(s))
 					  			if False == test:
									error = error + "\ttif not present"
								else:
									 source = True
	#print source
	##################  source - end ##################
	
	##################  mastered - begin ##################
	prog = re.compile(r"""^LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}\.tif""", re.X)
	mastered = bool(prog.search(s))
	if mastered == False:
		error = error + "\nmastered: "
		error = error + "\n_" + s +"_"
		prog = re.compile(r"""^LRC""", re.X)
		test = bool(prog.search(s))
		if False == test:
			error = error + "\tLRC- not present"
		else:
			prog = re.compile(r"""^LRC-\d{4}""", re.X)
			test = bool(prog.search(s))
			if False == test:
				error = error + "\tYear not present"
			else:
				prog = re.compile(r"""^LRC-\d{4}-B701_""", re.X)
				test = bool(prog.search(s))
				if False == test:
					error = error + "\tOrg not present"
				else:
					prog = re.compile(r"""^LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*""", re.X)
					test = bool(prog.search(s))
					if False == test:
						error = error + "\tDept not present"
					else:
						prog = re.compile(r"""^LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}""", re.X)
						test = bool(prog.search(s))
						if False == test:
							error = error + "\tSequence not present"
						else:
							prog = re.compile(r"""^LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}\.tif""", re.X)
							test = bool(prog.search(s))
							if False == test:
								error = error + "\ttif not present"
							else:
								 mastered = True
	#print mastered
	##################  mastered - end ##################
	#print "source:  "  + str(source)
	#print "mastered:  "  + str(mastered)
	
	
	
	resultBool =  (source or mastered)
	if resultBool == True:
		result = 0
	else:
		result = 1
		retObj.setError(error)
		#print error
	retObj.setRetVal(result)
	return retObj
	
def photoConnectMysqlDict(stage):
	dict = {'function' : 'photoConnectMysql'}
	dict['stage']= stage
	if stage == 'production':	
		hostName="pepe.larc.nasa.gov"
	elif stage == 'developmentMarvin':
		hostName="marvin.larc.nasa.gov"
	else:
		hostName="pepe.larc.nasa.gov"
	userName="jshipman"
	passwd="lowd0wn"
	databaseName="jlshipman"
	conn=connection(hostName, userName, passwd, databaseName)
	dict['conn']= conn	
	return dict
	 
#get list of images in the database
def photoImagesInDatabase(databaseImageListFile, stage):
	dict = {'function' : 'photoImagesInDatabase'}
	dict['stage']= stage
	photoImagesDatabase = []
	retDict = photoConnectMysqlDict(stage)
	conn = retDict['conn']
	resultDict = photoAllImagesNames (conn)	
	databaseImageList = resultDict['resultList']
  	c = conn.cursor()
  	c.close() 	
  	listToFile( databaseImageList, databaseImageListFile)
  	
def photoAllImagesNames (conn):
	dict = {'function' : 'photoAllImages'}
	dict['numberOfRows']= 0
	resultList = []
	#return emails
	statement = """SELECT fileName
				FROM P_L""";
	c = conn.cursor()	
	
	#My understanding is that it should follow the pattern 
	#cursor.execute( <select statement string>, <tuple>) 
	#and by putting only a single value in the tuple location 
	#it is actually just a string. To make the second argument 
	#the correct data type you need to put a comma in there
	c.execute (statement)
	rows = c.fetchall()
	try:
		numberOfRows = len (rows)		
	except Exception:
		lg.info ("      no records found for:  " + name)
		dict['retVal']= False
	if numberOfRows > 0:
		dict['retVal']= True
		for row in rows:
			resultList.append(row[0])
	else:
		dict['retVal']= False
	dict['numberOfRows']= numberOfRows
	sortList = sorted(resultList)
	dict['resultList']= sortList
	return dict
	
def photoExistObj (conn, name):
	retObj = funcReturn.funcReturn('photoExistObj')
	c = conn.cursor()	
	searchValue = name;
	statement = """SELECT *
				FROM P_L
				WHERE fileName = %s""";
	retObj.setCommand(statement)
	
	#My understanding is that it should follow the pattern 
	#cursor.execute( <select statement string>, <tuple>) 
	#and by putting only a single value in the tuple location 
	#it is actually just a string. To make the second argument 
	#the correct data type you need to put a comma in there
	c.execute (statement, (searchValue, ))
	rows = c.fetchall()
	try:
		numberOfRows = len (rows)		
	except Exception:
		retObj.setComment("no records found for:  " + name)
		retObj.setFound(0)
		return retObj
		
	retObj.setComment("numberOfRows:  " + str(numberOfRows))
	if numberOfRows == 1:
		result = 0
		retObj.setFound(0)
	else:
		result = 1
		
	retObj.setRetVal(0)
	return retObj

def photoDelete (conn, stage, name):
	retObj = funcReturn.funcReturn('photoDelete')
	searchArray = [name]
	statement = """DELETE FROM P_L
		WHERE  fileName = %s""";
	retObj.setCommand(statement)
	c = conn.cursor()	
	c.execute (statement, searchArray)	
	retObjExist = photoExistObj (conn, name)
	if retObjExist.getFound() == 0:
		retObj.setRetVal(1)
		retObj.setFound(0)
		retObj.setComment("Record found for:  " + name)
	else:
		retObj.setRetVal(0)
		retObj.setFound(1)
		retObj.setComment("No record found for:  " + name)
	return retObj
	
def photoInsert (lg, mailList, conn, name, cd):
	lg.setPrefix ("photoInsert")
	photo={}
	photoObj=photoParts(name, "jpg")
	photoResult = photoObj.getResult()
	type=photoResult['type'].strip()
	raw=photoResult['raw']
	alpha=photoResult['letter']
	retObj = prefix (conn)
	result = retObj.getResult()
	letter=result[alpha]
	year=photoResult['year']	
	if year == "":
		year = "noYear"
	seq=photoResult['seq']
	extra=photoResult['extra']
	if extra != "":
		seq = seq + extra
	type=photoResult['type']
	noSuffix=photoResult['noSuffix']
	
	webname=photoResult['webname']
	if type == "raw":
		rawStr = "on"
	else:
		rawStr = "off"
	lg.info ("        --rawStr  " + rawStr)
	lg.info ("        noSuffix  " + noSuffix)
	lg.info ("        type  " + type)
	searchArray = [webname, year, seq, letter, rawStr, cd]
	statement = """INSERT INTO P_L(fileName, lYear, lSequence, prefix,  timeModifiy, timeCreated, raw, rawDVD) 
		VALUES (%s , %s , %s , %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s )""";
	lg.info ("      insert statement:  " + statement)
	c = conn.cursor()	
	c.execute (statement, searchArray)	
		
def photoUpdate (lg, mailList, conn, name, cd):
	lg.setPrefix ("photoUpdate")
	lg.info ("        --name  " + name)
	photoObj= photoParts(name, "jpg")
	if photoObj.getRetVal() == 1:
		lg.info ("      problem with function photoParts in photoUpdate function")
		mailList['subject'] = "problem with function photoParts in photoUpdate function"
		message = "problem with function photoParts in photoUpdate function"
		mailList['message'] = message
		shortMessage (mailList)
		sys.exit(1)
				
	result = photoObj.getResult()
	raw=result['raw']
	year=result['year']	
	if year == "":
		year = "noYear"
	letter=result['letter']	
	seq=result['seq']
	type=result['type']
	noSuffix=result['noSuffix']
	alpha=""
	webname=result['webname']
	if type == "source":
		rawStr = "on"
	else:
		rawStr = "off"
	lg.info ("        --rawStr  " + rawStr)
	lg.info ("        type  " + type)
	lg.info ("        year  " + str(year))
	lg.info ("        seq  " + seq)
	lg.info ("        letter  " + letter)
	lg.info ("        cd  " + cd)
	lg.info ("        noSuffix  " + noSuffix)
	lg.info ("        webname  " + webname)
	searchArray = [rawStr, year, seq, letter, cd, webname]
	statement = """UPDATE P_L 
			SET timeModifiy =  CURRENT_TIMESTAMP, raw = %s, lYear = %s, lSequence = %s, 
				prefix = %s, rawDVD = %s	
			WHERE fileName = %s""";
	lg.info ("      update statement:  " + statement)
	c = conn.cursor()	
	c.execute (statement, searchArray)	
			
def photoEmails (lg, mailList, conn):
	#return emails
	searchValue = "photoUploadEmail";
	statement = """SELECT value
				FROM valuePair
				WHERE value2 = %s""";
	c = conn.cursor()	
	
	#My understanding is that it should follow the pattern 
	#cursor.execute( <select statement string>, <tuple>) 
	#and by putting only a single value in the tuple location 
	#it is actually just a string. To make the second argument 
	#the correct data type you need to put a comma in there
	c.execute (statement, (searchValue, ))
	
	result_set = c.fetchall()
	return result_set[0][0]

def photoExist (lg,	mailList, conn, name):
	searchValue = name;
	statement = """SELECT *
				FROM P_L
				WHERE fileName = %s""";
	c = conn.cursor()	
	
	#My understanding is that it should follow the pattern 
	#cursor.execute( <select statement string>, <tuple>) 
	#and by putting only a single value in the tuple location 
	#it is actually just a string. To make the second argument 
	#the correct data type you need to put a comma in there
	c.execute (statement, (searchValue, ))
	rows = c.fetchall()
	try:
		numberOfRows = len (rows)		
	except Exception:
		lg.info ("      no records found for:  " + name)
		return False
	lg.info ("      numberOfRows:  " + str(numberOfRows))
	if numberOfRows == 1:
		return True
	else:
		return False

def photoExist2 (conn, name):
	c = conn.cursor()	
	dict = {'function' : 'photoExist2'}
	searchValue = name;
	
	
	dict['retVal'] = 1
	statement = """SELECT *
				FROM P_L
				WHERE fileName = %s""";
	dict['statement'] = statement
	dict['comment'] = ""
	
	
	#My understanding is that it should follow the pattern 
	#cursor.execute( <select statement string>, <tuple>) 
	#and by putting only a single value in the tuple location 
	#it is actually just a string. To make the second argument 
	#the correct data type you need to put a comma in there
	c.execute (statement, (searchValue, ))
	rows = c.fetchall()
	try:
		numberOfRows = len (rows)		
	except Exception:
		dict['comment'] = "      no records found for:  " + name
		dict['retVal'] = 1
	dict['comment'] = "      numberOfRows:  " + str(numberOfRows)
	if numberOfRows == 1:
		dict['retVal'] = 0
	else:
		dict['retVal'] = 1
		
	return dict

def photoOrginalScan (conn, name):
	c = conn.cursor()	
	dict = {'function' : 'photoOrginalScan'}
	searchValue = name;
	
	
	dict['retVal'] = 1
	statement = """SELECT *
				FROM P_L
				WHERE fileName = %s
				AND raw = 'on'""";
	dict['statement'] = statement
	dict['comment'] = ""
	
	#My understanding is that it should follow the pattern 
	#cursor.execute( <select statement string>, <tuple>) 
	#and by putting only a single value in the tuple location 
	#it is actually just a string. To make the second argument 
	#the correct data type you need to put a comma in there
	c.execute (statement, (searchValue, ))
	rows = c.fetchall()
	try:
		numberOfRows = len (rows)		
	except Exception:
		dict['comment'] = "      no records found for:  " + name
		dict['retVal'] = -1
	dict['comment'] = "      numberOfRows:  " + str(numberOfRows)
	if numberOfRows == 1:
		dict['retVal'] = 0
	else:
		dict['retVal'] = 1
		
	return dict	

def prefix (conn):
	retObj = funcReturn.funcReturn('photoPrefix')
	# SELECT Prefxs ##
	statement = ""
	statement = statement + "SELECT * \n";
	statement = statement + "FROM P_Prefix";
	c = conn.cursor()	
	c.execute (statement)
	result_set = c.fetchall()
	dict = {}
	for row in result_set:
		dict[row[1]] = row[0]
	retObj.setResult(dict)
	return retObj	

def photoPrefix (lg, mailList, conn):
	# SELECT Prefxs ##
	statement = ""
	statement = statement + "SELECT * \n";
	statement = statement + "FROM P_Prefix";
	c = conn.cursor()	
	c.execute (statement)
	result_set = c.fetchall()
	dict = {}
	for row in result_set:
		dict[row[1]] = row[0]
	return dict


def photoConnectMysql2(stage):
	retObj = funcReturn.funcReturn('photoConnectMysql2')
	if stage == "production":	
		hostName="pepe.larc.nasa.gov"
	else:
		hostName="marvin.larc.nasa.gov"
	userName="jshipman"
	passwd="lowd0wn"
	databaseName="jlshipman"
	conn=connection(hostName, userName, passwd, databaseName)	
	retObj.setResult(conn)
	retObj.setComment(hostName)
	retObj.setRetVal(0)
	return retObj
	   		
def photoConnectMysql(lg, mailList, stage):
	lg.setPrefix ("photoCheckMysql")
	if stage == "production":	
		hostName="pepe.larc.nasa.gov"
	else:
		hostName="marvin.larc.nasa.gov"
	userName="jshipman"
	passwd="lowd0wn"
	databaseName="jlshipman"
	conn=connection(hostName, userName, passwd, databaseName)	
	return conn
	
def photoMysql(lg, mailList, dirContentsFileJpg, stage, cdNameFile, repositorylist):
	retObj = funcReturn.funcReturn('photoMysql')
	lg.setPrefix ("photoMysql")	
	
	cdName=readFirstLineFile(cdNameFile)
	lg.info ("      cdName:  " + cdName)
	if stage == "production":
		webDir = "msbwc"
	else:
		webDir = "msbwc-d"
	lg.info ("      webDir:  " + webDir)
		
	pathFin ="/usr/local/web/htdocs/" + webDir + "/photo/images"
	pathThumb ="/usr/local/web/htdocs/" + webDir + "/photo/thumbs"
	lg.info ("      pathFin:  " + pathFin)
	lg.info ("      pathThumb:  " + pathThumb)
	
	conn = photoConnectMysql(lg, mailList, stage)
	
	result=photoEmails (lg, mailList, conn)
	photoEmail=result
	lg.info ("      photoEmail:  " + photoEmail)
	
  	result=photoPrefix (lg, mailList, conn)
  	for key, value in result.items(): # returns the dictionary as a list of value pairs -- a tuple.
		lg.info ("      key:  " + key)
		lg.info ("      value:  " + str(value))
	
	jpgList = listFromFile(dirContentsFileJpg)
	for j in jpgList:
		j=j.rstrip()
		lg.info ("      j:  " + j)
		retObjName = imageProperlyNamedJpg(j)
		result = retObjName.getRetVal()
		if result == 0 :
			lg.info ("      photo is properly named")	
			lg.info ("      j:  " + j)
			retObjPart=photoParts(j, "jpg")
			
			if retObjPart.getRetVal() == 1:
				lg.info ("      problem with function photoParts in photoMysql function")
				mailList['subject'] = "problem with function photoParts in photoMysql function"
				message = "problem with function photoParts in photoMysql function"
				mailList['message'] = message
				shortMessage (mailList)
				
				sys.exit(1)
				
			result = retObjPart.getResult()
			raw=result['raw']
			year=result['year']	
			if year == "":
				year = "noYear"
			letter=result['letter']	
			seq=result['seq']
			type=result['type']
			noSuffix=result['noSuffix']
			webname=result['webname']
			
			lg.info ("      raw:  " + str(raw))
			lg.info ("      year:  " + str(year))
			lg.info ("      type:  " + type)
			lg.info ("      seq:  " + seq)
			lg.info ("      noSuffix:  " + noSuffix)
			lg.info ("      webname:  " + webname)
			existInDatabase=photoExist(lg,	mailList, conn, webname)
			lg.info ("      existInDatabase:  " + str(existInDatabase))
			if existInDatabase == True:
				retDict = repoCheck(j, repositorylist)
				comment = retDict['comment']
				lg.info (comment)
				if retDict['result'] == "update":
					lg.info ("\t\tupdate database")
					photoUpdate (lg, mailList, conn, j, cdName)
				else:
					lg.info ("      repoCheck:  " + retDict['result'])
			else:
				lg.info("      j:  " + j)
				lg.info("      cdName:  " + cdName)
				photoInsert (lg, mailList, conn, j, cdName)
				lg.info ("\t\tinsert database")
		else:
			lg.warn ("\t\tphoto is not properly named")	
			
  	c = conn.cursor()
  	c.close()
  	retObj.setResult(jpgList)
  	return retObj

def repoCheck(image, repositorylist):
	dict = {'function' : 'repoCheck'}
	#check for for file having raw in repository
	base = os.path.basename(image)
	dict['base'] = base
	dict['retVal'] = 0
	dict['checkOrig'] = 0
	dict['checkMod'] = 0
	dict['comment'] = ""
	comment = "\n"
	dict['result'] = "doNothing"
	retDict = photoPartsDict(base)
	year = retDict['year']
	typePhoto = retDict['type']
	noSuffix = retDict['noSuffix']
	if year == "":
		year = "noYear"
	else:
		year = retDict['year']	
	f = open(repositorylist)
	original = []
	modified = []
	lines = f.readlines()
	sep = "#"
	for line in lines:
		type, path = line.rstrip().split(sep)
		if type == "modified":
			modified.append(path)
		if type == "original":
			original.append(path)
	f.close()	
	#print "typePhoto:  _" + typePhoto + "_"
	if typePhoto == "raw":
		comment = comment + "file is original \n"
	else:
		comment = comment + "file is modified \n"
		
	modName = noSuffix.replace("R-", "")	
	for o in original:
		fileToCheck = o +  "/" + year +  "/pic/R-" + modName + ".tif"
		comment = comment + "fileToCheck: " + fileToCheck + " \n"
		if fileExist(fileToCheck):
			comment = comment + "original exists \n"
			dict['checkOrig'] =  1
	
	for m in modified:	
		fileToCheck = m  + "/" + year +  "/pic/" + modName + ".tif"
		comment = comment + "fileToCheck: " + fileToCheck + " \n"
		if fileExist(fileToCheck):
			comment = comment + "modified exists \n"
			dict['checkMod'] =  1
	
	#print "typePhoto:  _" + typePhoto + "_"
	#original scans with a modified file are not updated
	if typePhoto == "raw" and dict['checkMod'] == 1:
		dict['result'] = "doNothing"
		comment = comment + "original scans with a modified file are not updated \n"
		
	#original scans without a modified file are updated
	if typePhoto == "raw" and dict['checkMod'] == 0:
		dict['result'] = "update"
		comment = comment + "original scans without a modified file are updated \n"
	
	#any modified file is updated					
	if typePhoto == "processed":
		dict['result'] = "update"
		comment = comment + "any modified file is updated \n"
	
	comment = comment.rstrip()
	dict['comment'] = comment
	return dict
		
def photoTransfer(lg, mailList, archiveDir, stage, temp, outputFile, cdNameVarFile, repositorylist):
	lg.setPrefix ("photoTransfer")	
	now = datetime.datetime.now()
 	dirBaseName= now.strftime("%Y%m%d%H%M%S")
 	writeToFile( dirBaseName, cdNameVarFile)
	curDir=os.getcwd()
	user="msbwcup"
	server="lamp.larc.nasa.gov"
	public_key = '/Users/admin/.ssh/.ssh/id_rsa.pub'
	private_key = '/Users/admin/.ssh/.ssh/id_rsa'
	
	lg.info ("      stage:  " + stage )
	lg.info ("      archiveDir:  " + archiveDir )
	lg.info ("      temp:  " + temp )
	if stage == "production":
		sshConnect="msbwcup@lamp.larc.nasa.gov"	
		jpdDirFull=temp + "Full"
		#Create list of files with the Full directory within the temp directory
		dirContentsList = glob.glob(jpdDirFull + "/*" )
		sizeDir=len(dirContentsList)
		lg.info ("      ")
		lg.info ("    Image  ")	
		lg.info ("    jpdDirFull:  "+ jpdDirFull)	
		os.chdir(jpdDirFull)
		count=0
		dst="/usr/local/web/htdocs/msbwc/photo/images"
		#iterate through created list 
		#remove the R- 
		#push to lamps
		for t in dirContentsList:
			t=t.rstrip()
			lg.info ("    t:  " + t)
			retDict = repoCheck(t, repositorylist) 
			#if file does not exist or is modified image
			lg.info ("    comment:  " + retDict['comment'])
			if (retDict['result'] == "update"):
				lg.info ("file did not exist on repository or is a modified image")
				src = t.replace("R-", "")
				os.rename(t, src)
				lg.info ("    image - full:  "+ t)	
				lg.info ("    src:  "+ src)	
				if fileExist(outputFile):
					fileDelete (outputFile)
				fileCreate(outputFile)
				os.chmod(outputFile, 0777)
				resultDict=comWrapSSH(src, sshConnect, dst, "ladmin", outputFile)
				errorCheck = resultDict['errorCheck']
				lg.info ("      errorCheck:  " + str(errorCheck) )
				command = resultDict['command']
				lg.info ("      command:  " + command )
				output = resultDict['output']
				lg.info ("      output:  " + output )
				result =  resultDict['retVal']
				lg.info ("      result:  " + str(result) )
				if result == 0:
					lg.info ("    image - full:  "+ t)	
					fileDelete(src)
				else:
					lg.warn ("      unable to transfer image file:  " + t )
					command = resultDict['command']
					lg.info ("      command:  " + command )
					mailList['subject'] = "unable to transfer image file"
					mailList['message'] = message = "unable to transfer image file:  " + t
					shortMessage (mailList)
					sys.exit(1)	
			else:
				lg.info ("file did exist on repository")
				fileDelete(t)

		jpdDirThumb=temp + "Thumb"	
		dirContentsList = glob.glob(jpdDirThumb + "/*" )
		sizeDir=len(dirContentsList)
		lg.info ("      ")	
		lg.info ("    Thumb  ")	
		lg.info ("    jpdDirThumb:  "+ jpdDirThumb)	
		os.chdir(jpdDirThumb)
		count=0
		dst="/usr/local/web/htdocs/msbwc/photo/thumbs"
		for t in dirContentsList:
			t=t.rstrip()
			retDict = repoCheck(t, repositorylist) 
			#if file does not exist or is modified image
			if (retDict['result'] == "update"):
				src = t.replace("R-", "")
				os.rename(t, src)
				if fileExist(outputFile):
					fileDelete (outputFile)
				fileCreate(outputFile)
				os.chmod(outputFile, 0777)
				resultDict=comWrapSSH(src, sshConnect, dst, "ladmin", outputFile)
				errorCheck = resultDict['errorCheck']
				lg.info ("      errorCheck:  " + str(errorCheck) )
				command = resultDict['command']
				lg.info ("      command:  " + command )
				output = resultDict['output']
				lg.info ("      output:  " + output )
				result =  resultDict['retVal']
				lg.info ("      result:  " + str(result) )
				if result == 0:
					lg.info ("    image - thumb:  "+ t)	
					fileDelete(src)
				else:
					lg.warn ("      unable to transfer thumb file:  " + t )
					command = resultDict['command']
					lg.info ("      command:  " + command )
					mailList['subject'] = "unable to transfer thumb file"
					mailList['message'] = message = "unable to transfer thumb file:  " + t
					shortMessage (mailList)
					sys.exit(1)	
			else:
				lg.info ("file did exist on repository")
				fileDelete(t)

		num=countFiles(jpdDirFull)
		lg.info ("    files left in " + jpdDirFull + ":  " + str(num))	
		num=countFiles(jpdDirThumb)
		lg.info ("    files left in " + jpdDirThumb + ":  " + str(num))	
	else:
		lg.warn ("      no jpgs that are properly named ready for transfer  ")	
	os.chdir(curDir)
	#return dirBaseName
	
def photoSort (lg, mailList, dirContentsFile, resposDict, chksumDir, stage):
	lg.setPrefix ("photoSort")	
	dirContentsList = listFromFile(dirContentsFile)
	sizeDir=len(dirContentsList)
	lg.info ("    sizeDir:  "+ str(sizeDir))
	if int(sizeDir) > 0:
		count=0
		for t in dirContentsList:
			t=t.rstrip()
			lg.info ("    t:  "+ t)
			count+=1
			lg.info (str(count) +" of "+ str(sizeDir))
		
			base = os.path.basename(t) 
			lg.info ("        base:  "+ base)
		
			dirPath = os.path.dirname(t) 
			lg.info ("        dirPath:  "+ dirPath)
		
			result=isRaw(base)
			lg.info ("        isRaw:  " + str(result))
		
			retObjNamed = imageProperlyNamed(base)		
			retVal = retObjNamed.getRetVal()
			if retVal == 0:

				lg.info ("        photo is properly named:  ")
			
				retObj=photoParts(base)
			
				if retObj.getRetVal() == 1:
					lg.info ("      problem with function photoParts in function photoSort")
					mailList['subject'] = "problem with function photoParts in function photoSort"
					message = "problem with function photoParts in function photoSort"
					mailList['message'] = message
					shortMessage (mailList)
					sys.exit(1)
				
				result = retObj.getResult()
				raw=result['raw']
				year=result['year']	
				if year == "":
					year = "noYear"
				letter=result['letter']	
				seq=result['seq']
				type=result['type']
				noSuffix=result['noSuffix']
			
				reposProcess=resposDict['reposProcess']
				reposProcessLower=resposDict['reposProcessLower']
				reposProcessUpper=resposDict['reposProcessUpper']
				noYearProcess=resposDict['noYearProcess']
				repos1=resposDict['repos1']
				repos1Lower=resposDict['repos1Lower']
				repos1Upper=resposDict['repos1Upper']
				repos2=resposDict['repos2']
				repos2Lower=resposDict['repos2Lower']
				repos2Upper=resposDict['repos2Upper']
				reposProcess=resposDict['reposProcess']
				reposProcessLower=resposDict['reposProcessLower']
				reposProcessUpper=resposDict['reposProcessUpper']
				noYearRaw=resposDict['noYearRaw']
				newLocalFullPath=""
				if raw == True:					
					#go to raw repository
					lg.info ("      raw")
					if year!="":
						lg.info ("      year:  " + str(year))
						lg.info ("      repos1Lower:  " + str(repos1Lower))
						lg.info ("      repos1Upper:  " + str(repos1Upper))
						lg.info ("      repos2Lower:  " + str(repos2Lower))
						lg.info ("      repos2Upper:  " + str(repos2Upper))
						lg.info ("      (" + str(year) + ">=" +  str(repos1Lower)+") and (" + str(year) +"<="+  str(repos1Upper) +")")
						lg.info ("      (" + str(year) + ">=" +  str(repos2Lower)+") and (" + str(year) +"<="+  str(repos2Upper) +")")
						if (year >= repos1Lower) and (year <= repos1Upper):
							lg.info ("first if")
							newLocalFullPath=repos1 +  str(year) + "/pic/" + base	
							newLocalFullPathck=repos1 +  str(year) + "/ck/" + noSuffix + ".ck"		
						if (year >= repos2Lower) and (year <= repos2Upper):
							lg.info ("second if")
							newLocalFullPath=repos2  + str(year) + "/pic/" + base
							newLocalFullPathck=repos2  + str(year) + "/ck/" + noSuffix + ".ck"
					else:
						lg.info ("      noYear")
						newLocalFullPath=noYearRaw + "noYear/pic/" + base
						newLocalFullPathck=noYearRaw + "noYear/ck/"+ ".ck"
				else:
					lg.info ("      processed")
					lg.info ("      year:  " + str(year))
					#go to processed repository
					if year!="":
						lg.info ("      year:  " + str(year))
						newLocalFullPath=reposProcess  +  str(year) + "/pic/" + base
						newLocalFullPathck=reposProcess  +  str(year) + "/ck/" + noSuffix + ".ck"
					else:
						lg.info ("      noYear")
						newLocalFullPath=noYearProcess + "noYear/pic/" + base
						newLocalFullPathck=noYearProcess + "noYear/ck/" + noSuffix + ".ck"
					
				lg.info ("      for base:  " + base + " newPath:  " + newLocalFullPath)
				src = t
				dst = newLocalFullPath
				src2 = chksumFilePath=chksumDir + noSuffix + ".ck"
				lg.info ("      newLocalFullPathck:  " + newLocalFullPathck )
				dst2 = newLocalFullPathck
				lg.info ("      stage:  " + stage )
				if stage == "production":
					lg.info ("      src:  " + src )
					lg.info ("      dst:  " + dst )
					retDict = fileMove2(src, dst)
					result=retDict['retVal']
					if result == 1:
						error = retDict['error']
						if error == "destination directory does not exist":
							dstDir = os.path.dirname(dst)
							os.makedirs(dstDir)
							retDict = fileMove2(src, dst)
							result=retDict['retVal']
							if result == 1:
								lg.info ("      unable to move picture file:  " + src )
								lg.info ("      error:  " + error )
								mailList['subject'] = "unable to move picture file"
								message = "unable to move picture file:  " + src + "/n"
								message = message + error
								mailList['message'] = message
								shortMessage (mailList)
								sys.exit(1)	
						else:
							lg.info ("      unable to move picture file:  " + src )
							lg.info ("      error:  " + error )
							mailList['subject'] = "unable to move picture file"
							message = "unable to move picture file:  " + src + "/n"
							message = message + error
							mailList['message'] = message
							shortMessage (mailList)
							sys.exit(1)	
				
					retDict = fileMove2(src2, dst2)	
					result=retDict['retVal']
					if result == 1:
						error = retDict['error']
						if error == "destination directory does not exist":
							dstDir = os.path.dirname(dst2)
							os.makedirs(dstDir)
							retDict = fileMove2(src2, dst2)
							result=retDict['retVal']
							if result == 1:
								lg.info ("      unable to move picture file:  " + src2 )
								lg.info ("      error:  " + error )
								mailList['subject'] = "unable to move picture file"
								message = "unable to move picture file:  " + src2 + "/n"
								message = message + error
								mailList['message'] = message
								shortMessage (mailList)
								sys.exit(1)	
						else:
							lg.info ("      unable to move picture file:  " + src2 )
							lg.info ("      error:  " + error )
							mailList['subject'] = "unable to move picture file"
							message = "unable to move picture file:  " + src2 + "/n"
							message = message + error
							mailList['message'] = message
							shortMessage (mailList)
							sys.exit(1)	
			else:
				lg.warn ("      photo is not properly named:  ")	
					
def photoArchive (lg, mailList, dirContentsFile, archiveFile, baseError, chksumDir, stage):
	dirContentsList = listFromFile(dirContentsFile)
	lenCheck = int(len(dirContentsList))
	lg.setPrefix ("photoArchive")
	if lenCheck > 0:
		cssErrorMkdir=baseError + "cssErrorMkdir.txt"
		cssErrorCopyPic=baseError + "cssErrorCopyPic.txt"
		cssErrorCopyCK=baseError + "cssErrorCopyCK.txt"
		dirObj=makeDirectoryObj(chksumDir)
		retValDir= dirObj.getRetVal()
		if retValDir == 1:
			mailList['subject'] = "could not create directory:   ---" + dirPath
			message = "could not create directory:   ---" + dirPath
			l.abort(message)
			mailList['message'] = message
			shortMessage (mailList)
			sys.exit(1)

		
		hostName=socket.gethostname()
		lg.info (" hostName:  "+ hostName)
		archiveList = []
		archiveList = listFromFile(archiveFile)
	
		#remove old chksum
		chksumList = glob.glob(chksumDir + "/*" )
		for c in chksumList:
			result=comWrapDelete(c)
			if result == 1:
				mailList['subject'] = "unable to delete file"
				mailList['message'] = message = "unable to delete file:  " + c
				shortMessage (mailList)
				sys.exit(1)		
	
		try:
			curPath = os.getcwd()
		except Exception:
			mailList['subject'] = mailList['message'] = message = "unable to get current direcotry"
			shortMessage (mailList)
			sys.exit(1)	
		dirContentsList = listFromFile(dirContentsFile)
		sizeDir=len(dirContentsList)
		count=0
		for t in dirContentsList:
			t=t.rstrip()
			lg.info ("    t:  "+ t)
			count+=1
			lg.info (str(count) +" of "+ str(sizeDir))

			base = os.path.basename(t) 
			lg.info ("    base:  "+ base)
		
			dirPath = os.path.dirname(t) 
			lg.info ("    dirPath:  "+ dirPath)
		
			retObjNamed = imageProperlyNamed(base)		
			retVal = retObjNamed.getRetVal()
			if retVal == 0:		
				lg.info ("      photo is properly named:  ")
			
				photo={}
				retObj=photoParts(base)
			
				if retObj.getRetVal() == 1:
					lg.info ("      problem with function photoParts in function photoArchive")
					mailList['subject'] = "problem with function photoParts in function photoArchive"
					message = "problem with function photoParts in function photoArchive"
					mailList['message'] = message
					shortMessage (mailList)
					sys.exit(1)
				
				result = retObj.getResult()
				raw=result['raw']
				year=result['year']	
				if year == "":
					year = "noYear"
				letter=result['letter']	
				seq=result['seq']
				type=result['type']
				noSuffix=result['noSuffix']
							
				#create checksums and copy record to CSS
				for a in archiveList:
					archive=a.strip()	
					cssDirCk=archive + "/" + hostName + "/" + type + "/" + str(year) + "/ck" 
					lg.info ("      cssDirCk: " + cssDirCk)
					cssDirPic=archive + "/" + hostName + "/" + type + "/" + str(year) + "/pic" 
					lg.info ("      cssDirPic: " + cssDirPic)
					#create checkSum File
					#change directory to unprocessed folder
					try:
						os.chdir(dirPath)
					except Exception:
						mailList['subject'] = mailList['message'] = message = "unable to to change direcotry to: " + dirPath
						shortMessage (mailList)
						os.chdir(curPath)	
						sys.exit(1)		
					lg.info ("      changed directory to: " + dirPath)
					chksumFilePath=chksumDir + noSuffix + ".ck"
					lg.info ("      chksumFilePath:  " + chksumFilePath )
					result = comWrapCheckSum(base,chksumFilePath)
					if result != 0:
						mailList['subject'] = mailList['message'] = message = "unable to create checksum for " + base
						shortMessage (mailList)
						os.chdir(curPath)	
						sys.exit(1)
					else:
						lg.info ("      check sum created  ")
				
					lg.info ("      stage:  " + stage )
					if stage == "production":
						#copy to CSS
						lg.info ("      local full path: " + t)
						lg.info ("      cssDirPic: " + cssDirPic)
						resultDict = comWrapMasmkdir(cssDirPic, cssErrorMkdir)
						command = resultDict[ 'command']
						lg.info ("      command:  " + command )
						result = resultDict[ 'retVal']
						if result != 0:						
							lg.info ("      stage:  " + stage )
						
							function = resultDict[ 'function']
							lg.info ("      function:  " + function )
							command = resultDict[ 'command']
							lg.info ("      command:  " + command )
							error = resultDict[ 'error']
							lg.info ("      error:  " + error )
						
							function2 = resultDict[ 'function2']
							lg.info ("      function2:  " + function2 )
							command2 = resultDict[ 'function2Command']
							lg.info ("      command2:  " + command2 )
						
							mailList['subject'] = "unable to mkdir pic for CSS: " + cssDirPic
							message = "      function:  " + function + "\n"
							message = message + "      command:  " + command + "\n"
							message = message + "      error:  " + error + "\n"
							message = message + "      function2:  " + function2 + "\n"
							message = message + "      command2:  " + command2 + "\n"
							mailList['message'] = message
							shortMessage (mailList)
							os.chdir(curPath)	
							sys.exit(1)
						
						cssFullPath = cssDirPic + "/" + noSuffix + ".tif"
						lg.info ("      cssFullPath: " + cssFullPath)
						resultDict = comWrapMasputDelay2(t, cssFullPath, cssErrorCopyPic)	
						command = resultDict[ 'command']
						lg.info ("      command:  " + command )
						result = resultDict[ 'retVal']
						if result != 0:						
							lg.info ("      stage:  " + stage )
						
							function = resultDict[ 'function']
							lg.info ("      function:  " + function )
							command = resultDict[ 'command']
							lg.info ("      command:  " + command )
							error = resultDict[ 'error']
							lg.info ("      error:  " + error )
						
							function2 = resultDict[ 'function2']
							lg.info ("      function2:  " + function2 )
							command2 = resultDict[ 'function2Command']
							lg.info ("      command2:  " + command2 )
						
							mailList['subject'] = "unable to copy file to CSS: " + t
							message = "      function:  " + function + "\n"
							message = message + "      command:  " + command + "\n"
							message = message + "      error:  " + error + "\n"
							message = message + "      function2:  " + function2 + "\n"
							message = message + "      command2:  " + command2 + "\n"
							mailList['message'] = message
							shortMessage (mailList)
							os.chdir(curPath)	
							sys.exit(1)
						
						
						lg.info ("      chksumFilePath:  " + chksumFilePath )
						lg.info ("      cssDirCk:  " + cssDirCk )
						resultDict = comWrapMasmkdir(cssDirCk, cssErrorMkdir)
						command = resultDict[ 'command']
						lg.info ("      command:  " + command )
						result = resultDict[ 'retVal']
						if result != 0:						
							lg.info ("      stage:  " + stage )
						
							function = resultDict[ 'function']
							lg.info ("      function:  " + function )
							command = resultDict[ 'command']
							lg.info ("      command:  " + command )
							error = resultDict[ 'error']
							lg.info ("      error:  " + error )
						
							function2 = resultDict[ 'function2']
							lg.info ("      function2:  " + function2 )
							command2 = resultDict[ 'function2Command']
							lg.info ("      command2:  " + command2 )
						
							mailList['subject'] = "unable to mkdir checksum for CSS: " + cssDirCk
							message = "      function:  " + function + "\n"
							message = message + "      command:  " + command + "\n"
							message = message + "      error:  " + error + "\n"
							message = message + "      function2:  " + function2 + "\n"
							message = message + "      command2:  " + command2 + "\n"
							mailList['message'] = message
							shortMessage (mailList)
							os.chdir(curPath)	
							sys.exit(1)
						cssCkFullPath = cssDirCk + "/" + noSuffix + ".ck"
						lg.info ("      cssCkFullPath: " + cssCkFullPath)
						resultDict = comWrapMasputDelay2(chksumFilePath, cssCkFullPath, cssErrorCopyCK)	
						command = resultDict[ 'command']
						lg.info ("      command:  " + command )
						result = resultDict[ 'retVal']
						lg.info ("      result:  " + str(result) )
						if result != 0:
							lg.info ("      stage:  " + stage )
						
							function = resultDict[ 'function']
							lg.info ("      function:  " + function )
							command = resultDict[ 'command']
							lg.info ("      command:  " + command )
							error = resultDict[ 'error']
							lg.info ("      error:  " + error )
						
							function2 = resultDict[ 'function2']
							lg.info ("      function2:  " + function2 )
							command2 = resultDict[ 'function2Command']
							lg.info ("      command2:  " + command2 )

							mailList['subject'] = "unable to copy file to CSS: " + chksumFilePath						
							message = "      function:  " + function + "\n"
							message = message + "      command:  " + command + "\n"
							message = message + "      error:  " + error + "\n"
							message = message + "      function2:  " + function2 + "\n"
							message = message + "      command2:  " + command2 + "\n"

							mailList['message'] = message
							shortMessage (mailList)
							os.chdir(curPath)	
							sys.exit(1)

			else:
				lg.warn ("      photo is not properly named:  ")	
		os.chdir(curPath)	
	else:
		lg.info ("      no records in list")							
				
def photoFileConvert (lg, mailList, dirContentsFile, dirContentsFileJpg, temp, badName, badTif ):
	lg.setPrefix ("photoFileConvert")
	dirContentsList = listFromFile(dirContentsFile)
	newDirContentsList = []
	jpdDirFull=temp + "Full"
	makeDirectory(jpdDirFull)
	jpdDirThumb=temp + "Thumb"
	makeDirectory(jpdDirThumb)
	jpgList = []
	badNameList = []
	badTifList = []
	#change privilege and correct names
	sizeDir=len(dirContentsList)
	count=0
	for t in dirContentsList:
		t=t.rstrip()
		lg.info ("    t:  "+ t)
		count+=1
		lg.info (str(count) +" of "+ str(sizeDir))
		base = os.path.basename(t) 
		lg.info ("    base:  "+ base)
		retObjNamed = imageProperlyNamed(base)		
		retVal = retObjNamed.getRetVal()
		if retVal == 0:
			lg.info ("      photo is properly named:  ")				
			jpgBase = base.replace(".tif", ".jpg")
			jpgFull= jpdDirFull + "/" + jpgBase
			jpgThumb= jpdDirThumb + "/" + jpgBase
			lg.info ("      jpgFull:  "+ jpgFull)
			lg.info ("      jpgThumb:  "+ jpgThumb)
			resultDictFull = comWrapConvertTiff2Jpg( t, jpgFull)
			resultFull = resultDictFull['retVal']
			lg.info ("      resultFull:  "+ str(resultFull))
			resultDictThumb = comWrapConvertTiff2JpgThumb( t, jpgThumb)
			resultThumb = resultDictThumb['retVal']
			lg.info ("      resultThumb:  "+ str(resultThumb))
			commandThumb=resultDictThumb['command']
			commandFull=resultDictFull['command']
			#test to see that tif file was able to convert to jpg
			#change test to testing existence of file before going forward
			if (resultFull == 1 or resultThumb == 1):
				badTifList.append(t)
				lg.warn ("      tif is badly constructed and can't be converted:  " + t)
				lg.warn (commandFull)
				lg.warn (commandThumb) 
				src = t
				dst = badTif + "/" + base
				retDict = fileMove2 (src, dst)
				result=retDict['retVal']
				if result == 1:
					error = retDict['error']
					lg.warn ("      unable to move badly constructed tif file:  " + src )
					sys.exit(1)
			else:
				#create new list for next function
				newDirContentsList.append(t)
				jpgList.append(jpgBase)
		
		else:
			badNameList.append(t)
			lg.warn ("      photo is not properly named:  " + base)
			src = t
			dst = badName + "/" + base
			retDict = fileMove2 (src, dst)
			result=retDict['retVal']
			if result == 1:
				error = retDict['error']
				lg.warn ("      unable to move bad file:  " + src )

	sizeList = len(badNameList)
	if sizeList > 0:
		mailList2 = dict(mailList)
		mailList2['subject'] = "bad file submitted"
		message = "bad file submitted:  \n"
		for b in badNameList:
			message = message + b + "\n"
		mailList2['message'] = message
		mailList2['to_addr'] = "t.hornbuckle@nasa.gov,renato.c.cruz@nasa.gov"
		shortMessage (mailList2)
	
	sizeList = len(badTifList)
	if sizeList > 0:
		mailList2 = dict(mailList)
		mailList2['subject'] = "badly constructed tif files submitted"
		message = "bad constructed tif files submitted:  \n"
		for b in badTifList:
			message = message + b + "\n"
		mailList2['message'] = message
		mailList2['to_addr'] = "t.hornbuckle@nasa.gov,renato.c.cruz@nasa.gov"
		shortMessage (mailList2)
					
	listToFile(jpgList, dirContentsFileJpg)
	#create new dirContentsList
	listToFile(newDirContentsList, dirContentsFile)
	#print ("inside photoFileConvert")
	#for d in newDirContentsList:
		#print "\timage:  " + d		
		
	return newDirContentsList
	
def photoFileModReturnOld  (lg, dirContentsFile):
	dict = {'function' : 'photoFileModReturn'}
	dict['retVal'] = 0
	dict['error'] = ""
	dict['comment'] = "\n"
	dict['newTIFF'] = ""	
	dirContentsList = listFromFile(dirContentsFile)
	
	#change privilege and correct names
	sizeDir=len(dirContentsList)
	
	lg.info ("  sizeDir:  " + str(sizeDir) )
	
	count=0
	for t in dirContentsList:
		t=t.rstrip()
		lg.info ("    t:  "+ t)
		count+=1
		lg.info (str(count) +" of "+ str(sizeDir))
		#change owner to ladmin
		#allow rwx owner
		#rwx group
		#r world
		ownID = pwd.getpwnam("ladmin").pw_uid
		groupID = grp.getgrnam("photo").gr_gid
		try:
			os.chown(t, ownID, groupID)
		except Exception:
			dict['error'] = "photoProcess - unable to change ownership on a file:  " + t
			dict['retVal'] = 1
			return dict
			
		try:
			os.chmod(t, 0774)
		except Exception, e:
			dict['error'] = "photoProcess - unable to change posix on a file:  " + t
			dict['retVal'] = 1
			return dict
		
		imageTIFF = t.rstrip()
		#lg.info ("  image:  "+ imageTIFF)
		
		#test TIFF name
		oldTIFF = os.path.basename(imageTIFF) 
		lg.info ("  oldTIFF:  "+ oldTIFF)
		dirPath = os.path.dirname(imageTIFF) 
		lg.info ("  dirPath:  "+ dirPath)
		newTIFF = oldTIFF
		newTIFF = newTIFF.replace(" ", "")
		newTIFF = newTIFF.replace("R_", "R-")
		newTIFF = newTIFF.replace("--", "-")
		lg.info ("newTIFF:  " + newTIFF)
		
		#replace the second to last decimal in number with underscore
		#L-156345.1231234.tif to L-156345_1231234.tif
		lg.info ("three decimal ")
		def numReplace(matchobj):
			test = matchobj.group(0)
			if matchobj.group(0)[0] == ".":
				test = string.replace(matchobj.group(0), ".", "_", 1)
			return test	
		newTIFF = re.sub('.\d+.tif', numReplace, newTIFF)
		lg.info ("\tnewTIFF:  " + newTIFF)
		if oldTIFF != newTIFF:
			lg.info ("\toldTIFF:  " + oldTIFF + " != newTIFF:  " +newTIFF)
			newFullPath = dirPath + "/" + newTIFF
			lg.info ("\tnewFullPath:  " + newFullPath )
			os.renames (t, newFullPath)
			oldTIFF = newTIFF
			lg.info ("\tnewFullPath:  " + newFullPath )
		lg.info ("hyphen ")	
		#replace the last hyphen in number when it is the symbolic decimal
		def decHyphenReplace(matchobj):
			test = matchobj.group(0)
			lg.info ("\ttest:  " + test)
			lg.info ("\tmatchobj.group(0)[0]:  " + matchobj.group(0)[0])
			second_index = test.find("-", test.find("-")+1)
			if matchobj.group(0)[second_index] == "-":
				stringList = list(test)
				stringList[second_index] = "_"
				test = "".join(stringList)
				lg.info ("\ttest:  " + test)
			return test	
		newTIFF = re.sub('-\d+-\d+.tif', decHyphenReplace, newTIFF)
		lg.info ("\toldTIFF:  " + oldTIFF)
		lg.info ("\tnewTIFF:  " + newTIFF)
		if oldTIFF != newTIFF:
			lg.info ("\toldTIFF:  " + oldTIFF + " != newTIFF:  " +newTIFF)
			newFullPath = dirPath + "/" + newTIFF
			lg.info ("\tnewFullPath:  " + newFullPath )
			os.renames (t, newFullPath)
		dict['newTIFF'] = newTIFF	
	return dict

def photoFileModReturn  (lg, dirContentsFile):
	dict = {'function' : 'photoFileModReturn'}
	dict['retVal'] = 0
	dict['error'] = ""
	dict['comment'] = "\n"
	dict['newTIFF'] = ""	
	dirContentsList = listFromFile(dirContentsFile)
	
	#change privilege and correct names
	sizeDir=len(dirContentsList)
	
	lg.info ("  sizeDir:  " + str(sizeDir) )
	
	count=0
	for t in dirContentsList:
		t=t.rstrip()
		lg.info ("    t:  "+ t)
		count+=1
		lg.info (str(count) +" of "+ str(sizeDir))
		#change owner to ladmin
		#allow rwx owner
		#rwx group
		#r world
		ownID = pwd.getpwnam("ladmin").pw_uid
		groupID = grp.getgrnam("photo").gr_gid
		try:
			os.chown(t, ownID, groupID)
		except Exception:
			dict['error'] = "photoProcess - unable to change ownership on a file:  " + t
			dict['retVal'] = 1
			return dict
			
		try:
			os.chmod(t, 0774)
		except Exception, e:
			dict['error'] = "photoProcess - unable to change posix on a file:  " + t
			dict['retVal'] = 1
			return dict
		
		imageTIFF = t.rstrip()
		#lg.info ("  image:  "+ imageTIFF)
		
		#test TIFF name
		oldTIFF = os.path.basename(imageTIFF) 
		lg.info ("  oldTIFF:  "+ oldTIFF)
		dirPath = os.path.dirname(imageTIFF) 
		lg.info ("  dirPath:  "+ dirPath)
		newTIFF = oldTIFF
		newTIFF = newTIFF.replace(" ", "")
		newTIFF = newTIFF.replace("R_", "R-")
		newTIFF = newTIFF.replace("--", "-")
		lg.info ("newTIFF:  " + newTIFF)
		dict['newTIFF'] = newTIFF	
	return dict
				
def photoFileMod  (lg, mailList, dirContentsFile):
	lg.setPrefix ("photoFileMod")
	lg.info ("  photoFileMod" )
	dirContentsList = listFromFile(dirContentsFile)
	
	#change privilege and correct names
	sizeDir=len(dirContentsList)
	
	lg.info ("  sizeDir:  " + str(sizeDir) )
	
	count=0
	for t in dirContentsList:
		t=t.rstrip()
		lg.info ("    t:  "+ t)
		count+=1
		lg.info ("\t" + str(count) +" of "+ str(sizeDir))
		#change owner to ladmin
		#allow rwx owner
		#rwx group
		#r world
		ownID = pwd.getpwnam("ladmin").pw_uid
		groupID = grp.getgrnam("photo").gr_gid
		try:
			os.chown(t, ownID, groupID)
		except Exception:
			mailList['subject'] = mailList['message'] = message = "photoProcess - unable to change ownership on a file"
			shortMessage (mailList)
			sys.exit(1)
			
		try:
			os.chmod(t, 0774)
		except Exception, e:
			mailList['subject'] = mailList['message'] = message = "photoProcess - unable to change posix on a file"
			shortMessage (mailList)
			sys.exit(1)
		
		imageTIFF = t.rstrip()
		#lg.info ("  image:  "+ imageTIFF)
		
		#test TIFF name
		oldTIFF = os.path.basename(imageTIFF) 
		dirPath = os.path.dirname(imageTIFF) 
		newTIFF = oldTIFF
		newTIFF = newTIFF.replace(" ", "")
		newTIFF = newTIFF.replace("R_", "R-")
		newTIFF = newTIFF.replace("O", "0")
		newTIFF = newTIFF.replace("--", "-")
		
		#convert L-156345.132413.tif to L-156345_132413.tif
		#replace the second to last decimal in number with underscore
		#L-156345.1231234.tif to L-156345_1231234.tif
		lg.info ("\t\tthree decimal ")
		def numReplace(matchobj):
			test = matchobj.group(0)
			if matchobj.group(0)[0] == ".":
				test = string.replace(matchobj.group(0), ".", "_", 1)
			return test	
		newTIFF = re.sub('.\d+.tif', numReplace, newTIFF)
		lg.info ("\t\t\tnewTIFF:  " + newTIFF)
		if oldTIFF != newTIFF:
			lg.info ("\t\t\toldTIFF:  " + oldTIFF + " != newTIFF:  " +newTIFF)
			newFullPath = dirPath + "/" + newTIFF
			lg.info ("\t\t\tnewFullPath:  " + newFullPath )
			os.renames (t, newFullPath)
			oldTIFF = newTIFF
			lg.info ("\t\t\tnewFullPath:  " + newFullPath )
		lg.info ("\t\thyphen ")	
		
		#replace the last hyphen in number when it is the symbolic decimal
		def decHyphenReplace(matchobj):
			test = matchobj.group(0)
			lg.info ("\t\t\ttest:  " + test)
			lg.info ("\t\t\tmatchobj.group(0)[0]:  " + matchobj.group(0)[0])
			second_index = test.find("-", test.find("-")+1)
			if matchobj.group(0)[second_index] == "-":
				stringList = list(test)
				stringList[second_index] = "_"
				test = "".join(stringList)
				lg.info ("\t\t\ttest:  " + test)
			return test	
		newTIFF = re.sub('-\d+-\d+.tif', decHyphenReplace, newTIFF)
		lg.info ("\t\t\toldTIFF:  " + oldTIFF)
		lg.info ("\t\t\tnewTIFF:  " + newTIFF)
		if oldTIFF != newTIFF:
			lg.info ("\t\t\toldTIFF:  " + oldTIFF + " != newTIFF:  " +newTIFF)
			newFullPath = dirPath + "/" + newTIFF
			lg.info ("\t\t\tnewFullPath:  " + newFullPath )
			lg.info ("\t\t\tt:  " + t )
			os.renames (t, newFullPath)	

def imageProperlyNamedOld2(s):
	retObj = funcReturn.funcReturn('imageProperlyNamedOld2')
	prog = re.compile(r"""^R-     # Raw
					  \d{4}-      # Year
					  [a-zA-Z]+-  # Prefix
					  \d{5}       # Seq
					  (_\d+)*     # optional decimal seq
					  .tif        # tif suffix""", re.X)
	rawYear = bool(prog.search(s))
	#print "rawYear:  " + str(rawYear)
	prog = re.compile(r"""^R-     # Raw
					  [a-zA-Z]+-  # Prefix
					  \d{5}       # Seq
					  (_\d+)*     # optional decimal seq
					  .tif        # tif suffix""", re.X)
	rawNoYear = bool(prog.search(s))
	#print "rawNoYear:  " + str(rawNoYear)
	prog = re.compile(r"""^\d{4}-      # Year
					  [a-zA-Z]+-       # Prefix
					  \d{5}            # Seq
					  (_\d+)*          # optional decimal seq
					  .tif             # tif suffix""", re.X)
	processedYear = bool(prog.search(s))
	#print "processedYear:  " + str(processedYear)
	prog = re.compile(r"""^[a-zA-Z]+-	# Prefix
					  \d{5}				# Seq
					  (_\d+)*			# optional decimal seq
					  .tif				# tif suffix""", re.X)
	processedNoYear = bool(prog.search(s))
	#print "processedNoYear:  " + str(processedNoYear)
	resultBool =  (processedNoYear or processedYear or rawNoYear  or rawYear)
	if resultBool == True:
		result = 0
	else:
		result = 1
	retObj.setRetVal(result)
	return retObj
				
def imageProperlyNamedOld(s):
	prog = re.compile(r"""^R-     # Raw
					  \d{4}-      # Year
					  [a-zA-Z]+-  # Prefix
					  \d{5}       # Seq
					  (_\d+)*     # optional decimal seq
					  .tif        # tif suffix""", re.X)
	rawYear = bool(prog.search(s))
	
	prog = re.compile(r"""^R-     # Raw
					  [a-zA-Z]+-  # Prefix
					  \d{5}       # Seq
					  (_\d+)*     # optional decimal seq
					  .tif        # tif suffix""", re.X)
	rawNoYear = bool(prog.search(s))
	
	prog = re.compile(r"""^\d{4}-      # Year
					  [a-zA-Z]+-       # Prefix
					  \d{5}            # Seq
					  (_\d+)*          # optional decimal seq
					  .tif             # tif suffix""", re.X)
	processedYear = bool(prog.search(s))
	
	prog = re.compile(r"""^[a-zA-Z]+-	# Prefix
					  \d{5}				# Seq
					  (_\d+)*			# optional decimal seq
					  .tif				# tif suffix""", re.X)
	processedNoYear = bool(prog.search(s))

	return (rawYear or rawNoYear or processedYear or processedNoYear )
	
def imageProperlyNamedJpgOld(s):
	prog = re.compile(r"""^R-     # Raw
					  \d{4}-      # Year
					  [a-zA-Z]+-  # Prefix
					  \d{5}       # Seq
					  (_\d+)*     # optional decimal seq
					  .jpg        # jpg suffix""", re.X)
	rawYear = bool(prog.search(s))
	
	prog = re.compile(r"""^R-     # Raw
					  [a-zA-Z]+-  # Prefix
					  \d{5}       # Seq
					  (_\d+)*     # optional decimal seq
					  .jpg        # jpg suffix""", re.X)
	rawNoYear = bool(prog.search(s))
	
	prog = re.compile(r"""^\d{4}-      # Year
					  [a-zA-Z]+-       # Prefix
					  \d{5}            # Seq
					  (_\d+)*          # optional decimal seq
					  .jpg             # jpg suffix""", re.X)
	processedYear = bool(prog.search(s))
	
	prog = re.compile(r"""^[a-zA-Z]+-  # Prefix
					  \d{5}            # Seq
					  (_\d+)*          # optional decimal seq
					  .jpg            # jpg suffix""", re.X)
	processedNoYear = bool(prog.search(s))

	return (rawYear or rawNoYear or processedYear or processedNoYear )

def imageProperlyNamedNoSuffix(s):
	prog = re.compile(r"""^R-     # Raw
					  \d{4}-      # Year
					  [a-zA-Z]+-  # Prefix
					  \d{5}       # Seq
					  (_\d+)*     # optional decimal seq""", re.X)
	rawYear = bool(prog.search(s))
	
	prog = re.compile(r"""^R-     # Raw
					  [a-zA-Z]+-  # Prefix
					  \d{5}       # Seq
					  (_\d+)*     # optional decimal seq""", re.X)
	rawNoYear = bool(prog.search(s))
	
	prog = re.compile(r"""^\d{4}-      # Year
					  [a-zA-Z]+-       # Prefix
					  \d{5}            # Seq
					  (_\d+)*          # optional decimal seq""", re.X)
	processedYear = bool(prog.search(s))
	
	prog = re.compile(r"""^[a-zA-Z]+-  # Prefix
					  \d{5}            # Seq
					  (_\d+)*          # optional decimal seq""", re.X)
	processedNoYear = bool(prog.search(s))

	return (rawYear or rawNoYear or processedYear or processedNoYear )
		
def isRaw(s):
	return bool(re.search(r'^R-',s))

def photoPartsDict(fileName):
	dict = {
	'function' : 'photoPartsDict',
	'error' : "",
	'comment' : "",
	'retVal' : 0
	}
	splitDot=fileName.split('.')
			
	splitHyphen=splitDot[0].split('-')
	
	result=isRaw(fileName)
	dict['comment']= dict['comment'] + "      isRaw:  " + str(result) + "\n"
	
	raw=""
	year=""	
	letter=""	
	seq=""
	type=""
	if isRaw(fileName):
		#year test
		if isNumber(splitHyphen[1]):
			year = splitHyphen[1]
			letter = splitHyphen[2]
			seq = splitHyphen[3]
		else:
			letter = splitHyphen[1]
			seq = splitHyphen[2]
		webname = fileName.replace("R-", "")
	else:
		#year test
		if isNumber(splitHyphen[0]):
			year = splitHyphen[0]
			letter = splitHyphen[1]
			seq = splitHyphen[2]
		else:
			letter = splitHyphen[0]
			seq = splitHyphen[1]
		webname = fileName


	if isRaw(fileName):
		type = "raw"
	else:
		type ="processed"
		
	dict['raw'] = result
	dict['year'] = year
	dict['letter'] = letter
	dict['seq'] = seq
	dict['type'] = type
	dict['noSuffix'] = splitDot[0]
	dict['webname'] = webname
	return dict

def photoPartsOld(lg, fileName):
	
	splitDot=fileName.split('.')
			
	splitHyphen=splitDot[0].split('-')
	
	result=isRaw(fileName)
	lg.info ("      isRaw:  " + str(result))
	
	raw=""
	year=""	
	letter=""	
	seq=""
	type=""
	if isRaw(fileName):
		#year test
		if isNumber(splitHyphen[1]):
			year = splitHyphen[1]
			letter = splitHyphen[2]
			seq = splitHyphen[3]
		else:
			letter = splitHyphen[1]
			seq = splitHyphen[2]
		webname = fileName.replace("R-", "")
	else:
		#year test
		if isNumber(splitHyphen[0]):
			year = splitHyphen[0]
			letter = splitHyphen[1]
			seq = splitHyphen[2]
		else:
			letter = splitHyphen[0]
			seq = splitHyphen[1]
		webname = fileName
#  	lg.info ("      raw:  "+ str(result))	
#  	lg.info ("      year:  "+ year)	
#  	lg.info ("      letter:  "+ letter)	
#  	lg.info ("      seq:  "+ seq)

	if isRaw(fileName):
		type = "source"
	else:
		type ="mastered"
	return dict([('raw', result), ('year', year), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname)])	
