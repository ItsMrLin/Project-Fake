from chunk import Chunk
import cv2
cap = cv2.VideoCapture('obama.mp4')
c2 = Chunk(21,40,cap)
c = Chunk(0,20,cap)
print c.getTransitionWeight(c2)
from helpers import createVideo
createVideo(cap,[c,c2])