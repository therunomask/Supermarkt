import usb.core
import usb.util


dev = usb.core.find(idVendor=0x0922, idProduct=0x8003)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()
interface = 0
endpoint = dev[0][(0, 0)][0]
# if the OS kernel already claimed the device, which is most likely true
# thanks to
# http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
# if dev.is_kernel_driver_active(interface) is True:
#     # tell the kernel to detach
#     dev.detach_kernel_driver(interface)
#     # claim the device
#     usb.util.claim_interface(dev, interface)
collected = 0
attempts = 1000
while True:
    try:
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        collected += 1
        print(data, data[1])
        print('weith:', data[-1] * 255 + data[-2])
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue
# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)
