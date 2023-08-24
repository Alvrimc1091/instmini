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
             char bits[9];
             memcpy(bits, response, 8);
             bits[8] = '\0';
             decodeBits(bits);
        }
        usleep(30000000); // Introduce a delay of 30 seconds
    

        unsigned char command[] = "T";
        hid_write(device, command, sizeof(command));

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            char response_data[64];
            strncpy(response_data, (char *)response, bytes_read);

            float temperature;
            sscanf(response_data, "T,%f", &temperature);

            printf("Temperatura: %.2f°C\n", temperature);

            if (temperature >= 1.0 && temperature <= 5.0) {
                printf("Warning, low temperature\n");
            } else if (temperature > 5.0 && temperature <= 15.0) {
                printf("Device reaching low temperatures, please be careful\n");
            } else if (temperature > 15.0 && temperature <= 50.0) {
                printf("Unit in good health\n");
            } else if (temperature > 50.0 && temperature <= 55.0) {
                printf("Device reaching high temperatures, please be careful\n");
            } else if (temperature > 55.0 && temperature <= 59.0) {
                printf("Warning, high temperature\n");
            } else if (temperature > 59.0 || temperature < 0.9) {
                printf("Temperature outside safe range. Stopping program.\n");
                keep_running = 0;
            }
        }

        usleep(30000000); // Introduce a delay of 30 seconds
    }

    // Send additional commands and print their information
    const char *additional_commands[] = {
        "?", "T", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "R0010", "R0013", "R0014", "R0015"
    };

    const char *command_texts[] = {
        "Status", "Temperature", "V1 Info", "V2 Info", "V3 Info", "V4 Info", "V5 Info",
        "V6 Info", "V7 Info", "V8 Info", "V9 Info", "R0010 Info", "R0013 Info",
        "R0014 Info", "R0015 Info"
    };

    for (int i = 0; i < sizeof(additional_commands) / sizeof(additional_commands[0]); i++) {
        hid_write(device, additional_commands[i], strlen(additional_commands[i]));

        unsigned char response[64];
        int bytes_read = hid_read(device, response, sizeof(response));
        if (bytes_read > 0) {
            response[bytes_read] = '\0';
            printf("%s Command: %s\n", command_texts[i], additional_commands[i]);
            printf("%s Response: %s\n", command_texts[i], response);
        }

        if (i < sizeof(additional_commands) / sizeof(additional_commands[0]) - 1) {
            printf("Waiting 5 seconds before the next command...\n");
            sleep(5); // Introduce a delay of 5 seconds
        }
    }

    hid_close(device);
    hid_exit();

    printf("Programa finalizado.\n");

    return 0;
}
