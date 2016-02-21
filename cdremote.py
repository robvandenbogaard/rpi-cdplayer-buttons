import atexit
import time
import os
import lirc
from mpd import MPDClient

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
def do_pause():
  player(lambda p: p.pause())
  time.sleep(0.5)
def do_next():
  player(lambda p: p.next())
  time.sleep(0.5)
def do_previous():
  player(lambda p: p.previous())
  time.sleep(0.5)
def do_forward():
  player(lambda p: p.seekcur('+10'))
  time.sleep(0.2)
def do_rewind():
  player(lambda p: p.seekcur('-10'))
  time.sleep(0.2)
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

commands = {
  'eject': do_eject,
  'stop': do_stop,
  'play': do_play,
  'pause': do_pause,
  'next': do_next,
  'previous': do_previous,
  'seek+': do_forward,
  'seek-': do_rewind,
  'vol+': do_volume_up,
  'vol-': do_volume_down,
  'shutdown': do_shutdown
}

def setup():
  lirc.init("cdremote")

def teardown():
  lirc.deinit()

atexit.register(teardown)

setup()
while True:
  time.sleep(0.05)
  codes = lirc.nextcode()
  for code in codes:
    command = commands[code]
    if command:
      command()
