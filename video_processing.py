import cv2

def getPhonemeLists(filename, timeList):
    '''
    Given filename and a list fo time info tuple (startTime, endTime, phonemeName),
    return a list of tuple containing (startFrameIndex, endFrameIndex, phonemeName)

    time is in format hh:mm:ss
    '''
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened(): 
        print "could not open :",fn
        return
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    frameList = [None] * len(timeList)
    for i, timeTuple in enumerate(timeList):
        frameList[i] = (int(_getSec(timeTuple[0])*fps), int(_getSec(timeTuple[1])*fps), timeTuple[2])

    return frameList

def _getSec(timeString):
    '''
    parse time hh:mm:ss and output its value in seconds
    '''
    l = timeString.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])