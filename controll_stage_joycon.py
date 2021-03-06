import pyvisa as visa
import hid
from time import sleep

VENDOR_ID = 0x057e
L_PRODUCT_ID = 0x2006
toInputStatus = False


def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)


def move_signal_submit(move_val):
    if move_val >= 0:
        sig = "M:1+P"+str(abs(move_val))
    elif move_val <= 0:
        sig = "M:1-P"+str(abs(move_val))
    stage.write(sig)
    print("send the request" if stage.read() == "OK" else "test1")
    stage.write("G:")
    print("start move" if stage.read() == "OK" else "test2")
    while True:
        stage.write("!:")
        judge = stage.read()
        if judge == "R":
            break
        sleep(50*10**-3)
    print("can operate")
    return move_val


def main():
    global changeOfPosition
    move_val = 2000
    while 1:
        joy_button_status = joycon_device.read(12)
        if joy_button_status[5] == 8:
            changeOfPosition += move_signal_submit(move_val)
            print("now posittion:"+str(changeOfPosition))
        elif joy_button_status[5] == 4:
            changeOfPosition += move_signal_submit(move_val*-1)
            print("now posittion:"+str(changeOfPosition))
        elif joy_button_status[5] == 64:
            if move_val != 2000:
                move_val = 2000
                print("now move distance:"+str(move_val))
        elif joy_button_status[5] == 128:
            if move_val != 6000:
                move_val = 6000
                print("now move distance:"+str(move_val))
        elif joy_button_status[5] == 2:
            if changeOfPosition != 0:
                changeOfPosition += move_signal_submit(changeOfPosition*-1)
                print(changeOfPosition)
            if changeOfPosition != 0:
                print("error")
        else:
            pass
        sleep(100*10**-3)


if __name__ == "__main__":
    # GPIB????????????
    rm = visa.ResourceManager('C:\\Windows\\SysWOW64\\visa32.dll')
    stage = rm.open_resource("GPIB0::8::INSTR")
    # initialize
    n = 201  # x movement for n times
    # move to -point
    stage.write("D:1S10F1000R10")
    sleep(500*10**-3)
    print("can operate stage" if stage.read() == "OK" else "test3")

    # set up to use joycon
    joycon_device = hid.device()
    joycon_device.open(VENDOR_ID, L_PRODUCT_ID)
    write_output_report(joycon_device, 0, b'\x01', b'\x03', b'\x33')
    print("can use joycon")

    changeOfPosition = 0

    try:
        main()
    except KeyboardInterrupt:
        if changeOfPosition != 0:
            changeOfPosition += move_signal_submit(changeOfPosition*-1)
            print(changeOfPosition)
        # GPIB??????
        stage.close()
        # ??????
        quit()
