#!/usr/bin/python

from phue import Bridge

b = Bridge('192.168.0.105')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()
# Set brightness of lamp 1 to max
b.set_light(1, 'bri', 254)
b.get_light('Kitchen')
