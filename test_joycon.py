import hid
import time

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
    joycon_device = hid.device()
    joycon_device.open(VENDOR_ID, L_PRODUCT_ID)

    write_output_report(joycon_device, 0, b'\x01', b'\x03', b'\x33')

    while 1:
        joy_button_status = joycon_device.read(12)
        print(joy_button_status[5])


if __name__ == "__main__":
    main()
