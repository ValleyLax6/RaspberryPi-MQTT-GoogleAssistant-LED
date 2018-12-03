#!usr/bin/python

from flask import(
    Flask,
    render_template,
    request,
)
import pigpio

app = Flask(__name__)

pi = pigpio.pi()

RED_PIN = 18
GREEN_PIN = 23
BLUE_PIN = 24

rgbLastSet = (255 * .75, 255 * .75, 255 * .75)
rgbLightsOff = (0,0,0)
currentStatus = False

#http://XXX.XXX.XXX.XXX:YYYY/lights/on
@app.route('/lights/on', methods=['GET', 'POST'])
def lightsOn():
    lightsToState(True)
    return "Lights On"

#http://XXX.XXX.XXX.XXX:YYYY/lights/off
@app.route('/lights/off', methods=['GET', 'POST'])
def lightsOff():
    lightsToState(False)
    return "Lights Off"

#http://XXX.XXX.XXX.XXX:YYYY/lights/toggle
@app.route('/lights/toggle', methods=['GET', 'POST'])
def lightsToggle():
    global currentStatus
    lightsToState(not currentStatus)
    if(currentStatus):
        return "Lights On"
    else:
        return "Lights Off"

#http://XXX.XXX.XXX.XXX:YYYY/lights/levelcolor?level= {{NumberField}}&color= {{TextField}}
@app.route('/lights/levelcolor', methods=['GET', 'POST'])
def lightsLevelColor():
    global rgbLastSet
    color = request.values['color']
    level = clamp(int(int(request.values['level']) * 2.55), 0, 255) #Scales and limits request (0-100% to 0-255)
 
    rgbLastSet = calcRGBColorLevels(color, level)
    lightsToState(level > 0)
 
    return "Lights set to %s and %s" % (level, color)
 
def setLights(levels):
    r, g, b = levels
    pi.set_PWM_dutycycle(RED_PIN, r)
    pi.set_PWM_dutycycle(GREEN_PIN, g)
    pi.set_PWM_dutycycle(BLUE_PIN, b)


def lightsToState(state):
    global rgbLastSet
    global rgbLightsOff
    global currentStatus
    
    if(state):
        #Set Office Lights to last used setting and indicate they are currently on
        setLights(rgbLastSet)
        currentStatus = True
    else:
        #Turn lights off and set current status variable
        setLights(rgbLightsOff)
        currentStatus = False



def calcRGBColorLevels(color, level):
    levels = (level, level, level)

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
    return levels
	
def clamp(n, minimum, maximum):
    return max(min(maximum, n), minimum)
	
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')
