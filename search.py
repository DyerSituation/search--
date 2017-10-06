from apiclient.discovery import build
import json
import sys 		#to take command line args
import re
from itertools import permutations
import pprint
from collections import Counter
import operator

#removes html tags, and special characters. Splits on spaces and tabs
def parseWords(string):
	htmlClnr = re.compile('<.*?>')
	string = re.sub(htmlClnr, '', string)
	string = re.sub("[^a-zA-Z 	]+", "", string) #does this work?
	return string.split()

#takes in file with stopwords, removes them from list
def removeStopWords(tokenList):
	with open('stopWords.txt') as f:
		stopList = f.read().splitlines()
	return [token for token in tokenList if token not in stopList]

#returns most common if not in query already
def mostCommon(tokenList, queryList):
	uniqueList = [token for token in tokenList if token not in queryList]
	freqs = Counter(uniqueList)
	results = [freqs.most_common(2)[0][0], freqs.most_common(2)[1][0]]
	return results

#takes in list of words and q. for each pair of words in q
def reorder(q, wordsList):
	wordPairs = permutations(q.split(),2)
	wordsString = ' '.join(wordsList)
	newQ = []
	freqs = {}
	for pair in wordPairs:
		pairString = ' '.join(pair)
		if pairString in wordsString:
			freqs[pair] = wordsString.count(pairString)

	sortedPairs = sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)

	for pair in sortedPairs:
		if pair[0][0] not in newQ and pair[0][1] not in newQ: 
				newQ.append(pair[0][0])
				newQ.append(pair[0][1])

	for word in q.split():
		if word not in newQ:
			newQ.append(word)
	return ' '.join(newQ)

def sendQuery(service, q):
	res = service.cse().list(
		q=q,
		cx='007382945159574133954:avqdfgjg420',
		).execute()
	return res

def main():
	clientKey = 'AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs'
	engineKey = '007382945159574133954:avqdfgjg420'
	q = sys.argv[3]
	precision = sys.argv[2]
	print ("Parameters:\nClient key = {}\nEnginekey = {}\nQuery = {}\nprecision = {}"
			.format(clientKey, engineKey, q, precision))
	service = build("customsearch", "v1", developerKey="AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs")
	
	goalP = float(sys.argv[2]) * 10
	p = -1
	q = sys.argv[3]
	queryList = []
	queryList.extend(q.split())
	while p < goalP and p != 0:
		res = sendQuery(service, q)
		if 'items' not in res:
			print "no response"
			sys.exit()
		if len(res['items']) < 10:
			print "too few results"
			sys.exit()
		print("============================================")
		print("Google search results:")
		print("new query: \n")
		print("\n" + q + "\n")
		titles = []
		snippets = []
		p = 0
		print("res[items] size: \n")
		
		for page in res['items']:
			tit = page['htmlTitle']
			snip = page['htmlSnippet']
			url = page['displayLink']
			print(url)
			print("\n" + tit + "\n" + snip + "\n")
			mark = raw_input('relevant, y/n?\n')
			if mark.lower() == 'y':
				titles.extend(removeStopWords(parseWords(tit.lower())))
				snippets.extend(removeStopWords(parseWords(snip.lower())))
				p += 1
		if p == 0:
			print "no results"
			sys.exit()
		print("All titles: ")
		print (titles)
		newWords = mostCommon(titles + snippets, queryList)
		print ("new words: ") 
		print (newWords)
		print("queryList: ")
		print(queryList)
		for word in newWords:
			queryList.append(word)
			q = q + " " + str(word)
		q = reorder(q, titles + snippets)
		print("next loop\n")

	print("done")

if __name__ == '__main__': main()
