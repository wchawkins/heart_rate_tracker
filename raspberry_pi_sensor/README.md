# SpO2 Pi Python

This project is intended to run on a Raspberry Pi in order to read data from a
MAX30105 light sensor and calculate pulse oximetry skin temperature and heart rate..

# Parts List
## Raspberry Pi zero starter kit
This option comes with a bundle that includes:
Raspberry Pi Zero W - the type of low cost game-changing product Raspberry Pi's known for - the super light, super lean microcomputer we've come to know and low, but now with built-in WiFi.
Mini HDMI to HDMI Adapter - Will let you convert the little port on the Zero to a standard sized HDMI jack. You can get 1080P HDMI video + audio out of this little computer!
USB OTG Cable - Lets you plug in a normal USB device such as WiFi dongle, USB hub, keyboard, mouse, etc into the Zero.
8GB SD Card - May come blank or pre-burned with NooBs! Since NooBs has recently updated to add Pi Zero W support we recommend reformatting/burning NooBs on from scratch if your Pi Zero doesn't run!
Adafruit Pi Zero Enclosure - Adafruit's classic, sturdy plastic enclosure. Keeps your Pi Zero safe and sleek.
5V 1A Power Supply & USB A/Micro B Cable OR 5V 2.4A Power Supply w/ Micro USB Cable - the best way to power up your Pi Zero with a stable 5V power supply that wont vary or sag.
2x20 Male header strip - Solder this in to plug in Pi HATs, GPIO cables, etc as you would into a normal Pi. (We also have a 2x20 Female and 2x20 Female right-angle style for more exotic connecting)
Buy Here- https://www.adafruit.com/product/3410

If you buy this starter pack you will still need to buy a battery, usb-charger, battery shim (connects battery to the pi) and the MAX 30105 sensor.

Reccomended lithium ion rechargable battery- https://www.adafruit.com/product/2011
Reccomended battery charger- https://www.adafruit.com/product/1304
Reccomended battery shim- https://www.adafruit.com/product/3196

## Already own a Raspberry Pi and supporting cables/supplies?
Ask yourself the following questions to make sure you have what you need!
	Do I have a Raspberry Pi?
	Do I have a micro SD card that has at least 8 GB of storage?
	Do I have a battery, a way to charge the battery and a way to power the  pi using this battery? (You can power the raspberry pi using a cable but then your pi won't be mobile)
	Do I have a MAX 30105 sensor?

## MAX 30105 light sensor and wires
Lastly you will need to purchase the photo sensor https://www.sparkfun.com/products/14045
Keep in mind you will need to wire the MAX 30105 sensor to the Rapsberry Pi and we recomend soldering on both ends if you can afford to designate your Raspberry Pi to this project. 
Somthing like this will work https://amzn.to/35MyWuU

# Notes about assembly
Headers are recomended for attaching the battery shim to the Pi zero. The plastic case that comes with a starter pack serves as a perfect way to protect your Pi as well as a resting place for the shim during/after soldering. 

## Very Important assembly steps
We recomend soldering the sensores that connect the MAX 30105 sensor to your pi when the pi is not in its protective case

The protective case MUST be on the Pi before soldering the shim to the Pi. Once the shim is soldered the protective case can not be taken off without un-soldering. 

# Connecting to Raspberry Pi and installing files
## Installing
Currently this project is using Python 3 and is intended to be ran on a Raspberry Pi.
The `requirements.txt` file lists the Python packages this project depends on.
You can try installing by doing `pip install -r requirements.txt`. Before doing so,
you may have to install Pandas with `sudo apt-get install python-pandas`.

## Usage
Run `python3 main.py filename` from the RPi.
This will save raw Red, IR light data to `filename` file.

Alternatively, if you want to send SpO2 and HR data to the web app, you can run
`python3 main.py filname wss://spo2-web.herokuapp.com username`, where username
is the username you signed-up with at https://spo2-web.herokuapp.com. Visit
https://spo2-web.herokuapp.com/graph to see the live data.

## Connecting to Pi
### Connecting to Pi with SSH
In order to connect to the Pi in a console/terminal-based fashion, use Secure Shell (SSH). From your computer's command-line run:

`ssh pi@pi-zero.local`

and then enter your username (pi) and password (raspberrypi). This assumes the Pi's hostname is `pi-zero` and your computer and the Pi are connected to the same local network (hence the `.local`). See the section below on Wifi for configuring wireless networks.

### Copying to Pi with SSH
To copy files to the Pi, you could use a flash drive or email but SSH is nice once you get the hang of it, since it lets you copy the file and then remote into the Pi with a couple commands.

SSH provides a tool called `scp` to securely copy files to and from remote machines.

Run `scp filename pi@pi-zero.local:`to copy the `filename` file from your computer to the Pi.

If you get stuck... here is a helpful article about SSH'ing into Pi's
https://itsfoss.com/ssh-into-raspberry/

#### Configuring Wifi on Pi
Once you're connected to the Pi (whether through SSH or monitor and mouse), if you want to add a new wifi network (so you don't have to always use a hotspot, for example), edit the `/etc/wpa_supplicant/wpa_supplicant.conf` file. If you're SSH'ed into the Pi, you can run `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` from the command-line to bring up a console text editor. Otherwise, you can use some type of GUI text editor, but you will need superuser rights (sudo). There should already be an entry that looks like:

```
network={
    ssid="MyWifiHotspot"
    psk="MyWifiHotspotPa$$word"
    key_mgmt=WPA-PSK
}
```

Copy-paste those lines to the bottom of the file, substituting in your new wireless network name and password. The final final should look something like:

```
country=US
network={
    ssid="MyWifiHotspot"
    psk="MyWifiHotspotPa$$word"
    key_mgmt=WPA-PSK
}
network={
    ssid="MyWifi"
    psk="MyWifiPa$$word"
    key_mgmt=WPA-PSK
}
```
