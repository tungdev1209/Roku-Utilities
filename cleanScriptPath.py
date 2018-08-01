import os
import fnmatch
import argparse
import re

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True,
	help="path to input dir")
ap.add_argument("-f", "--filePath", required=False,
	help="path to input file")
ap.add_argument("-m", "--modulePath", required=False,
	help="path to input file")
args = vars(ap.parse_args())

mainPath = args["path"]
filePathRoot = "/" + mainPath.split("/")[-1]
targetXmlFilePath = args["filePath"]
targetModulePath = args["modulePath"]

print "PATH:", mainPath, "- PROJECT DIR:", filePathRoot

xmlFileMatches = []
brsFileMatches = {}

# Get all xml files that need fixing script path
if targetXmlFilePath == None and targetModulePath == None:
	for root, dirnames, filenames in os.walk(mainPath):
		for filename in fnmatch.filter(filenames, "*.xml"):
			xmlFileMatches.append(os.path.join(root, filename))
else:
	if targetXmlFilePath != None:
		xmlFileMatches.append(targetXmlFilePath)
	if targetModulePath != None:
		for root, dirnames, filenames in os.walk(targetModulePath):
			for filename in fnmatch.filter(filenames, "*.xml"):
				xmlFileMatches.append(os.path.join(root, filename))

# Get all brs files
for root, dirnames, filenames in os.walk(mainPath):
	for filename in fnmatch.filter(filenames, "*.brs"):
		brsFileMatches[filename] = os.path.join(root, filename)

def foundSymbolInline(symbol, line):
	return line.find(symbol) != -1

def cleanPathInFile(filePath):
	print ">>>", filePath.split(mainPath)[-1]
	file = open(filePath, "r+")
	isModify = 0
	fileContent = ""
	findingEndSymbol = False
	scriptElementContent = ""
	for line in file:
		if foundSymbolInline("<script ", line): # is a script element
			if not foundSymbolInline("/>", line):
				findingEndSymbol = True
				scriptElementContent += line
				continue
		elif not findingEndSymbol:
			fileContent += line
			continue

		scriptElementContent += line
		if not foundSymbolInline("/>", line):
			continue

		findingEndSymbol = False

		brsIndex = scriptElementContent.find(".brs")
		pkgIndex = scriptElementContent.find("pkg:/")

		scriptName = scriptElementContent[pkgIndex + 4: brsIndex + 4].split("/")[-1]

		# print "scriptName:", scriptName

		newLine = ""
		if scriptName in brsFileMatches:
			inProjUriPath = brsFileMatches[scriptName].split(mainPath)[1]
			newLine = scriptElementContent[: pkgIndex + 4] + inProjUriPath + scriptElementContent[brsIndex + 4:]
		else:
			print "+++ file not found:", scriptName
			
		if scriptElementContent != newLine and newLine != "":
			print "--- fixing path for:", scriptName
			scriptElementContent = newLine
			isModify = 1

		fileContent += scriptElementContent
		scriptElementContent = ""

	if isModify == 1:
		file.seek(0)
		file.truncate()
		file.write(fileContent)
		print "<<< fixed"

	file.close()

for xmlFile in xmlFileMatches:
	cleanPathInFile(xmlFile)
