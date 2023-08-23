import usb.core
import usb.backend.libusb1

dev=usb.core.find(idVendor=0xc216, idProduct=0x0180, find_all=True)
ep=dev[0].interfaces()[0].endpoints()[0]
i=dev[0].interfaces()[0].bInterfaceNumber
dev.reset()

if dev.is_kernel_driver_active(i):
    dev.detach_kernel_driver(i)

dev.set_configuration()
eaddr=ep.bEndpointAddress

while True:
    try:
        r=dev.read(eaddr, 80, 6000000)
    except usb.core.USBError as e:
        print("Error reading response: {}".format(e.args))
        break

    byte_str = ''.join(chr(n) for n in r)
    result_str = byte_str.split('\x00',1)[0]

    print(result_str)