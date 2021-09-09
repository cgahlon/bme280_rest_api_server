# bme280_rest_api_server

A simple REST API Server using Flask to allo collection of data from a
bme280 sensor on a Raspberry Pi. This is going to be part of my freezer
monitor setup so I used the Pi Zero W so it could be wireless.

And yes, I know you can run multiple sensors on an i2c bus. Intitially
this code only needs to support one until I decide to build a weather
station version.

## Pi Zero bme280 i2c Bus Connectivity Issues
The Pi Zero and the bme280 are 3.3v logic so connect the bme280 vcc
to the Pi Zero 3.3v output instead of the 5v like you'll see in a lot
of weather station tutorials.  The bme280 has a regulator so it is 5v
safe, but it randombly disappears from the i2c bus is powered by 5v.
A powercycle is required for it to be reachable again.

## My Quick And Dirty Headless Raspberry Pi Static IP Setup

Burn your sdcard with Raspberry Pi OS lite.  Google it if you don't
know where to get it or how to do it.Ensure you mount the correct 
/dev/sdX device in the shell commands.

After you plug your sd card in you can run `cat /procp/partitions`
to view a list of what partionts the kernel knows about. Yours may
be `/dev/mmcXYZ` if you have a laptop with a build in reader.

Mount your sdcard:

```shell
sudo mkdir -p /mnt/sdcard/{boot,rootfs}
sudo mount /dev/sdc1 /mnt/sdcard/boot
sudo mount /dev/sdc2 /mnt/sdcard/rootfs
```

I change the config.txt so the I2C interface kerenel module loads
at boot time.

```shell
sed -i 's/^#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /mnt/sdcard/boot/config.txt
```

Next I Enable SSH at boot time and set a static IP address:
```shell
sudo touch /mnt/sdcard/boot/ssh
sudo bash -c 'cat <<EOF > /mnt/sdcard/rootfs/etc/dhcpcd.conf
interface wlan0
static ip_address=192.168.15.241/24
static routers=192.168.15.254
static domain_name_servers=192.168.15.254

EOF'
```

Since I am on a Pi Zero W I enable WIF to connect to my network.
You will want to change NETWORK_NAME and WIFI_PASSWORD to match
your network

```shell
sudo bash -c 'cat <<EOF > /mnt/sdcard/rootfs/etc/wpa_supplicant/wpa_supplicant.conf
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
  ssid="NETWORK_NAME"
  psk="WIFI_PASSWORD"
}
EOF'
```
## Installation

As of this writing the lite image supplied by raspberry is WAY out of
date. To actually update software you will need to run apt-get update
with the `--allow-releaseinfo-change` argument or it will not download
new package metadata.

### Install Prerequisites

```shell
sudo apt-get update --allow-releaseinfo-change && apt-get update -y
sudo apt-get install -y python3-pip
git clone https://github.com/cgahlon/bme280_rest_api_server.git
sudo pip3 install -r requirements.txt
```

### Quick Server Test
You can now start the server to test connectivity/fucntionality
```shell
sudo python3 bme280_rest_api_server.git
```

From a remote host or another terminal on the pi run a curl test.
```shell
curl http://127.0.0.1/temperature
```
You should see the temperature of your sensor as the only information
returned.  If there are errors, check the output of the terminal you
started the application in.  Most likely you forgot to update the i2c
device address or bus in the code.

``shell
## Running The Server At Boot
TODO: Add boot time start instructions
TODO: Write ansible playbook to do all the things and test the device
