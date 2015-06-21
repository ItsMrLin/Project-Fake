import cv2
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import mechanize
import csv
from bs4 import BeautifulSoup
from pydub import AudioSegment
import os

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
        #print "smoothed" , smoothed.shape
        c = 0
        for j in range(indexes[i]-4,indexes[i]+4):
            images[j] = smoothed[:,:,:,c].astype("uint8")
            c = c+1
    for img in images:
        #cv2.imshow('hi',img)
        video.write(img)
        #raw_input()
        #print img

    cv2.destroyAllWindows()
    video.release()
    video = None

def createAudio(audioChunks): 
    song = AudioSegment.from_wav("media/obama-speech.wav")
    newAudio = song[0:0]
    for chunk in audioChunks:
        newAudio = newAudio + song[chunk[0]:chunk[1]]
    newAudio.export("audio.wav",format="wav")

def writeVideo(chunks, audioChunks):
    createVideo(chunks)
    createVideo(audioChunks)
    os.system("ffmpeg -i video.mov -i audio.wav -vcodec copy -acodec copy final.mov")

def phonemize(sentence):
    phoneme_input = sentence.replace(" ", "+")
    br = mechanize.Browser()
    br.open("http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=" + phoneme_input)
    phonemes = str(BeautifulSoup(br.response().read()).findAll('tt')[1].contents[0])
    return phonemes

def tsvToTimeList(tsvFilename):
    timeList = []
    with open(tsvFilename, 'rb') as csvfile:
        csvReader = csv.reader(csvfile, delimiter="\t")
        for row in csvReader:
            timeList.append((int(row[0]),int(row[1]),row[2]))
    return timeList
