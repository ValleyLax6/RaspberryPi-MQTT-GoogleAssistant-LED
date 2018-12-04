# RaspberryPi-MQTT-LED

This program requires the use of a few libraries that need to be installed before using on your own Raspberry Pi.

## Install instructions
### pigpio
First type this into your terminal
```
sudo apt-get update
sudo apt-get install pigpio
pigpiod -v
```
If the version installed isnt the current version, install the lastest version.
First build-essentials needs to be installed if not already
```
sudo apt-get install build-essential
```
Next, install the latest version
```
rm master.zip
sudo rm -rf pigpio-master
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
```
pigio should now be sucessfully installed on your Pi
### Neopixel
Since I used a WS2812 type LED strip a special neopixel library has to be installed
#### Prep
The package sources are updated:
```
sudo apt-get update
sudo apt-get install gcc make build-essential python-dev git scons swig
```
The audio output must be deactivated to use PWM on the Pi. For this we edit the file
```
sudo nano /etc/modprobe.d/snd-blacklist.conf
```
Here we add the following line:
```
blacklist snd_bcm2835
```
Then the file is saved by pressing CTRL + O and CTRL + X closes the editor.

We also need to edit the configuration file:
```
sudo nano /boot/config.txt
```
Below are lines with the following content (with Ctrl + W you can search):
```
# Enable audio (loads snd_bcm2835)
dtparam=audio=on
```
This bottom line is commented out with a hashtag # at the beginning of the line: #dtparam=audio=on
Restart the system
```
sudo reboot
```
#### Install
Now we can download the library.
```
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x/
sudo scons
cd python
```
Here we carry out the installation:
```
sudo python setup.py build
sudo python setup.py install
```

### MQTT
I'm using a MQTT server hosted on the Raspberry Pi, you will need both Mosquitto (to host the server) and the library paho-mqtt to have the client connect to the server.
```
sudo apt-get install mosquitto
sudo apt-get install python3-pip
sudo pip3 install paho-mqtt
```
Now everything is installed!

