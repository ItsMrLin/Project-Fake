import cv2

class chunk:
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
        return self.videoCap.read()
    def readLast(self):
        retVal = None
        self.reset()
        for i in range(self.getStart(),self.getEnd()):
            eh, retVal = self.read()
        return retVal
    def reset(self):
        self.getVideoCap().set(cv2.cv.CV_CAP_PROP_POS_FRAMES,self.getStart())

    def getSimilarity(self, chunk2):
        self.reset()
        ret1 = self.readLast()

        chunk2.reset()
        eh, ret2 = chunk2.read()
        ret1 = cv2.cvtColor(ret1,cv2.COLOR_RGB2GRAY)
        ret2 = cv2.cvtColor(ret2,cv2.COLOR_RGB2GRAY)

        return sum(sum(cv2.absdiff(ret1,ret2)))








