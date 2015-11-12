import sys, os, os.path, time
import json
import re
import twitterAccess as tw
from TwitterAPI import TwitterAPI

numTweets = 1000
trackTweets = ['Fallout4', 'LeagueofLegends,lolesports', 'Football Manager', 'FIFA16,FIFA', "Assasin'sCreedSyndicate", 'GTAV,GTA5', 'ChibiRobo',\
'NBALive', 'PlantsVSZombies', 'DarkSouls2,DarkSoulsII', 'DiabloIII,Diablo3', 'Destiny', 'Witcher3', 'RideToHellRetribution', 'Hypervoid', 'Borderlands',\
'CallofDutyBlackOps3', 'TonyHawkProSkater5', 'Minecraft', 'Skyrim', 'LegendOfZelda', 'Halo5', 'Starcraft2,StarcraftII', 'CounterStrike', 'SonictheHedgehog']

gtaFile = './tweets/train/gta5Train.json'
csFile = './tweets/train/counterstrikeTrain.json'
skyrimFile = './tweets/train/skyrimTrain.json'
rocketFile = './tweets/train/rocketleagueTrain.json'
witcherFile = './tweets/train/witcher3Train.json'
troveFile = './tweets/train/troveTrain.json'

gtaTestFile = './tweets/test/gta5Test.json'
csTestFile = './tweets/test/counterstrikeTest.json'
skyrimTestFile = './tweets/test/skyrimTest.json'
rocketTestFile = './tweets/test/rocketleagueTest.json'
witcherTestFile = './tweets/test/witcher3Test.json'
troveTestFile = './tweets/test/troveTest.json'

trainThreshold = time.strptime("Tue Aug 11 00:00:00 +0000 2015", "%a %b %d %H:%M:%S +0000 %Y")

# Download tweets separated into categories/games
def downloadTweets():
	api = TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_token, tw.access_token_secret)

	for i in xrange(len(trackTweets)):
		r = api.request('statuses/filter', {'track': trackTweets[i], 'since':2014-07-19})
		# r = api.request('search/tweets', {'q': '#LeagueOfLegends', 'since': '2014-11-03', 'until': '2014-11-11'})
		count = 0
		trainTweets = []
		testTweets = []

		trainfilename = 'tweets/train/' + trackTweets[i] + 'Train.json'
		testfilename = 'tweets/test/' + trackTweets[i] + 'Test.json'
		train = open(trainfilename, 'w')
		test = open(testfilename, 'w')

		for item in r: #download and save to array
			if count == numTweets: break
			if 'delete' in item: continue
			if count < numTweets / 3:
				trainTweets.append(json.dumps(item))
			else:
				testTweets.append(json.dumps(item))
			count += 1

		train.write("[")
		train.write(",\n".join(trainTweets))
		train.write("]")
		train.close

		test.write("[")
		test.write(",\n".join(testTweets))
		test.write("]")
		test.close

	print "SAVED TRAIN AND TEST TWEETS TO FILE"


# Read in tweets from the dataset and search for occurrences of the hashtags for each
# of the games in the text. If it appears, write that json object to our outfile (either
# train or test based on the time stamp for the provided tweet).
# This is our filtering mechanism for getting tweets older than the time that the
# TwitterAPI allows for.
def filterTweetsOnHashtag():
	gta = open(gtaFile, 'w')
	cs = open(csFile, 'w')
	skyrim = open(skyrimFile, 'w')
	rocket = open(rocketFile, 'w')
	witcher = open(witcherFile, 'w')
	trove = open(troveFile, 'w')

	gtaTest = open(gtaTestFile, 'w')
	csTest = open(csTestFile, 'w')
	skyrimTest = open(skyrimTestFile, 'w')
	rocketTest = open(rocketTestFile, 'w')
	witcherTest = open(witcherTestFile, 'w')
	troveTest = open(troveTestFile, 'w')

	#Go through all of the files and create our outfile
	for root, _, files in os.walk('./08/'):
		for f in files:
			if not f.endswith(".json"): continue

			filename = os.path.join(root, f)
			with open(filename, 'r') as d:
				for line in d:
					item = json.loads(line)

					if 'delete' in item: continue # Skip items that have been deleted
					text = item['text']
					if re.findall(r'(#gta5\b|#gtav\b)', text, re.IGNORECASE):
						print "gta"
						if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
							gta.write(json.dumps(item))
							gta.write('\n')
						else:
							gtaTest.write(json.dumps(item))
							gtaTest.write('\n')
					elif re.findall(r'(#counterstrike\b|#csgo\b)', text, re.IGNORECASE):
						print "cs"
						if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
							cs.write(json.dumps(item))
							cs.write('\n')
						else:
							csTest.write(json.dumps(item))
							csTest.write('\n')
					elif re.findall(r'#skyrim\b', text, re.IGNORECASE):
						print "skyrim"
						if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
							skyrim.write(json.dumps(item))
							skyrim.write('\n')
						else:
							skyrimTest.write(json.dumps(item))
							skyrimTest.write('\n')
					elif re.findall(r'#rocketleague\b', text, re.IGNORECASE):
						print "rocketleague"
						if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
							rocket.write(json.dumps(item))
							rocket.write('\n')
						else:
							rocketTest.write(json.dumps(item))
							rocketTest.write('\n')
					elif re.findall(r'#witcher3\b', text, re.IGNORECASE):
						print "witcher"
						if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
							witcher.write(json.dumps(item))
							witcher.write('\n')
						else:
							witcherTest.write(json.dumps(item))
							witcherTest.write('\n')
					elif re.findall(r'#trove\b', text, re.IGNORECASE):
						print "trove"
						if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
							trove.write(json.dumps(item))
							trove.write('\n')
						else:
							troveTest.write(json.dumps(item))
							troveTest.write('\n')

	gta.close
	cs.close
	skyrim.close
	rocket.close
	witcher.close
	trove.close

	gtaTest.close
	csTest.close
	skyrimTest.close
	rocketTest.close
	witcherTest.close
	troveTest.close

	print "FINISHED FILTERING FILES"


def trainTweets():
	data = []
	with open(trainfilename, 'r') as f:
		data = json.load(f)


def testTweets():
	data = []
	with open(testfilename, 'r') as f:
		data = json.load(f)

if __name__ == "__main__":
	filterTweetsOnHashtag()