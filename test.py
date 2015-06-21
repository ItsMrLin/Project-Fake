from chunk import VideoChunk
import cv2
cap = cv2.VideoCapture('obama.mp4')

img1= cap.read()[1]
img2= cap.read()[1]


c = VideoChunk(1200,1240,cap)
c2 = VideoChunk(1250,1260,cap)
c3 = VideoChunk(1270,1290,cap)
print c.getTransitionWeight(c2)
from helpers import createVideo
createVideo([c,c2])