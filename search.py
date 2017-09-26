from apiclient.discovery import build
import json
import sys 		#to take command line args

import pprint

service = build("customsearch", "v1", developerKey="AIzaSyBbGfil_xv2ICSW4xjT5RYY92l96nahFEs")

res = service.cse().list(
	q='cow',
	cx='007382945159574133954:avqdfgjg420',
	).execute()


pprint.pprint(res['items'][0]['htmlTitle'])
pprint.pprint(res['items'][0]['formattedUrl'])
pprint.pprint(res['items'][0]['htmlSnippet'])