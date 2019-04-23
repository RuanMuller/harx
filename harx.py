#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HAR File Extractor.

* This code is a proof of concept only and is not warranted for production use
* No support is available for this software
* This code has not been audited for security issues
* Use entirely at your own risk

Notes:

	Required Python modules::

		### python-magic module
		pip install python-magic
			or
		pip install -r requirements.txt

		Requirements for module is listed in ./requirements.txt.

	Configuration
		None
"""

#////////////////////////////////////////////////////////////////////////////////////
# HAR File Extractor
# Author: Ruan Müller
#////////////////////////////////////////////////////////////////////////////////////

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import argparse
import csv
import json
import magic
import os
import sys
import urlparse
import base64
import posixpath
import hashlib
import codecs


# -----------------------------------------------------------------------------
# Write CSV
# -----------------------------------------------------------------------------
def writeCSV(file, objects):
	"""Write CSV"""
	f = csv.writer(open(file, "wb+"))

	### write header
	f.writerow(["index", "time", "method", "mimetype", "size", "url"])

	idx = 0

	while idx != len(objects):
		f.writerow([
			idx,
			objects[idx]["time"],
			objects[idx]["method"],
			objects[idx]["mimeType"],
			objects[idx]["size"],
			objects[idx]["url"]])

		idx += 1


# -----------------------------------------------------------------------------
# Create Directory
# -----------------------------------------------------------------------------
def createDir(path):
	"""Create directory."""
	if not os.path.exists(path):
		os.makedirs(path)


# -----------------------------------------------------------------------------
# Get File Magic
# -----------------------------------------------------------------------------
def getMagic(fileName):
	"""Get file magic."""

	mime = magic.Magic(mime=True)
	mimeType = mime.from_file(fileName)

	return mimeType


# -----------------------------------------------------------------------------
# Get Object List
# -----------------------------------------------------------------------------
def getObjects(har):
	"""Generate file asset list"""

	objects = dict()
	idx = 0

	for entry in har['log']['entries']:

		method = entry['request']['method']
		mimeType = entry['response']['content']['mimeType']
		size = entry['response']['content']['size']
		if 'text' in entry['response']['content']:
			content = entry['response']['content']['text']
		url = entry['request']['url']
		time = entry['startedDateTime']

		objects[idx] = {}
		objects[idx]['time'] = time
		objects[idx]['method'] = method
		objects[idx]['mimeType'] = mimeType
		objects[idx]['content'] = content
		objects[idx]['size'] = size
		objects[idx]['url'] = url

		idx += 1

	return objects


# -----------------------------------------------------------------------------
# Print Object List
# -----------------------------------------------------------------------------
def printObjects(objects):
	"""Generate file asset list"""

	idx = 0

	while idx != len(objects):

		fileObject = "[" + str(idx).rjust(3, " ") + "] " +\
			"[" + objects[idx]['time'] + "] " +\
			"[" + objects[idx]['method'].rjust(6, " ") + "] " +\
			"[" + objects[idx]['mimeType'].rjust(30, " ") + "] " +\
			"[Size: " + str(objects[idx]['size']).rjust(8, " ") + "] " +\
			"[" + objects[idx]['url'] + "]"

		print fileObject

		idx += 1


# -----------------------------------------------------------------------------
# Get Filename From URL
# -----------------------------------------------------------------------------
def getURL(URL):
	"""Get santizied URL"""

	parsedURL = urlparse.urlparse(URL).netloc

	### remove port
	if ":" in parsedURL:
		workURL = parsedURL.split(':')
		cleanURL =  workURL[1]
		return cleanURL
	else:
		return parsedURL


# -----------------------------------------------------------------------------
# Get Filename From URL
# -----------------------------------------------------------------------------
def getFilename(URL):
	"""Get filename from URL"""

	path = urlparse.urlparse(URL).path

	workPath = path.split('/')

	filename =  workPath[-1]

	### generate filename based on url.file when no filename exists
	if filename == "":
		filename = getURL(URL) + ".file"

	return filename


# -----------------------------------------------------------------------------
# Generate MD5
# -----------------------------------------------------------------------------
def getMD5(fileName):
	"""Generate file MD5 hash."""

	hash_md5 = hashlib.md5()

	with open(fileName, "rb") as f:

		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)

	return hash_md5.hexdigest()


# -----------------------------------------------------------------------------
# Human redable file size
# -----------------------------------------------------------------------------
def getSize(fileName, suffix='B'):
	"""Returns a human readable filesize."""

	num = os.path.getsize(fileName)

	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0

	return "%.1f%s%s" % (num, 'Yi', suffix)


# -----------------------------------------------------------------------------
# Base64 Decode Data
# -----------------------------------------------------------------------------
def getB64Decode(data):
	"""Base64 Decode Data if possible."""

	try:
		result = base64.b64decode(data)
		return result
	except (TypeError, UnicodeEncodeError) as e:
	    return data


# -----------------------------------------------------------------------------
# Test if data is UTF8
# -----------------------------------------------------------------------------
def getUTF8(data):
	"""Test if data is UTF8"""

	try:
		result = base64.b64decode(data)
		return result
	except (TypeError, UnicodeEncodeError) as e:
	    return data


# -----------------------------------------------------------------------------
# Process Object
# -----------------------------------------------------------------------------
def processObject(idx, content, filename, path, numberFiles):
	"""Common Object Processing"""

	data = getB64Decode(content)

	if numberFiles:
		file = str(idx) + "-" + getFilename(filename)
	else:
		file = getFilename(filename)

	writeFile(path + file, data)
	md5 = getMD5(path + file)
	size = getSize(path + file)
	mime = getMagic(path + file)

	print "[" + str(idx).rjust(3, " ") + "] " +\
		"[" + file[0:30].rjust(30, " ") + "] " +\
		"[Size: " + size.rjust(8, " ") + "] "+\
		"[" + md5 + "] [" + mime.rjust(30, " ") + "] " +\
		"[" + objectList[idx]['url'] + "]"

	return True


# -----------------------------------------------------------------------------
# Extract File Assets
# -----------------------------------------------------------------------------
def extractObject(objectList, index, path="", numberFiles=False):
	"""Extract File Assets"""

	if path != "":
		### cross platform trailing slash fix
		if path[-1] != os.sep:
			path = path + os.sep
		createDir(path)

	if index == "all":

		idx = 0

		while idx != len(objectList):
			if 'content' in objectList[idx]:
				processObject(idx, objectList[idx]['content'], objectList[idx]['url'], path, numberFiles)
			else:
				print "[" + str(idx).rjust(3, " ") + "] No content for object found."

			idx += 1

	elif isinstance(index, int):

		idx = index

		if idx in objectList:
			if 'content' in objectList[idx]:
				processObject(idx, objectList[idx]['content'], objectList[idx]['url'], path, numberFiles)
			else:
				print "[" + str(index).rjust(3, " ") + "] No content for object found."
		else:
			print "[" + str(index).rjust(3, " ") + "] Object not found."


# -----------------------------------------------------------------------------
# Write File
# -----------------------------------------------------------------------------
def writeFile(file, data):
	"""Write data to file."""

	try:
		with codecs.open(file, "w", 'utf8') as exportFile:
			exportFile.write(data)
	except (UnicodeDecodeError) as e:
		with open(file, "w") as exportFile:
			exportFile.write(data)

	return True


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--csv', help="Save object list to [CSV]")
	parser.add_argument('-l', '--list', action='store_true', default=0, help="List objects")
	parser.add_argument('-x', '--eXtract', type=int, help="eXtract object matching index from -l output")
	parser.add_argument('-xa', '--eXtractAll', action='store_true', default=0, help="eXtract all objects")
	parser.add_argument('-d', '--directory', help="[DIRECTORY] to extract files to")
	parser.add_argument('-n', '--number', action='store_true', default=0, help="prepend output filename with index from -l output")
	parser.add_argument('har_file')
	args = parser.parse_args()


	### Read HAR file
	try:
		har = json.load(file(args.har_file, 'r'))
	except IndexError:
		sys.stderr.write("Usage: %s <file.har>\n" % (sys.argv[0]))
		sys.exit(1)
	except ValueError, e:
		sys.stderr.write("Invalid .har file: %s\n" % (str(e)))
		sys.exit(2)

	### Export Objects List to CSV
	if args.csv:
		objectList = getObjects(har)
		writeCSV(args.csv, objectList)

	### List Objects
	if args.list:
		objectList = getObjects(har)
		printObjects(objectList)

	### Extract Specific Object
	if args.eXtract:

		objectList = getObjects(har)

		if args.directory:
			extractObject(objectList, args.eXtract, args.directory, args.number)
		else:
			extractObject(objectList, args.eXtract, "", args.number)

	### Extract All Objects
	if args.eXtractAll:

		objectList = getObjects(har)

		if args.directory:
			extractObject(objectList, 'all', args.directory, args.number)
		else:
			extractObject(objectList, 'all', "", args.number)
