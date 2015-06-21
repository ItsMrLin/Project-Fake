class ChunkGraph:

    phonemeDict = {}
    chunkList = []
    distDict = {}

    def __init__(self, chunkList):
        self.chunkList = chunkList
        for i, chunk in enumerate(chunkList):
            if chunk.getPhonemeName() not in phonemeDict:
                phonemeDict[chunk.getPhonemeName()] = [i]
            else:
                phonemeDict[chunk.getPhonemeName()].append(i)

    def findShortestPath(phonemeList):
        '''
        Input: a list of phoneme names
        Output: a list of chunks with the smallest differences between adjacent phonemes
        '''
        pass

    def _getDifference(chunkIndex1, chunkIndex2):
        if chunkIndex1 in distDict:
            if chunkIndex2 in distDict[chunkIndex1]:
                return distDict[chunkIndex1][chunkIndex2]
            else:
                distDict[chunkIndex1][chunkIndex2] = chunkList[chunkIndex1].getDifference(chunkIndex2)
                return distDict[chunkIndex1][chunkIndex2]
        else:
            distDict[chunkIndex1] = {}
            distDict[chunkIndex1][chunkIndex2] = chunkList[chunkIndex1].getDifference(chunkIndex2)
            return distDict[chunkIndex1][chunkIndex2]