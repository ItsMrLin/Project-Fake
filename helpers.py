import cv2

def createVideo(cap, chunks):
    chunks[0].reset()
    ret = chunks[0].read()
    height , width , layers =  ret.shape
    video = cv2.VideoWriter('video.mp4',cv2.cv.CV_FOURCC('M','P','4','2'),1,(width,height))
    for chunk in chunks:
        chunk.reset()
        for i in range(chunk.getStart(),chunk.getEnd()):
            img = chunk.read()
            video.write(img)

    cv2.destroyAllWindows()
    video.release()

