#!/usr/bin/python3
#i2cdetect -y 0
import smbus
import time
import sys


AHT20_CMD_INITIALIZE = [0xBE, 0x08, 0x00]
AHT20_CMD_MEASURE = [0xAC, 0x33, 0x00]

if len(sys.argv) == 3:
     DEVICE = int(sys.argv[1],16)
     bus = smbus.SMBus(int(sys.argv[2],16))
else:
    print('-1 | -1')
    sys.exit(1)


def getAll(bus,addr=DEVICE):
    #initialize
    bus.write_i2c_block_data(addr, 0x0, AHT20_CMD_INITIALIZE)
    #time.sleep(0.1)
    byt = bus.read_byte(addr)
    #Send MeasureCMD and read data
    bus.write_i2c_block_data(addr, 0x0, AHT20_CMD_MEASURE)
    time.sleep(0.08)
    data = bus.read_i2c_block_data(addr,0x00, 7)
    temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
    ctemp = ((temp*200) / 1048576) - 50

    hum = ((data[1] << 12) | (data[2] << 4) | data[3]) >> 4
    chum = int(hum * 100 / 1048576)
    return ctemp,chum
def main():
    try:
        temperature,humidity=getAll(bus)
        print('{0:0.1f} | {1:0.1f}'.format(temperature, humidity))
    except:
        print('-1 | -1')

if __name__=="__main__":
   main()
