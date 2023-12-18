import spidev
import time

# Define SPI communication settings
spi_bus = 0  # SPI bus 0 (Raspberry Pi 3 and earlier) or 1 (Raspberry Pi 4 and later)
spi_device = 1  # CE0 pin (GPIO 8) or CE1 pin (GPIO 7)
spi_speed = 1000000  # SPI speed in Hz (adjust as needed)

# Create SPI instance
spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = spi_speed

# AD7193 register addresses
AD7193_REG_DATA = 3

# Function to read raw data from the AD7193
def read_raw_data():
    spi.writebytes([0x58, 0x00, 0x00, 0x00])  # Start a single conversion on channel 0
    time.sleep(0.1)  # Wait for conversion to complete (adjust as needed)
    
    # Read the raw data from the data register (24 bits)
    response = spi.xfer2([0x48, 0x00, 0x00, 0x00])
    raw_data = (response[1] << 16) | (response[2] << 8) | response[3]
    
    return raw_data

def main():
    try:
        while True:
            raw_data = read_raw_data()
            print(f"Raw Data: {raw_data}")
            time.sleep(1)  # Adjust the delay as needed

    except KeyboardInterrupt:
        spi.close()

if __name__ == "__main__":
    main()
