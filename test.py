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
		fileName = fileName.replace("R-", "")
		#year test
		if isNumber(splitHyphen[1]):
			#print "isNumber if"	
			if len(splitHyphen) == 5:
				year = splitHyphen[1]
				letter = splitHyphen[2]
				seq = splitHyphen[3]
				extra = splitHyphen[4]
				seqName="_F"+ extra+ "-"+seq
				newName ="R-LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
			else:
				year = splitHyphen[1]
				letter = splitHyphen[2]
				seq = splitHyphen[3]
				seqList=seq.split('.')
				if len(seqList) == 4:
					seqName="_F"+ seqList[1]+ "-"+seqList[0]
				else:
					seqName="-" + seq
				seqList=seq.split('_')
				#print "seq:  "  + str(seq)
				#print "seqList:  "  + str(seqList)
				if len(seqList) == 2:
					seqName="_F"+ seqList[1]+ "-"+seqList[0]
				newName ="R-LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
		else:
			#print "isNumber else"	
			letter = splitHyphen[1]
			seq = splitHyphen[2]
			seqList=seq.split('.')
			if len(seqList) == 2:
				seqName="_F"+ seqList[1]+ "-"+seqList[0]
			else:
				seqName="-" + seq
			seqList=seq.split('_')
			if len(seqList) == 2:
				seqName="_F"+ seqList[1]+ "-"+seqList[0]
			newName ="R-LRC-B701_P" + str(seqName) + "." + splitDot[1]
		webname = newName.replace(".tif", ".jpg")	
		type = "raw"

	else:
		#year test
		if isNumber(splitHyphen[0]):
			year = splitHyphen[0]
			letter = splitHyphen[1]
			seq = splitHyphen[2]
			seqList=seq.split('.')
			#print "year:  " + str(year)
			#print "seq:  " + str(seq)
			if len(seqList) == 2:
				seqName="_F"+ seqList[1]+ "-"+seqList[0]
			else:
				seqName="-" + seq
			seqList=seq.split('_')
			#print seqList
			if len(seqList) == 2:
				seqName="_F"+ seqList[1]+ "-"+seqList[0]
			newName ="LRC-" + str(year) + "-B701_P" + str(seqName) + "." + splitDot[1]
		else:
			letter = splitHyphen[0]
			seq = splitHyphen[1]
			seqList=seq.split('.')
			if len(seqList) == 2:
				seqName="_F"+ seqList[1]+ "-"+seqList[0]
			else:
				seqName="-" + seq
			seqList=seq.split('_')
			if len(seqList) == 2:
				seqName="_F"+ seqList[1]+ "-"+seqList[0]
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

def photoParts(fileName, type = "tif"):
	retObj = funcReturn.funcReturn('photoParts')
	
	if type == "tif":
		retObj2 = imageProperlyNamed(fileName)
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
		year=""	
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
			year = int(splitHyphen[2])
			meta = splitHyphen[3]
			seq = splitHyphen[4]
			webname = fileName.replace("R-", "")
		else:
			#print "mastered"
			if splitHyphen[0] == "LRC":    #LRC test
				center = splitHyphen[0]
				year = int(splitHyphen[1])
				meta = splitHyphen[2]
				seq = splitHyphen[3]
			webname = fileName

		if isRaw(fileName):
			type = "source"
		else:
			type ="mastered"
		result =  dict([('raw', result), ('center', center), ('meta', meta), ('year', year), ('letter', letter), ('seq', seq), ('type', type), ('noSuffix', splitDot[0]), ('webname', webname)])	
		retObj.setResult(result)
		retObj.setRetVal(0)
	return retObj

def imageProperlyNamedJpg(s):
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

def imageProperlyNamed(s):
	#^LRC-\d{4}-B701_[PAVG][0-9a-zA-Z_]*-\d{5}\.tif
	retObj = funcReturn.funcReturn('imageProperlyNamed')
	prog = re.compile(r"""^R-		# Raw
					  LRC-				# LRC
					  \d{4}-			# Year
					  B701_				# org
					  [PAVG]			# dept
					  [0-9a-zA-Z_]*		# metadata
					  -\d{5}			# Seq
					  \.tif				# tif suffix""", re.X)
	source = bool(prog.search(s))
	#print source
	prog = re.compile(r"""^LRC-			# LRC
					  \d{4}-			# Year
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
		
def photoInsert (lg, mailList, conn, name, cd):
	lg.setPrefix ("photoInsert")
	lg.info ("        --name  " + name)
	photo={}
	photo=photoParts(lg, name)
	type=photo['type'].strip()
	raw=photo['raw']
	alpha=photo['letter']
	retObj = prefix (conn)
	result = retObj.getResult()
	letter=result[alpha]
	year=photo['year']	
	if year == "":
		year = "noYear"
	seq=photo['seq']
	type=photo['type']
	noSuffix=photo['noSuffix']
	webname=photo['webname']
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
		retObj = imageProperlyNamedJpg(j)
		result = retObj.getRetVal()
		if result == 0 :
			lg.info ("      photo is properly named")	
			lg.info ("      j:  " + j)
			retObj=photoParts(j, "jpg")
			
			if retObj.getRetVal() == 1:
				lg.info ("      problem with function photoParts in photoMysql function")
				mailList['subject'] = "problem with function photoParts in photoMysql function"
				message = "problem with function photoParts in photoMysql function"
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
					lg.info ("      update database")
					photoUpdate (lg, mailList, conn, j, cdName)
				else:
					lg.info ("      repoCheck:  " + retDict['result'])
			else:
				photoInsert (lg, mailList, conn, j, cdName)
				lg.info ("      insert database")
		else:
			lg.warn ("      photo is not properly named")	
			
  	c = conn.cursor()
  	c.close()

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
	#print retDict
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
		fileToCheck = o +  "/" + year +  "/R-" + modName + ".tif"
		comment = comment + "fileToCheck: " + fileToCheck + " \n"
		if fileExist(fileToCheck):
			comment = comment + "original exists \n"
			dict['checkOrig'] =  1
	
	for m in modified:	
		fileToCheck = m  + "/" + year +  "/" + modName + ".tif"
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
		if imageProperlyNamed(base):
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

	lg.setPrefix ("photoArchive")
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
		
		
		if imageProperlyNamed(base):
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
		
		if imageProperlyNamed(base):
			lg.info ("      photo is properly named:  ")				
			jpgBase = base.replace(".tif", ".jpg")
			jpgList.append(jpgBase)
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