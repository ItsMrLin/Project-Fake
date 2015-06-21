import cv2

def getFrameList(filename, timeList):
    '''
    Given filename and a list fo time info tuple (startTime, endTime, phonemeName),
    return a list of tuple containing (startFrameIndex, endFrameIndex, phonemeName)

    time is in milliseconds
    '''
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened(): 
        print "could not open :",fn
        return
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    frameList = [None] * len(timeList)
    for i, timeTuple in enumerate(timeList):
        frameList[i] = (int(timeTuple[0]*fps/1000), int(timeTuple[1]*fps/1000), timeTuple[2])

    return frameList