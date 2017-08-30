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
testAmount=amountTif
#testAmount=16
amountJpg=7	
print repositorySearchListFile
repositoryImageListFile=curDir+"/TEMP/repositoryImageListFile.txt"
repositoryImageListFileFullPath=curDir+"/TEMP/repositoryImageListFileFullPath.txt"
TEMP=curDir + "/TEMP"
folder1=curDir + "/TEMP/folder1"
folder2=curDir + "/TEMP/folder2"
import photoRepo
import fileFunctions


class TestPhotoRepo(unittest.TestCase):
 	print "Tests for `TestPhotoRepo.py`."
 	
	def setUp(self):
		base="testing"			
		suffixTif=".tif"			
		suffixJpg=".jpg"
		#dirToSearch="/Users/admin/Desktop/201  21204\n/Users/admin/Desktop/201  21205"
		dirToSearch=TEMP
		#os.unlink(repositorySearchListFile)
		fileFunctions.writeToFile( dirToSearch, repositorySearchListFile)
		retDict=fileFunctions.createFiles(folder1, amountTif, base, suffixTif)
		retDict=fileFunctions.createFiles(folder2, amountJpg, base, suffixJpg)
		retDict=fileFunctions.createFiles(folder2, amountTif, base, suffixTif)
 
 	def testPhotoImagesRepos(self):
 		suffix="tif"
 		dict=photoRepo.photoImagesRepos(repositorySearchListFile, repositoryImageListFile, repositoryImageListFileFullPath, suffix)
 		self.assertEqual( dict['count'] , testAmount )
 		print dict['comment']
 		
 	def testPhotoImagesReposWithdup(self):
 		suffix="tif"
 		dict=photoRepo.photoImagesRepos(repositorySearchListFile, repositoryImageListFile, repositoryImageListFileFullPath, suffix)
 		self.assertEqual( dict['count'] , testAmount )
 		print dict['comment']
 				
	def tearDown(self):
		#pass
		fileFunctions.deleteFiles(folder1,".tif")
		fileFunctions.deleteFiles(folder1,".jpg")
		fileFunctions.deleteFiles(folder2,".tif")
		fileFunctions.deleteFiles(folder2,".jpg")
		
if __name__ == '__main__':
    unittest.main()
 