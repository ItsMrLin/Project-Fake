import cv2

class Chunk:
    start = 0
    end = 0    
    videoCap = None
    phonemeName = ""

    def __init__(self, start, end, video, phonemeName = ""):
        self.start = start
        self.end = end
        self.videoCap = video
        self.phonemeName = phonemeName

    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end
    def getVideoCap(self):
        return self.videoCap
    def getPhonemeName(self):
        return self.phonemeName        
    def read(self):
        return self.videoCap.read()[1]
    def readLast(self):
        retVal = None
        self.reset()
        for i in range(self.getStart(),self.getEnd()):
            retVal = self.read()
        return retVal
    def reset(self):
        self.getVideoCap().set(cv2.cv.CV_CAP_PROP_POS_FRAMES,self.getStart())

    def getTransitionWeight(self, chunk2):
        self.reset()
        ret1 = self.readLast()

        chunk2.reset()
        ret2 = chunk2.read()

        if (ret1 == None):
            raise Exception("There was an error reading the last frame of the chunk.")
        if (ret2 == None):
            raise Exception("There was an error reading the first frame of the chunk.")

        ret1 = cv2.cvtColor(ret1,cv2.COLOR_RGB2GRAY)
        ret2 = cv2.cvtColor(ret2,cv2.COLOR_RGB2GRAY)

        return sum(sum(cv2.absdiff(ret1,ret2)))






