import numpy as np
import cv2
from matplotlib import pyplot as plt
import scipy as sp

def findFace(image):
    cascPath = "/usr/local/Cellar/opencv/2.4.11_1/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
    eye_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv/2.4.11_1/share/OpenCV/haarcascades/haarcascade_eye.xml')
    nose_cascase = cv2.CascadeClassifier('/usr/local/Cellar/opencv/2.4.11_1/share/OpenCV/haarcascades/haarcascade_mcs_leftear.xml')
    
    faceCascade = cv2.CascadeClassifier(cascPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    maxArea = 0
    maxFace = [0,0,0,0]
    for (x, y, w, h) in faces:
        if (w*h > maxArea):
            maxFace = [x,y,w,h]

    # Eyes
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = image[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    
    eyes2 = []
    for (ex,ey,ew,eh) in eyes:
        eyes2.append([ex,ey,ew,eh,ew*eh])
        

    eyes2 = np.float32(eyes2)
    eyes2.view('f32,f32,f32,f32,f32').sort(order=['f4'], axis=0)
    eyes2 = eyes2[::-1]
    print "THE FUCKING EYES",eyes2
    eyes2 = np.delete(eyes2,4,axis=1)
    eyes2 = eyes2.tolist()

    # Draw rectangles around the eyes
    # cv2.rectangle(roi_color,(int(eyes2[0][0]),int(eyes2[0][1])),(int(eyes2[0][0]+eyes2[0][2]),int(eyes2[0][1]+eyes2[0][3])),(0,0,255),2)
    # cv2.rectangle(roi_color,(int(eyes2[1][0]),int(eyes2[1][1])),(int(eyes2[1][0]+eyes2[0][2]),int(eyes2[1][1]+eyes2[1][3])),(0,0,255),2)

    # Nose
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = image[y:y+h, x:x+w]
    nose = nose_cascase.detectMultiScale(roi_gray)
    maxArea = 0
    maxNose = [0,0,0,0]
    for (nx, ny, nw, nh) in faces:
        if (w*h > maxArea):
            maxNose = [nx,ny,nw,nh]
        # cv2.rectangle(image, (nx, ny), (nx+nw, ny+nh), (255, 0, 0), 2)
    
    maxFace[0] = maxFace[0]-(maxFace[2]/4)
    maxFace[2] = maxFace[2]+(maxFace[2]/2)
    maxFace[1] = maxFace[1]-(maxFace[3]/4)
    maxFace[3] = maxFace[3]+(maxFace[3]/2)

    cv2.rectangle(image, (maxFace[0], maxFace[1]), (maxFace[0]+maxFace[2], maxFace[1]+maxFace[3]), (0, 255, 0), 2)
    # #cv2.rectangle(image, (maxNose[0], maxNose[1]), (maxNose[0]+maxNose[2], maxNose[1]+maxNose[3]), (0, 255, 0), 2)

    # cv2.imshow("Faces found" ,image)
    # cv2.waitKey(0)
    print maxFace
    return maxFace,eyes2  


# TODO: DOES NOT WORK
def matchAndWarp(img1,img2):
    MIN_MATCH_COUNT = 10

    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)



    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w,d = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img1 = cv2.cvtColor(img1,cv2.COLOR_RGB2GRAY)
        img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)

        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
        view[:h1, :w1, 0] = img1
        view[:h2, w1:, 0] = img2
        view[:, :, 1] = view[:, :, 0]
        view[:, :, 2] = view[:, :, 0]

        for m in matches:
            # draw the keypoints
            # print m.queryIdx, m.trainIdx, m.distance
            color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
            cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])) , (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)


        cv2.imshow("view", view)
        cv2.waitKey()

    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    plt.imshow(img3, 'gray'),plt.show()