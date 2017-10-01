from apiclient.discovery import build
import json
import sys 		#to take command line args
import re
import pprint
from collections import Counter

def removeStopWords(tokenList):
	with open('stopWords.txt') as f:
		stopList = f.read().splitlines()
	return [token for token in tokenList if token not in stopList]



def mostCommon(tokenList):
	freqs = Counter(tokenList)
	results = [freqs.most_common(2)[0][0], freqs.most_common(2)[1][0]]
	return results

def main():
	service = build("customsearch", "v1", developerKey="AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs")

	res = service.cse().list(
		q='cow',
		cx='007382945159574133954:avqdfgjg420',
		).execute()

	title = res['items'][0]['htmlTitle'].lower()
	summary = res['items'][0]['htmlSnippet'].lower()

	titleTokens = removeStopWords(re.findall(r'\b[a-z]{3,20}\b', title))
	summaryTokens = removeStopWords(re.findall(r'\b[a-z]{3,20}\b', summary))
	print mostCommon(summaryTokens)
#	print titleTokens
#	pprint.pprint(res['items'][0]['htmlTitle'])
#	pprint.pprint(res['items'][0]['formattedUrl'])
#	pprint.pprint(res['items'][0]['htmlSnippet'])
#	pprint.pprint(res['items'])




if __name__ == '__main__': main()