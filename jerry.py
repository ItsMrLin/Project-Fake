import video_processing
import helpers
from ChunkGraph import ChunkGraph

testList = [
    (1000, 1100, "hey"),
    (1130, 1200, "yo"),
    (10000, 11000, "heyi"),
    (20000, 21000, "hoho"),
]

# helpers.wordsToPhonemes() 

phonemeList = helpers.tsvToTimeList("phonemes.tsv")
wordAndphonemeList = helpers.tsvToTimeList("words.tsv")
wordSet = set([word[2].upper() for word in wordAndphonemeList])
wordAndphonemeList.extend(phonemeList)
chunkList = video_processing.getChunkList("local/obama.mp4", wordAndphonemeList)
graph = ChunkGraph(chunkList)
print "done creat graph"

# sentence = "americans shouldn't pay taxes"
# sentence = "illegal immigrants"
# sentence = "hello world richard"
# sentence = "how do you think of jay peg"
# sentence = "AH AH AH AH AH AH"
# sentence = "uh uh uh uh uh uh"
# sentence = "i think we are the best ever"
# sentence = "Georgia Tech is the best"
sentence = "how you doing"
rawPhonemeInput = sentence.split()
phonemeInput = []
for rawInput in rawPhonemeInput:
    if rawInput.upper() in wordSet:
        phonemeInput.append(rawInput)
    else:
        phonemeInput.extend(helpers.phonemize(rawInput).replace(".","").strip().split(" "))

# phonemeInput = [phoneme for phoneme in helpers.phonemize(sentence).replace(".","").split(" ") if phoneme!= ""]
print phonemeInput

videoChunkList = graph.findShortestPath(phonemeInput)
print "done find path"

print videoChunkList
# helpers.createVideo(videoChunkList)
audioChunkList = [(videoChunk.getStartTime(), videoChunk.getEndTime()) for videoChunk in videoChunkList]
helpers.writeVideo(videoChunkList, audioChunkList)
