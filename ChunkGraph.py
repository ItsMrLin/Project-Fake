import sys
import operator
import numpy as np

class ChunkGraph:

    phonemeDict = {}
    chunkList = []
    distDict = {}

    def __init__(self, chunkList):
        self.chunkList = chunkList
        for i, chunk in enumerate(self.chunkList):
            if chunk.getStartTime() < 10000:
                continue
            if chunk.getPhonemeName() not in self.phonemeDict:
                self.phonemeDict[chunk.getPhonemeName()] = [i]
            else:
                self.phonemeDict[chunk.getPhonemeName()].append(i)

        for phoneme in self.phonemeDict.keys():
            if len(self.phonemeDict[phoneme]) > 10:
                self.phonemeDict[phoneme] = np.random.choice(self.phonemeDict[phoneme], 10)

    def findShortestPath(self, phonemeList):
        '''
        Input: a list of phoneme names
        Output: a list of chunks with the smallest differences between adjacent phonemes
        '''

        if len(phonemeList) == 0:
            return []

        # for v in self.phonemeDict.values():
        #     print len(v)

        shortestDist = [{} for i in phonemeList]
        father = [{} for i in phonemeList]

        for initialPhonemeIndex in self.phonemeDict[phonemeList[0]]:
            shortestDist[0][initialPhonemeIndex] = 0
            father[0][initialPhonemeIndex] = -1

        # # dynamic programming
        # for i in range(1, len(phonemeList)):
        #     print "At Level", i
        #     currentPhonemeName = phonemeList[i]
        #     for currentPhonemeIndex in self.phonemeDict[currentPhonemeName]:
        #         shortestDist[i][currentPhonemeIndex] = sys.maxint
        #         for prevPhonemeIndex in self.phonemeDict[phonemeList[i - 1]]:
        #             diff = self._getDifference(prevPhonemeIndex, currentPhonemeIndex)
        #             if shortestDist[i][currentPhonemeIndex] > shortestDist[i-1][prevPhonemeIndex] + diff:
        #                 shortestDist[i][currentPhonemeIndex] = shortestDist[i-1][prevPhonemeIndex] + diff
        #                 father[i][currentPhonemeIndex] = prevPhonemeIndex

        # greedy
        for i in range(1, len(phonemeList)):
            print "At Level", i
            currentPhonemeName = phonemeList[i]
            for currentPhonemeIndex in self.phonemeDict[currentPhonemeName]:
                shortestDist[i][currentPhonemeIndex] = sys.maxint
                prevPhonemeIndex = max(shortestDist[i-1].iteritems(), key=operator.itemgetter(1))[0]
                shortestDist[i][currentPhonemeIndex] = shortestDist[i-1][prevPhonemeIndex] + self._getDifference(prevPhonemeIndex, currentPhonemeIndex)
                father[i][currentPhonemeIndex] = prevPhonemeIndex

        minDestIndex = -1
        minDistance =  sys.maxint
        for destIndex in shortestDist[len(phonemeList) - 1].keys():
            if shortestDist[len(phonemeList) - 1][destIndex] < minDistance:
                minDistance = shortestDist[len(phonemeList) - 1][destIndex]
                minDestIndex = destIndex

        return self._traceBackShortestChunkPath(father, minDestIndex)
        
    def _traceBackShortestChunkPath(self, father, destIndex):
        chunkIndex = destIndex
        shortestPathChunkList = []
        for currentFather in reversed(father):
            shortestPathChunkList.insert(0, self.chunkList[chunkIndex])
            if chunkIndex != -1:
                chunkIndex = currentFather[chunkIndex]
        return shortestPathChunkList


    def _getDifference(self, chunkIndex1, chunkIndex2):
        '''
        Calculate and cache chunk differences
        '''
        if chunkIndex1 in self.distDict:
            if chunkIndex2 in self.distDict[chunkIndex1]:
                return self.distDict[chunkIndex1][chunkIndex2]
            else:
                self.distDict[chunkIndex1][chunkIndex2] = self.chunkList[chunkIndex1].getTransitionWeight(self.chunkList[chunkIndex2])
                return self.distDict[chunkIndex1][chunkIndex2]
        else:
            self.distDict[chunkIndex1] = {}
            self.distDict[chunkIndex1][chunkIndex2] = self.chunkList[chunkIndex1].getTransitionWeight(self.chunkList[chunkIndex2])
            return self.distDict[chunkIndex1][chunkIndex2]