import cv2
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

def createVideo(chunks):
    chunks[0].reset()
    ret = chunks[0].read()
    height , width , layers =  ret.shape
    video = cv2.VideoWriter()
    video.open('video.mov',cv2.cv.CV_FOURCC(*'mp4v'),30,(width,height),True)
    images = []
    indexes = []
    for chunk in chunks:
        chunk.reset()
        indexes.append(len(images))
        for i in range(chunk.getStart(),chunk.getEnd()):
            img = chunk.read()
            images.append(img)

    # Gaussian Smoothing

    for i in range(1,len(indexes)):
        img_array = np.zeros((height,width,3,8))
        c = 0
        for j in range(indexes[i]-4,indexes[i]+4):
            img_array[:,:,:,c] = images[j]
            c = c+1

        smoothed = gaussian_filter1d(img_array,sigma=1.5,axis=3)
        print "smoothed" , smoothed.shape
        c = 0
        for j in range(indexes[i]-4,indexes[i]+4):
            images[j] = smoothed[:,:,:,c].astype("uint8")
            c = c+1


    for img in images:
        #cv2.imshow('hi',img)
        video.write(img)
        #raw_input()
        print img

    cv2.destroyAllWindows()
    video.release()
    video = None

