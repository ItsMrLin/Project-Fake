# matching features of two images
import cv2
import sys
import scipy as sp
from alignment import findFace
import numpy as np
import math
def orth(x1,y1,x2,y2,s):
    h = math.sqrt((s**2 + 1) * ((x1 - x2)**2 + (y1 - y2)**2))
    s = math.sqrt(h**2 / ((x1 - x2)**2 + (y1 - y2)**2)) - 1
    return (x1 + s*(y2 - y1), y1 + s*(x1 - x2))


if len(sys.argv) < 3:
    print 'usage: %s img1 img2' % sys.argv[0]
    sys.exit(1)

img1_path = sys.argv[1]
img2_path = sys.argv[2]

img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)
print "img1",img1
print "img2",img2

face1, eyes1 = findFace(img1)
img1 = img1[face1[1]:face1[1]+face1[3],face1[0]:face1[0]+face1[2],:]
face2, eyes2 = findFace(img2)
img2 = img2[face2[1]:face2[1]+face2[3],face2[0]:face2[0]+face2[2],:]

orth1 = orth(eyes1[0][0],eyes1[0][1],eyes1[1][0],eyes1[1][1],10)
eyes1 = np.float32([
                        [eyes1[0][0],eyes1[0][1]],
                        [eyes1[1][0],eyes1[1][1]],
                        [orth1[0],orth1[1]]
                    ])

orth2 = orth(eyes2[0][0],eyes2[0][1],eyes2[1][0],eyes2[1][1],10)
eyes2 = np.float32([
                        [eyes2[0][0],eyes2[0][1]],
                        [eyes2[1][0],eyes2[1][1]],
                        [orth2[0],orth2[1]]
                    ])

print "eyes1", eyes1
print "eyes2", eyes2

# pts1 = np.float32([[50,50],[200,50],[50,200]])
# pts2 = np.float32([[10,100],[200,50],[100,250]])
M = cv2.getAffineTransform(eyes1,eyes2)
img3 = cv2.warpAffine(img1,M,(face1[3],face1[2]))

# visualization
h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]
view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
img1 = cv2.cvtColor(img1,cv2.COLOR_RGB2GRAY)
img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)    
view[:h1, :w1, 0] = img1
view[:h2, w1:, 0] = img2
view[:, :, 1] = view[:, :, 0]
view[:, :, 2] = view[:, :, 0]

kp1 = []
kp2 = []

cv2.imshow("view", view)

print kp1
# M = cv2.getPerspectiveTransform(kp1,kp2)
# dst = cv2.warpPerspective(img2,M,(h1,w1))
cv2.imshow("view2",img3)



cv2.waitKey()