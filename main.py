import smbus
import time

# i2c channel
i2c_ch = 1
# address of gy-30 light sensor on i2c bus
i2c_address = 0x23

ONE_TIME_HIGH_RES_MODE_1 = 0x20

bus = smbus.SMBus(1)

# convert 2 bytes of data to a decimal number
# method taken from online bh1750 library located at https://gist.github.com/bwaldvogel/65d5202d5da5849a03a3c1b7711e6661
def convert_data(data):
    return (data[1] + (256*data[0])) / 1.2

def read_light(addr = i2c_address):
    # read data from the i2c interface
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convert_data(data)

previous_reading = 0
try:
    while True:
        light_level = read_light()
        if light_level != previous_reading:    
            light_string = ("{0:1.2f} lx".format(light_level))

            if light_level <= 100:
                print("Too dark. Light level is:", light_string)
            elif light_level <= 250:
                print("Dark. Light level is:", light_string)
            elif light_level <= 500:
                print("Medium. Light level is:", light_string)
            elif light_level <= 2500:
                print("Bright. Light level is:", light_string)    
            else:
                print("Too bright. Light level is:", light_string)
        time.sleep(1)
        previous_reading = light_level
except KeyboardInterrupt:    
    pass
print("User cancelled operation.")
    
    
    