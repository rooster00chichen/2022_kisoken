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
    x_henni = 2000
    while 1:
        joy_button_status = joycon_device.read(12)
        if joy_button_status[5] == 8:
            move_pottion = "M:1+P"+str(x_henni)
        elif joy_button_status[5] == 4:
            move_pottion = "M:1-P"+str(x_henni)
        elif joy_button_status[5] == 64:
            if x_henni != 2000:
                x_henni = 2000
                a = "now move distance:"+str(x_henni)
                print(a)
            move_pottion = ""
        elif joy_button_status[5] == 128:
            if x_henni != 6000:
                x_henni = 6000
                a = "now move distance:"+str(x_henni)
                print(a)
            move_pottion = ""
        else:
            move_pottion = ""

        if move_pottion != "":
            stage.write(move_pottion)
            print(stage.read())
            stage.write("G:")
            print(stage.read())
            while True:
                stage.write("!:")
                judge = stage.read()
                if judge == "R":
                    print("OK")
                    break
                sleep(50*10**-3)
            print(move_pottion)


if __name__ == "__main__":
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

    try:
        main()
    except KeyboardInterrupt:
        # GPIB切断

        stage.close()

        # 終了
        quit()
