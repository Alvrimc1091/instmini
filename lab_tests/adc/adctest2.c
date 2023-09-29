#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>
#include <string.h>

#define SPI_DEVICE "/dev/spidev0.1"  // SPI device file for CE1 (SPI1)
#define SPI_SPEED 1000000            // SPI speed (1 MHz)

uint8_t spi_mode = SPI_MODE_3;
uint8_t bits_per_word = 8;
uint32_t spi_speed = SPI_SPEED;

// Function to read ADC ID from PMOD AD5
uint8_t read_adc_id(int spi_fd) {
    uint8_t tx_buffer[2];
    uint8_t rx_buffer[2];

    tx_buffer[0] = 0x60;  // Read register command
    tx_buffer[1] = 0x00;  // Address of the ID register

    struct spi_ioc_transfer tr = {
        .tx_buf = (unsigned long)tx_buffer,
        .rx_buf = (unsigned long)rx_buffer,
        .len = 2,
        .delay_usecs = 0,
        .speed_hz = spi_speed,
        .bits_per_word = bits_per_word,
    };

    if (ioctl(spi_fd, SPI_IOC_MESSAGE(1), &tr) < 0) {
        perror("SPI transfer error");
        return 0;
    }

    return rx_buffer[1];
}

int main() {
    int spi_fd;
    uint8_t adc_id;

    // Open SPI device
    spi_fd = open(SPI_DEVICE, O_RDWR);
    if (spi_fd < 0) {
        perror("SPI device open error");
        return 1;
    }

    // Set SPI mode and speed
    if (ioctl(spi_fd, SPI_IOC_WR_MODE, &spi_mode) < 0) {
        perror("SPI mode setting error");
        close(spi_fd);
        return 1;
    }

    if (ioctl(spi_fd, SPI_IOC_WR_BITS_PER_WORD, &bits_per_word) < 0) {
        perror("SPI bits per word setting error");
        close(spi_fd);
        return 1;
    }

    if (ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &spi_speed) < 0) {
        perror("SPI speed setting error");
        close(spi_fd);
        return 1;
    }

    // Read ADC ID
    adc_id = read_adc_id(spi_fd);
    printf("ADC ID: %d\n", adc_id);

    // Close SPI device
    close(spi_fd);

    return 0;
}
