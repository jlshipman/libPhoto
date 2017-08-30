import sys
sys.path.append('lib')
sys.path.append('libPhoto')
import listFunctions
import directory
import fileFunctions
import photoFunctions
import funcReturn

def findImagesMetadata (
	repositorySearchList, #listing of directories to search for a images
	resultFile, #listing of images found within a directories with full path with metadata
	suffix,  #images with suffix to search for
	sep  #separator
	):
	retObj = funcReturn.funcReturn('findImagesMetadata')
	dirList=listFunctions.listFromFile(repositorySearchList)
	bigList = []
	for d in dirList:
		searchDict = directory.listFilesSuffixNoDups(d, suffix)
		metaDataList = searchDict['resultListMetaData']
		if len(metaDataList) > 0:
			retObj.setRetVal(0)
			retObj.setResult(metaDataList)
			#if this is the non-first iteration update or add to dictionary
			if len(metaDataList) > 0:
				bigList = bigList + metaDataList
			#otherwise copy dictionary to new dictionary
			else:		
				bigList=metaDataList
	resDict=fileFunctions.listofListToFile(bigList, resultFile, sep)
	return retObj
	
	
def photoImagesReproLocation (repositorySearchListNoSuffixPrefix, resposDict, stage):	
	dict = {
	'function' : 'photoImagesReproLocation',
	'error' : "",
	'comment' : "",
	'retVal' : 0
	}
	searchList = repositorySearchListNoSuffixPrefix
	imagesNotFound=[]
	imagesFound=[]
	imagesImproperName=[]
	for t in searchList:
		if imageProperlyNamedNoSuffix(t):
			photo={}
			photo=photoPartsDict(t)
			if photo['year'] != "":
				year=int(photo['year'])
			else:
				year=""
			letter=photo['letter']	
			seq=photo['seq']
			type=photo['type']
			noSuffix=photo['noSuffix']
			webname=photo['webname']
			tifName=noSuffix+".tif"
		
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
			unprocessed=resposDict['unprocessed']
			newLocalFullPath=""
			if year!="":
				#create processed year location
				procYearLocation=reposProcess  +  str(year) + "/" + tifName	
				#create raw year location
				dict["comment"] = dict["comment"] + (str(year)  + " > " + str(repos1Lower) + " and " + str(year)  + " <= " + str(repos1Upper) ) + "/n"
				dict["comment"] = dict["comment"] + (str(year)  + " => " + str(repos2Lower) + " and " + str(year)  + " <= " + str(repos2Upper) )	+ "/n"
				if (year > repos1Lower) and (year <= repos1Upper):
					rawYearLocation=repos1 +  str(year) + "/R-" + tifName	
				if (year >= repos2Lower) and (year <= repos2Upper):
					rawYearLocation=repos2  + str(year) + "/R-" + tifName	
				dict["comment"] = dict["comment"] + "        rawYearLocation:  "+ rawYearLocation + "/n" 					
						
				if fileExist(procYearLocation):
					dict["comment"] = dict["comment"] + "          processed file exists" + "/n"
					imageFile = unprocessed + "/" +  tifName
					dict["comment"] = dict["comment"] + "          imageFile" + imageFile + "/n"
					if not (fileExist(imageFile)):
						try:
							if stage == "production":
								copyfile(procYearLocation, imageFile)
							imagesFound.append(procYearLocation)
						except Exception:
							dict['error']="unable to copy file: " + imageFile + "/n"
							dict['retVal']=1
							return dict
				else:
					if fileExist(rawYearLocation):
						dict["comment"] = dict["comment"] + "         raw file exists" + "/n"
						imageFile = unprocessed + "/R-" +  tifName
						dict["comment"] = dict["comment"] + "          imageFile: " +  imageFile + "/n"
						if not (fileExist(imageFile)):
							try:
								if stage == "production":
									copyfile(rawYearLocation, imageFile)
								imagesFound.append(rawYearLocation)
							except Exception:
								dict['error']="unable to copy file: " + imageFile + "/n"
								dict['retVal']=1
								return dict
					else:
						dict["comment"] = dict["comment"] + imageFile + " does not exists /n"
						imagesNotFound.append(tifName)
					
			else:
				#create processed no year location
				procNoYearLocation=noYearProcess + "noYear/" + tifName
				dict["comment"] = dict["comment"] + "          procNoYearLocation: " +  procNoYearLocation + "/n"
				
				#create raw no year location
				rawNoYearLocation=noYearRaw + "noYear/R-" + tifName
				dict["comment"] = dict["comment"] + "          rawNoYearLocation: " +  rawNoYearLocation + "/n"
			
				if fileExist(procNoYearLocation):
					dict["comment"] = dict["comment"] + "          processed file exists" + "/n"
					imageFile = unprocessed + "/" +  tifName
					dict["comment"] = dict["comment"] + "          imageFile" + imageFile + "/n"
					if not (fileExist(imageFile)):
						try:
							if stage == "production":
								copyfile(procNoYearLocation, imageFile)
							imagesFound.append(procNoYearLocation)						
						except Exception:
							dict['error']="unable to copy file: " + imageFile + "/n"
							dict['retVal']=1
							return dict						
				else:				
					if fileExist(rawNoYearLocation):
						dict["comment"] = dict["comment"] + "          raw file exists /n"
						imageFile = unprocessed + "/R-" +  tifName
						dict["comment"] = dict["comment"] + "          imageFile" + imageFile + "/n"
						if not (fileExist(imageFile)):
							try:
								if stage == "production":
									copyfile(rawNoYearLocation, imageFile)
								imagesFound.append(rawNoYearLocation)
							except Exception:
								dict['error']="unable to copy file: " + imageFile + "/n"
								dict['retVal']=1
								return dict
					else:
						#create list of files not found
						dict["comment"] = dict["comment"] + tifName + " does not exist /n"
						imagesNotFound.append(tifName)
		else:
			dict["comment"] = dict["comment"] + tifName + " photo is not properly named: " + t + "/n"
			imagesImproperName.append(t)
	dict ['listImagesNotFound'] = imagesNotFound
	dict ['listImagesFound'] = imagesFound
	dict ['listimagesImproperName'] = imagesImproperName
	return dict

def photoImagesRepos (
	repositorySearchList, #listing of directories to search within a file
	repositoryImageListFile, #listing of images found within a file
	repositoryImageListFileFullPath, #listing of images found within a file with full path
	suffix  #images with suffix to search for
	):
	retDict = {'function' : 'photoImagesRepos'}
	comment=""
	searchList = fileFunctions.listFromFile(repositorySearchList)
	fullListImageRepository = []
	mergedList = []
	mergedListFull = []
	for item in searchList:
		print "item:  " + item
		dict = directory.listFilesSuffixNoDups(item.strip(), suffix)
		listing = dict['resultList']
		listingFull = dict['resultListFullPath']
		count = len(listing)
		mergedList = mergedList + listing
		mergedListFull = mergedListFull + listingFull
		old = comment
		comment =  old  + "count of " + str(item) + " :  " + str(count) + "\n"
	resultList = sorted(mergedList)
	resultListFull = sorted(mergedListFull)
	countMerge = len(resultList)
	countMergeFull = len(resultListFull)
	retDict['count']=countMerge
	retDict['countFull']=countMergeFull
	old = comment
	comment = old + "count of list merged:  " + str(countMerge) +"\n"
	retDict['resultList']=resultList
	retDict['resultListFull']=resultListFull
	retDict['comment']=comment
	fileFunctions.listToFile(resultList, repositoryImageListFile)
	fileFunctions.listToFile(resultListFull, repositoryImageListFileFullPath)
	return retDict
	
def photoImagesReposLoL (
	repositorySearchList, #listing of directories to search within a file
	repositoryImageListFile, #listing of images found within a file
	repositoryImageListFileFullPath, #listing of images found within a file with full path
	repositoryImageListFileBoth, #listing of images found within a file with full path
	repositoryImageListFileMeta, #listing of images found within a file with full path with metadata
	suffix,  #images with suffix to search for
	sep  #separator
	):
	retDict = {'function' : 'photoImagesReposLoL'}
	comment=""
	searchList = fileFunctions.listFromFile(repositorySearchList)
	fullListImageRepository = []
	mergedList = []
	mergedListFull = []
	mergedListBoth = []
	mergedListMeta = []
	for item in searchList:
		print "item:  " + item
		dict = directory.listFilesSuffixNoDups(item.strip(), suffix)
		listing = dict['resultList']
		listingFull = dict['resultListFullPath']
		listingBoth = dict['resultListBoth']
		listingMeta = dict['resultListMetaData']
		count = len(listing)
		mergedList = mergedList + listing
		mergedListFull = mergedListFull + listingFull
		mergedListBoth = mergedListBoth + listingBoth
		mergedListMeta = mergedListMeta + listingMeta
		old = comment
		comment =  old  + "count of " + str(item) + " :  " + str(count) + "\n"
	resultList = sorted(mergedList)
	resultListFull = sorted(mergedListFull)
	resultListBoth = sorted(mergedListBoth)
	resultListMeta = sorted(mergedListMeta)
	countMerge = len(resultList)
	countMergeFull = len(resultListFull)
	countMergeBoth = len(resultListBoth)
	countMergeMeta = len(resultListMeta)
	retDict['count']=countMerge
	retDict['countFull']=countMergeFull
	retDict['countBoth']=countMergeBoth
	retDict['countMeta']=countMergeMeta
	old = comment
	comment = old + "count of list merged:  " + str(countMerge) +"\n"
	retDict['resultList']=resultList
	retDict['resultListFull']=resultListFull
	retDict['resultListBoth']=resultListBoth
	retDict['resultListMeta']=resultListMeta
	retDict['comment']=comment
	fileFunctions.listToFile(resultList, repositoryImageListFile)
	fileFunctions.listToFile(resultListFull, repositoryImageListFileFullPath)
	fileFunctions.listofListToFile(resultListBoth, repositoryImageListFileBoth, sep)
	fileFunctions.listofListToFile(resultListMeta, repositoryImageListFileMeta, sep)
 	return retDict
 	
def photoImagesReposLoL (
	repositorySearchList, #listing of directories to search within a file
	repositoryImageListFile, #listing of images found within a file
	repositoryImageListFileFullPath, #listing of images found within a file with full path
	repositoryImageListFileBoth, #listing of images found within a file with full path
	repositoryImageListFileMeta, #listing of images found within a file with full path with metadata
	suffix,  #images with suffix to search for
	sep  #separator
	):
	retDict = {'function' : 'photoImagesReposLoL'}
	comment=""
	searchList = fileFunctions.listFromFile(repositorySearchList)
	fullListImageRepository = []
	mergedList = []
	mergedListFull = []
	mergedListBoth = []
	mergedListMeta = []
	for item in searchList:
		print "item:  " + item
		dict = directory.listFilesSuffixNoDups(item.strip(), suffix)
		listing = dict['resultList']
		listingFull = dict['resultListFullPath']
		listingBoth = dict['resultListBoth']
		listingMeta = dict['resultListMetaData']
		count = len(listing)
		mergedList = mergedList + listing
		mergedListFull = mergedListFull + listingFull
		mergedListBoth = mergedListBoth + listingBoth
		mergedListMeta = mergedListMeta + listingMeta
		old = comment
		comment =  old  + "count of " + str(item) + " :  " + str(count) + "\n"
	resultList = sorted(mergedList)
	resultListFull = sorted(mergedListFull)
	resultListBoth = sorted(mergedListBoth)
	resultListMeta = sorted(mergedListMeta)
	countMerge = len(resultList)
	countMergeFull = len(resultListFull)
	countMergeBoth = len(resultListBoth)
	countMergeMeta = len(resultListMeta)
	retDict['count']=countMerge
	retDict['countFull']=countMergeFull
	retDict['countBoth']=countMergeBoth
	retDict['countMeta']=countMergeMeta
	old = comment
	comment = old + "count of list merged:  " + str(countMerge) +"\n"
	retDict['resultList']=resultList
	retDict['resultListFull']=resultListFull
	retDict['resultListBoth']=resultListBoth
	retDict['resultListMeta']=resultListMeta
	retDict['comment']=comment
	fileFunctions.listToFile(resultList, repositoryImageListFile)
	fileFunctions.listToFile(resultListFull, repositoryImageListFileFullPath)
	fileFunctions.listofListToFile(resultListBoth, repositoryImageListFileBoth, sep)
	fileFunctions.listofListToFile(resultListMeta, repositoryImageListFileMeta, sep)
 	return retDict
	retDict = {'function' : 'photoImagesReposLoL'}
	comment=""
	searchList = fileFunctions.listFromFile(repositorySearchList)
	fullListImageRepository = []
	mergedList = []
	mergedListFull = []
	mergedListBoth = []
	mergedListMeta = []
	for item in searchList:
		print "item:  " + item
		dict = directory.listFilesSuffixNoDups(item.strip(), suffix)
		listing = dict['resultList']
		listingFull = dict['resultListFullPath']
		listingBoth = dict['resultListBoth']
		listingMeta = dict['resultListMetaData']
		count = len(listing)
		mergedList = mergedList + listing
		mergedListFull = mergedListFull + listingFull
		mergedListBoth = mergedListBoth + listingBoth
		mergedListMeta = mergedListMeta + listingMeta
		old = comment
		comment =  old  + "count of " + str(item) + " :  " + str(count) + "\n"
	resultList = sorted(mergedList)
	resultListFull = sorted(mergedListFull)
	resultListBoth = sorted(mergedListBoth)
	resultListMeta = sorted(mergedListMeta)
	countMerge = len(resultList)
	countMergeFull = len(resultListFull)
	countMergeBoth = len(resultListBoth)
	countMergeMeta = len(resultListMeta)
	retDict['count']=countMerge
	retDict['countFull']=countMergeFull
	retDict['countBoth']=countMergeBoth
	retDict['countMeta']=countMergeMeta
	old = comment
	comment = old + "count of list merged:  " + str(countMerge) +"\n"
	retDict['resultList']=resultList
	retDict['resultListFull']=resultListFull
	retDict['resultListBoth']=resultListBoth
	retDict['resultListMeta']=resultListMeta
	retDict['comment']=comment
	fileFunctions.listToFile(resultList, repositoryImageListFile)
	fileFunctions.listToFile(resultListFull, repositoryImageListFileFullPath)
	fileFunctions.listofListToFile(resultListBoth, repositoryImageListFileBoth, sep)
	fileFunctions.listofListToFile(resultListMeta, repositoryImageListFileMeta, sep)
 	return retDict