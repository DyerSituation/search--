from apiclient.discovery import build
import json
import sys 		#to take command line args
import re
import pprint

def removeStopWords(tokenList):
	with open('stopWords.txt') as f:
		stopList = f.read().splitlines()
	return [token for token in tokenList if token not in stopList]



def findFrequency(alist):
	alist = ['chicken']
	return alist

def sendQuery(service, q):
	res = service.cse().list(
		q=q,
		cx='007382945159574133954:avqdfgjg420',
		).execute()
	return res

def main():
	service = build("customsearch", "v1", developerKey="AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs")
	
	goalP = float(sys.argv[2]) * 10
	p = -1
	q = sys.argv[3]
	res = sendQuery(service, q)
	while p < goalP and p != 0:
		print(q)
		titles = []
		snippets = []
		for page in res['items']:
			tit = page['htmlTitle'].encode("utf-8")
			snip = page['htmlSnippet'].encode("utf-8")
			print(tit + "\n" + snip)
			mark = raw_input('relevant, y/n?')
			if mark == 'y':
				titles.append(tit.lower)
				snippets.append(snip.lower)

		p = len(titles)

		newWords = findFrequency(titles)
		for word in newWords:
			q = q + " " + word

		res = sendQuery(service, q)
	print("done")

if __name__ == '__main__': main()