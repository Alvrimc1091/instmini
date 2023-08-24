// RUN
// gcc -o freqsendsynth freqsendsynth.c -lhidapi-hidraw
// sudo ./freqsendsynth

#include <stdio.h>
#include <hidapi/hidapi.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>

#define VENDOR_ID 0x04d8   // Replace with your device's vendor ID
#define PRODUCT_ID 0x003f  // Replace with your device's product ID

volatile sig_atomic_t keep_running = 1;

void handle_interrupt(int signum) {
    keep_running = 0;
}

void decodeBits(const char *bits) {
    if (strlen(bits) != 8) {
        printf("Input must be an 8-bit binary sequence\n");
        return;
    }
    
    int d0 = bits[0] - '0';
    int d1 = bits[1] - '0';
    int d6 = bits[6] - '0';
    int d7 = bits[7] - '0';
    
    if (d0 == 0) {
        printf("D0: 100 MHz Unlocked (Internal Ref)\n");
    } else {
        printf("D0: 100 MHz Locked (Internal Ref)\n");
    }
    
    if (d1 == 0) {
        printf("D1: YIG PLL Unlocked (External Ref)\n");
    } else {
        printf("D1: YIG PLL Locked (External Ref)\n");
    }
    
    // D2 to D5 not used
    
    if (d6 == 0) {
        printf("D6: Self Test Failed\n");
    } else {
        printf("D6: Self Test Passed\n");
    }
    
    if (d7 == 0) {
        printf("D7: NOVO Unlocked\n");
    } else {
        printf("D7: NOVO Locked\n");
    }
}

int main() {
    if (hid_init()) {
        printf("Error initializing HIDAPI library.\n");
        return 1;
    }

    hid_device *device = hid_open(VENDOR_ID, PRODUCT_ID, NULL);
    if (!device) {
        printf("Error: Device not found.\n");
        return 1;
    }

    signal(SIGINT, handle_interrupt);

    printf("Conexión establecida. Puedes enviar comandos.\n");

    int frequency = 8000;  // Replace with your calculated frequency
    char command[64];
    snprintf(command, sizeof(command), "f%04X", frequency);
    hid_write(device, command, sizeof(command));

    printf("Frecuencia seteada: %d\n", frequency);

    usleep(1000000); // Introduce a delay of 1 second

    while (keep_running) {
        unsigned char command[] = "?";
        hid_write(device, command, sizeof(command));

        unsigned char response[8];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            response[bytes_read] = '\0';
            decodeBits((const char *)response);
        }

        usleep(30000000); // Introduce a delay of 30 seconds
    }

    // Send additional commands and print their information
    const char *additional_commands[] = {
        "?", "T", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "SF", "R0010", "R0013", "R0014", "R0015"
    };
    
    for (int i = 0; i < sizeof(additional_commands) / sizeof(additional_commands[0]); i++) {
        hid_write(device, additional_commands[i], strlen(additional_commands[i]));

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            response[bytes_read] = '\0';
            printf("%s Response: %s\n", additional_commands[i], response);
        }
    }

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
