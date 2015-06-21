import cv2

class VideoChunk:
    start = 0
    end = 0    
    startTime = 0
    endTime = 0    
    videoCap = None
    phonemeName = ""

    def __init__(self, startTime, endTime, phonemeName, video):
        self.startTime = startTime
        self.endTime = endTime
        self.videoCap = video
        self.fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        self.start = self.startTime * self.fps / 1000
        self.end = self.endTime * self.fps / 1000
        self.phonemeName = phonemeName

    def __str__(self):
        return "(" + str(self.start) + ", " + str(self.end) + ", " + str(self.phonemeName) + ")"

    def __repr__(self):
        return self.__str__()

    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end
    def getStartTime(self):
        return self.startTime
    def getEndTime(self):
        return self.endTime
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






