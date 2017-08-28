import ibuddy_usbapi as usb

devices = usb.usbapi().getDevices()

while True:
    input = raw_input("What would you like me to do next?")
    devices.play(input)
    devices.wait()