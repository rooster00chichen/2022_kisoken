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


def main():
    # GPIB接続設定
    rm = visa.ResourceManager('C:\\Windows\\SysWOW64\\visa32.dll')
    stage = rm.open_resource("GPIB0::8::INSTR")
    # initialize
    n = 201  # x movement for n times
    # move to -point
    stage.write("D:1S10F1000R10")
    sleep(500*10**-3)
    print(stage.read())

    # set up to use joycon
    joycon_device = hid.device()
    joycon_device.open(VENDOR_ID, L_PRODUCT_ID)
    write_output_report(joycon_device, 0, b'\x01', b'\x03', b'\x33')
    move_val = 2000
    print("now move_val:"+str(move_val))

    while 1:
        joy_button_status = joycon_device.read(12)
        if joy_button_status[5] == 8:
            move_pottion = "M:1+P"+str(move_val)
        elif joy_button_status[5] == 4:
            move_pottion = "M:1-P"+str(move_val)
        elif joy_button_status[5] == 64:
            if move_val != 2000:
                move_val = 2000
                print("now move_val:"+str(move_val))
            move_pottion = ""
        elif joy_button_status[5] == 128:
            if move_val != 6000:
                print(move_val)
                print("now move_val:"+str(move_val))
            move_pottion = ""
        else:
            move_pottion = ""

        if move_pottion != "":
            print(move_pottion)
            stage.write(move_pottion)
            print(stage.read())
            stage.write("G:")
            print(stage.read())
            while True:
                stage.write("!:")
                judge = stage.read()
                if judge == "R":
                    print("now can operate")
                    break
                else:
                    print("but")
                sleep(1*10*10**-3)


if __name__ == "__main__":
    main()
