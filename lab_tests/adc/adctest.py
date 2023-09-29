import spidev
import time

# Define SPI communication settings
spi_bus = 0  # SPI bus 0 (Raspberry Pi 3 and earlier) or 1 (Raspberry Pi 4 and later)
spi_device = 0  # CE0 pin (GPIO 8) or CE1 pin (GPIO 7)
spi_speed = 1000000  # SPI speed in Hz (adjust as needed)

# Create SPI instance
spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = spi_speed

# AD7193 register addresses
AD7193_REG_COMM = 0
AD7193_REG_CONF = 2
AD7193_REG_MODE = 1
AD7193_REG_DATA = 3
AD7193_REG_ID = 4

# Functions to communicate with AD7193
def spi_read_register(register_address, num_bytes):
    command = [0, 0, 0]
    command[0] = (1 << 6) | (register_address << 3) | num_bytes
    response = spi.xfer2(command)
    
    # Ensure the response has at least 3 bytes
    while len(response) < 3:
        response.append(0x00)
    
    # Append a 0 byte to make it 4 bytes
    response.append(0x00)
    
    return response[0:4]



def spi_write_register(register_address, data):
    command = [0, 0, 0]
    command[0] = (1 << 6) | (1 << 5) | (register_address << 3) | 1
    command[1] = data[0]
    command[2] = data[1]
    spi.xfer2(command)

def read_adc_channel(channel):
    spi_write_register(AD7193_REG_MODE, [0x80, 0x00])  # Set to single conversion mode
    spi_write_register(AD7193_REG_CONF, [0x10, 0x20])  # Configure channel and gain
    time.sleep(0.1)  # Wait for conversion to complete
    adc_data = spi_read_register(AD7193_REG_DATA, 4)
    adc_value = (adc_data[0] << 24) | (adc_data[1] << 16) | (adc_data[2] << 8) | adc_data[3]
    return adc_value

def main():
    try:
        while True:
            adc_reading = read_adc_channel(0)  # Read data from channel 0
            voltage = (adc_reading / 0x7FFFFF) * 2.5  # Assuming a 2.5V reference voltage
            print(f"ADC Reading: {adc_reading}, Voltage: {voltage}V")
            time.sleep(1)  # Adjust the delay as needed

    except KeyboardInterrupt:
        spi.close()

if __name__ == "__main__":
    main()
