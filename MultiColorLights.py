import time
from neopixel import *
import argparse
import threading


LED_COUNT = 150     

strip = Adafruit_NeoPixel(LED_COUNT, 18, 800000, 10, False, 255, 0)

strip.begin()


rgbLastSet = (255 , 255 , 255)
currentPattern = "standard"
rainbowStatus = False
ontoNightLight = False

    


def lightsOn():
    if currentPattern == "rainbow":
        rainbowOn()
    else:
        setLights(rgbLastSet)


def lightsOff():
    global rainbowStatus
    rainbowStatus = False
    levels = 0,0,0
    setLights(levels)

def setLights(levels):
    global strip
    global rgbLastSet
    global onOffThread
    global currentPattern
    global nightThread
    global doorwayThread
    r ,g, b =levels
    if(r>0 and g>0 and b>0):
        rgbLastSet = levels
    if currentPattern == "nightlight":
        nightThread  = threading.Thread(target = nightLight, args = (strip,Color(g,r,b),))
        nightThread.start()
    elif currentPattern == "doorway":
        doorwayThread = threading.Thread(target = doorwayAnimation, args=(strip,Color(g,r,b),))
        doorwayThread.start()
    else:
        onOffThread = threading.Thread(target=colorWipe, args =(strip,Color(g,r,b),20,))
        onOffThread.start()
        

def changePattern(newPattern):
    global currentPattern
    global ontoNightLight
    if(currentPattern == "rainbow"):   
        rainbowOff()

    if(newPattern == "rainbow"):
        currentPattern = "rainbow"
        rainbowOn()
    elif(newPattern == "standard"):
        currentPattern = "standard"
        setLights(rgbLastSet)
    elif(newPattern == "nightlight"):
        currentPattern = "nightlight"
        ontoNightLight = True
        setLights(rgbLastSet)
    elif(newPattern == "doorway"):
        currentPattern = "doorway"
        setLights(rgbLastSet)


        

def rainbowOn():
    global rainbowStatus
    global strip
    global rainbowThread
    rainbowStatus = True
    rainbowThread = threading.Thread(target=rainbow, args = (strip,))
    rainbowThread.start()

def rainbowOff():
    global rainbowStatus
    rainbowStatus = False


def doorwayAnimation(strip,color):
    doorwayRightThread = threading.Thread(target = doorwayRight,args = (strip,color,))
    doorwayLeftThread = threading.Thread(target = doorwayLeft, args = (strip,color,))
    doorwayRightThread.start()
    doorwayLeftThread.start()

def doorwayRight(strip,color):
    for i in range(71):
        strip.setPixelColor(i,color)
        strip.show()
        time.sleep(25/1000.0)

def doorwayLeft(strip,color):
    for i in range(150,70,-1):
        strip.setPixelColor(i,color)
        strip.show()
        time.sleep(18.75/1000.0)
    
    

def nightLight(strip, color,wait_ms=20):
    global ontoNightLight
    for i in range(strip.numPixels()):
        if i<52 or i>88:
            strip.setPixelColor(i,Color(0,0,0))
            if(ontoNightLight):
                time.sleep(wait_ms/1000.0)
        else:
            strip.setPixelColor(i,color)
            time.sleep(wait_ms/1000.0)
        strip.show()
    ontoNightLight = False
        

        
def colorWipe(strip, color, wait_ms=20):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        if(i == 70):
            strip.setPixelColor(i,Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)



def theaterChase(strip, color, wait_ms=20, iterations=10):
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def rainbow(strip, wait_ms=20, iterations=1):
    while(rainbowStatus):
        for j in range(256*iterations):
            for i in range(strip.numPixels()):
                if(not rainbowStatus):
                    return
                strip.setPixelColor(i, rainbowWheel((int(i * 256 / strip.numPixels()) + j) & 255))
    
            strip.show()
            time.sleep(wait_ms/1000.0)
            
        
def rainbowWheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
