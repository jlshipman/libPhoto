#!/usr/bin/python	
import unittest
import os, sys

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
print curDir

ret=curDir.split("/")
ret.pop()
ret.pop()
scriptDir=ret.pop()

sys.path.append("/scripts/"+scriptDir+"/lib")
sys.path.append("/scripts/"+scriptDir+"/libPhoto")
sys.path.append("/scripts/"+scriptDir+"/libPhoto/unitTests")
threeDecimalFile = curDir+"/TEMP/threeDecimal.txt"
threeDecimalItem=curDir+"/TEMP/1981-L-12345.000.tif"
testFile=curDir+"/TEMP/1981-L-12345.000.tif"
testFile2=curDir+"/TEMP/1981-L-12345.000.jpg"
repositorySearchListFile=curDir+"/TEMP/repositorySearchListFile.txt"
amountTif=5	
#testAmount=amountTif+1
testAmount=16
amountJpg=7	
print repositorySearchListFile
repositoryImageListFile=curDir+"/TEMP/repositoryImageListFile.txt"
TEMP=curDir + "/TEMP"
import photoFunctions
from log import *
import fileFunctions


class TestPhotoFunc(unittest.TestCase):
 	print "Tests for `TestPhotoFunc.py`."
 	
	def setUp(self):
		base="testing"			
		suffixTif=".tif"			
		suffixJpg=".jpg"
		dirToSearch="/Users/admin/Desktop/201  21204\n/Users/admin/Desktop/201  21205"
		#dirToSearch=TEMP
		#os.unlink(repositorySearchListFile)
		fileFunctions.writeToFile( dirToSearch, repositorySearchListFile)
		retDict=fileFunctions.createFiles(TEMP, amountTif, base, suffixTif)
		retDict=fileFunctions.createFiles(TEMP, amountJpg, base, suffixJpg)
		fileFunctions.writeToFile( threeDecimalItem, threeDecimalFile)
		fileFunctions.fileCreate(testFile)
		fileFunctions.fileCreate(testFile2)
 
 	def testPhotoImagesRepos(self):
 		suffix="tif"
 		dict=photoFunctions.photoImagesRepos(repositorySearchListFile, repositoryImageListFile, suffix)
 		self.assertEqual( dict['count'] , testAmount )
 		print dict['comment']
 		
	def testPhotoFileModReturn(self):
		l=log()
		prefix="test"
		l.setData(prefix, "myLogger")
		knownAnswer="1981-L-12345_000.tif"
		retDic=photoFunctions.photoFileModReturn (l, threeDecimalFile)
		newTIFF=retDic['newTIFF']
 		print "_"+newTIFF+"_"
		error=retDic['error']	
		print "_"+error+"_"
		self.assertEqual( newTIFF , knownAnswer )
		
	def tearDown(self):
		#pass
		fileFunctions.deleteFiles(TEMP,".tif")
		fileFunctions.deleteFiles(TEMP,".jpg")
		
if __name__ == '__main__':
    unittest.main()
 