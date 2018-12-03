import paho.mqtt.client as mqtt
import re
import standardLED as sLED
import MultiColorLights as mLED

def on_log(client, userdata, level, buf):
    print("log: "+buf)
    

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad Connection, code=",rc)

        
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code "+str(rc))

    
def on_message(client, userdata,msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("message recieved",topic, m_decode)
    
    #Standard one color lights
    if m_decode == "on" and topic == "/pi/led":
        sLED.lightsOn()
        
    elif m_decode == "off" and topic == "/pi/led":
        sLED.lightsOff()
        
    elif "rgb" in m_decode and topic == "/pi/led":
        color = re.findall('\d+', m_decode)
        sLED.lightsColor(color)


   # MultiColored Lights
    elif m_decode == "on" and topic == "/pi/multi":
        mLED.lightsOn()

    elif m_decode == "off" and topic == "/pi/multi":
        mLED.lightsOff()

    elif "rgb" in m_decode and topic == "/pi/multi":
        levels = re.findall('\d+', m_decode)
        color = map(int,levels)
        mLED.setLights(color)
        
    elif "standard" in m_decode:
        mLED.changePattern("standard")

    elif "nightlight" in m_decode:
        mLED.changePattern("nightlight")

    elif "rainbow" in m_decode:
        mLED.changePattern("rainbow")

    elif "doorway" in m_decode:
        mLED.changePattern("doorway")
    else:
        color = m_decode
        sLED.colorFromText(color)
    

broker = "localhost"
client = mqtt.Client("Pi")

client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message

print("Connecting to broker ",broker)

client.connect(broker)

client.subscribe([("/pi/led",0),("/pi/multi",0)])
client.loop_forever()
