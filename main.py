# Main program for running the MagStripe reader at events

import usb.core
import usb.backend.libusb1

class MagStripeReader:

    def __init__(self):
        self.dev=usb.core.find(idVendor=0xc216, idProduct=0x0180)

        if self.dev is None:
            print("No MSR90 MagStripe readers detected, exiting.")
            exit(-1)

        ep=self.dev[0].interfaces()[0].endpoints()[0]
        i=self.dev[0].interfaces()[0].bInterfaceNumber
        self.dev.reset()

        if self.dev.is_kernel_driver_active(i):
            self.dev.detach_kernel_driver(i)

        self.dev.set_configuration()
        self.eaddr=ep.bEndpointAddress

        return
    
    def read_input(self) -> str:
        try:
            r=self.dev.read(self.eaddr, 80, 6000000)
        except usb.core.USBError as e:
            print("Error reading response: {}".format(e.args))
            exit(-1)

        byte_str = ''.join(chr(n) for n in r)
        result_str = byte_str.split('\x00',1)[0]

        return result_str
    
filename = "students.csv"

def process_string(str_in):
    inputs = str_in.split("&")
    um_id = inputs[0][8:16]
    
    name = inputs[1]
    last, first = name.split("/")

    uniqname = inputs[2].split("?")[0]
    uniqname = ''.join([i for i in uniqname if not i.isdigit()]).lower()

    return [um_id, first, last, uniqname]

def write_data(data):
    file = open(filename, "a")

    for i in range(0, len(data)-1):
        file.write(data[i]+", ")
    file.write(data[-1]+"\n")

    file.close()
    return

def process_data(str_in):
    [um_id, first, last, uniqname] = process_string(str_in)
    email = uniqname + "@umich.edu"
    data = [uniqname, first, last, um_id, email]
    write_data(data)

    return 
    
if __name__ == "__main__":

    Reader = MagStripeReader()

    file = open(filename, "a+")

    if (file.read(8) != "uniqname"):
        # Add header column for new file
        file.close()
        write_data(["uniqname", "first", "last", "UMID", "email"])

    while True:
        str_in = Reader.read_input()
        process_data(str_in)



