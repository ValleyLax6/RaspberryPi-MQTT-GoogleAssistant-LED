import pigpio

pi = pigpio.pi()

RED_PIN = 25
GREEN_PIN = 23
BLUE_PIN = 24

rgbLastSet = (255 , 255, 255)
rgbLightsOff = (0,0,0)



def lightsOn():
    setLights(rgbLastSet)


def lightsOff():
    setLights(rgbLightsOff)

 
def setLights(levels):
    r, g, b = levels
    pi.set_PWM_dutycycle(RED_PIN, r)
    pi.set_PWM_dutycycle(GREEN_PIN, g)
    pi.set_PWM_dutycycle(BLUE_PIN, b)


def colorFromText(color):
    level = 255

    if ("red" in color.lower()):
        levels = (level, 0, 0)
    elif ("orange" in color.lower()):
        levels = (level, level * .75,0)
    elif ("yellow" in color.lower()):
        levels = (level * .75,level,0)
    elif ("green" in color.lower()):
        levels = (0, level, 0)
    elif ("aqua" in color.lower()):
        levels = (0, level, level * .75)
    elif ("cyan" in color.lower()):
        levels = (0, level * .75, level)
    elif ("blue" in color.lower()):
        levels = (0, 0, level)
    elif ("purple" in color.lower()):
        levels = (level * .75, 0, level)
    elif ("pink" in color.lower()):
        levels = (level, 0, level * .75)
    setLights(levels)

def lightsColor(color):
    global rgbLastSet
    rgbLastSet = color
    setLights(rgbLastSet)
    
	

