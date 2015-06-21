import cv2
from VideoChunk import VideoChunk

def getChunkList(filename, timeList):
    '''
    Given filename and a list fo time info tuple (startTime, endTime, phonemeName),
    return a list of tuple containing (startFrameIndex, endFrameIndex, phonemeName)

    time is in milliseconds
    '''
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened(): 
        print "could not open :",filename
        return
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    chunkList = [None] * len(timeList)
    for i, timeTuple in enumerate(timeList):
        # chunkList[i] = Chunk(int(timeTuple[0]*fps/1000), int(timeTuple[1]*fps/1000), cap, timeTuple[2])
        chunkList[i] = VideoChunk(timeTuple[0], timeTuple[1], timeTuple[2], cap)

    return chunkList
