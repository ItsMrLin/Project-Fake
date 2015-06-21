import sys

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
        
        if len(phonemeList) == 0:
            return []

        shortestDist = [{}] * len(phonemeList)
        father = [{}] * len(phonemeList)

        for initialPhonemeIndex in phonemeDict[phonemeList[0]]
            shortestDist[0][initialPhonemeIndex] = 0
            father[0][initialPhonemeIndex] = -1

        for i in range(1, len(phonemeList))
            currentPhonemeName = phonemeList[i]
            for currentPhonemeIndex in phonemeDict[currentPhonemeName]:
                shortestDist[i][currentPhonemeIndex] = sys.maxint
                for prevPhonemeIndex in phonemeDict[phonemeList[i - 1]]
                    diff = _getDifference(prevPhonemeIndex, currentPhonemeIndex)
                    if shortestDist[i][currentPhonemeIndex] > shortestDist[i-1][prevPhonemeIndex] + diff:
                        shortestDist[i][currentPhonemeIndex] = shortestDist[i-1][prevPhonemeIndex] + diff
                        father[i][currentPhonemeIndex] = prevPhonemeIndex

        minDestIndex = -1
        minDistance =  sys.maxint
        for destIndex in shortestDist[len(phonemeList) - 1].keys():
            if shortestDist[len(phonemeList) - 1][destIndex] < minDistance:
                minDistance = shortestDist[len(phonemeList) - 1][destIndex]
                minDestIndex = destIndex

        return _traceBackShortestChunkPath(father, minDestIndex)
        
    def _traceBackShortestChunkPath(father, destIndex):
        chunkIndex = destIndex
        shortestPathChunkList = []
        for currentFather in reversed(father):
            chunkList.insert(0, chunkList[chunkIndex])
            chunkIndex = currentFather[chunkIndex]
        return shortestPathChunkList


    def _getDifference(chunkIndex1, chunkIndex2):
        '''
        Calculate and cache chunk differences
        '''
        if chunkIndex1 in distDict:
            if chunkIndex2 in distDict[chunkIndex1]:
                return distDict[chunkIndex1][chunkIndex2]
            else:
                distDict[chunkIndex1][chunkIndex2] = chunkList[chunkIndex1].getTransitionWeight(chunkList[chunkIndex2])
                return distDict[chunkIndex1][chunkIndex2]
        else:
            distDict[chunkIndex1] = {}
            distDict[chunkIndex1][chunkIndex2] = chunkList[chunkIndex1].getTransitionWeight(chunkList[chunkIndex2])
            return distDict[chunkIndex1][chunkIndex2]