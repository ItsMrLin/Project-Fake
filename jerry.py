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

# phonemeList = helpers.tsvToTimeList("phonemes.tsv")
phonemeList = helpers.tsvToTimeList("words.tsv")
chunkList = video_processing.getChunkList("local/obama.mp4", phonemeList)
graph = ChunkGraph(chunkList)
print "done creat graph"

# sentence = "americans shouldn't pay taxes"
sentence = "illegal immigrants"
# sentence = "hello world"
# phonemeInput = [phoneme for phoneme in helpers.phonemize(sentence).replace(".","").split(" ") if phoneme!= ""]
phonemeInput = sentence.split()
print phonemeInput

videoChunkList = graph.findShortestPath(phonemeInput)
print "done find path"

print videoChunkList
# helpers.createVideo(videoChunkList)
audioChunkList = [(videoChunk.getStartTime(), videoChunk.getEndTime()) for videoChunk in videoChunkList]
helpers.writeVideo(videoChunkList, audioChunkList)
