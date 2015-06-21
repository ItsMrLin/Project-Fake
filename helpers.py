import cv2
import mechanize
from bs4 import BeautifulSoup

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

def phonemize(sentence):
    phoneme_input = sentence.replace(" ", "+")
    br = mechanize.Browser()
    br.open("http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=" + phoneme_input)
    phonemes = str(BeautifulSoup(br.response().read()).findAll('tt')[1].contents[0])
    return phonemes