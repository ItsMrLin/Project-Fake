import cv2

def createVideo(chunks):
    chunks[0].reset()
    ret = chunks[0].read()
    height , width , layers =  ret.shape
    video = cv2.VideoWriter()
    video.open('video.mov',cv2.cv.CV_FOURCC(*'mp4v'),30,(width,height),True)
    for chunk in chunks:
        chunk.reset()
        for i in range(chunk.getStart(),chunk.getEnd()):
            img = chunk.read()
            video.write(img)

    cv2.destroyAllWindows()
    video.release()
    video = None

