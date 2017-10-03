from apiclient.discovery import build
import json
import sys 		#to take command line args
import re
import pprint
from collections import Counter

def parseWords(string):

def removeStopWords(tokenList):
	with open('stopWords.txt') as f:
		stopList = f.read().splitlines()
	return [token for token in tokenList if token not in stopList]

def mostCommon(tokenList):
	freqs = Counter(tokenList)
	results = [freqs.most_common(2)[0][0], freqs.most_common(2)[1][0]]
	return results


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
	while p < goalP and p != 0:
		res = sendQuery(service, q)
		print("new query: \n")
		print("\n" + q + "\n")
		titles = []
		snippets = []
		for page in res['items']:
			tit = page['htmlTitle']
			snip = page['htmlSnippet']
			print(tit + "\n" + snip)
			mark = raw_input('relevant, y/n?')
			if mark == 'y':
				titles.append(parseWords(tit.lower()))
				snippets.append(parseWords(snip.lower()))

		p = len(titles)
		print("All titles: ")
		print ( titles)
		newWords = mostCommon(titles)
		print ("new words: ") 
		print (newWords)
		for word in newWords:
			q = q + " " + word

	print("done")

if __name__ == '__main__': main()
