import RPi.GPIO as GPIO
import time
import os
from mpd import MPDClient

bin1 = 25
bin2 = 26
bin3 = 27
bout1 = 22
bout2 = 23
bout3 = 24
active = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(bin1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(bin2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(bin3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(bout1,GPIO.OUT)
GPIO.output(bout1,0)
GPIO.setup(bout2,GPIO.OUT)
GPIO.output(bout2,0)
GPIO.setup(bout3,GPIO.OUT)
GPIO.output(bout3,0)

# limit speed to 16x to reduce drive noise
os.system("eject -x 16 /dev/sr0")

# do we need this before each eject?
# eject [-vn] -i on|off|1|0 [<name>]	-- toggle manual eject protection on/off

def player(command):
  client = MPDClient()
  client.timeout = 10
  client.idletimeout = None
  client.connect('localhost', 6600)
  result = command(client)
  client.close()
  client.disconnect()
  return result

def do_eject():
  # try toggling the tray, if failed just open it
  os.system("eject -T /dev/sr0 || eject /dev/sr0")
  player(lambda p: p.stop())
  time.sleep(0.5)
def do_stop():
  player(lambda p: p.stop())
  time.sleep(0.5)
def do_play():
  player(lambda p: p.play())
  time.sleep(0.5)
def do_next():
  player(lambda p: p.next())
  time.sleep(0.5)
def do_previous():
  player(lambda p: p.previous())
  time.sleep(0.5)
def do_volume_up():
  player(lambda p: p.setvol(min(100, int(p.status()['volume'])+5)))
  time.sleep(0.2)
def do_volume_down():
  player(lambda p: p.setvol(max(0, int(p.status()['volume'])-5)))
  time.sleep(0.2)
def do_shutdown():
  os.system("poweroff")
  time.sleep(0.5)
def do_switch_source():
  time.sleep(0.5)

while True:
  time.sleep(0.05)
  GPIO.output(bout1,1)
  if GPIO.input(bin1): do_eject()
  if GPIO.input(bin2): do_next()
  if GPIO.input(bin3): do_volume_up()
  GPIO.output(bout1,0)
  time.sleep(0.05)
  GPIO.output(bout2,1)
  if GPIO.input(bin1): do_stop()
  if GPIO.input(bin2): do_previous()
  if GPIO.input(bin3): do_volume_down()
  GPIO.output(bout2,0)
  time.sleep(0.05)
  GPIO.output(bout3,1)
  if GPIO.input(bin1): do_play()
  if GPIO.input(bin2): do_shutdown()
  if GPIO.input(bin3): do_switch_source()
  GPIO.output(bout3,0)

