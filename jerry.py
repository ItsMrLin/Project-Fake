import video_processing
import helpers
from ChunkGraph import ChunkGraph

testList = [
    (1000, 1100, "hey"),
    (1130, 1200, "yo"),
    (10000, 11000, "heyi"),
    (20000, 21000, "hoho"),
]

testList = helpers.tsvToTimeList("words.tsv")

chunkList = video_processing.getChunkList("obama.mp4", testList)

graph = ChunkGraph(chunkList)
sentence = "americans shouldn't pay taxes"
videoChunkList = graph.findShortestPath(sentence.split(" "))

print videoChunkList

# helpers.createVideo(videoChunkList)
audioChunkList = [(videoChunk.getStartTime(), videoChunk.getEndTime()) for videoChunk in videoChunkList]
helpers.writeVideo(videoChunkList, audioChunkList)
